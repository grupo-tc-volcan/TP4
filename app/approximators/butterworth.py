# Third-party modules
import scipy.signal as ss

# filters-tool project modules
from app.approximators.approximator import AttFilterApproximator

class ButterworthApprox(AttFilterApproximator):

    def __init__(self):
        super(ButterworthApprox, self).__init__()
