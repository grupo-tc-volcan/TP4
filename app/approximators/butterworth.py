# Third-party modules
import scipy.signal as ss
import numpy as np

# filters-tool project modules
from app.approximators.approximator import AttFilterApproximator
from app.approximators.approximator import ApproximationErrorCode


class ButterworthApprox(AttFilterApproximator):

    def __init__(self):
        super(ButterworthApprox, self).__init__()

    # ------------------------- #
    #  Internal Public Methods  #
    # ------------------------- #

    def compute_normalised_by_template(self, ap, aa, wpn, wan) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the normalised template """
        order = self.compute_order(ap, aa, wan)
        return self.compute_normalised_by_order(ap, order)

    def compute_normalised_by_order(self, ap, n, aa) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the fixed order """
        # Computing needed constants 
        epsilon = self.compute_epsilon(ap)
        factor = 1 / np.float_power(epsilon, 1 / n)

        # Getting the Butterworth approximation for the given order
        # and matching it with the given maximum attenuation for pass band
        zeros, poles, gain = ss.buttap(n)
        new_zeros = zeros
        new_poles = [factor * pole for pole in poles]
        new_gain = gain

        # Updating the local transfer function, no errors!
        self.h_norm = ss.ZerosPolesGain(new_zeros, new_poles, new_gain)
        return ApproximationErrorCode.OK

    # ----------------- #
    #  Private Methods  #
    # ----------------- #

    @staticmethod
    def compute_order(ap, aa, wan):
        order = np.log10(np.sqrt(10 ** (aa / 10) - 1) / np.sqrt(10 ** (ap / 10) - 1)) / np.log10(wan)
        rounded_order = round(order)
        return rounded_order if rounded_order >= order else rounded_order + 1

    @staticmethod
    def compute_epsilon(ap):
        return np.sqrt(10 ** (ap / 10) - 1)
