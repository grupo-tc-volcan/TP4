# Third-party modules
import scipy.signal as ss
import numpy as np
from matplotlib import pyplot

# filters-tool project modules
from app.approximators.approximator import AttFilterApproximator
from app.approximators.approximator import ApproximationErrorCode


class ChebyshevIIApprox(AttFilterApproximator):

    def __init__(self):
        super(ChebyshevIIApprox, self).__init__()

    # ------------------------- #
    #  Internal Public Methods  #
    # ------------------------- #
    def get_norm_template(self) -> tuple:
        """ Returns a 4-element tuple containing the normalised
        parameters of the template.
        Returns -> (wa, aa, wp, ap)
        """
        wa, aa, wp, ap = super(ChebyshevIIApprox, self)._normalised_template()
        return None if wp == 0 else 1 / wp, aa, None if wa == 0 else 1 / wa, ap

    def denormalise_to_low_pass(self) -> tuple:
        """ Denormalises the filter to low pass and returns the denormalised (zeros, poles, gain) """
        return ss.lp2lp_zpk(self.h_norm.zeros, self.h_norm.poles, self.h_norm.gain, 2 * np.pi * self.fal)

    def denormalise_to_high_pass(self) -> tuple:
        """ Denormalises the filter to high pass and returns the denormalised (zeros, poles, gain) """
        return ss.lp2hp_zpk(self.h_norm.zeros, self.h_norm.poles, self.h_norm.gain, 2 * np.pi * self.fal)

    def denormalise_to_band_pass(self) -> tuple:
        """ Denormalises the filter to high pass and returns the denormalised (zeros, poles, gain) """
        return ss.lp2bp_zpk(self.h_norm.zeros, self.h_norm.poles, self.h_norm.gain, 2 * np.pi * np.sqrt(self.fal * self.far), 2 * np.pi * (self.far - self.fal))

    def denormalise_to_band_stop(self) -> tuple:
        """ Denormalises the filter to high pass and returns the denormalised (zeros, poles, gain) """
        return ss.lp2bs_zpk(self.h_norm.zeros, self.h_norm.poles, self.h_norm.gain, 2 * np.pi * np.sqrt(self.fpl * self.fpr), 2 * np.pi * (self.far - self.fal))

    def compute_normalised_by_template(self, ap, aa, wpn, wan) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the normalised template """
        order = self.compute_order(ap, aa, wpn)
        error_code = self.compute_normalised_by_order(ap, order, aa)
        return error_code

    def compute_normalised_by_order(self, ap, n, aa) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the fixed order """
        # Computing needed constants
        zeros, poles, gain = ss.cheb2ap(n, aa)
        wa, aa, wp, ap = self.get_norm_template()
        self.h_norm = ss.ZerosPolesGain(zeros, poles, gain)
        return ApproximationErrorCode.OK

    def denormalisation_factor(self, wa, aa, wp, ap):
        """ Returns the denormalisation factor to be used when
        adjusting the zeros and poles of the transfer function between the transition
        band. """
        if self.q == 0 and self.ord == 0:
            w_values, mag_values, _ = ss.bode(self.h_norm, w=np.linspace(wp / 100, wa * 10, num=10000))
            pass_band = [w for w, mag in zip(w_values, mag_values) if mag >= (-ap)]
            relative_adjust = ((wp - pass_band[-1]) / pass_band[-1]) * ((100 - self.denorm) / 100) + 1
        else:
            relative_adjust = 1

        return relative_adjust

    def _validate_low_pass_by_fixed(self) -> ApproximationErrorCode:
        if self.Aal <= 0:
            return ApproximationErrorCode.INVALID_ATTE
        elif self.fal <= 0:
            return ApproximationErrorCode.INVALID_FREQ
        else:
            return ApproximationErrorCode.OK

    def _validate_high_pass_by_fixed(self) -> ApproximationErrorCode:
        if self.Aal <= 0:
            return ApproximationErrorCode.INVALID_ATTE
        elif self.fal <= 0:
            return ApproximationErrorCode.INVALID_FREQ
        else:
            return ApproximationErrorCode.OK

    def _validate_band_pass_by_fixed(self) -> ApproximationErrorCode:
        if self.Aal <= 0 or self.Aar < 0:
            return ApproximationErrorCode.INVALID_ATTE
        elif self.fal <= 0 or self.far <= 0:
            return ApproximationErrorCode.INVALID_FREQ
        elif self.far <= self.fal:
            return ApproximationErrorCode.INVALID_FREQ
        else:
            return ApproximationErrorCode.OK

    def _validate_band_stop_by_fixed(self) -> ApproximationErrorCode:
        if self.Aal <= 0 or self.Aar < 0:
            return ApproximationErrorCode.INVALID_ATTE
        elif self.fal <= 0 or self.far <= 0:
            return ApproximationErrorCode.INVALID_FREQ
        elif self.far <= self.fal:
            return ApproximationErrorCode.INVALID_FREQ
        else:
            return ApproximationErrorCode.OK

    # ----------------- #
    #  Private Methods  #
    # ----------------- #

    @staticmethod
    def compute_epsilon(ap):
        return 1 / np.sqrt(10 ** (ap / 10) - 1)

    @staticmethod
    def compute_order(ap, aa, wpn):
        order = np.arccosh(ChebyshevIIApprox.compute_epsilon(ap) / ChebyshevIIApprox.compute_epsilon(aa)) / np.arccosh(1 / wpn)
        rounded_order = round(order)
        return rounded_order if rounded_order >= order else rounded_order + 1
