# Third-party modules
import scipy.signal as ss

# filters-tool project modules
from app.approximators.approximator import AttFilterApproximator

class ChebyshevIAprrox(AttFilterApproximator):

    def __init__(self):
        super(ChebyshevIAprrox, self).__init__()