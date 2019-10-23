# Third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.filters_data.group_delay import Ui_GroupDelayData

class GroupDelayData(QtWid.QWidget, Ui_GroupDelayData):

    def __init__(self, *args, **kwargs):
        super(GroupDelayData, self).__init__(*args, **kwargs)
        self.setupUi(self)