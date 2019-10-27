# Third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.aux_widgets.cell_block import Ui_CellBlock

class CellBlock(QtWid.QWidget, Ui_CellBlock):

    def __init__(self, *args, **kwargs):
        super(CellBlock, self).__init__(*args, **kwargs)
        self.setupUi(self)
