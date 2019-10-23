# third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.main_view.main_view_imp import MainView


app = QtWid.QApplication([])
view = MainView()
view.show()
app.exec()