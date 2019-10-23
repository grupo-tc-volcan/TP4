# Third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.filters_data.band_stop import Ui_BandStopData

class BandStopData(QtWid.QWidget, Ui_BandStopData):

    def __init__(self, *args, **kwargs):
        super(BandStopData, self).__init__(*args, **kwargs)
        self.setupUi(self)