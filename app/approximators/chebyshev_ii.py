# Third-party modules
import scipy.signal as ss

# filters-tool project modules
from app.approximators.approximator import AttFilterApproximator

class ChebyshevIIApprox(AttFilterApproximator):

    def __init__(self):
        super(ChebyshevIIApprox, self).__init__()