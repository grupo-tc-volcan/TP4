# Third-party modules
import PyQt5.QtWidgets as QtWid
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore

# filters-tool project modules
from app.designer.aux_widgets.pole_block import Ui_PoleBlock

class PoleBlock(QtWid.QWidget, Ui_PoleBlock):

    def __init__(self, *args, **kwargs):
        super(PoleBlock, self).__init__(*args, **kwargs)
        self.setupUi(self)

    def mousePressEvent(self, ev):
        drag = QtGui.QDrag()
        mime_data = QtCore.QMimeData()

        data = str(self.fp.text) + ' ' + str(self.q_val) + ' ' + str(self.order)
        mime_data.setData(data)
        drag.setMimeData(mime_data)