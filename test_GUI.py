# python native modules
import sys

# third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.main_view.main_view_imp import MainView

def test_main_view():
    app = QtWid.QApplication([])
    view = MainView()
    view.show()
    app.exec()