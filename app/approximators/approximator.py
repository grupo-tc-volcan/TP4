# Third-party modules
import scipy.signal as ss

# Python native modules
from enum import Enum


class ApproximationErrorCode(Enum):
    """ Approximation error codes returned when trying to compute H(s). 
    """
    OK = "OK"                           # No errors detected
    INVALID_TYPE = "INVALID_TYPE"       # Non-identified filter type in self.type
    INVALID_GAIN = "INVALID_GAIN"       # Gain is 0
    INVALID_FREQ = "INVALID_FREQ"       # Frequency is <= 0 or fpr < fpl or fp > fa (Depending the type of filter)
    INVALID_ATTE = "INVALID_ATTE"       # Attenuation is 0, or negative...
    INVALID_Q = "INVALID_Q"             # Negative Q factor
    INVALID_ORDER = "INVALID_ORDER"     # Negative order
    INVALID_DENORM = "INVALID_DENORM"   # Invalid range of denormalisation factor


class AttFilterApproximator():
    def __init__(self):
        # Data to perform approximation
        self.reset_parameters()

    #----------------#
    # Public Methods #
    #----------------#

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

        self.h_norm = None
        self.h_denorm = None
    
    def compute(self) -> ApproximationErrorCode:
        """ Computes the transfer function with the filled parameters
        of the approximation. Any error will be returned as an error code.
        """
        # Default error code
        error_code = self._validate_general()
        if error_code is ApproximationErrorCode.OK:

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

            # Findind the transfer function for the given parameters
            if error_code is ApproximationErrorCode.OK:
                
                # When a fixed order is given, it should be prioritised...
                # calculates the normalised transfer function
                if self.ord > 0:
                    error_code = self.compute_normalised_by_order(self.Apl, self.ord)
                elif self.q > 0:
                    error_code = self.compute_normalised_by_selectivity(self.Apl, self.q)
                else:
                    ap, aa, wan = self._normalised_template()
                    error_code = self.compute_normalised_by_template(ap, aa, wan)
                
                # Denormalisation process, first we need to pass every transfer function
                # to a TrasnferFunction object, using that apply the denormalisation
                # algorithm of scipy.signal... finally translating ir to a ZeroPolesGain object!
                if error_code is ApproximationErrorCode.OK:
                    error_code = self._denormalised_transfer_function()

        # Returning the error code...
        return error_code
    
    #-------------------------#
    # Internal Public Methods #
    #-------------------------#

    def compute_normalised_by_selectivity(self, ap, q) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the minimum order which not
        exceeds the given maximum q factor """
        raise NotImplementedError

    def compute_normalised_by_template(self, ap, aa, wan) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the normalised template """
        raise NotImplementedError

    def compute_normalised_by_order(self, ap, n) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the fixed order """
        raise NotImplementedError
    
    #-----------------#
    # Private Methods #
    #-----------------#

    def _denormalised_transfer_function(self) -> ApproximationErrorCode:
        """ Denormalises the transfer function returned by the approximation used. """
        return ApproximationErrorCode.OK # Code here please!

    def _normalised_template(self) -> tuple:
        """ Given the filter type and its parameters, it returns
        a tuple containing the normalised parameters of the template.
        Returns -> (ap, aa, aan)
        """
        return 0, 0, 0 # Code here please!

    def _validate_general(self) -> ApproximationErrorCode:
        """ Returns if general parameters are valid """
        if self.gain <= 0:
            return ApproximationErrorCode.INVALID_GAIN
        elif self.ord <= 0:
            return ApproximationErrorCode.INVALID_ORDER
        elif self.q <= 0:
            return ApproximationErrorCode.INVALID_Q
        elif self.denorm < 0 or self.denorm > 100:
            return ApproximationErrorCode.INVALID_DENORM

        return ApproximationErrorCode.OK

    def _validate_low_pass(self) -> ApproximationErrorCode:
        """ Returns whether the parameters of the approximation
        are valid or not using a low-pass.
        """
        if self.ord == 0 and self.q == 0:
            if self.fpl >= self.fal or self.fpl <= 0 or self.fal <= 0:
                return ApproximationErrorCode.INVALID_FREQ
            elif self.Apl <= 0 or self.Aal <= 0:
                return ApproximationErrorCode.INVALID_ATTE
        else:
            if self.Apl <= 0:
                return ApproximationErrorCode.INVALID_ATTE
            elif self.fpl <= 0:
                return ApproximationErrorCode.INVALID_FREQ
        
        return ApproximationErrorCode.OK


    def _validate_high_pass(self) -> ApproximationErrorCode:
        """ Returns whether the parameters of the approximation
        are valid or not using a high-pass.
        """
        if self.ord == 0 and self.q == 0:
            if self.fpl <= self.fal or self.fpl <= 0 or self.fal <= 0:
                return ApproximationErrorCode.INVALID_FREQ
            elif self.Apl <= 0 or self.Aal <= 0:
                return ApproximationErrorCode.INVALID_ATTE
        else:
            if self.Apl <= 0:
                return ApproximationErrorCode.INVALID_ATTE
            elif self.fpl <= 0:
                return ApproximationErrorCode.INVALID_FREQ
        
        return ApproximationErrorCode.OK

    def _validate_band_pass(self) -> ApproximationErrorCode:
        """ Returns whether the parameters of the approximation
        are valid or not using a band-pass.
        """
        if self.ord == 0 or self.q == 0:
            if self.fpl <= 0 or self.fpr <= 0 or self.fal <= 0 or self.far <= 0:
                return ApproximationErrorCode.INVALID_FREQ
            elif self.fpl >= self.fpr or self.fal >= self.far:
                return ApproximationErrorCode.INVALID_FREQ
            elif self.fpl <= self.fal or self.fpr >= self.far:
                return ApproximationErrorCode.INVALID_FREQ
            elif self.Apl <= 0 or self.Aal <= 0:
                return ApproximationErrorCode.INVALID_ATTE
        else:
            if self.fpl <= 0 or self.fpr <= 0:
                return ApproximationErrorCode.INVALID_FREQ
            elif self.fpl >= self.fpr:
                return ApproximationErrorCode.INVALID_FREQ
            elif self.Apl <= 0:
                return ApproximationErrorCode.INVALID_ATTE
        
        return ApproximationErrorCode.OK

    def _validate_band_reject(self) -> ApproximationErrorCode:
        """ Returns whether the parameters of the approximation
        are valid or not using a band-reject.
        """
        if self.ord == 0 or self.q == 0:
            if self.fpl <= 0 or self.fpr <= 0 or self.fal <= 0 or self.far <= 0:
                return ApproximationErrorCode.INVALID_FREQ
            elif self.fpl >= self.fpr or self.fal >= self.far:
                return ApproximationErrorCode.INVALID_FREQ
            elif self.fpl >= self.fal or self.fpr <= self.far:
                return ApproximationErrorCode.INVALID_FREQ
            elif self.Apl <= 0 or self.Aal <= 0:
                return ApproximationErrorCode.INVALID_ATTE
        else:
            if self.fpl <= 0 or self.fpr <= 0:
                return ApproximationErrorCode.INVALID_FREQ
            elif self.fpl >= self.fpr:
                return ApproximationErrorCode.INVALID_FREQ
            elif self.Apl <= 0:
                return ApproximationErrorCode.INVALID_ATTE
        
        return ApproximationErrorCode.OK


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
