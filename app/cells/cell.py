# Third-party modules

# Python native modules
from enum import Enum
from random import *
from time import *


class CellErrorCodes(Enum):
    """ Error codes used to classify what went wrong. """
    OK = "Ok"                                   # Everything is ok
    NOT_AVAILABLE_TYPE = "NotAvailableType"     # Using a not available type of cell
    NOT_DEFINED_CELL = "NotDefinedCell"         # The given parameters do not target any cell
    NOT_SELECTED_CELL = "NotSelectedCell"       # CellGroup has not received yet the set_cell()
    NOT_DEFINED_COMPONENTS = "NotDefinedComp"   # Trying to calculate or compute without setting component values
    INVALID_PARAMETERS = "InvalidParameters"   # Designing with wrong parameters or missing some of them


class CellError(Exception):
    """ Handling errors is solved by raising always only one exception whenever an error
    has occured. Internal error codes and messages will be stored in this class to ease
    the error finding process. """
    def __init__(self, error_code):
        super(CellError, self).__init__("An error occurred when using a Cell. Check the error code {}!".format(error_code))

        # Internal storage of the error code
        self.error_code = error_code


class CellMode(Enum):
    """ If it is needed, a general definition is provided for those cells that may need
    change internally some computing process when is gain or attenuation... """
    GAIN = "gain"
    UNITY_GAIN = "unity-gain"
    ATTENUATION = "attenuation"

    @staticmethod
    def float_to_cell_mode(value: float):
        value = abs(value)
        if value < 1:
            return CellMode.ATTENUATION
        elif value == 1:
            return CellMode.UNITY_GAIN
        else:
            return CellMode.GAIN


class CellType(Enum):
    """ Internal mapping of filter types, strings are expected and are matched
    with these enumerated values. """
    LOW_PASS = "low-pass"
    HIGH_PASS = "high-pass"
    BAND_PASS = "band-pass"
    BAND_STOP = "band-stop"


class Cell:
    """ Abstract base class of cells """
    def __init__(self, name: str, cell_type: str, circuit=None):

        # Internal storage of the cell component values, as dictionary,
        # the names are formatted as "R1", "C1", etc... and should be matched
        # with the names used in the circuit being drawn.
        # Components dictionary is of public access to allow live design of the cell.
        self.components = {}
        self.results = []

        # Description of the cell, its name and the available type of transfer function
        # that can be implemented, should be always filled by the children class.
        # Example, type="low-pass", name = "Sallen Key"
        self.circuit = circuit
        self.type = cell_type
        self.name = name
        self.error = 0.1

        # Additional internal options of any cell
        self.options = {
            "canGain": None,
            "canUnityGain": None,
            "canAttenuate": None
        }

    # -------------------- #
    # Public Query Methods #
    # -------------------- #
    def is_valid_gain_mode(self, gain=None, mode=None):
        """ Returns whether this cell can be used with the given gain """
        if gain is None and mode is None:
            raise CellError(CellErrorCodes.NOT_DEFINED_CELL)
        else:
            target_mode = CellMode.float_to_cell_mode(gain) if gain is not None else mode
            if target_mode is CellMode.GAIN:
                return self.options["canGain"]
            elif target_mode is CellMode.UNITY_GAIN:
                return self.options["canUnityGain"]
            elif target_mode is CellMode.ATTENUATION:
                return self.options["canAttenuate"]

    def get_name(self) -> str:
        """ Returns the name of the cell. """
        return self.name

    def get_type(self) -> str:
        """ Returns the type of transfer function that can be implemented with this cell. """
        return self.type

    def get_results(self) -> list:
        """ Returns the list of possible results of components. """
        return self.results

    def get_circuit(self) -> str:
        """ Returns the file path of the circuit's image for the given cell type. """
        return self.circuit

    # -------------- #
    # Public Methods #
    # -------------- #
    def set_error(self, error: float):
        """ Sets the relative tolerance used to calculate all components """
        self.error = error

    def get_parameters(self) -> tuple:
        """ Returns (zeros, poles, gain) in the same format as described in get_components(...),
            and it uses the internal values of components to calculate them.
        """
        raise NotImplementedError

    def get_sensitivities(self) -> dict:
        """ Returns a dictionary with the sensitivities of the circuit, using the internal values
            of components to calculate them.
            Should expect that sensitivities are returned with the following syntax:
                {
                    "wp": {
                        "R2": 1,
                        "R1": -1
                    }
                }
            """
        raise NotImplementedError

    def design_components(self, zeros: dict, poles: dict, gain: float, stop_at_first=False) -> dict:
        """ Returns the components needed after designing the cell for the given parameters.
            [Expected format of parameters]
                zeros = {
                    "wz": zero's frequency,
                    "nz": zero's order
                }
                poles = {
                    "wp": pole's frequency,
                    "qp": pole's quality factor
                }

            Remember, when returning a Q value of poles equal to cero or not described in the dictionary,
            we are refering to a simple real pole, not a complex pair of them.
         """
        raise NotImplementedError

    # ---------------- #
    # Internal Methods #
    # ---------------- #
    def calculate_with_components(self, expression, **kwargs):
        """ Returns the evaluation of the given expression using components """
        if type(expression) is int or type(expression) is float:
            return expression
        else:
            return expression.evalf(subs={**self.components, **kwargs})

    def flush_results(self):
        """ Clean the non-complete results, when not all components are defined in every result """
        targets = [result for result in self.results if len(result.keys()) < len(self.components.keys())]
        for target in targets:
            self.results.remove(target)

    def choose_random_result(self):
        """ Update the current selection of components using any of the possible results randomly. """
        if self.results:
            seed(time())
            shuffle(self.results)
            self.components = choice(self.results)


class CellGroup:
    """ Grouping cell types class, used to manage the usage of different types of cells of the same
    topology. """
    def __init__(self, name: str, mapping_types: dict):
        # Mapping types is saved as a dictionary, using as keys the strings declared in CellTypes,
        # as a way of mapping which Cell object should handle each case.
        # [Example]
        #   mapping_types = {
        #       "low-pass": SallenKeyLowPass
        #   }
        self.mapping_types = mapping_types
        self.current_cell = None
        self.name = name

    # -------------------- #
    # Public Query Methods #
    # -------------------- #
    def is_valid_gain_mode(self, cell_type: str, gain=None, mode=None) -> bool:
        """ Returns whether the given cell type can implement the gain or not """
        if gain is None and mode is None:
            raise CellError(CellErrorCodes.NOT_DEFINED_CELL)
        else:
            if cell_type not in self.get_available_types():
                raise CellError(CellErrorCodes.NOT_AVAILABLE_TYPE)
            else:
                target_mode = mode if mode is not None else CellMode.float_to_cell_mode(gain)
                if type(self.mapping_types[cell_type]) is list:
                    for option in self.mapping_types[cell_type]:
                        if option.is_valid_gain_mode(mode=target_mode):
                            return True
                    else:
                        return False
                else:
                    return self.mapping_types[cell_type].is_valid_gain_mode(mode=target_mode)

    def get_name(self) -> str:
        """ Returns the name of the group of cells. """
        return self.name

    def get_available_types(self) -> list:
        """ Returns a list of the available types of cells in this group. """
        return self.mapping_types.keys()

    def get_circuit(self) -> str:
        """ Given a type of a cell, the filepath of its circuit's image is returned. """
        self._verify_cell()
        return self.current_cell.get_circuit()

    def get_results(self) -> list:
        """ Returns a list of possible combinations of components to be used. """
        self._verify_cell()
        return self.current_cell.get_results()

    def get_components(self) -> dict:
        """ Returns a dictionary of components by reference to allow external changes. """
        self._verify_cell()
        return self.current_cell.components

    # -------------- #
    # Public Methods #
    # -------------- #
    def set_cell(self, cell_type: str, gain=None, mode=None):
        """ Sets the current working cell that will be used.
            Either gain or mode can be used to define which cell is used, but at least one is needed. """
        target_mode = mode if mode is not None else CellMode.float_to_cell_mode(gain)
        if self.is_valid_gain_mode(cell_type, mode=target_mode):
            target_cells = self.mapping_types[cell_type]
            if type(target_cells) is list:
                for target_cell in target_cells:
                    if target_cell.is_valid_gain_mode(mode=target_mode):
                        self.current_cell = target_cell
                        break
            else:
                self.current_cell = target_cells
        else:
            raise CellError(CellErrorCodes.NOT_DEFINED_CELL)

    def set_error(self, error: float):
        """ Sets the error or relative tolerance used to calculate components. """
        self._verify_cell()
        self.current_cell.set_error(error)

    def set_components(self, components: dict):
        """ Sets the current dictionary of components """
        self._verify_cell()
        self.current_cell.components = components

    def get_parameters(self) -> tuple:
        """ Returns (zeros, poles, gain) in the same format as described in get_components(...),
            and it uses the internal values of components to calculate them.
        """
        self._verify_cell()
        self._verify_components()
        return self.current_cell.get_parameters()

    def get_sensitivities(self, cell_type: str) -> dict:
        """ Returns a dictionary with the sensitivities of the circuit, using the internal values
            of components to calculate them. """
        self._verify_cell()
        self._verify_components()
        return self.current_cell.get_sensitivities()

    def design_components(self, zeros: dict, poles: dict, gain: float, stop_at_first=False) -> dict:
        """ Returns the components needed after designing the cell for the given parameters. """
        self._verify_cell()
        return self.current_cell.design_components(zeros, poles, gain, stop_at_first)

    # ------------------------ #
    # Internal Private Methods #
    # ------------------------ #
    def _verify_cell(self):
        """ Verifies if the current working cell has been defined.
            Raises an exception of NOT_SELECTED_CELL if not.
            """
        if self.current_cell is None:
            raise CellError(CellErrorCodes.NOT_SELECTED_CELL)

    def _verify_components(self):
        """ Verifies if component values have been set into the cell.
            Raises an exception of NOT_DEFINED_COMPONENTS if not.
            """
        components = self.get_components()
        if None in components.values():
            raise CellError(CellErrorCodes.NOT_DEFINED_COMPONENTS)
