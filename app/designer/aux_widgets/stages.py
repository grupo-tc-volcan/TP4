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

        # Callback to execute when a cell changes its gain
        self.update_gain_action = self.ignore_drop_action

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

                # Checking if there is already a cell in that position
                item_content = self.itemWidget(self.itemAt(x, y))
                if not item_content:
                    # Deleting element added by super
                    self.takeItem(item_index)

                # Creating cell block
                new_stage_data = {
                    'pole': self.dropped_data,
                    'zero': None,
                    'gain': 0,
                    'type': ''
                }
                self.add_cell(item_index, new_stage_data)

            elif self.dropped_data['type'] == 'zero':
                x = ev.pos().x()
                y = ev.pos().y()
                list_item = self.itemAt(x, y)
                item_widget = self.itemWidget(list_item)

                if item_widget is not None:
                    self.validate_and_add_zero(item_widget, self.dropped_data)

                item_widget.what_am_i()

            # Executing callback
            self.drop_action()
        
        else:
            super(StagesList, self).dropEvent(ev)

    
    def clean_empty_items(self):
        for i in range(self.count()):
            item_content = self.itemWidget(self.item(i))
            if not item_content:
                self.takeItem(i)


    def validate_and_add_zero(self, cell_widget : QtWid.QWidget, zero_data):
        if zero_data['n'] == 2:
            # Only second order poles can have second order zeros
            if cell_widget.cell_data['pole']['n'] == 2 and cell_widget.cell_data['zero'] is None:
                # Checking that the cell in which the zero was dropped has a second order pole and doesn't have any zeros
                cell_widget.cell_data['zero'] = zero_data

                cell_widget.f0.setText('{:.3E}'.format(cell_widget.cell_data['zero']['f0']))
                cell_widget.n0.setText('{}'.format(cell_widget.cell_data['zero']['n']))

                # Setting zero as used
                self.dropped_data['used'] = True

        elif zero_data['n'] == 1:
            if cell_widget.cell_data['pole']['n'] == 2:
                if cell_widget.cell_data['zero'] is None:
                    # If the cell has no zeros, this simple zero is added
                    cell_widget.cell_data['zero'] = zero_data

                    cell_widget.f0.setText('{:.3E}'.format(cell_widget.cell_data['zero']['f0']))
                    cell_widget.n0.setText('{}'.format(cell_widget.cell_data['zero']['n']))

                    # Setting zero as used
                    self.dropped_data['used'] = True

                elif cell_widget.cell_data['zero']['n'] == 1:
                    # If the cell already has a first degree zero, this new first degree zero is added as well
                    # Increasing order of the zero and adding it to the zeros list
                    cell_widget.cell_data['zero']['n'] = 2
                    cell_widget.cell_data['zero']['zeros'].append(zero_data['zeros'][0])
                    cell_widget.cell_data['zero']['zero_attached'] = zero_data

                    cell_widget.f0.setText('{:.3E}'.format(cell_widget.cell_data['zero']['f0']))
                    cell_widget.n0.setText('{}'.format(cell_widget.cell_data['zero']['n']))

                    # Setting zero as used
                    self.dropped_data['used'] = True

            elif cell_widget.cell_data['pole']['n'] == 1 and cell_widget.cell_data['zero'] is None:
                # Checking that the cell in which the zero was dropped doesn't have any zeros
                cell_widget.cell_data['zero'] = zero_data

                cell_widget.f0.setText('{:.3E}'.format(cell_widget.cell_data['zero']['f0']))
                cell_widget.n0.setText('{}'.format(cell_widget.cell_data['zero']['n']))

                # Setting zero as used
                self.dropped_data['used'] = True


    def add_cell(self, index, new_data):
        self.stages_data.append(new_data)

        new_cell_widget = CellBlock(new_data)
        new_cell_widget.fp.setText('{:.3E}'.format(self.dropped_data['fp']))
        new_cell_widget.np.setText('{}'.format(self.dropped_data['n']))
        if self.dropped_data['n'] == 2:
            new_cell_widget.q_val.setText('{:.3E}'.format(self.dropped_data['q']))
        else:
            new_cell_widget.q_val.setText('-')
        new_cell_widget.what_am_i()

        # Setting callback for drag event and Gain input
        new_cell_widget.pass_data_action = self.drag_action
        new_cell_widget.update_gain_action = self.update_gain_action

        new_item = QtWid.QListWidgetItem()
        new_item.setSizeHint(new_cell_widget.sizeHint())

        self.insertItem(index, new_item)
        self.setItemWidget(new_item, new_cell_widget)

        # Setting pole as used
        self.dropped_data['used'] = True




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
                # If the zero is of second order, then it's possible that it was originally two first order zeros in the origin
                if self.dropped_data['zero']['n'] == 2:
                    if self.dropped_data['zero']['zeros'][0] == self.dropped_data['zero']['zeros'][1]:
                        # Correcting changes done when combining zeros
                        self.dropped_data['zero']['n'] = 1
                        self.dropped_data['zero']['zeros'].pop()
                        self.dropped_data['zero']['zero_attached']['used'] = False
                        self.dropped_data['zero']['zero_attached'] = None

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
                # If the zero is of second order, then it's possible that it was originally two first order zeros in the origin
                if self.dropped_data['zero']['n'] == 2:
                    if self.dropped_data['zero']['zeros'][0] == self.dropped_data['zero']['zeros'][1]:
                        # Correcting changes done when combining zeros
                        self.dropped_data['zero']['n'] = 1
                        self.dropped_data['zero']['zeros'].pop()
                        self.dropped_data['zero']['zero_attached']['used'] = False
                        self.dropped_data['zero']['zero_attached'] = None

                self.dropped_data['zero']['used'] = False

            # Executing callback
            self.drop_action()


