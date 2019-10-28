# Third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.aux_widgets.pole_block import Ui_PoleBlock

class PoleBlock(QtWid.QWidget, Ui_PoleBlock):

    def __init__(self, pole_data, *args, **kwargs):
        super(PoleBlock, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.pole_data = pole_data

        self.pass_data_action = self.ignore_data_action


    def ignore_data_action(self, *args, **kwargs):
        pass


    def mousePressEvent(self, ev):
        super(PoleBlock, self).mousePressEvent(ev)
        self.pass_data_action(self.pole_data)