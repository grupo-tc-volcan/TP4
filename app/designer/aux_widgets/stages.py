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

    def dropEvent(self, ev):
        super(StagesList, self).dropEvent(ev)

        #TODO data = str(ev.mimeData().text())
        #TODO fp, q, n = data.split(' ')
        #TODO 
        #TODO new_cell_widget = CellBlock()
        #TODO new_cell_widget.fp.setText(fp)
        #TODO new_cell_widget.order.setText(n)
        #TODO new_cell_widget.q_val.setText(q)
        #TODO 
        #TODO new_item = QtWid.QListWidgetItem()
        #TODO new_item.setSizeHint(new_cell_widget.sizeHint())
        #TODO self.poles_list.insertItem(0, new_item)
        #TODO self.poles_list.setItemWidget(new_item, new_cell_widget)
        self.takeItem(self.count() - 1)

        new_cell_widget = CellBlock()
        new_cell_widget.fp.setText(self.new_stage_data['fp'])
        new_cell_widget.order.setText(self.new_stage_data['n'])
        new_cell_widget.q_val.setText(self.new_stage_data['q'])

        new_item = QtWid.QListWidgetItem()
        new_item.setSizeHint(new_cell_widget.sizeHint())

        item_index = self.count()
        self.insertItem(item_index, new_item)
        self.setItemWidget(new_item, new_cell_widget)

