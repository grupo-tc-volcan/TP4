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
    INVALID_GAIN = "INVALID_GAIN"                   # Gain < 0
    INVALID_FREQ = "INVALID_FREQ"                   # Frequency is <= 0 or fpr < fpl or fp > fa (Depending the type of filter)
    INVALID_ATTE = "INVALID_ATTE"                   # Attenuation is 0, or negative...
    INVALID_Q = "INVALID_Q"                         # Negative Q factor
    INVALID_ORDER = "INVALID_ORDER"                 # Negative order
    INVALID_DENORM = "INVALID_DENORM"               # Invalid range of denormalisation factor
    MAXIMUM_ORDER_REACHED = "MAXIMUM_ORDER_REACHED"         # Iterative approximation reached maximum order
    UNDEFINED_APPROXIMATION = "UNDEFINED_APPROXIMATION"     # Using the base class not an specific one
    INVALID_GROUP_DELAY = "INVALID_GROUP_DELAY"             # Group delay is 0 or negative
    INVALID_TOLERANCE = "INVALID_TOLERANCE"


class FilterType(Enum):
    """ Approximation filter types """
    LOW_PASS = "low-pass"
    HIGH_PASS = "high-pass"
    BAND_PASS = "band-pass"
    BAND_REJECT = "band-stop"


# noinspection PyAttributeOutsideInit,PyUnresolvedReferences
class AttFilterApproximator:
    def __init__(self):
        # Data to perform approximation
        self.reset_parameters()

    # ---------------  #
    #  Public Methods  #
    # ---------------- #
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

        self.h_aux = None
        self.h_norm = None
        self.h_denorm = None
        self.error_code = None

    def get_norm_template(self) -> tuple:
        """ Returns a 4-element tuple containing the normalised
        parameters of the template.
        Returns -> (wa, aa, wp, ap)
        """
        return self._normalised_template()
    
    def get_normalised_zpk(self):
        """ Returns a tuple of three elements containing Zeros, Poles and Gain,
        of the normalised transfer function.
        Return -> (zeros, poles, gain) or None if not computed!
        """
        if self.h_norm is None:
            return None
        else:
            return self.h_norm
    
    def get_zpk(self):
        """ Returns a tuple of three elements containing Zeros, Poles and Gain,
        of the denormalised transfer function.
        Return -> (zeros, poles, gain) or None if not computed!
        """
        if self.h_denorm is None:
            return None
        else:
            return self.h_denorm
    
    def compute(self) -> ApproximationErrorCode:
        """ Computes the transfer function with the filled parameters
        of the approximation. Any error will be returned as an error code.
        """
        # Default error code
        error_code = self._validate_general()
        if error_code is ApproximationErrorCode.OK:

            # Verifying if valid filter type is given
            if self.type == FilterType.LOW_PASS.value:
                error_code = self.validate_low_pass()
            elif self.type == FilterType.HIGH_PASS.value:
                error_code = self.validate_high_pass()
            elif self.type == FilterType.BAND_PASS.value:
                error_code = self.validate_band_pass()
            elif self.type == FilterType.BAND_REJECT.value:
                error_code = self.validate_band_stop()
            else:
                error_code = ApproximationErrorCode.INVALID_TYPE

            # Finding the transfer function for the given parameters
            if error_code is ApproximationErrorCode.OK:
                self.adjust_symmetry_condition()
                
                # When using a maximum Q value, iterates with fixed orders
                # and verifies if matches...
                begin_order = 1 if self.q > 0 else self.ord
                end_order = MAXIMUM_ORDER if self.q > 0 else self.ord
                for order in range(end_order, begin_order - 1, -1):
                    self.ord = order

                    # Normalising the filter template, choosing design mode between fixed order or
                    # a template based design, trying to match the given parameters
                    wan, aa, wpn, ap = self.get_norm_template()
                    if self.ord > 0:
                        try:
                            error_code = self.compute_normalised_by_order(ap, self.ord, aa)
                        except NotImplementedError:
                            error_code = ApproximationErrorCode.UNDEFINED_APPROXIMATION
                    else:
                        error_code = self.compute_normalised_by_template(ap, aa, wpn, wan)

                    # If maxima
                    
                    # Denormalisation process, first we need to pass every transfer function
                    # to a TrasnferFunction object, using that apply the denormalisation
                    # algorithm of scipy.signal... finally translating ir to a ZeroPolesGain object!
                    if error_code is ApproximationErrorCode.OK:
                        error_code = self._denormalised_transfer_function()

                        # If using the Q maximum value mode of design, check if valid h_denorm
                        if error_code is ApproximationErrorCode.OK:
                            if self.q > 0:
                                if self.matches_selectivity(self.q, self.h_denorm):
                                    break
                        else:
                            break
                else:
                    if self.q > 0:
                        error_code = ApproximationErrorCode.MAXIMUM_ORDER_REACHED

        # Returning the error code and storing it in the class
        self.error_code = error_code
        return error_code
    
    # ------------------------- #
    # Internal Public Methods   #
    # ------------------------- #
    def adjust_symmetry_condition(self):
        """ Adjusts the template of the bandpass or bandstop filter """
        if self.type == FilterType.BAND_PASS.value:
            if self.fpl * self.fpr <= self.fal * self.far:
                self.far = (self.fpl * self.fpr) / self.fal
            else:
                self.fal = (self.fpl * self.fpr) / self.far
        elif self.type == FilterType.BAND_REJECT.value:
            if self.fal * self.far <= self.fpl * self.fpr:
                self.fpr = (self.fal * self.far) / self.fpl
            else:
                self.fpl = (self.fal * self.far) / self.fpr

    def adjust_function_gain(self, gain, target=None):
        """ Adjusts the normalised transfer function to have a given gain """
        transfer = self.h_aux if target is None else target

        if transfer is not None:
            current_gain = self.h_aux.gain
            for zero in transfer.zeros:
                current_gain *= abs(zero)
            for pole in transfer.poles:
                current_gain /= abs(pole)

            transfer.gain = (transfer.gain / current_gain) * gain

    def compute_normalised_by_template(self, ap, aa, wpn, wan) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the normalised template """
        return self._compute_normalised_by_match(ap, aa, partial(self.matches_normalised_template, ap, aa, wan))

    def compute_normalised_by_order(self, ap, n, aa) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the fixed order """
        raise NotImplementedError

    def validate_low_pass(self) -> ApproximationErrorCode:
        """ Returns whether the parameters of the approximation are valid or not using a low-pass. """
        if self.ord == 0 and self.q == 0:
            return self._validate_low_pass_by_template()
        else:
            return self._validate_low_pass_by_fixed()

    def validate_high_pass(self) -> ApproximationErrorCode:
        """ Returns whether the parameters of the approximation are valid or not using a high pass. """
        if self.ord == 0 and self.q == 0:
            return self._validate_high_pass_by_template()
        else:
            return self._validate_high_pass_by_fixed()

    def validate_band_pass(self) -> ApproximationErrorCode:
        """ Returns whether the parameters of the approximation are valid or not using a band pass. """
        if self.ord == 0 and self.q == 0:
            return self._validate_band_pass_by_template()
        else:
            return self._validate_band_pass_by_fixed()

    def validate_band_stop(self) -> ApproximationErrorCode:
        """ Returns whether the parameters of the approximation are valid or not using a band stop. """
        if self.ord == 0 and self.q == 0:
            return self._validate_band_stop_by_template()
        else:
            return self._validate_band_stop_by_fixed()

    def denormalisation_factor(self, wa, aa, wp, ap):
        """ Returns the denormalisation factor to be used when
        adjusting the zeros and poles of the transfer function between the transition
        band. """
        if self.q == 0 and self.ord == 0:
            w_values, mag_values, _ = ss.bode(self.h_aux, w=np.linspace(wp / 10, wa * 5, num=100000))
            stop_band = [w for w, mag in zip(w_values, mag_values) if mag <= (-aa)]
            relative_adjust = ((wa - stop_band[0]) / stop_band[0]) * (self.denorm / 100) + 1
        else:
            relative_adjust = 1

        return relative_adjust

    def denormalise_to_low_pass(self) -> tuple:
        """ Denormalises the filter to low pass and returns the denormalised (zeros, poles, gain) """
        return ss.lp2lp_zpk(self.h_aux.zeros, self.h_aux.poles, self.h_aux.gain, 2 * np.pi * self.fpl)

    def denormalise_to_high_pass(self) -> tuple:
        """ Denormalises the filter to high pass and returns the denormalised (zeros, poles, gain) """
        return ss.lp2hp_zpk(self.h_aux.zeros, self.h_aux.poles, self.h_aux.gain, 2 * np.pi * self.fpl)

    def denormalise_to_band_pass(self) -> tuple:
        """ Denormalises the filter to high pass and returns the denormalised (zeros, poles, gain) """
        return ss.lp2bp_zpk(self.h_aux.zeros, self.h_aux.poles, self.h_aux.gain, 2 * np.pi * np.sqrt(self.fpl * self.fpr), 2 * np.pi * (self.fpr - self.fpl))

    def denormalise_to_band_stop(self) -> tuple:
        """ Denormalises the filter to high pass and returns the denormalised (zeros, poles, gain) """
        return ss.lp2bs_zpk(self.h_aux.zeros, self.h_aux.poles, self.h_aux.gain, 2 * np.pi * np.sqrt(self.fal * self.far), 2 * np.pi * (self.fpr - self.fpl))

    # ----------------- #
    # Private Methods   #
    # ----------------- #
    def _denormalised_transfer_function(self) -> ApproximationErrorCode:
        """ Denormalises the transfer function returned by the approximation used. """

        # Unity gain of the normalised transfer function, factor of denormalisation...
        # moving it between the transition band
        self.adjust_function_gain(1)
        wa, aa, wp, ap = self.get_norm_template()
        relative_adjust = self.denormalisation_factor(wa, aa, wp, ap)

        new_zeros = self.h_aux.zeros * relative_adjust
        new_poles = self.h_aux.poles * relative_adjust
        new_gain = self.h_aux.gain * relative_adjust

        self.h_aux = ss.ZerosPolesGain(new_zeros, new_poles, new_gain)
        self.adjust_function_gain(1)

        # Final normalised transfer function being stored, keep working on auxiliar transfer function
        self.h_norm = ss.ZerosPolesGain(self.h_aux.zeros, self.h_aux.poles, self.h_aux.gain)
        self.adjust_function_gain(10 ** (self.gain / 20))

        # Frequency transformation to get the desired filter
        if self.type == FilterType.LOW_PASS.value:
            z, p, k = self.denormalise_to_low_pass()
        elif self.type == FilterType.HIGH_PASS.value:
            z, p, k = self.denormalise_to_high_pass()
        elif self.type == FilterType.BAND_PASS.value:
            z, p, k = self.denormalise_to_band_pass()
        elif self.type == FilterType.BAND_REJECT.value:
            z, p, k = self.denormalise_to_band_stop()
        self.h_denorm = ss.ZerosPolesGain(z, p, k)

        return ApproximationErrorCode.OK

    def _compute_normalised_by_match(self, ap, aa, callback) -> ApproximationErrorCode:
        """ Generates normalised transfer function for each order until the callbacks
        verifies it matches the requierements. 
        The callback should expect a ZerosPoleGain object from Scipy.Signal,
        returning whether it verifies or not the requirements. """
        for order in range(1, MAXIMUM_ORDER + 1):
            try:
                error_code = self.compute_normalised_by_order(ap, order, aa)
            except NotImplementedError:
                error_code = ApproximationErrorCode.UNDEFINED_APPROXIMATION

            if error_code is ApproximationErrorCode.OK:
                if callback(self.h_aux):
                    return ApproximationErrorCode.OK
                else:
                    self.h_aux = None
            else:
                return error_code
        else:
            return ApproximationErrorCode.MAXIMUM_ORDER_REACHED

    def _normalised_template(self) -> tuple:
        """ Given the filter type and its parameters, it returns
        a tuple containing the normalised parameters of the template.
        Returns -> (wa, aa, wp, ap)
        """
        # Choosing the maximum attenuation of the pass band
        # and adapting it to use a Gain
        if self.Apl > 0 and self.Apr > 0:
            ap = min(self.Apl, self.Apr)
        elif self.Apl > 0:
            ap = self.Apl
        elif self.Apr > 0:
            ap = self.Apr
        else:
            ap = None

        # Choosing the minimum attenuation of the stop band
        # and adapting it to use a Gain
        if self.Aal > 0 and self.Aar > 0:
            aa = max(self.Aal, self.Aar)
        elif self.Aal > 0:
            aa = self.Aal
        elif self.Aar > 0:
            aa = self.Aar
        else:
            aa = None
        if aa is not None:
            aa = aa + self.gain

        if self.type == FilterType.LOW_PASS.value:
            return None if self.fpl == 0 else self.fal / self.fpl, aa, 1, ap
        elif self.type == FilterType.HIGH_PASS.value:
            return None if self.fal == 0 else self.fpl / self.fal, aa, 1, ap
        elif self.type == FilterType.BAND_PASS.value:
            return None if self.fpr == self.fpl else (self.far - self.fal) / (self.fpr - self.fpl), aa, 1, ap
        elif self.type == FilterType.BAND_REJECT.value:
            return None if self.far == self.fal else (self.fpr - self.fpl) / (self.far - self.fal), aa, 1, ap

    def _validate_general(self) -> ApproximationErrorCode:
        """ Returns if general parameters are valid """
        if self.gain is None or type(self.gain) is str or self.gain < 0:
            return ApproximationErrorCode.INVALID_GAIN
        elif self.ord is None or type(self.ord) is str or self.ord < 0 or self.ord > MAXIMUM_ORDER:
            return ApproximationErrorCode.INVALID_ORDER
        elif self.q is None or type(self.q) is str or self.q < 0:
            return ApproximationErrorCode.INVALID_Q
        elif self.denorm is None or type(self.denorm) is str or self.denorm < 0 or self.denorm > 100:
            return ApproximationErrorCode.INVALID_DENORM

        return ApproximationErrorCode.OK

    def _validate_low_pass_by_template(self) -> ApproximationErrorCode:
        """ Specializes the validation by template of a low pass design """
        if self.fpl >= self.fal or self.fpl <= 0 or self.fal <= 0:
            return ApproximationErrorCode.INVALID_FREQ
        elif self.Apl <= 0 or self.Aal <= 0:
            return ApproximationErrorCode.INVALID_ATTE
        elif self.Apl >= self.Aal:
            return ApproximationErrorCode.INVALID_ATTE
        else:
            return ApproximationErrorCode.OK

    def _validate_low_pass_by_fixed(self) -> ApproximationErrorCode:
        """ Specializes the validation by fixed values of a low pass design """
        if self.Apl <= 0:
            return ApproximationErrorCode.INVALID_ATTE
        elif self.fpl <= 0:
            return ApproximationErrorCode.INVALID_FREQ
        else:
            return ApproximationErrorCode.OK

    def _validate_high_pass_by_template(self) -> ApproximationErrorCode:
        """ Specializes the validation by template of a high pass design """
        if self.fpl <= self.fal or self.fpl <= 0 or self.fal <= 0:
            return ApproximationErrorCode.INVALID_FREQ
        elif self.Apl <= 0 or self.Aal <= 0:
            return ApproximationErrorCode.INVALID_ATTE
        elif self.Apl >= self.Aal:
            return ApproximationErrorCode.INVALID_ATTE
        else:
            return ApproximationErrorCode.OK

    def _validate_high_pass_by_fixed(self) -> ApproximationErrorCode:
        """Specializes the validation by fixed values of a high pass design """
        if self.Apl <= 0:
            return ApproximationErrorCode.INVALID_ATTE
        elif self.fpl <= 0:
            return ApproximationErrorCode.INVALID_FREQ
        else:
            return ApproximationErrorCode.OK

    def _validate_band_pass_by_template(self) -> ApproximationErrorCode:
        """ Specializes the validation by template of a band pass design """
        if self.fpl <= 0 or self.fpr <= 0 or self.fal <= 0 or self.far <= 0:
            return ApproximationErrorCode.INVALID_FREQ
        elif self.fpl >= self.fpr or self.fal >= self.far:
            return ApproximationErrorCode.INVALID_FREQ
        elif self.fpl <= self.fal or self.fpr >= self.far:
            return ApproximationErrorCode.INVALID_FREQ
        elif self.Apl <= 0 or self.Aal <= 0 or self.Aar < 0:
            return ApproximationErrorCode.INVALID_ATTE
        elif self.Apl >= self.Aal or self.Apl >= self.Aar:
            return ApproximationErrorCode.INVALID_ATTE
        else:
            return ApproximationErrorCode.OK

    def _validate_band_pass_by_fixed(self) -> ApproximationErrorCode:
        """ Specializes the validation by fixed values of a band pass design """
        if self.fpl <= 0 or self.fpr <= 0:
            return ApproximationErrorCode.INVALID_FREQ
        elif self.fpl >= self.fpr:
            return ApproximationErrorCode.INVALID_FREQ
        elif self.Apl <= 0:
            return ApproximationErrorCode.INVALID_ATTE
        else:
            return ApproximationErrorCode.OK

    def _validate_band_stop_by_template(self) -> ApproximationErrorCode:
        """ Specializes the validation by template of a band stop design """
        if self.fpl <= 0 or self.fpr <= 0 or self.fal <= 0 or self.far <= 0:
            return ApproximationErrorCode.INVALID_FREQ
        elif self.fpl >= self.fpr or self.fal >= self.far:
            return ApproximationErrorCode.INVALID_FREQ
        elif self.fpl >= self.fal or self.fpr <= self.far:
            return ApproximationErrorCode.INVALID_FREQ
        elif self.Apl <= 0 or self.Aal <= 0 or self.Apr < 0:
            return ApproximationErrorCode.INVALID_ATTE
        elif self.Apl >= self.Aal or self.Apr >= self.Aal:
            return ApproximationErrorCode.INVALID_ATTE
        else:
            return ApproximationErrorCode.OK

    def _validate_band_stop_by_fixed(self) -> ApproximationErrorCode:
        """ Specializes the validation by fixed values of a band stop design """
        if self.fpl <= 0 or self.fpr <= 0:
            return ApproximationErrorCode.INVALID_FREQ
        elif self.fpl >= self.fpr:
            return ApproximationErrorCode.INVALID_FREQ
        elif self.Apl <= 0:
            return ApproximationErrorCode.INVALID_ATTE
        else:
            return ApproximationErrorCode.OK
    
    # ---------------- #
    #  Static Methods  #
    # ---------------- #
    @staticmethod
    def calculate_xi(root):
        k = (root.imag / root.real) ** 2
        return np.sqrt(1 / (1 + k))

    @staticmethod
    def calculate_frequency(root):
        xi = AttFilterApproximator.calculate_xi(root)
        return abs(root.real) / (xi * 2 * np.pi)

    @staticmethod
    def calculate_selectivity(root):
        xi = AttFilterApproximator.calculate_xi(root)
        return 1 / (2 * xi)

    @staticmethod
    def matches_normalised_template(ap, aa, wa, zpk) -> bool:
        """ Returns whether the ZeroPolesGain object verifies the normalised
        template given by the aa, ap, wa values. """
        if zpk is None:
            return False

        _, mag, _ = ss.bode(zpk, w=[1, wa])
        return mag[0] >= -ap and mag[1] <= -aa

    @staticmethod
    def matches_selectivity(max_q, zpk) -> bool:
        """ Returns whether the ZeroPolesGain object does not exceed the maximum
        selectivity value given by the user. """
        if zpk is None:
            return False

        for pole in zpk.poles:
            if pole.imag:
                q = AttFilterApproximator.calculate_selectivity(pole)
                if q > max_q:
                    return False
        return True


class GroupDelayFilterApproximator():
    def __init__(self):
        # Data to perform approximation
        self.reset_parameters()

    # ----------------#
    # Public Methods #
    # ----------------#

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

        self.h_norm = None
        self.h_denorm = None
        self.error_code = None
        self.denorm_order = 0

    def compute(self):
        """ Computes the transfer function with the filled parameters
        of the approximation. Any error will be returned as an error code.
        """
        error_code = self._validate()
        if(error_code == ApproximationErrorCode.OK):
            # if data isa valid, calculate approximation
            # When using a maximum Q value, iterates with fixed orders
            # and verifies if matches...
            begin_order = 1 if self.q > 0 else self.ord
            end_order = MAXIMUM_ORDER if self.q > 0 else self.ord
            for order in range(end_order, begin_order - 1, -1):
                self.ord = order

                # Normalising the filter template, choosing design mode between fixed order or
                # a template based design, trying to match the given parameters
                wan, aa, wfn, gdn, tolerance = self._normalised_template()
                if self.ord > 0:
                    try:
                        error_code = self.compute_normalised_by_order(gdn, wfn, self.ord)
                        self.denorm_order = self.ord
                    except NotImplementedError:
                        error_code = ApproximationErrorCode.UNDEFINED_APPROXIMATION
                else:
                    error_code = self.compute_normalised_by_template(gdn, wfn, aa, wan, tolerance)

                # If maxima

                # Denormalisation process, first we need to pass every transfer function
                # to a TrasnferFunction object, using that apply the denormalisation
                # algorithm of scipy.signal... finally translating ir to a ZeroPolesGain object!
                if error_code is ApproximationErrorCode.OK:
                    error_code = self._denormalised_transfer_function()

                    # If using the Q maximum value mode of design, check if valid h_denorm
                    if error_code is ApproximationErrorCode.OK:
                        if self.q > 0:
                            if self.matches_selectivity(self.q, self.h_denorm):
                                break
                    else:
                        break

        # if data is not valid, return error code
        else:
            self.error_code = error_code
            return error_code
        self.error_code = error_code
        return error_code

    def get_norm_template(self) -> tuple:
        """ Returns a 4-element tuple containing the normalised
        parameters of the template.
        Returns -> (wan, aa, wfn, gdn, tolerance)
        """
        wan, aa, wfn, gdn, tolerance = self._normalised_template()
        return wan, aa, 0, 0

    def get_normalised_zpk(self):
        """ Returns a tuple of three elements containing Zeros, Poles and Gain,
        of the normalised transfer function.
        Return -> (zeros, poles, gain) or None if not computed!
        """
        if self.h_norm is None:
            return None
        else:
            return self.h_norm

    def get_zpk(self):
        """ Returns a tuple of three elements containing Zeros, Poles and Gain,
        of the denormalised transfer function.
        Return -> (zeros, poles, gain) or None if not computed!
        """
        if self.h_denorm is None:
            return None
        else:
            return self.h_denorm

    # -------------------------#
    # Internal Public Methods #
    # -------------------------#

    def compute_normalised_by_template(self, gdn, wfn, aa, wan, tolerance) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the normalised template and group delay """
        return self._compute_normalised_by_match(gdn, wfn, tolerance, partial(self.matches_normalised_gd_temp, aa, wan, wfn, tolerance))

    def compute_normalised_by_order(self, gdn, wfn, order) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the fixed order """
        raise NotImplementedError

    # -----------------#
    # Private Methods #
    # -----------------#

    def _validate(self) -> ApproximationErrorCode:
        """ Returns if general parameters are valid """
        if self.gain < 0:
            return ApproximationErrorCode.INVALID_GAIN
        elif self.group_delay < 0:
            return ApproximationErrorCode.INVALID_GROUP_DELAY
        elif self.ord < 0:
            return ApproximationErrorCode.INVALID_ORDER
        elif self.q < 0:
            return ApproximationErrorCode.INVALID_Q
        elif self.tol < 0 or self.tol > 100:
            return ApproximationErrorCode.INVALID_TOLERANCE
        elif self.ft <= 0:
            return ApproximationErrorCode.INVALID_FREQ
        elif self.ord == 0 and self.q == 0:
            if self.fa <= 0:
                return ApproximationErrorCode.INVALID_FREQ
            elif self.Aa <= 0:
                return ApproximationErrorCode.INVALID_ATTE
            else:
                return ApproximationErrorCode.OK
        else:
            return ApproximationErrorCode.OK

    def _compute_normalised_by_match(self, gdn, wfn, tolerance, callback) -> ApproximationErrorCode:
        """ Generates normalised transfer function for each order until the callbacks
        verifies it matches the requierements.
        The callback should expect a ZerosPoleGain object from Scipy.Signal,
        returning whether it verifies or not the requirements. """
        for order in range(1, MAXIMUM_ORDER + 1):
            try:
                error_code = self.compute_normalised_by_order(gdn, wfn, order)
            except NotImplementedError:
                error_code = ApproximationErrorCode.UNDEFINED_APPROXIMATION

            if error_code is ApproximationErrorCode.OK:
                if callback(self.h_norm):
                    self.denorm_order = order
                    return ApproximationErrorCode.OK
                else:
                    self.h_norm = None
            else:
                return error_code
        else:
            return ApproximationErrorCode.MAXIMUM_ORDER_REACHED

    def _denormalised_transfer_function(self):
        raise NotImplementedError

    # ----------------#
    # Static Methods #
    # ----------------#

    @staticmethod
    def calculate_xi(root):
        k = (root.imag / root.real) ** 2
        return np.sqrt(1 / (1 + k))

    @staticmethod
    def calculate_frequency(root):
        xi = GroupDelayFilterApproximator.calculate_xi(root)
        return root.real / (xi * 2 * np.pi)

    @staticmethod
    def calculate_selectivity(root):
        xi = GroupDelayFilterApproximator.calculate_xi(root)
        return 1 / (2 * xi)

    @staticmethod
    def adjust_function_gain(transfer_function, gain):
        if transfer_function is not None:
            current_gain = transfer_function.gain
            for zero in transfer_function.zeros:
                current_gain *= abs(zero)
            for pole in transfer_function.poles:
                current_gain /= abs(pole)

            transfer_function.gain = (transfer_function.gain / current_gain) * gain

    @staticmethod
    def matches_normalised_gd_temp(aa,wa,wf,tolerance, zpk) -> bool:
        """ Returns whether the ZeroPolesGain object verifies the normalised
        template given by the aa, wa values. Also checks if  """
        if zpk is None:
            return False

        w, mag, phase = ss.bode(zpk, w=[wa])
        template_cond = mag[0] <= -aa
        aux = zpk.to_tf()
        w, h = ss.freqs(aux.num, aux.den)
        gd = -np.diff(np.unwrap(np.angle(h))) / np.diff(w)
        gd = np.divide(gd, gd[0])
        index = 0
        for i in gd:
            if i < tolerance:
                index = np.where(gd == i)
                break
        gd_cond = w[index] >= wf
        return template_cond and gd_cond



    @staticmethod
    def matches_selectivity(max_q, zpk) -> bool:
        """ Returns whether the ZeroPolesGain object does not exceed the maximum
        selectivity value given by the user. """
        if zpk is None:
            return False

        for pole in zpk.poles:
            if pole.imag:
                q = GroupDelayFilterApproximator.calculate_selectivity(pole)
                if q > max_q:
                    return False
        return True

    def _normalised_template(self) -> tuple:
        """ Given the filter type and its parameters, it returns
        a tuple containing the normalised parameters of the template.
        Returns -> (wan, aa, wfn, gdn, tolerance)
        """

        return self.fa * 2 * np.pi * self.group_delay * 1e-3, self.Aa, self.ft * 2 * np.pi * self.group_delay * 1e-3, 1, 1 - self.tol/100