# Third-party modules
import PyQt5.QtWidgets as QtWid
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore

class StagesList(QtWid.QListWidget):
    def __init__(self, *args, **kwargs):
        super(StagesList, self).__init__(*args, **kwargs)
        self.acceptDrops(True)

    def dropEvent(self, ev):
        pass