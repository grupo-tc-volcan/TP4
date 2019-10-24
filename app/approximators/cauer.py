# Third-party modules
import scipy.signal as ss

# filters-tool project modules
from app.approximators.approximator import AttFilterApproximator

class CauerApprox(AttFilterApproximator):

    def __init__(self):
        super(CauerApprox, self).__init__()
