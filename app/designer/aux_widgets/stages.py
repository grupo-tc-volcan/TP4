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

        # Contains the stage_blocks data
        self.stages_data = []

        # Callback to execute when dropping events
        self.drop_action = self.ignore_drop_action

        # Callback for cell_widgets to call when they are dragged
        self.drag_action = self.ignore_drop_action


    def ignore_drop_action(self, *args, **kwargs):
        pass


    def dropEvent(self, ev):
        if self.dropped_data:
            if self.dropped_data['type'] == 'pole':
                super(StagesList, self).dropEvent(ev)
                # Getting drop position
                x = ev.pos().x()
                y = ev.pos().y()
                item_index = self.row(self.itemAt(x, y))

                # Deleting element added by super
                self.takeItem(item_index)

                # Creating cell block
                new_stage_data = {
                    'pole': self.dropped_data,
                    'zero': None,
                    'gain': 0
                }
                self.stages_data.append(new_stage_data)

                new_cell_widget = CellBlock(new_stage_data)
                new_cell_widget.fp.setText('{:.3E}'.format(self.dropped_data['fp']))
                new_cell_widget.np.setText('{}'.format(self.dropped_data['n']))
                if self.dropped_data['n'] == 2:
                    new_cell_widget.q_val.setText('{:.3E}'.format(self.dropped_data['q']))
                else:
                    new_cell_widget.q_val.setText('-')

                # Setting callback for drag event
                new_cell_widget.pass_data_action = self.drag_action
                new_item = QtWid.QListWidgetItem()
                new_item.setSizeHint(new_cell_widget.sizeHint())

                self.insertItem(item_index, new_item)
                self.setItemWidget(new_item, new_cell_widget)

                # Setting pole as used
                self.dropped_data['used'] = True

            elif self.dropped_data['type'] == 'zero':
                x = ev.pos().x()
                y = ev.pos().y()
                list_item = self.itemAt(x, y)
                item_widget = self.itemWidget(list_item)

                item_widget.cell_data['zero'] = self.dropped_data
                
                cell_widget = self.itemWidget(list_item)
                cell_widget.f0.setText('{:.3E}'.format(self.dropped_data['f0']))
                cell_widget.n0.setText('{}'.format(self.dropped_data['n']))

                # Setting zero as used
                self.dropped_data['used'] = True

            # Executing callback
            self.drop_action()
        
        else:
            super(StagesList, self).dropEvent(ev)
            # Getting drop position
            x = ev.pos().x()
            y = ev.pos().y()
            item_index = self.row(self.itemAt(x, y))
        
            # Deleting element added by super
            #self.takeItem(item_index)

    
    def clean_empty_items(self):
        for i in range(self.count()):
            item_content = self.itemWidget(self.item(i))
            if not item_content:
                self.takeItem(i)



class PolesList(QtWid.QListWidget):
    def __init__(self, *args, **kwargs):
        super(PolesList, self).__init__(*args, **kwargs)
        self.acceptDrops()
        self.dropped_data = {}

        # Callback to execute when dropping events
        self.drop_action = self.ignore_action


    def ignore_action(self, *args, **kwargs):
        pass


    def dropEvent(self, ev):
        # Only drops coming from stages_list will be accepted
        if self.dropped_data != {}:
            super(PolesList, self).dropEvent(ev)

            # Getting drop position
            x = ev.pos().x()
            y = ev.pos().y()
            item_index = self.row(self.itemAt(x, y))

            # Deleting element added by super
            self.takeItem(item_index)

            # Setting pole as unused
            self.dropped_data['pole']['used'] = False
            if self.dropped_data['zero'] is not None:
                self.dropped_data['zero']['used'] = False

            # Executing callback
            self.drop_action()



class ZerosList(QtWid.QListWidget):
    def __init__(self, *args, **kwargs):
        super(ZerosList, self).__init__(*args, **kwargs)
        self.acceptDrops()
        self.dropped_data = {}

        # Callback to execute when dropping events
        self.drop_action = self.ignore_action


    def ignore_action(self, *args, **kwargs):
        pass


    def dropEvent(self, ev):
        # Only drops coming from stages_list will be accepted
        if self.dropped_data != {}:
            super(ZerosList, self).dropEvent(ev)

            # Getting drop position
            x = ev.pos().x()
            y = ev.pos().y()
            item_index = self.row(self.itemAt(x, y))

            # Deleting element added by super
            self.takeItem(item_index)

            # Setting pole as unused
            self.dropped_data['pole']['used'] = False
            if self.dropped_data['zero'] is not None:
                self.dropped_data['zero']['used'] = False

            # Executing callback
            self.drop_action()


