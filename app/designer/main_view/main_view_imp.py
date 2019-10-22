# third-party modules
import PyQt5.QtWidgets as QtWid

# labtool project modules
from app.designer.main_view.main_view import Ui_MainView

class MainView(QtWid.QMainWindow, Ui_MainView):

    def __init__(self, *args, **kwargs):
        super(MainView, self).__init__(*args, **kwargs)
        self.setupUi(self)