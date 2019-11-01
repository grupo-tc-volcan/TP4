# Third-party modules
import PyQt5.QtWidgets as QtWid
import PyQt5.QtCore as QtCore


# filters-tool project modules
from app.designer.aux_widgets.cells_settings import Ui_CellsSettings
from app.cells.sallen_key import SallenKey, CellGroup
from app.cells.active_first_order import ActiveFirstOrder

class CellsSettings(QtWid.QWidget, Ui_CellsSettings):

    def __init__(self, cell_data, *args, **kwargs):
        super(CellsSettings, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.cell_data = cell_data
        self.cell_designers = [ActiveFirstOrder(), ActiveFirstOrder(), SallenKey(), None, None, None, None, None, None]

        self.check_available_cells()


    def check_available_cells(self):
        cell_type = self.cell_data['type']
        gain = 10**(self.cell_data['gain_data']/20)

        # ActiveFirstOrder are inverters, therefore their module gain is negative 
        if self.cell_designers[0].is_valid_gain_mode(cell_type, gain) and self.cell_data['pole']['n'] == 1:
            # Enable Compensated Derivator and Integrator
            variant_enable = QtCore.QVariant(1 | 32)
            self.cell_selector.setItemData(0, variant_enable, QtCore.Qt.UserRole - 1)
            self.cell_selector.setItemData(1, variant_enable, QtCore.Qt.UserRole - 1)
        else:
            # Disable Compensated Derivator and Integrator
            variant_disable = QtCore.QVariant(0)
            self.cell_selector.setItemData(0, variant_disable, QtCore.Qt.UserRole - 1)
            self.cell_selector.setItemData(1, variant_disable, QtCore.Qt.UserRole - 1)

        if self.cell_designers[2].is_valid_gain_mode(cell_type, gain) and self.cell_data['pole']['n'] == 2:
            # Enable Sallen Key
            variant_enable = QtCore.QVariant(1 | 32)
            self.cell_selector.setItemData(2, variant_enable, QtCore.Qt.UserRole - 1)
        else:
            # Disable Sallen Key
            variant_disable = QtCore.QVariant(0)
            self.cell_selector.setItemData(2, variant_disable, QtCore.Qt.UserRole - 1)

        #if self.cell_designers[2].is_valid_gain_mode(cell_type, gain) and self.cell_data['pole']['n'] == 2:
        #    # Enable Sallen Key
        #    variant_enable = QtCore.QVariant(1 | 32)
        #    self.cell_selector.setItemData(8, variant_enable, QtCore.Qt.UserRole - 1)
        #else:
        #    # Disable Sallen Key
        #    variant_disable = QtCore.QVariant(0)
        #    self.cell_selector.setItemData(8, variant_disable, QtCore.Qt.UserRole - 1)

        # Disabeling the rest
        for i in range(self.cell_selector.count()):
            if i != 0 and i != 1:
                # Disable
                variant_disable = QtCore.QVariant(0)
                self.cell_selector.setItemData(i, variant_disable, QtCore.Qt.UserRole - 1)


    def design_cell(self):
        self.cell_designers