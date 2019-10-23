# Third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.filters_data.high_pass import Ui_HighPassData

class HighPassData(QtWid.QWidget, Ui_HighPassData):

    def __init__(self, *args, **kwargs):
        super(HighPassData, self).__init__(*args, **kwargs)
        self.setupUi(self)