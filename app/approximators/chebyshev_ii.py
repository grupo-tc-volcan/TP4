# Third-party modules
import scipy.signal as ss
import numpy as np

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

    def compute_normalised_by_template(self, ap, aa, wpn, wan) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the normalised template """
        order = self.compute_order(ap, aa, wpn)
        return self.compute_normalised_by_order(ap, order, aa)

    def compute_normalised_by_order(self, ap, n, aa) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the fixed order """
        # Computing needed constants
        zeros, poles, gain = ss.cheb2ap(n, aa)
        self.h_norm = ss.ZerosPolesGain(zeros, poles, gain)
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
