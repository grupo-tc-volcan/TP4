# Third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.aux_widgets.pole_block import Ui_PoleBlock

class PoleBlock(QtWid.QWidget, Ui_PoleBlock):

    def __init__(self, *args, **kwargs):
        super(PoleBlock, self).__init__(*args, **kwargs)
        self.setupUi(self)

        