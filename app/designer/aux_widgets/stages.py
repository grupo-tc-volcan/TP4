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
        self.dropped_data = {}

        # Callback to execute when dropping events
        self.drop_action = self.ignore_drop_action


    def ignore_drop_action(self, *args, **kwargs):
        pass


    def dropEvent(self, ev):
        if self.dropped_data['type'] == 'pole':
            super(StagesList, self).dropEvent(ev)

            # Getting drop position
            x = ev.pos().x()
            y = ev.pos().y()
            item_index = self.row(self.itemAt(x, y))

            # Deleting element added by super
            self.takeItem(item_index)

            # Creating cell block
            new_cell_widget = CellBlock()
            new_cell_widget.fp.setText('{:.3E}'.format(self.dropped_data['fp']))
            new_cell_widget.np.setText('{}'.format(self.dropped_data['n']))
            if self.dropped_data['n'] == 2:
                new_cell_widget.q_val.setText('{:.3E}'.format(self.dropped_data['q']))
            else:
                new_cell_widget.q_val.setText('-')

            new_item = QtWid.QListWidgetItem()
            new_item.setSizeHint(new_cell_widget.sizeHint())

            self.insertItem(item_index, new_item)
            self.setItemWidget(new_item, new_cell_widget)

            # Setting pole as used
            self.dropped_data['used'] = True

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
