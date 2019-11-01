# Third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.aux_widgets.comp_par_block import Ui_CompParBlock

class CompParBlock(QtWid.QWidget, Ui_CompParBlock):

    def __init__(self, *args, **kwargs):
        super(CompParBlock, self).__init__(*args, **kwargs)
        self.setupUi(self)