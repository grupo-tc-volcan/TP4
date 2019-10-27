# Third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.aux_widgets.cells_settings import Ui_CellsSettings

class CellsSettings(QtWid.QWidget, Ui_CellsSettings):

    def __init__(self, *args, **kwargs):
        super(CellsSettings, self).__init__(*args, **kwargs)
        self.setupUi(self)