# Third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.filters_data.high_pass import Ui_HighPassData
from app.approximators.butterworth import ButterworthApprox
from app.approximators.chebyshev_i import ChebyshevIAprrox
from app.approximators.chebyshev_ii import ChebyshevIIApprox
from app.approximators.legendre import LegendreApprox
from app.approximators.bessel import BesselApprox
from app.approximators.gauss import GaussApprox
from app.approximators.cauer import CauerApprox

class HighPassData(QtWid.QWidget, Ui_HighPassData):

    def __init__(self, *args, **kwargs):
        super(HighPassData, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Approximators for passing data to
        self.approximators = [ButterworthApprox(), ChebyshevIAprrox(), ChebyshevIIApprox(), LegendreApprox(), BesselApprox(), GaussApprox(), CauerApprox()]
        self.approx_index = 0

        # Signal and slot connections
        self.gain.valueChanged.connect(self.on_change)
        self.pass_freq.valueChanged.connect(self.on_change)
        self.stop_freq.valueChanged.connect(self.on_change)
        self.pass_att.valueChanged.connect(self.on_change)
        self.stop_att.valueChanged.connect(self.on_change)
        self.denorm_perc.valueChanged.connect(self.on_change)
        self.order.valueChanged.connect(self.on_change)
        self.q_max.valueChanged.connect(self.on_change)
        self.denorm_select.currentIndexChanged.connect(self.on_change)
        self.order_fixed.stateChanged.connect(self.on_change)
        self.q_fixed.stateChanged.connect(self.on_change)

        self.on_change()


    def on_change(self):
        if self.order_fixed.isChecked():
            if self.approx_index != 6:
                # Cauer filter needs the stopband attenuation data
                self.stop_att.setDisabled(True)
            else:
                self.stop_att.setEnabled(True)
            self.order.setEnabled(True)
            if self.approx_index != 2:
                # Cheby 2 needs the stopband frequency instead of the passband frequency
                self.pass_freq.setDisabled(True)
            else:
                self.stop_freq.setDisabled(True)
            self.denorm_select.setCurrentIndex(0)
            self.denorm_perc.setValue(0)
            self.denorm_select.setDisabled(True)
            self.denorm_perc.setDisabled(True)
            self.q_fixed.setDisabled(True)

        elif self.q_fixed.isChecked():
            if self.approx_index != 6:
                # Cauer filter needs the stopband attenuation data
                self.stop_att.setDisabled(True)
            else:
                self.stop_att.setEnabled(True)
            self.q_max.setEnabled(True)
            if self.approx_index != 2:
                # Cheby 2 needs the stopband frequency instead of the passband frequency
                self.pass_freq.setDisabled(True)
            else:
                self.stop_freq.setDisabled(True)
            self.denorm_select.setCurrentIndex(0)
            self.denorm_perc.setValue(0)
            self.denorm_select.setDisabled(True)
            self.denorm_perc.setDisabled(True)
            self.order_fixed.setDisabled(True)

        else:
            self.order.setDisabled(True)
            self.q_max.setDisabled(True)
            self.stop_freq.setEnabled(True)
            self.stop_att.setEnabled(True)
            self.denorm_select.setEnabled(True)
            self.order_fixed.setEnabled(True)
            self.q_fixed.setEnabled(True)

        if self.denorm_select.currentIndex() != 2:
            self.denorm_perc.setDisabled(True)
        else:
            self.denorm_perc.setEnabled(True)
        if self.denorm_select.currentIndex() == 0:
            self.denorm_perc.setValue(0)
        elif self.denorm_select.currentIndex() ==1:
            self.denorm_perc.setValue(100)

        self.approximators[self.approx_index].type = 'high-pass'
        self.approximators[self.approx_index].gain = self.gain.value()
        self.approximators[self.approx_index].fpl = self.pass_freq.value()
        self.approximators[self.approx_index].fal = self.stop_freq.value()
        self.approximators[self.approx_index].Apl = self.pass_att.value()
        self.approximators[self.approx_index].Aal = self.stop_att.value()
        self.approximators[self.approx_index].denorm = self.denorm_perc.value()
        self.approximators[self.approx_index].ord = self.order.value()
        self.approximators[self.approx_index].q = self.q_max.value()