# Third-party modules
import scipy.signal as ss

# filters-tool project modules
from app.approximators.approximator import GroupDelayFilterApproximator

class BesselApprox(GroupDelayFilterApproximator):

    def __init__(self):
        super(BesselApprox, self).__init__()
