# Third-party modules
import scipy.signal as ss

# filters-tool project modules
from app.approximators.approximator import FilterApproximator

class GaussApprox(FilterApproximator):

    def __init__(self):
        # Data to perform approximation
        self.reset_paramethers()


    def reset_paramethers(self):
        self.type = 'group-delay'
        self.gain = 0
        self.fp = 0
        self.group_delay = 0
        self.tol = 0
        self.ord = 0
        self.q = 0

