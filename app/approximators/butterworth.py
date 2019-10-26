# Third-party modules
import scipy.signal as ss
import numpy as np

# filters-tool project modules
from app.approximators.approximator import AttFilterApproximator
from app.approximators.approximator import ApproximationErrorCode

class ButterworthApprox(AttFilterApproximator):

    def __init__(self):
        super(ButterworthApprox, self).__init__()

    #-------------------------#
    # Internal Public Methods #
    #-------------------------#

    def compute_normalised_by_selectivity(self, ap, q) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the minimum order which not
        exceeds the given maximum q factor """
        return super(ButterworthApprox, self).compute_normalised_by_selectivity(ap, q)

    def compute_normalised_by_template(self, ap, aa, wan) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the normalised template """
        order = self.compute_order(ap, aa, wan)
        return self.compute_normalised_by_order(ap, order)

    def compute_normalised_by_order(self, ap, n) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the fixed order """
        # Computing needed constants 
        epsilon = self.compute_epsilon(ap)
        factor = 1 / np.float_power(epsilon, 1 / n)

        # Getting the Butterworth approximation for the given order
        # and matching it with the given maximum attenuation for pass band
        zeros, poles, gain = ss.buttap(n)
        new_poles = [factor * pole for pole in poles]
        
        # Updating the local transfer function, no errors!
        self.h_norm = ss.lti(zeros, new_poles, gain)
        return ApproximationErrorCode.OK

    #-----------------#
    # Private Methods #
    #-----------------#

    @staticmethod
    def compute_order(ap, aa, wan):
        return np.log10( np.sqrt(10 ** (aa / 10) - 1) / np.sqrt(10 ** (ap / 10) - 1) ) / np.log10(wan)

    @staticmethod
    def compute_epsilon(ap):
        return np.sqrt(10 ** (ap / 10) - 1)
