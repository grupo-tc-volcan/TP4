# Third-party modules
import PyQt5.QtWidgets as QtWid
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore

import math

# filters-tool project modules
from app.designer.aux_widgets.cell_block_imp import CellBlock

class StagesList(QtWid.QListWidget):
    def __init__(self, *args, **kwargs):
        super(StagesList, self).__init__(*args, **kwargs)
        self.acceptDrops()
        self.new_stage_data = {}

        # Callback to execute when dropping events
        self.drop_action = self.ignore_drop_action


    def ignore_drop_action(self, *args, **kwargs):
        pass


    def dropEvent(self, ev):
        super(StagesList, self).dropEvent(ev)

        # Getting drop position
        item_index = self.row(self.itemAt(ev.pos().x(), ev.pos().y()))

        # Deleting element added by super
        self.takeItem(item_index)

        # Creating cell block
        new_cell_widget = CellBlock()
        new_cell_widget.fp.setText(self.new_stage_data['fp'])
        new_cell_widget.order.setText(self.new_stage_data['n'])
        new_cell_widget.q_val.setText(self.new_stage_data['q'])

        new_item = QtWid.QListWidgetItem()
        new_item.setSizeHint(new_cell_widget.sizeHint())

        self.insertItem(item_index, new_item)
        self.setItemWidget(new_item, new_cell_widget)

        # Executing callback
        self.drop_action()



class PolesList(QtWid.QListWidget):
    def __init__(self, *args, **kwargs):
        super(PolesList, self).__init__(*args, **kwargs)
        self.acceptDrops()

        # Callback to execute when dropping events
        self.drop_action = self.ignore_action


    def ignore_action(self, *args, **kwargs):
        pass


    def dropEvent(self, ev):
        super(PolesList, self).dropEvent(ev)
