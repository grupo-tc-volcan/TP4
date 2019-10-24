# Third-party modules
import PyQt5.QtWidgets as QtWid
import PyQt5.QtCore as QtCore

# filters-tool project modules
from app.designer.main_view.main_view import Ui_MainView
from app.designer.filters_data.low_pass_imp import LowPassData
from app.designer.filters_data.high_pass_imp import HighPassData
from app.designer.filters_data.band_pass_imp import BandPassData
from app.designer.filters_data.band_stop_imp import BandStopData
from app.designer.filters_data.group_delay_imp import GroupDelayData

class MainView(QtWid.QMainWindow, Ui_MainView):

    def __init__(self, *args, **kwargs):
        super(MainView, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Loading filter_data widgets
        self.filter_data_widgets = [LowPassData(), HighPassData(), BandPassData(), BandStopData(), GroupDelayData()]

        # Signal and slot connections
        self.filter_selector.currentIndexChanged.connect(self.filter_selected)
        self.approx_selector.currentIndexChanged.connect(self.set_approx)
        self.calculate_button.released.connect(self.calculate_approx)

        # Set up things for the first time
        self.on_start_up()


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
        pass


    def on_start_up(self):
        # Default filter is Low-Pass
        self.filter_selected()

        # Disabeling plot controls
        self.label_x_1.setDisabled(True)
        self.scale_x_1.setDisabled(True)
        self.min_x_1.setDisabled(True)
        self.max_x_1.setDisabled(True)
        self.label_y_1.setDisabled(True)
        self.scale_y_1.setDisabled(True)
        self.min_y_1.setDisabled(True)
        self.max_y_1.setDisabled(True)
        self.auto_scale_1.setDisabled(True)
        self.plot_template_1.setDisabled(True)
        self.label_x_2.setDisabled(True)
        self.scale_x_2.setDisabled(True)
        self.min_x_2.setDisabled(True)
        self.max_x_2.setDisabled(True)
        self.label_y_2.setDisabled(True)
        self.scale_y_2.setDisabled(True)
        self.min_y_2.setDisabled(True)
        self.max_y_2.setDisabled(True)
        self.auto_scale_2.setDisabled(True)
        self.plot_template_2.setDisabled(True)
        self.label_x_3.setDisabled(True)
        self.scale_x_3.setDisabled(True)
        self.min_x_3.setDisabled(True)
        self.max_x_3.setDisabled(True)
        self.label_y_3.setDisabled(True)
        self.scale_y_3.setDisabled(True)
        self.min_y_3.setDisabled(True)
        self.max_y_3.setDisabled(True)
        self.auto_scale_3.setDisabled(True)
        self.label_x_4.setDisabled(True)
        self.scale_x_4.setDisabled(True)
        self.min_x_4.setDisabled(True)
        self.max_x_4.setDisabled(True)
        self.label_y_4.setDisabled(True)
        self.scale_y_4.setDisabled(True)
        self.min_y_4.setDisabled(True)
        self.max_y_4.setDisabled(True)
        self.auto_scale_4.setDisabled(True)
        self.label_x_5.setDisabled(True)
        self.scale_x_5.setDisabled(True)
        self.min_x_5.setDisabled(True)
        self.max_x_5.setDisabled(True)
        self.label_y_5.setDisabled(True)
        self.scale_y_5.setDisabled(True)
        self.min_y_5.setDisabled(True)
        self.max_y_5.setDisabled(True)
        self.auto_scale_5.setDisabled(True)
        self.label_x_6.setDisabled(True)
        self.scale_x_6.setDisabled(True)
        self.min_x_6.setDisabled(True)
        self.max_x_6.setDisabled(True)
        self.label_y_6.setDisabled(True)
        self.scale_y_6.setDisabled(True)
        self.min_y_6.setDisabled(True)
        self.max_y_6.setDisabled(True)
        self.auto_scale_6.setDisabled(True)
        self.label_x_7.setDisabled(True)
        self.scale_x_7.setDisabled(True)
        self.min_x_7.setDisabled(True)
        self.max_x_7.setDisabled(True)
        self.label_y_7.setDisabled(True)
        self.scale_y_7.setDisabled(True)
        self.min_y_7.setDisabled(True)
        self.max_y_7.setDisabled(True)
        self.auto_scale_7.setDisabled(True)
        self.label_x_8.setDisabled(True)
        self.scale_x_8.setDisabled(True)
        self.min_x_8.setDisabled(True)
        self.max_x_8.setDisabled(True)
        self.label_y_8.setDisabled(True)
        self.scale_y_8.setDisabled(True)
        self.min_y_8.setDisabled(True)
        self.max_y_8.setDisabled(True)
        self.auto_scale_8.setDisabled(True)

