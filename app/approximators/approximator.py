# Third-party modules
import scipy.signal as ss
import numpy as np

# Python native modules
from enum import Enum
from functools import partial

# Constant Values
MAXIMUM_ORDER = 20


class ApproximationErrorCode(Enum):
    """ Approximation error codes returned when trying to compute H(s). 
    """
    OK = "OK"                                       # No errors detected
    INVALID_TYPE = "INVALID_TYPE"                   # Non-identified filter type in self.type
    INVALID_GAIN = "INVALID_GAIN"                   # Gain is 0
    INVALID_FREQ = "INVALID_FREQ"                   # Frequency is <= 0 or fpr < fpl or fp > fa (Depending the type of filter)
    INVALID_ATTE = "INVALID_ATTE"                   # Attenuation is 0, or negative...
    INVALID_Q = "INVALID_Q"                         # Negative Q factor
    INVALID_ORDER = "INVALID_ORDER"                 # Negative order
    INVALID_DENORM = "INVALID_DENORM"               # Invalid range of denormalisation factor
    MAXIMUM_ORDER_REACHED = "MAXIMUM_ORDER_REACHED" # Iterative approximation reached maximum order


class FilterType(Enum):
    """ Approximation filter types """
    LOW_PASS = "low-pass"
    HIGH_PASS = "high-pass"
    BAND_PASS = "band-pass"
    BAND_REJECT = "band-reject"


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
    
    def get_normalised_zpk(self) -> tuple:
        """ Returns a tuple of three elements containing Zeros, Poles and Gain,
        of the normalised transfer function.
        Return -> (zeros, poles, gain) or None if not computed!
        """
        if self.h_norm is None:
            return None
        else:
            return (self.h_norm.zeros, self.h_norm.poles, self.h_norm.gain)
    
    def get_zpk(self) -> tuple:
        """ Returns a tuple of three elements containing Zeros, Poles and Gain,
        of the denormalised transfer function.
        Return -> (zeros, poles, gain) or None if not computed!
        """
        if self.h_denorm is None:
            return None
        else:
            return (self.h_denorm.zeros, self.h_denorm.poles, self.h_denorm.gain)
    
    def compute(self) -> ApproximationErrorCode:
        """ Computes the transfer function with the filled parameters
        of the approximation. Any error will be returned as an error code.
        """
        # Default error code
        error_code = self._validate_general()
        if error_code is ApproximationErrorCode.OK:

            # Verifying if valid filter type is given
            if self.type == FilterType.LOW_PASS.value:
                error_code = self._validate_low_pass()
            elif self.type == FilterType.HIGH_PASS.value:
                error_code = self._validate_high_pass()
            elif self.type == FilterType.BAND_PASS.value:
                error_code = self._validate_band_pass()
            elif self.type == FilterType.BAND_REJECT.value:
                error_code = self._validate_band_reject()
            else:
                error_code = ApproximationErrorCode.INVALID_TYPE

            # Findind the transfer function for the given parameters
            if error_code is ApproximationErrorCode.OK:
                
                # When using a maximum Q value, iterates with fixed orders
                # and verifies if matches...
                begin_order = 1 if self.q > 0 else self.ord
                end_order = MAXIMUM_ORDER if self.q > 0 else self.ord
                for order in range(begin_order, end_order + 1):
                    self.ord = order

                    # When a fixed order is given, it should be prioritised...
                    # calculates the normalised transfer function
                    if self.ord > 0:
                        error_code = self.compute_normalised_by_order(self.Apl, self.ord)
                    else:
                        ap, aa, wan = self._normalised_template()
                        error_code = self.compute_normalised_by_template(ap, aa, wan)
                    
                    # Denormalisation process, first we need to pass every transfer function
                    # to a TrasnferFunction object, using that apply the denormalisation
                    # algorithm of scipy.signal... finally translating ir to a ZeroPolesGain object!
                    if error_code is ApproximationErrorCode.OK:
                        error_code = self._denormalised_transfer_function()

                        # If using the Q maximum value mode of design, check if valid h_denorm
                        if error_code is ApproximationErrorCode.OK:
                            if self.matches_normalised_selectivity(self.q, self.h_denorm):
                                break
                        else:
                            break

        # Returning the error code...
        return error_code
    
    #-------------------------#
    # Internal Public Methods #
    #-------------------------#

    def compute_normalised_by_template(self, ap, aa, wan) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the normalised template """
        return self._compute_normalised_by_match(ap, partial(self.matches_normalised_template, ap, aa, wan))

    def compute_normalised_by_order(self, ap, n) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the fixed order """
        raise NotImplementedError
    
    #-----------------#
    # Private Methods #
    #-----------------#

    def _denormalised_transfer_function(self) -> ApproximationErrorCode:
        """ Denormalises the transfer function returned by the approximation used. """
        return ApproximationErrorCode.OK # Code here please!
    
    def _compute_normalised_by_match(self, ap, callback) -> ApproximationErrorCode:
        """ Generates normalised transfer function for each order until the callbacks
        verifies it matches the requierements. 
        The callback should expect a ZerosPoleGain object from Scipy.Signal,
        returning whether it verifies or not the requirements. """
        for order in range(1, MAXIMUM_ORDER + 1):
            error_code = self.compute_normalised_by_order(ap, order)
            if error_code is ApproximationErrorCode.OK:
                if callback(self.h_norm):
                    return ApproximationErrorCode.OK
                else:
                    self.h_norm = None
            else:
                return error_code
        else:
            return ApproximationErrorCode.MAXIMUM_ORDER_REACHED

    def _normalised_template(self) -> tuple:
        """ Given the filter type and its parameters, it returns
        a tuple containing the normalised parameters of the template.
        Returns -> (ap, aa, wan)
        """
        if self.Apl > 0 and self.Apr > 0:
            ap = min(self.Apl, self.Apr)
        elif self.Apl > 0:
            ap = self.Apl
        elif self.Apr > 0:
            ap = self.Apr

        if self.Aal > 0 and self.Aar > 0:
            aa = max(self.Aal, self.Aar)
        elif self.Aal > 0:
            aa = self.Aal
        elif self.Aar > 0:
            aa = self.Aar

        if self.type == FilterType.LOW_PASS.value:
            return ap, aa, self.fal / self.fpl
        elif self.type == FilterType.HIGH_PASS.value:
            return ap, aa, self.fpl / self.fal
        elif self.type == FilterType.BAND_PASS.value:
            return ap, aa, (self.far - self.fal) / (self.fpr - self.fpl)
        elif self.type == FilterType.BAND_REJECT.value:
            return ap, aa, (self.fpr - self.fpl) / (self.far - self.fal)

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
    
    #----------------#
    # Static Methods #
    #----------------#

    @staticmethod
    def matches_normalised_template(ap, aa, wa, zpk) -> bool:
        """ Returns whether the ZeroPolesGain object verifies the normalised
        template given by the aa, ap, wa values. """
        if zpk is None:
            return False

        w, mag, phase = ss.bode(zpk, w=[1, wa])
        return mag[0] >= -ap and mag[1] <= -aa

    @staticmethod
    def matches_normalised_selectivity(max_q, zpk) -> bool:
        """ Returns whether the ZeroPolesGain object does not exceed the maximum
        selectivity value given by the user. """
        if zpk is None:
            return False

        for pole in zpk.poles:
            if type(pole) is complex:
                k = ( pole.imag / pole.real ) ** 2
                xi = np.sqrt( 1 / (1 + k) )
                q = 1 / (2 * xi)
                
                if q > max_q:
                    return False
            else:
                continue
        else:
            return True

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
