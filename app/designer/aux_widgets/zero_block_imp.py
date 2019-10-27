# Third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.aux_widgets.zero_block import Ui_ZeroBlock

class ZeroBlock(QtWid.QWidget, Ui_ZeroBlock):

    def __init__(self, *args, **kwargs):
        super(ZeroBlock, self).__init__(*args, **kwargs)
        self.setupUi(self)