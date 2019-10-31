# Third-party modules
import PyQt5.QtWidgets as QtWid
import PyQt5.QtCore as QtCore

from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

import scipy.signal as ss
import numpy as np
import math

# filters-tool project modules
from app.designer.main_view.main_view import Ui_MainView
from app.designer.filters_data.low_pass_imp import LowPassData
from app.designer.filters_data.high_pass_imp import HighPassData
from app.designer.filters_data.band_pass_imp import BandPassData
from app.designer.filters_data.band_stop_imp import BandStopData
from app.designer.filters_data.group_delay_imp import GroupDelayData
from app.designer.aux_widgets.pole_block_imp import PoleBlock
from app.designer.aux_widgets.zero_block_imp import ZeroBlock
from app.designer.aux_widgets.cell_block_imp import CellBlock
from app.designer.aux_widgets.cells_settings_imp import CellsSettings

from app.approximators.approximator import ApproximationErrorCode
from app.plotter.plotter import FilterPlotter
from app.auxiliary_calculators.wp_w0_q import SecondOrderAuxCalc
from app.cascader.cascader import AutomaticCascader

FILTER_INDEX_TO_NAME = ['low-pass', 'high-pass', 'band-pass', 'band-stop', 'group-delay']

class MainView(QtWid.QMainWindow, Ui_MainView):

    def __init__(self, *args, **kwargs):
        super(MainView, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Loading filter_data widgets
        self.filter_data_widgets = [LowPassData(), HighPassData(), BandPassData(), BandStopData(), GroupDelayData()]

        # Loading plotter
        self.plotters = [FilterPlotter(), FilterPlotter(), FilterPlotter(), FilterPlotter(), FilterPlotter(), FilterPlotter(), FilterPlotter(), FilterPlotter(), FilterPlotter()]

        # Creating auxiliary calculators
        self.second_order_calc = SecondOrderAuxCalc()
        self.cascader = AutomaticCascader()

        # Signal and slot connections
        self.filter_selector.currentIndexChanged.connect(self.filter_selected)
        self.approx_selector.currentIndexChanged.connect(self.set_approx)
        self.calculate_button.released.connect(self.calculate_approx)
        self.plot_template_1.stateChanged.connect(self.plot_template_toggle)
        self.stages_list.itemSelectionChanged.connect(self.plot_stage)
        self.accumulative_plot.stateChanged.connect(self.plot_stage)
        self.v_min.valueChanged.connect(self.update_dynamic_range)
        self.v_max.valueChanged.connect(self.update_dynamic_range)
        self.automatic_cascade.released.connect(self.calculate_automatic_cascade)

        # Loading callbacks
        self.stages_list.drag_action = self.pass_data_from_stages
        self.stages_list.update_gain_action = self.update_gain_in_stage

        # Set up things for the first time
        self.on_start_up()


############# METHODS CALLED BY SIGNALS #############


    def filter_selected(self):
        self.template_pic.setCurrentIndex(self.filter_selector.currentIndex())
        if self.filter_data.count() > 2:
            # Cleaning stacked widget
            self.filter_data.removeWidget(self.filter_data.currentWidget())

        # When group-delay is selected, the only approximations that should be available are Bessel and Gauss, which shouldn't be available for other filter types
        if self.filter_selector.currentIndex() == 4:
            # Sets current approximation to Bessel
            self.approx_selector.setCurrentIndex(4)
            for item_index in range(self.approx_selector.count()):
                if item_index != 4 and item_index != 5:
                    # Disable Butter, Cheby, Legendre and Cauer approximations
                    variant_disable = QtCore.QVariant(0)
                    self.approx_selector.setItemData(item_index, variant_disable, QtCore.Qt.UserRole - 1)
                else:
                    # Enable Bessel and Gauss approximations
                    variant_enable = QtCore.QVariant(1 | 32)
                    self.approx_selector.setItemData(item_index, variant_enable, QtCore.Qt.UserRole - 1)
        else:
            # Sets current approximation to Butterworth
            self.approx_selector.setCurrentIndex(0)
            for item_index in range(self.approx_selector.count()):
                if item_index != 4 and item_index != 5:
                    # Enable Butter, Cheby, Legendre and Cauer approximations
                    variant_enable = QtCore.QVariant(1 | 32)
                    self.approx_selector.setItemData(item_index, variant_enable, QtCore.Qt.UserRole - 1)
                else:
                    # Disable Bessel and Gauss approximations
                    variant_disable = QtCore.QVariant(0)
                    self.approx_selector.setItemData(item_index, variant_disable, QtCore.Qt.UserRole - 1)
        
        filter_index = self.filter_selector.currentIndex()
        self.filter_data.setCurrentIndex(self.filter_data.addWidget(self.filter_data_widgets[filter_index]))

    
    def set_approx(self):
        # Set type of approximation to current filter type
        self.filter_data_widgets[self.filter_selector.currentIndex()].approx_index = self.approx_selector.currentIndex()

        self.filter_data_widgets[self.filter_selector.currentIndex()].on_change()


    def calculate_approx(self):
        # Loading transfer_function into plotter and setting filter type
        filter_index = self.filter_selector.currentIndex()
        approx_index = self.approx_selector.currentIndex()
        if self.filter_data_widgets[filter_index].approximators[approx_index].compute() == ApproximationErrorCode.OK:
            # Enabling all widgets that make sense once the approximation is calculated
            self.enable_when_calculating()

            # Plotting
            self.plot_attenuation()
            self.plot_norm_attenuation()
            self.plot_phase()
            self.plot_group_delay()
            self.plot_poles_and_zeros()
            self.plot_q()
            self.plot_impulse_response()
            self.plot_step_response()

            # Adding all poles and zeros to lists in stages tab
            filter_index = self.filter_selector.currentIndex()
            approx_index = self.approx_selector.currentIndex()
            tf = self.filter_data_widgets[filter_index].approximators[approx_index].get_zpk()
            self.second_order_calc = SecondOrderAuxCalc(tf)
            self.fill_poles_and_zeros_lists()

            # Clearing stages_list
            self.stages_list.clear()

        elif self.filter_data_widgets[filter_index].approximators[approx_index].compute() == ApproximationErrorCode.INVALID_FREQ:
            mb = QtWid.QMessageBox()
            mb.setIcon(QtWid.QMessageBox.Critical)
            mb.setWindowTitle('Wrong input data.')
            mb.setText("Inconsistent frequencies entered. Please reffer to the filter's template image for better understanding of the input values.")
            mb.setFixedSize(500,200)
            mb.exec()

        elif self.filter_data_widgets[filter_index].approximators[approx_index].compute() == ApproximationErrorCode.INVALID_ATTE:
            mb = QtWid.QMessageBox()
            mb.setIcon(QtWid.QMessageBox.Critical)
            mb.setWindowTitle('Wrong input data.')
            mb.setText("Inconsistent attenuations entered. Please reffer to the filter's template image for better understanding of the input values. Recall that attenuation cannot be 0.")
            mb.setFixedSize(500,200)
            mb.exec()


    def plot_stage(self):
        current_item = self.stages_list.currentItem()
        stage_index = self.stages_list.row(current_item)

        if self.accumulative_plot.isChecked():
            start = 0
        else:
            start = stage_index

        poles_list = []
        zeros_list = []
        total_gain = 1
        for i in range(start,stage_index + 1):
            widget = self.stages_list.itemWidget(self.stages_list.item(i))
            if widget.cell_data['zero'] is not None:
                zeros = [zero * 2*np.pi for zero in widget.cell_data['zero']['zeros']]
            else:
                zeros = []
            zeros_list += zeros
            poles = [pole * 2*np.pi for pole in widget.cell_data['pole']['poles']]
            poles_list += poles

            gain = 10**(widget.cell_data['gain_data']/20)
            gain_needed_to_plot = self.adjust_function_gain(zeros, poles, gain)
            total_gain *= gain_needed_to_plot

        tf = ss.ZerosPolesGain(zeros_list, poles_list, total_gain)
        self.plot_attenuation_for_stages(tf)


    def plot_template_toggle(self):
        self.plot_attenuation()
        self.plot_norm_attenuation()
        self.plot_phase()


    def update_dynamic_range(self):
        v_min = self.v_min.value()
        v_max = self.v_max.value()

        filter_index = self.filter_selector.currentIndex()
        gain_in_db = self.filter_data_widgets[filter_index].gain.value()
        gain = 10**(gain_in_db/20)

        if gain_in_db > 0:
            dr = 20 * np.log10((v_max / gain) / v_min)
        else:
            dr = 20 * np.log10(v_max / (v_min / gain))

        self.dynamic_range.setText('{:.3f}'.format(dr))


    def update_gain_in_stage(self, stage_block_changed : QtWid.QWidget):
        filter_index = self.filter_selector.currentIndex()
        total_gain = 0
        for i in range(self.stages_list.count()):
            stage_widget = self.stages_list.itemWidget(self.stages_list.item(i))
            total_gain += stage_widget.gain.value()

        if total_gain > self.filter_data_widgets[filter_index].gain.value():
            mb = QtWid.QMessageBox()
            mb.setIcon(QtWid.QMessageBox.Critical)
            mb.setWindowTitle('Beware.')
            mb.setText("Total gain excedes the design specifications.")
            mb.setFixedSize(500,200)
            mb.exec()

        # Now plotting with new gain.
        self.plot_stage()


    def calculate_automatic_cascade(self):
        self.stages_list.clear()

        # Loading transfer_function into plotter and setting filter type
        filter_index = self.filter_selector.currentIndex()

        zero_blocks = self.second_order_calc.zero_blocks
        pole_blocks = self.second_order_calc.pole_blocks
        gain = self.filter_data_widgets[filter_index].gain.value()
        self.cascader.set_zeros_poles_gain(zero_blocks, pole_blocks, gain)

        self.cascader.separate_in_stages()
        self.cascader.sort_stages()
        self.cascader.assign_gains()

        for i in range(len(self.cascader.stages)):
            self.stages_list.add_stage_with_data(i, self.cascader.stages[i])

        self.fill_poles_and_zeros_lists()


############# METHODS FOR PLOTTING #############


    def plot_attenuation(self, transfer_function : ss.ZerosPolesGain = None):
        # Loading transfer_function into plotter and setting filter type
        filter_index = self.filter_selector.currentIndex()
        approx_index = self.approx_selector.currentIndex()
        if transfer_function is None:
            tf = self.filter_data_widgets[filter_index].approximators[approx_index].get_zpk()
        else:
            tf = transfer_function
        self.plotters[0].set_transfer_function(tf)

        self.plotters[0].set_filter_type(FILTER_INDEX_TO_NAME[filter_index])

        # Checking what kind of filter it is and building template accordingly
        if self.filter_selector.currentIndex() == 0 or self.filter_selector.currentIndex() == 1 or self.filter_selector.currentIndex() == 4:
            template = {
                'G' : self.filter_data_widgets[filter_index].gain.value(),
                'fp': self.filter_data_widgets[filter_index].pass_freq.value(),
                'fa': self.filter_data_widgets[filter_index].stop_freq.value(),
                'Ap': self.filter_data_widgets[filter_index].pass_att.value(),
                'Aa': self.filter_data_widgets[filter_index].stop_att.value()
            }
        elif self.filter_selector.currentIndex() == 2:
            template = {
                'G' : self.filter_data_widgets[filter_index].gain.value(),
                'fpl': self.filter_data_widgets[filter_index].pass_freq_l.value(),
                'fpr': self.filter_data_widgets[filter_index].pass_freq_r.value(),
                'fal': self.filter_data_widgets[filter_index].stop_freq_l.value(),
                'far': self.filter_data_widgets[filter_index].stop_freq_r.value(),
                'Ap': self.filter_data_widgets[filter_index].pass_att.value(),
                'Aal': self.filter_data_widgets[filter_index].stop_att_l.value(),
                'Aar': self.filter_data_widgets[filter_index].stop_att_r.value()
            }
        elif self.filter_selector.currentIndex() == 3:
            template = {
                'G' : self.filter_data_widgets[filter_index].gain.value(),
                'fpl': self.filter_data_widgets[filter_index].pass_freq_l.value(),
                'fpr': self.filter_data_widgets[filter_index].pass_freq_r.value(),
                'fal': self.filter_data_widgets[filter_index].stop_freq_l.value(),
                'far': self.filter_data_widgets[filter_index].stop_freq_r.value(),
                'Apl': self.filter_data_widgets[filter_index].pass_att_l.value(),
                'Apr': self.filter_data_widgets[filter_index].pass_att_r.value(),
                'Aa': self.filter_data_widgets[filter_index].stop_att.value()
            }

        # Plotting attenuation and template
        self.plotters[0].plot_attenuation()
        if self.plot_template_1.isChecked():
            self.plotters[0].plot_template(template)

        # Adding plot and navigation toolbar to tab
        if self.plot_1.count() > 2:
            # Cleaning stacked widget
            self.plot_1.removeWidget(self.filter_data.currentWidget())
        self.plot_1.setCurrentIndex(self.plot_1.addWidget(self.plotters[0].canvas))
        toolbar = NavigationToolbar(self.plotters[0].canvas, self)
        if self.toolbar_1.count() > 2:
            # Cleaning stacked widget
            self.toolbar_1.removeWidget(self.filter_data.currentWidget())
        self.toolbar_1.setCurrentIndex(self.toolbar_1.addWidget(toolbar))


    def plot_norm_attenuation(self, transfer_function : ss.ZerosPolesGain = None):
        # Loading transfer_function into plotter and setting filter type
        filter_index = self.filter_selector.currentIndex()
        approx_index = self.approx_selector.currentIndex()
        if transfer_function is None:
            tf = self.filter_data_widgets[filter_index].approximators[approx_index].get_normalised_zpk()
        else:
            tf = transfer_function
        self.plotters[1].set_transfer_function(tf)

        self.plotters[1].set_filter_type('low-pass')

        # Setting filter template to plotter
        # Normalised filters are all low-pass
        wa, Aa, wp, Ap = self.filter_data_widgets[filter_index].approximators[approx_index].get_norm_template()
        template = {
            'G' : 0,
            'fp': wp/(2*np.pi),
            'fa': wa/(2*np.pi),
            'Ap': Ap,
            'Aa': Aa
        }

        # Plotting normalised attenuation and template
        self.plotters[1].plot_attenuation()
        if self.plot_template_1.isChecked():
            self.plotters[1].plot_template(template)

        # Adding plot and navigation toolbar to tab
        if self.plot_2.count() > 2:
            # Cleaning stacked widget
            self.plot_2.removeWidget(self.filter_data.currentWidget())
        self.plot_2.setCurrentIndex(self.plot_2.addWidget(self.plotters[1].canvas))
        toolbar = NavigationToolbar(self.plotters[1].canvas, self)
        if self.toolbar_2.count() > 2:
            # Cleaning stacked widget
            self.toolbar_2.removeWidget(self.filter_data.currentWidget())
        self.toolbar_2.setCurrentIndex(self.toolbar_2.addWidget(toolbar))


    def plot_phase(self, transfer_function : ss.ZerosPolesGain = None):
        # Loading transfer_function into plotter and setting filter type
        filter_index = self.filter_selector.currentIndex()
        approx_index = self.approx_selector.currentIndex()
        if transfer_function is None:
            tf = self.filter_data_widgets[filter_index].approximators[approx_index].get_zpk()
        else:
            tf = transfer_function
        self.plotters[2].set_transfer_function(tf)

        self.plotters[2].set_filter_type(FILTER_INDEX_TO_NAME[filter_index])

        # Plotting phase
        self.plotters[2].plot_phase()

        # Adding plot and navigation toolbar to tab
        if self.plot_3.count() > 2:
            # Cleaning stacked widget
            self.plot_3.removeWidget(self.filter_data.currentWidget())
        self.plot_3.setCurrentIndex(self.plot_3.addWidget(self.plotters[2].canvas))
        toolbar = NavigationToolbar(self.plotters[2].canvas, self)
        if self.toolbar_3.count() > 2:
            # Cleaning stacked widget
            self.toolbar_3.removeWidget(self.filter_data.currentWidget())
        self.toolbar_3.setCurrentIndex(self.toolbar_3.addWidget(toolbar))


    def plot_group_delay(self, transfer_function : ss.ZerosPolesGain = None):
        if transfer_function is None:
            # Loading transfer_function into plotter and setting filter type
            filter_index = self.filter_selector.currentIndex()
            approx_index = self.approx_selector.currentIndex()
            tf = self.filter_data_widgets[filter_index].approximators[approx_index].get_zpk()
        else:
            tf = transfer_function
        self.plotters[3].set_transfer_function(tf)

        self.plotters[3].set_filter_type(FILTER_INDEX_TO_NAME[filter_index])

        # Setting filter template to plotter
        if filter_index == 4:
            gd_template = {
                'ft': self.filter_data_widgets[filter_index].group_delay_freq.value(),
                'group_delay': self.filter_data_widgets[filter_index].group_delay.value(),
                'tol': self.filter_data_widgets[filter_index].tol.value()
            }

        # Plotting group delay and template
        self.plotters[3].plot_group_delay()
        if self.plot_template_1.isChecked() and filter_index == 4:
            self.plotters[3].plot_gd_template(gd_template)

        # Adding plot and navigation toolbar to tab
        if self.plot_4.count() > 2:
            # Cleaning stacked widget
            self.plot_4.removeWidget(self.filter_data.currentWidget())
        self.plot_4.setCurrentIndex(self.plot_4.addWidget(self.plotters[3].canvas))
        toolbar = NavigationToolbar(self.plotters[3].canvas, self)
        if self.toolbar_4.count() > 2:
            # Cleaning stacked widget
            self.toolbar_4.removeWidget(self.filter_data.currentWidget())
        self.toolbar_4.setCurrentIndex(self.toolbar_4.addWidget(toolbar))


    def plot_poles_and_zeros(self, transfer_function : ss.ZerosPolesGain = None):
        # Loading transfer_function into plotter and setting filter type
        filter_index = self.filter_selector.currentIndex()
        approx_index = self.approx_selector.currentIndex()
        if transfer_function is None:
            tf = self.filter_data_widgets[filter_index].approximators[approx_index].get_zpk()
        else:
            tf = transfer_function
        self.plotters[4].set_transfer_function(tf)

        self.plotters[4].set_filter_type(FILTER_INDEX_TO_NAME[filter_index])

        # Plotting poles and zeros
        self.plotters[4].plot_poles_and_zeros()

        # Adding plot and navigation toolbar to tab
        if self.plot_5.count() > 2:
            # Cleaning stacked widget
            self.plot_5.removeWidget(self.filter_data.currentWidget())
        self.plot_5.setCurrentIndex(self.plot_5.addWidget(self.plotters[4].canvas))
        toolbar = NavigationToolbar(self.plotters[4].canvas, self)
        if self.toolbar_5.count() > 2:
            # Cleaning stacked widget
            self.toolbar_5.removeWidget(self.filter_data.currentWidget())
        self.toolbar_5.setCurrentIndex(self.toolbar_5.addWidget(toolbar))


    def plot_q(self, transfer_function : ss.ZerosPolesGain = None):
        # Loading transfer_function into plotter and setting filter type
        filter_index = self.filter_selector.currentIndex()
        approx_index = self.approx_selector.currentIndex()
        if transfer_function is None:
            tf = self.filter_data_widgets[filter_index].approximators[approx_index].get_zpk()
        else:
            tf = transfer_function
        self.plotters[5].set_transfer_function(tf)

        self.plotters[5].set_filter_type(FILTER_INDEX_TO_NAME[filter_index])

        # Plotting Q factor
        self.plotters[5].plot_q()

        # Adding plot and navigation toolbar to tab
        if self.plot_6.count() > 2:
            # Cleaning stacked widget
            self.plot_6.removeWidget(self.filter_data.currentWidget())
        self.plot_6.setCurrentIndex(self.plot_6.addWidget(self.plotters[5].canvas))
        toolbar = NavigationToolbar(self.plotters[5].canvas, self)
        if self.toolbar_6.count() > 2:
            # Cleaning stacked widget
            self.toolbar_6.removeWidget(self.filter_data.currentWidget())
        self.toolbar_6.setCurrentIndex(self.toolbar_6.addWidget(toolbar))


    def plot_impulse_response(self, transfer_function : ss.ZerosPolesGain = None):
        # Loading transfer_function into plotter and setting filter type
        filter_index = self.filter_selector.currentIndex()
        approx_index = self.approx_selector.currentIndex()
        if transfer_function is None:
            tf = self.filter_data_widgets[filter_index].approximators[approx_index].get_zpk()
        else:
            tf = transfer_function
        self.plotters[6].set_transfer_function(tf)

        self.plotters[6].set_filter_type(FILTER_INDEX_TO_NAME[filter_index])

        # Plotting impulse response
        self.plotters[6].plot_impulse_response()

        # Adding plot and navigation toolbar to tab
        if self.plot_7.count() > 2:
            # Cleaning stacked widget
            self.plot_7.removeWidget(self.filter_data.currentWidget())
        self.plot_7.setCurrentIndex(self.plot_7.addWidget(self.plotters[6].canvas))
        toolbar = NavigationToolbar(self.plotters[6].canvas, self)
        if self.toolbar_7.count() > 2:
            # Cleaning stacked widget
            self.toolbar_7.removeWidget(self.filter_data.currentWidget())
        self.toolbar_7.setCurrentIndex(self.toolbar_7.addWidget(toolbar))


    def plot_step_response(self, transfer_function : ss.ZerosPolesGain = None):
        # Loading transfer_function into plotter and setting filter type
        filter_index = self.filter_selector.currentIndex()
        approx_index = self.approx_selector.currentIndex()
        if transfer_function is None:
            tf = self.filter_data_widgets[filter_index].approximators[approx_index].get_zpk()
        else:
            tf = transfer_function
        self.plotters[7].set_transfer_function(tf)

        self.plotters[7].set_filter_type(FILTER_INDEX_TO_NAME[filter_index])

        # Plotting step response
        self.plotters[7].plot_step_response()

        # Adding plot and navigation toolbar to tab
        if self.plot_8.count() > 2:
            # Cleaning stacked widget
            self.plot_8.removeWidget(self.filter_data.currentWidget())
        self.plot_8.setCurrentIndex(self.plot_8.addWidget(self.plotters[7].canvas))
        toolbar = NavigationToolbar(self.plotters[7].canvas, self)
        if self.toolbar_8.count() > 2:
            # Cleaning stacked widget
            self.toolbar_8.removeWidget(self.filter_data.currentWidget())
        self.toolbar_8.setCurrentIndex(self.toolbar_8.addWidget(toolbar))


    def plot_attenuation_for_stages(self, transfer_function : ss.ZerosPolesGain):
         # Loading transfer_function into plotter and setting filter type
        self.plotters[8].set_transfer_function(transfer_function)

        # Plotting attenuation
        self.plotters[8].plot_attenuation()

        # Adding plot and navigation toolbar
        if self.stage_plot.count() > 2:
            # Cleaning stacked widget
            self.stage_plot.removeWidget(self.filter_data.currentWidget())
        self.stage_plot.setCurrentIndex(self.stage_plot.addWidget(self.plotters[8].canvas))
        toolbar = NavigationToolbar(self.plotters[8].canvas, self)
        if self.stages_toolbar.count() > 2:
            # Cleaning stacked widget
            self.stages_toolbar.removeWidget(self.filter_data.currentWidget())
        self.stages_toolbar.setCurrentIndex(self.stages_toolbar.addWidget(toolbar))


############# CALLBACKS FOR DRAG AND DROP #############


    def fill_poles_and_zeros_lists(self):
        self.poles_list.clear()
        for i in range(len(self.second_order_calc.pole_blocks)):
            # Checking if it is used or not
            if not self.second_order_calc.pole_blocks[i]['used']:
                new_pole_widget = PoleBlock(self.second_order_calc.pole_blocks[i])
                new_pole_widget.fp.setText('{:.3E}'.format(self.second_order_calc.pole_blocks[i]['fp']))
                new_pole_widget.order.setText('{}'.format(self.second_order_calc.pole_blocks[i]['n']))
                if self.second_order_calc.pole_blocks[i]['n'] == 2:
                    new_pole_widget.q_val.setText('{:.3E}'.format(self.second_order_calc.pole_blocks[i]['q']))
                else:
                    new_pole_widget.q_val.setText('-')

                # Setting callback for drag event
                new_pole_widget.pass_data_action = self.pass_data_from_poles
                new_item = QtWid.QListWidgetItem()
                new_item.setSizeHint(new_pole_widget.sizeHint())
                
                self.poles_list.insertItem(i, new_item)
                self.poles_list.setItemWidget(new_item, new_pole_widget)

            # Enabling zeros_list if at least one pole is used
            if all([(not block['used']) for block in self.second_order_calc.pole_blocks]):
                # If all blocks are NOT used
                self.zeros_list.setDisabled(True)
            else:
                self.zeros_list.setEnabled(True)

        self.zeros_list.clear()
        for i in range(len(self.second_order_calc.zero_blocks)):
            # Checking if it is used or not
            if not self.second_order_calc.zero_blocks[i]['used']:
                new_zero_widget = ZeroBlock(self.second_order_calc.zero_blocks[i])
                new_zero_widget.f0.setText('{:.3E}'.format(self.second_order_calc.zero_blocks[i]['f0']))
                new_zero_widget.order.setText('{}'.format(self.second_order_calc.zero_blocks[i]['n']))

                # Setting callback for drag event
                new_zero_widget.pass_data_action = self.pass_data_from_zeros
                new_item = QtWid.QListWidgetItem()
                new_item.setSizeHint(new_zero_widget.sizeHint())
                
                self.zeros_list.insertItem(i, new_item)
                self.zeros_list.setItemWidget(new_item, new_zero_widget)

        # When a stage was dragged out of stages_list, this cleans the empty icon remaining 
        self.stages_list.clean_empty_items()


    def pass_data_from_poles(self, data):
        for block in self.second_order_calc.pole_blocks:
            if block == data:
                self.stages_list.dropped_data = block

        # Setting callback for drop event
        self.stages_list.drop_action = self.fill_poles_and_zeros_lists

        # Cleaning data from drags of other lists
        self.zeros_list.dropped_data = {}
        self.poles_list.dropped_data = {}


    def pass_data_from_zeros(self, data):
        for block in self.second_order_calc.zero_blocks:
            if block == data:
                self.stages_list.dropped_data = block

        # Setting callback for drop event
        self.stages_list.drop_action = self.fill_poles_and_zeros_lists

        # Cleaning data from drags of other lists
        self.poles_list.dropped_data = {}
        self.zeros_list.dropped_data = {}

    
    def pass_data_from_stages(self, data):
        for block in self.second_order_calc.pole_blocks:
            if block == data['pole']:
                self.poles_list.dropped_data = data
        for block in self.second_order_calc.zero_blocks:
            if block == data['zero']:
                self.zeros_list.dropped_data = data

        # Setting callback for drop event
        self.poles_list.drop_action = self.fill_poles_and_zeros_lists
        self.zeros_list.drop_action = self.fill_poles_and_zeros_lists

        # Cleaning data from drags of other lists
        self.stages_list.dropped_data = {}


############# AUXILIARY METHODS #############


    def on_start_up(self):
        # Default filter is Low-Pass
        self.filter_selected()

        self.plot_template_1.setDisabled(True)

        self.poles_list.setDisabled(True)
        self.zeros_list.setDisabled(True)
        self.stages_list.setDisabled(True)
        self.automatic_cascade.setDisabled(True)
        self.accumulative_plot.setDisabled(True)
        self.v_min.setDisabled(True)
        self.v_max.setDisabled(True)


    def enable_when_calculating(self):
        self.plot_template_1.setEnabled(True)

        self.poles_list.setEnabled(True)
        self.zeros_list.setDisabled(True)
        self.stages_list.setEnabled(True)
        self.automatic_cascade.setEnabled(True)
        self.accumulative_plot.setEnabled(True)
        self.v_min.setEnabled(True)
        self.v_max.setEnabled(True)


    @staticmethod
    def adjust_function_gain(zeros: list, poles: list, gain):
        transfer_function = ss.ZerosPolesGain(zeros, poles, gain)
        w, mag, phase = ss.bode(transfer_function, n=1000)

        dmag = np.diff(mag)/np.diff(w)

        frequencies_to_check = 10
        zero_condition = 1.0e-4
        for i in range(len(dmag) - frequencies_to_check):
            values_checked = []
            for j in range(frequencies_to_check):
                values_checked.append(dmag[i + j])
            
            if all([value < zero_condition for value in values_checked]):
                frequency_to_evaluate = math.floor(i + frequencies_to_check/2)
                useless_1, gain_in_passband, useless_2 = ss.bode(transfer_function, [w[frequency_to_evaluate]])
                gain_in_passband = 10**(gain_in_passband/20)
                gain_needed = gain**2/gain_in_passband
                return gain_needed