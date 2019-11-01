# Third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.aux_widgets.zero_block import Ui_ZeroBlock

class ZeroBlock(QtWid.QWidget, Ui_ZeroBlock):

    def __init__(self, zero_data, *args, **kwargs):
        super(ZeroBlock, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.zero_data = zero_data

        self.pass_data_action = self.ignore_data_action


    def ignore_data_action(self, *args, **kwargs):
        pass


    def mousePressEvent(self, ev):
        super(ZeroBlock, self).mousePressEvent(ev)
        self.pass_data_action(self.zero_data)