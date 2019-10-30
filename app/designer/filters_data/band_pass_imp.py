# Third-party modules
import PyQt5.QtWidgets as QtWid

# filters-tool project modules
from app.designer.filters_data.band_pass import Ui_BandPassData
from app.approximators.butterworth import ButterworthApprox
from app.approximators.chebyshev_i import ChebyshevIApprox
from app.approximators.chebyshev_ii import ChebyshevIIApprox
from app.approximators.legendre import LegendreApprox
from app.approximators.bessel import BesselApprox
from app.approximators.gauss import GaussApprox
from app.approximators.cauer import CauerApprox

class BandPassData(QtWid.QWidget, Ui_BandPassData):

    def __init__(self, *args, **kwargs):
        super(BandPassData, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Approximators for passing data to
        self.approximators = [ButterworthApprox(), ChebyshevIApprox(), ChebyshevIIApprox(), LegendreApprox(), BesselApprox(), GaussApprox(), CauerApprox()]
        self.approx_index = 0

        # Signal and slot connections
        self.gain.valueChanged.connect(self.on_change)
        self.pass_freq_l.valueChanged.connect(self.on_change)
        self.pass_freq_r.valueChanged.connect(self.on_change)
        self.stop_freq_l.valueChanged.connect(self.on_change)
        self.stop_freq_r.valueChanged.connect(self.on_change)
        self.pass_att.valueChanged.connect(self.on_change)
        self.stop_att_l.valueChanged.connect(self.on_change)
        self.stop_att_r.valueChanged.connect(self.on_change)
        self.denorm_perc.valueChanged.connect(self.on_change)
        self.order.valueChanged.connect(self.on_change)
        self.q_max.valueChanged.connect(self.on_change)
        self.denorm_select.currentIndexChanged.connect(self.on_change)
        self.order_fixed.stateChanged.connect(self.on_change)
        self.q_fixed.stateChanged.connect(self.on_change)

        self.on_change()


    def on_change(self):
        if self.order_fixed.isChecked():
            if self.approx_index == 6:
                # Cauer filter needs the stopband attenuation data
                self.stop_att_l.setEnabled(True)
                self.stop_att_r.setEnabled(True)
            elif self.approx_index == 2:
                # Cheby 2 needs the stopband attenuation instead of the passband attenuation
                self.pass_att.setDisabled(True)
                self.stop_att_l.setEnabled(True)
                self.stop_att_r.setEnabled(True)
            else:
                self.pass_att.setEnabled(True)
                self.stop_att_l.setDisabled(True)
                self.stop_att_r.setDisabled(True)

            if self.approx_index == 2:
                # Cheby 2 needs the stopband frequency instead of the passband frequency
                self.pass_freq_l.setDisabled(True)
                self.pass_freq_r.setDisabled(True)
                self.stop_freq_l.setEnabled(True)
                self.stop_freq_r.setEnabled(True)
            else:
                self.stop_freq_l.setDisabled(True)
                self.stop_freq_r.setDisabled(True)
                self.pass_freq_l.setEnabled(True)
                self.pass_freq_r.setEnabled(True)

            self.denorm_select.setCurrentIndex(0)
            self.denorm_perc.setValue(0)
            self.denorm_select.setDisabled(True)
            self.denorm_perc.setDisabled(True)
            self.order.setEnabled(True)
            self.q_fixed.setDisabled(True)

        elif self.q_fixed.isChecked():
            if self.approx_index == 6:
                # Cauer filter needs the stopband attenuation data
                self.stop_att_l.setEnabled(True)
                self.stop_att_r.setEnabled(True)
            elif self.approx_index == 2:
                # Cheby 2 needs the stopband attenuation instead of the passband attenuation
                self.pass_att.setDisabled(True)
                self.stop_att_l.setEnabled(True)
                self.stop_att_r.setEnabled(True)
            else:
                self.pass_att.setEnabled(True)
                self.stop_att_l.setDisabled(True)
                self.stop_att_r.setDisabled(True)

            if self.approx_index == 2:
                # Cheby 2 needs the stopband frequency instead of the passband frequency
                self.pass_freq_l.setDisabled(True)
                self.pass_freq_r.setDisabled(True)
                self.stop_freq_l.setEnabled(True)
                self.stop_freq_r.setEnabled(True)
            else:
                self.stop_freq_l.setDisabled(True)
                self.stop_freq_r.setDisabled(True)
                self.pass_freq_l.setEnabled(True)
                self.pass_freq_r.setEnabled(True)

            self.denorm_select.setCurrentIndex(0)
            self.denorm_perc.setValue(0)
            self.denorm_select.setDisabled(True)
            self.denorm_perc.setDisabled(True)
            self.q_max.setEnabled(True)
            self.order_fixed.setDisabled(True)

        else:
            self.order.setDisabled(True)
            self.q_max.setDisabled(True)
            self.stop_freq_l.setEnabled(True)
            self.stop_freq_r.setEnabled(True)
            self.stop_att_l.setEnabled(True)
            self.stop_att_r.setEnabled(True)
            self.pass_att.setEnabled(True)
            self.pass_freq_l.setEnabled(True)
            self.pass_freq_r.setEnabled(True)
            self.denorm_select.setEnabled(True)
            self.order_fixed.setEnabled(True)
            self.q_fixed.setEnabled(True)
            self.q_max.setValue(0)
            self.order.setValue(0)

        if self.denorm_select.currentIndex() != 2:
            self.denorm_perc.setDisabled(True)
        else:
            self.denorm_perc.setEnabled(True)
        if self.denorm_select.currentIndex() == 0:
            self.denorm_perc.setValue(0)
        elif self.denorm_select.currentIndex() ==1:
            self.denorm_perc.setValue(100)

        self.approximators[self.approx_index].type = 'band-pass'
        self.approximators[self.approx_index].gain = self.gain.value()
        self.approximators[self.approx_index].fpl = self.pass_freq_l.value()
        self.approximators[self.approx_index].fpr = self.pass_freq_r.value()
        self.approximators[self.approx_index].fal = self.stop_freq_l.value()
        self.approximators[self.approx_index].far = self.stop_freq_r.value()
        self.approximators[self.approx_index].Apl = self.pass_att.value()
        self.approximators[self.approx_index].Aal = self.stop_att_l.value()
        self.approximators[self.approx_index].Aar = self.stop_att_r.value()
        self.approximators[self.approx_index].denorm = self.denorm_perc.value()
        self.approximators[self.approx_index].ord = self.order.value()
        self.approximators[self.approx_index].q = self.q_max.value()