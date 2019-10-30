# Third-party modules

# Python native modules
from enum import Enum


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
    def __init__(self,
                 name: str,
                 cell_type: str):

        # Internal storage of the cell component values, as dictionary,
        # the names are formatted as "R1", "C1", etc... and should be matched
        # with the names used in the circuit being drawn.
        # Components dictionary is of public access to allow live design of the cell.
        self.components = {}

        # Description of the cell, its name and the available type of transfer function
        # that can be implemented, should be always filled by the children class.
        # Example, type="low-pass", name = "Sallen Key"
        self.name = name
        self.type = cell_type

    # -------------- #
    # Public Methods #
    # -------------- #
    def get_name(self) -> str:
        """ Returns the name of the cell. """
        return self.name

    def get_type(self) -> str:
        """ Returns the type of transfer function that can be implemented with this cell. """
        return self.type

    def get_circuit(self) -> str:
        """ Returns the file path of the circuit's image for the given cell type. """
        raise NotImplementedError

    def get_components(self, zeros: dict, poles: dict, gain: float) -> dict:
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

    def get_parameters(self) -> tuple:
        """ Returns (zeros, poles, gain) in the same format as described in get_components(...),
            and it uses the internal values of components to calculate them.
        """
        raise NotImplementedError

    def get_sensitivities(self) -> dict:
        """ Returns a dictionary with the sensitivities of the circuit, using the internal values
            of components to calculate them. """
        raise NotImplementedError
