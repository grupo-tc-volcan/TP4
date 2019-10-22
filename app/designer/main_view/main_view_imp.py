# third-party modules
import PyQt5.QtWidgets as QtWid

# labtool project modules
from app.designer.main_view.main_view import Ui_MainView

class MainView(QtWid.QDialog, Ui_MainView):

    def _init_(self, *args, **kwargs):
        super(MainView, self)._init_(*args, **kwargs)
        self.setupUi(self)