# Third-party modules
import scipy.signal as ss
import numpy as np

# filters-tool project modules
from app.approximators.approximator import AttFilterApproximator
from app.approximators.approximator import ApproximationErrorCode


class CauerApprox(AttFilterApproximator):

    def __init__(self):
        super(CauerApprox, self).__init__()

    # ------------------------- #
    #  Internal Public Methods  #
    # ------------------------- #
    def adjust_function_gain(self, gain):
        """ Adjusts the normalised transfer function to have a unity gain """
        super(CauerApprox, self).adjust_function_gain(gain)

        # According to the order... normalise
        wa, aa, _, ap = self.get_norm_template()
        if len(self.h_norm.poles) % 2 == 0:
            self.h_norm.gain = self.h_norm.gain / (10 ** (ap / 20))

    def compute_normalised_by_order(self, ap, n, aa=None) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the fixed order """
        # Computing needed constants
        zeros, poles, gain = ss.ellipap(n, ap, aa)
        self.h_norm = ss.ZerosPolesGain(zeros, poles, gain)
        return ApproximationErrorCode.OK

    def _validate_low_pass_by_fixed(self) -> ApproximationErrorCode:
        error_code = super(CauerApprox, self)._validate_low_pass_by_fixed()
        if error_code is ApproximationErrorCode.OK:
            if self.Aal <= 0:
                error_code = ApproximationErrorCode.INVALID_ATTE
            elif self.Aal <= self.Apl:
                error_code = ApproximationErrorCode.INVALID_ATTE
        return error_code

    def _validate_high_pass_by_fixed(self) -> ApproximationErrorCode:
        error_code = super(CauerApprox, self)._validate_high_pass_by_fixed()
        if error_code is ApproximationErrorCode.OK:
            if self.Aal <= 0:
                error_code = ApproximationErrorCode.INVALID_ATTE
            elif self.Aal <= self.Apl:
                error_code = ApproximationErrorCode.INVALID_ATTE

        return error_code

    def _validate_band_pass_by_fixed(self) -> ApproximationErrorCode:
        error_code = super(CauerApprox, self)._validate_band_pass_by_fixed()
        if error_code is ApproximationErrorCode.OK:
            if self.Aal <= 0 or self.Aar < 0:
                error_code = ApproximationErrorCode.INVALID_ATTE
            elif self.Apl >= self.Aal or (self.Apl >= self.Aar and self.Aar):
                error_code = ApproximationErrorCode.INVALID_ATTE
            else:
                if self.Apr:
                    if self.Apr >= self.Aal or (self.Apr >= self.Aar and self.Aar):
                        error_code = ApproximationErrorCode.INVALID_ATTE

        return error_code

    def _validate_band_stop_by_fixed(self) -> ApproximationErrorCode:
        """ Returns whether the parameters of the approximation
        are valid or not using a band-reject.
        """
        error_code = super(CauerApprox, self)._validate_band_stop_by_fixed()
        if error_code is ApproximationErrorCode.OK:
            if self.Aal <= 0 or self.Aar < 0:
                error_code = ApproximationErrorCode.INVALID_ATTE
            elif self.Apl >= self.Aal or (self.Apl >= self.Aar and self.Aar):
                error_code = ApproximationErrorCode.INVALID_ATTE
            else:
                if self.Apr:
                    if self.Apr >= self.Aal or (self.Apr >= self.Aar and self.Aar):
                        error_code = ApproximationErrorCode.INVALID_ATTE

        return error_code
