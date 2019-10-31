# Third-party modules

# Python native modules
from enum import Enum
from random import *


class CellErrorCodes(Enum):
    """ Error codes used to classify what went wrong. """
    OK = "Ok"                                   # Everything is ok
    NOT_AVAILABLE_TYPE = "NotAvailableType"     # Using a not available type of cell
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


class CellType(Enum):
    """ Internal mapping of filter types, strings are expected and are matched
    with these enumerated values. """
    LOW_PASS = "low-pass"
    HIGH_PASS = "high-pass"
    BAND_PASS = "band-pass"
    BAND_STOP = "band-stop"


class Cell:
    """ Abstract base class of cells """
    def __init__(self, name: str, cell_type: str, circuit: str):

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
    def can_gain(self) -> bool:
        """ Returns whether the cell can have gain in the band pass """
        return self.options["canGain"]

    def can_unity_gain(self) -> bool:
        """ Returns whether the cell can have unity gain in the band pass """
        return self.options["canUnityGain"]

    def can_attenuate(self) -> bool:
        """ Returns whether the cell can have attenuation in the band pass """
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

    def get_components(self) -> dict:
        """ Returns the dictionary of components of the cell. """
        return self.components

    def get_circuit(self) -> str:
        """ Returns the file path of the circuit's image for the given cell type. """
        raise self.circuit

    # -------------- #
    # Public Methods #
    # -------------- #
    def set_error(self, error: float):
        """ Sets the relative tolerance used to calculate all components """
        self.error = error

    def set_components(self, components: dict):
        """ Sets the current dictionary of components """
        self.components = components

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
    def flush_results(self):
        """ Clean the non-complete results, when not all components are defined in every result """
        targets = [result for result in self.results if len(result.keys()) < len(self.components.keys())]
        for target in targets:
            self.results.remove(target)

    def choose_random_result(self):
        """ Update the current selection of components using any of the possible results randomly. """
        if self.results:
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
        self.name = name

    # -------------------- #
    # Public Query Methods #
    # -------------------- #
    def can_gain(self, cell_type: str) -> bool:
        """ Returns whether the cell can have gain in the band pass """
        return self._switch_cell_method_by_type(cell_type, "can_gain")

    def can_unity_gain(self, cell_type: str) -> bool:
        """ Returns whether the cell can have unity gain in the band pass """
        return self._switch_cell_method_by_type(cell_type, "can_unity_gain")

    def can_attenuate(self, cell_type: str) -> bool:
        """ Returns whether the cell can have attenuation in the band pass """
        return self._switch_cell_method_by_type(cell_type, "can_attenuate")

    def get_name(self) -> str:
        """ Returns the name of the group of cells. """
        return self.name

    def get_available_types(self) -> list:
        """ Returns a list of the available types of cells in this group. """
        return self.mapping_types.keys()

    def get_circuit(self, cell_type: str) -> str:
        """ Given a type of a cell, the filepath of its circuit's image is returned. """
        return self._switch_cell_method_by_type(cell_type, "get_circuit")

    def get_results(self, cell_type: str) -> list:
        """ Returns a list of possible combinations of components to be used. """
        return self._switch_cell_method_by_type(cell_type, "get_results")

    def get_components(self, cell_type: str) -> dict:
        """ Returns a dictionary of components by reference to allow external changes. """
        return self._switch_cell_method_by_type(cell_type, "get_components")

    # -------------- #
    # Public Methods #
    # -------------- #
    def set_error(self, cell_type: str, error: float):
        """ Sets the error or relative tolerance used to calculate components. """
        self._switch_cell_method_by_type(cell_type, "set_error", error)

    def set_components(self, cell_type: str, components: dict):
        """ Sets the current dictionary of components """
        self._switch_cell_method_by_type(cell_type, "set_components", components)

    def get_parameters(self, cell_type: str) -> tuple:
        """ Returns (zeros, poles, gain) in the same format as described in get_components(...),
            and it uses the internal values of components to calculate them.
        """
        self._verify_components(cell_type)
        return self._switch_cell_method_by_type(cell_type, "get_parameters")

    def get_sensitivities(self, cell_type: str) -> dict:
        """ Returns a dictionary with the sensitivities of the circuit, using the internal values
            of components to calculate them. """
        self._verify_components(cell_type)
        return self._switch_cell_method_by_type(cell_type, "get_sensitivities")

    def design_components(self, cell_type: str, zeros: dict, poles: dict, gain: float, stop_at_first=False) -> dict:
        """ Returns the components needed after designing the cell for the given parameters. """
        return self._switch_cell_method_by_type(cell_type, "design_components", zeros, poles, gain, stop_at_first)

    # ------------------------ #
    # Internal Private Methods #
    # ------------------------ #
    def _switch_cell_method_by_type(self, cell_type: str, method_name: str, *args, **kwargs):
        """ Executes a method switching according to the internal mapp of instances. """
        if cell_type in self.mapping_types.keys():
            return getattr(self.mapping_types[cell_type], method_name)(*args, *kwargs)
        else:
            raise CellError(CellErrorCodes.NOT_AVAILABLE_TYPE)

    def _verify_components(self, cell_type: str):
        """ Verifies if component values have been set into the cell, if not
        raises an error. """
        components = self.get_components(cell_type)
        if None in components.values():
            raise CellError(CellErrorCodes.NOT_DEFINED_COMPONENTS)
