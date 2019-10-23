# Third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.main_view.main_view import Ui_MainView
from app.designer.filters_data.low_pass_imp import LowPassData
from app.designer.filters_data.high_pass_imp import HighPassData
from app.designer.filters_data.band_pass_imp import BandPassData
from app.designer.filters_data.band_stop_imp import BandStopData
from app.designer.filters_data.group_delay_imp import GroupDelayData

class MainView(QtWid.QMainWindow, Ui_MainView):

    def __init__(self, *args, **kwargs):
        super(MainView, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Loading filter_data widgets
        self.filter_data_widgets = [LowPassData(), HighPassData(), BandPassData(), BandStopData(), GroupDelayData()]

        # Signal and slot connections
        self.filter_selector.currentIndexChanged.connect(self.filter_selected)
        self.approx_selector.currentIndexChanged.connect(self.set_approx)

        # Set up things for the first time
        self.on_start_up()


    def on_start_up(self):
        # Default filter is Low-Pass
        self.filter_data.setCurrentIndex(self.filter_data.addWidget(self.filter_data_widgets[0]))


    def filter_selected(self):
        self.template_pic.setCurrentIndex(self.filter_selector.currentIndex())
        if self.filter_data.count() > 2:
            # Cleaning stacked widget
            self.filter_data.removeWidget(self.filter_data.currentWidget())
        
        filter_index = self.filter_selector.currentIndex()
        self.filter_data.setCurrentIndex(self.filter_data.addWidget(self.filter_data_widgets[filter_index]))

    
    def set_approx(self):
        # Set type of approximation to current filter type
        self.filter_data_widgets[self.filter_selector.currentIndex()].approx_index = self.approx_selector.currentIndex()
        self.filter_data_widgets[self.filter_selector.currentIndex()].on_change()
