# Third-party modules
import PyQt5.QtWidgets as QtWid

import numpy as np
import scipy.signal as ss

# filters-tool project modules
from app.designer.aux_widgets.cell_block import Ui_CellBlock
from app.auxiliary_calculators.wp_w0_q import SecondOrderAuxCalc

class CellBlock(QtWid.QWidget, Ui_CellBlock):

    def __init__(self, cell_data, *args, **kwargs):
        super(CellBlock, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.cell_data = cell_data

        # Callbacks
        self.pass_data_action = self.ignore_data_action
        self.update_gain_action = self.ignore_data_action

        # Signal and slot connections
        self.v_min.valueChanged.connect(self.update_dynamic_range)
        self.v_max.valueChanged.connect(self.update_dynamic_range)
        self.gain.valueChanged.connect(self.update_dynamic_range)


    def update_dynamic_range(self):
        v_min = self.v_min.value()
        v_max = self.v_max.value()

        if v_max and v_min:
            gain_in_db = self.gain.value()
            gain = 10**(gain_in_db/20)

            if gain_in_db > 0:
                dr = 20 * np.log10((v_max / gain) / v_min)
            else:
                dr = 20 * np.log10(v_max / (v_min / gain))

            self.dynamic_range.setText('{:.3f}'.format(dr))

        self.cell_data['gain'] = self.gain.value()

        self.update_gain_action(self)


    def ignore_data_action(self, *args, **kwargs):
        pass


    def mousePressEvent(self, ev):
        super(CellBlock, self).mousePressEvent(ev)
        self.pass_data_action(self.cell_data)


    def what_am_i(self):
        if self.cell_data['pole']['n'] == 1:
            # If it is a first degree cell, it can only be a low-pass or a high-pass
            if self.cell_data['zero'] is None:
                # If it doesn't have any zeros, it's a low-pass
                self.cell_data['type'] = 'low-pass'
            elif self.cell_data['zero']['n'] == 1:
                # If it has a zero, it's a high-pass
                self.cell_data['type'] = 'high-pass'

        elif self.cell_data['pole']['n'] == 2:
            # A second degree cell can either be a low-pass with no zeros, band-pass, high-pass with zeros in the origin, a notch, or low-pass and high-pass with 2 imaginary zeros
            if self.cell_data['zero'] is None:
                self.cell_data['type'] = 'low-pass'
            elif self.cell_data['zero']['n'] == 1:
                self.cell_data['type'] = 'band-pass'
            elif self.cell_data['zero']['n'] == 2:
                # If the zeros are both in the origin, then it's a high-pass
                if self.cell_data['zero']['zeros'][0] == self.cell_data['zero']['zeros'][1]:
                    self.cell_data['type'] = 'high-pass'
                else:
                    # If the zeros are not the same, it should be checked which comes first in terms of frequency, the pole or the zero
                    if np.isclose(self.cell_data['zero']['f0'], self.cell_data['pole']['fp']):
                        self.cell_data['type'] = 'notch'
                    elif self.cell_data['zero']['f0'] > self.cell_data['pole']['fp']:
                        self.cell_data['type'] = 'low-pass'
                    elif self.cell_data['zero']['f0'] < self.cell_data['pole']['fp']:
                        self.cell_data['type'] = 'high-pass'

        self.type.setText(self.cell_data['type'])