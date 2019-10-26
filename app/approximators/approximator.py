# Third-party modules
import scipy.signal as ss

# Python native modules
from enum import Enum


class ApproximationErrorCode(Enum):
    """ Approximation error codes returned when trying to compute H(s).
    """
    OK = "OK"
    INVALID_TYPE = "INVALID_TYPE"


class AttFilterApproximator():
    def __init__(self):
        # Data to perform approximation
        self.reset_parameters()

    #--------------------
    # Public Methods 
    #--------------------

    def reset_parameters(self):
        """ Resets the parameters of the approximation to
        a default state.
        """
        self.type = 'low-pass'
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
    
    def compute(self):
        """ Computes the transfer function with the filled parameters
        of the approximation. Any error will be returned as an error code.
        """
        # Default error code
        error_code = ApproximationErrorCode.OK

        # Verifying if valid filter type is given
        if self.type == "low-pass":
            error_code = self._validate_low_pass()
        elif self.type == "high-pass":
            error_code = self._validate_high_pass()
        elif self.type == "band-pass":
            error_code = self._validate_band_pass()
        elif self.type == "band-reject":
            error_code = self._validate_band_reject()
        else:
            error_code = ApproximationErrorCode.INVALID_TYPE

        # Returning the error code...
        return error_code
    
    #--------------------
    # Private Methods
    #--------------------

    def _validate_low_pass(self) -> ApproximationErrorCode:
        """ Returns whether the parameters of the approximation
        are valid or not using a low-pass.
        """
        return True # Code here please!

    def _validate_high_pass(self) -> ApproximationErrorCode:
        """ Returns whether the parameters of the approximation
        are valid or not using a high-pass.
        """
        return True # Code here please!

    def _validate_band_pass(self) -> ApproximationErrorCode:
        """ Returns whether the parameters of the approximation
        are valid or not using a band-pass.
        """
        return True # Code here please!

    def _validate_band_reject(self) -> ApproximationErrorCode:
        """ Returns whether the parameters of the approximation
        are valid or not using a band-reject.
        """
        return True # Code here please!


class GroupDelayFilterApproximator():
    def __init__(self):
        # Data to perform approximation
        self.reset_parameters()


    def reset_parameters(self):
        """ Resets the parameters of the approximation to
        a default state.
        """
        self.type = 'group-delay'
        self.gain = 0
        self.fa = 0
        self.Aa = 0
        self.ft = 0
        self.group_delay = 0
        self.tol = 0
        self.ord = 0
        self.q = 0
    
    def compute(self):
        """ Computes the transfer function with the filled parameters
        of the approximation. Any error will be returned as an error code.
        """
        pass