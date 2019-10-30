# Third-party modules
import PyQt5.QtWidgets as QtWid

import numpy as np

# filters-tool project modules
from app.designer.aux_widgets.cell_block import Ui_CellBlock

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

        self.update_gain_action(self)


    def ignore_data_action(self, *args, **kwargs):
        pass


    def mousePressEvent(self, ev):
        super(CellBlock, self).mousePressEvent(ev)
        self.pass_data_action(self.cell_data)