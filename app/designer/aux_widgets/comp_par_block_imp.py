# Third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.aux_widgets.comp_par_block import Ui_CompParBlock

class CompParBlock(QtWid.QWidget, Ui_CompParBlock):

    def __init__(self, input_action=None, *args, **kwargs):
        super(CompParBlock, self).__init__(*args, **kwargs)
        self.setupUi(self)

        if input_action is None:
            self.input_action = self.ignore_data_action
        else:
            self.input_action = input_action

        # Signal and slot connections
        self.val.editingFinished.connect(self.send_data)


    def ignore_data_action(self, *args, **kwargs):
        pass


    def send_data(self):
        self.input_action(self.comp.text(), self.val.value())