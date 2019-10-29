# Third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.aux_widgets.cell_block import Ui_CellBlock

class CellBlock(QtWid.QWidget, Ui_CellBlock):

    def __init__(self, cell_data, *args, **kwargs):
        super(CellBlock, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.cell_data = cell_data

        self.pass_data_action = self.ignore_data_action


    def ignore_data_action(self, *args, **kwargs):
        pass


    def mousePressEvent(self, ev):
        super(CellBlock, self).mousePressEvent(ev)
        self.pass_data_action(self.cell_data)