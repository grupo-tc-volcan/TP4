# Third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.filters_data.band_pass import Ui_BandPassData

class BandPassData(QtWid.QWidget, Ui_BandPassData):

    def __init__(self, *args, **kwargs):
        super(BandPassData, self).__init__(*args, **kwargs)
        self.setupUi(self)