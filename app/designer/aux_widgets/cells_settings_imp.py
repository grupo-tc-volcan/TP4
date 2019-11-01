# Third-party modules
import PyQt5.QtWidgets as QtWid
import PyQt5.QtCore as QtCore

import numpy as np

# filters-tool project modules
from app.designer.aux_widgets.cells_settings import Ui_CellsSettings
from app.designer.aux_widgets.comp_par_block_imp import CompParBlock
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
            self.cell_selector.setCurrentIndex(0)
        else:
            # Disable Compensated Derivator and Integrator
            variant_disable = QtCore.QVariant(0)
            self.cell_selector.setItemData(0, variant_disable, QtCore.Qt.UserRole - 1)

        if self.cell_designers[1].is_valid_gain_mode(cell_type, gain) and self.cell_data['pole']['n'] == 2:
            # Enable Sallen Key
            variant_enable = QtCore.QVariant(1 | 32)
            self.cell_selector.setItemData(1, variant_enable, QtCore.Qt.UserRole - 1)
            self.cell_selector.setCurrentIndex(1)
        else:
            # Disable Sallen Key
            variant_disable = QtCore.QVariant(0)
            self.cell_selector.setItemData(1, variant_disable, QtCore.Qt.UserRole - 1)

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
        for i in range(self.cell_selector.count()):

            # Designing cell
            cell_selected = self.cell_selector.currentIndex()
            cell_type = self.cell_data['type']
            gain = self.cell_data['gain_data']
            zeros = {
                'wz': self.cell_data['zero']['f0'] * 2*np.pi,
                'nz': self.cell_data['zero']['n'] 
            }
            poles = {
                'wp': self.cell_data['pole']['fp'] * 2*np.pi,
                'qp': self.cell_data['pole']['q'] 
            }

            self.cell_designers[cell_selected].set_cell(cell_type, gain)
            self.cell_designers[cell_selected].design_components(zeros, poles, gain)

            # Adding components
            components = self.cell_designers[cell_selected].get_components()
            self.add_components(components)

            # Adding parameters and sensitivities
            zeros, poles, gain = self.cell_designers[cell_selected].get_parameters()
            sensitivities = self.cell_designers[cell_selected].get_sensitivities()
            self.add_parameters_and_sensitivies(zeros, poles, gain, sensitivities)

        
    def add_components(self, components):
        self.cell_components.clear()

        for component in components.keys():
            new_component_block = CompParBlock()
            new_component_block.comp.setText(component + ':')
            new_component_block.val.setValue(components[component])

            index = self.cell_components.count()

            new_item = QtWid.QListWidgetItem()
            new_item.setSizeHint(new_component_block.sizeHint())
            self.cell_components.insertItem(index, new_item)
            self.cell_components.setItemWidget(new_item, new_component_block)

    
    def add_parameters_and_sensitivies(self, zeros, poles, gain, sensitivities):
        self.cell_sensitivities.clear()
        
        new_parameter_block = CompParBlock()
        new_parameter_block.comp.setText('f0:')
        new_parameter_block.val.setValue(zeros['wz'] / 2*np.pi)
        new_item = QtWid.QListWidgetItem()
        new_item.setSizeHint(new_parameter_block.sizeHint())
        self.insertItem(0, new_item)
        self.setItemWidget(new_item, new_parameter_block)

        new_parameter_block = CompParBlock()
        new_parameter_block.comp.setText('fp:')
        new_parameter_block.val.setValue(poles['wp'] / 2*np.pi)
        new_item = QtWid.QListWidgetItem()
        new_item.setSizeHint(new_parameter_block.sizeHint())
        self.insertItem(1, new_item)
        self.setItemWidget(new_item, new_parameter_block)

        new_parameter_block = CompParBlock()
        new_parameter_block.comp.setText('Q:')
        new_parameter_block.val.setValue(poles['qp'])
        new_item = QtWid.QListWidgetItem()
        new_item.setSizeHint(new_parameter_block.sizeHint())
        self.insertItem(2, new_item)
        self.setItemWidget(new_item, new_parameter_block)

        for sensitivity in sensitivities.keys():
            for parameter in sensitivities[sensitivity]:
                new_component_block = CompParBlock()
                new_component_block.comp.setText(sensitivity + '->' + parameter + ':')
                new_component_block.val.setValue(sensitivities[sensitivity][parameter])

                index = self.cell_components.count()

                new_item = QtWid.QListWidgetItem()
                new_item.setSizeHint(new_component_block.sizeHint())
                self.cell_components.insertItem(index, new_item)
                self.cell_components.setItemWidget(new_item, new_component_block)