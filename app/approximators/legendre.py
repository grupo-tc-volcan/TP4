# Third-party modules
import scipy.signal as ss

# Third-party modules
import scipy.signal as ss

# filters-tool project modules
from app.approximators import legendre_calculator as l_calc
from app.approximators.approximator import AttFilterApproximator

class LegendreApprox(AttFilterApproximator):

    def __init__(self):
        super(LegendreApprox, self).__init__()