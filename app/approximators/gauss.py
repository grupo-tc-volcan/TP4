# Third-party modules
import scipy.signal as ss

# filters-tool project modules
from app.approximators.approximator import GroupDelayFilterApproximator

class GaussApprox(GroupDelayFilterApproximator):

    def __init__(self):
        super(GaussApprox, self).__init__()