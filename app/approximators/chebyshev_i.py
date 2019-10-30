# Third-party modules
import scipy.signal as ss
import numpy as np

# filters-tool project modules
from app.approximators.approximator import AttFilterApproximator
from app.approximators.approximator import ApproximationErrorCode


class ChebyshevIApprox(AttFilterApproximator):

    def __init__(self):
        super(ChebyshevIApprox, self).__init__()

    # ------------------------- #
    #  Internal Public Methods  #
    # ------------------------- #
    def adjust_function_gain(self, gain):
        """ Adjusts the normalised transfer function to have a unity gain """
        super(ChebyshevIApprox, self).adjust_function_gain(gain)

        # Using the normalised template to verify when the order is even
        # and moving the ripple gain
        wa, aa, _, ap = self.get_norm_template()
        order = self.ord if self.ord else self.compute_order(ap, aa, wa)
        if order % 2 == 0:
            # Compute epsilon and the ripple and move the gain of the function
            self.h_norm.gain = self.h_norm.gain / (10 ** (ap / 20))

    def compute_normalised_by_template(self, ap, aa, wpn, wan) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the normalised template """
        order = self.compute_order(ap, aa, wan)
        return self.compute_normalised_by_order(ap, order, aa)

    def compute_normalised_by_order(self, ap, n, aa) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the fixed order """
        # Computing needed constants
        zeros, poles, gain = ss.cheb1ap(n, ap)
        self.h_norm = ss.ZerosPolesGain(zeros, poles, gain)
        return ApproximationErrorCode.OK

    # ----------------- #
    #  Private Methods  #
    # ----------------- #
    @staticmethod
    def compute_epsilon(ap):
        return np.sqrt(10 ** (ap / 10) - 1)

    @staticmethod
    def compute_order(ap, aa, wan):
        order = np.arccosh(ChebyshevIApprox.compute_epsilon(aa) / ChebyshevIApprox.compute_epsilon(ap)) / np.arccosh(wan)
        rounded_order = round(order)
        return rounded_order if rounded_order >= order else rounded_order + 1

    @staticmethod
    def compute_ripple(epsilon):
        return 1 / (1 + epsilon ** 2)
