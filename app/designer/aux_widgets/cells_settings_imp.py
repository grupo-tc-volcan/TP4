# Third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.aux_widgets.cells_settings import Ui_CellsSettings
from app.cells.sallen_key import SallenKey
from app.cells.active_first_order import ActiveFirstOrder

class CellsSettings(QtWid.QWidget, Ui_CellsSettings):

    def __init__(self, cell_data, *args, **kwargs):
        super(CellsSettings, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.cell_designers = [ActiveFirstOrder(), SallenKey()]

        self.check_available_cells()


    def check_available_cells(self):
        pass