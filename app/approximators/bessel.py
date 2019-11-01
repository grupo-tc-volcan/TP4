# Third-party modules
# Third-party modules
import scipy.signal as ss
import numpy as np

# filters-tool project modules
from app.approximators.approximator import GroupDelayFilterApproximator
from app.approximators.approximator import ApproximationErrorCode


class BesselApprox(GroupDelayFilterApproximator):

    def __init__(self):
        super(BesselApprox, self).__init__()

    # -------------------------#
    # Internal Public Methods #
    # -------------------------#

    def compute_normalised_by_order(self, gdn, wfn, order) -> ApproximationErrorCode:
        b, a = ss.bessel(order, gdn, analog=True,norm = 'delay')
        self.h_norm = ss.TransferFunction(b,a).to_zpk()
        return ApproximationErrorCode.OK
    # -----------------#
    # Private Methods #
    # -----------------#
    def _denormalised_transfer_function(self):
        b, a = ss.bessel(self.denorm_order, np.divide(1, self.group_delay * 1e-3), analog=True, norm='delay')
        self.h_denorm = ss.TransferFunction(b, a).to_zpk()
        self.adjust_function_gain(self.h_denorm, np.float_power(10, np.divide(self.gain,20)))
        return ApproximationErrorCode.OK
