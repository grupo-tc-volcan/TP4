# Third-party modules
import scipy.signal as ss

class ButterworthApprox():

    def __init__(self):
        # Data to perform approximation
        self.reset_paramethers()


    def reset_paramethers(self):
        self.type = ''
        self.gain = 0
        self.fpl = 0
        self.fpr = 0
        self.fal = 0
        self.far = 0
        self.Apl = 0
        self.Apr = 0
        self.Aal = 0
        self.Aar = 0
        self.denorm = 0
        self.ord = 0
        self.q = 0
        self.group_delay = 0
        self.tol = 0
