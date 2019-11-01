# Third-party modules

# Python native modules

# Project modules
from app.cells.electronics import compute_commercial_by_iteration
from app.cells.electronics import build_expression_callback
from app.cells.electronics import nexpand_component_list
from app.cells.electronics import ComponentType

from app.cells.cell import CellErrorCodes
from app.cells.cell import CellGroup
from app.cells.cell import CellError
from app.cells.cell import CellType
from app.cells.cell import Cell


# --------------------- #
# Cell Group Definition #
# --------------------- #
class ActiveFirstOrder(CellGroup):

    def __init__(self):
        super(ActiveFirstOrder, self).__init__(
            "Active First Order",
            {
                CellType.LOW_PASS.value: CompensatedIntegrator(),
                CellType.HIGH_PASS.value: CompensatedDerivator()
            }
        )


# ---------------- #
# Cell Definitions #
# ---------------- #
class CompensatedDerivator(Cell):

    def __init__(self):
        super(CompensatedDerivator, self).__init__(
            "Compensated Derivator",
            CellType.HIGH_PASS.value,
            "app/images/compensated_derivator.png"
        )

        self.options = {
            "inverter": True,
            "canGain": True,
            "canUnityGain": True,
            "canAttenuate": True
        }

        self.components = {
            "R1": None,
            "R2": None,
            "C1": None
        }

    # -------------- #
    # Public Methods #
    # -------------- #
    def design_components(self, zeros: dict, poles: dict, gain: float, stop_at_first=False) -> dict:
        if "wp" not in poles.keys() or "wz" not in zeros.keys() or gain >= 0 or poles["wp"] <= 0 or zeros["wz"] != 0:
            raise CellError(CellErrorCodes.INVALID_PARAMETERS)
        else:
            # Declaring and cleaning
            self.results = []

            # First, compute possible R2 values based on C1 targetting the Wp value
            r1_c1_options = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Capacitor,
                lambda c1: 1 / (poles["wp"] * c1),
                self.error
            )

            # With the given values of R2, targetting K gain, calculates R1
            r2_r1_options = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Resistor,
                lambda r1: -gain * r1,
                self.error,
                fixed_two_values=[r2_option for r2_option, _ in r1_c1_options]
            )

            # Collecting results!
            self.results = nexpand_component_list(self.results, r2_r1_options, "R2", "R1")
            self.results = nexpand_component_list(self.results, r1_c1_options, "R1", "C1")
            self.flush_results()
            self.choose_random_result()

    def get_parameters(self) -> tuple:
        zeros = {"wz": 0, "nz": 1}
        poles = {"wp": self.wp()}
        gain = self.k()
        return zeros, poles, gain

    def get_sensitivities(self) -> dict:
        return {
            "k": {
                "R1": -1,
                "R2": 1,
                "C1": 0
            },
            "wp": {
                "R1": -1,
                "R2": 0,
                "C1": -1
            }
        }

    # -------------- #
    # Static Methods #
    # -------------- #
    def load_variables(self):
        return (
            self.components["R1"],
            self.components["R2"],
            self.components["C1"]
        )

    def wp(self):
        R1, R2, C1 = self.load_variables()
        return 1 / (R1 * C1)

    def k(self):
        R1, R2, C1 = self.load_variables()
        return - R2 / R1


# noinspection PyPep8Naming,PyShadowingNames
class CompensatedIntegrator(Cell):

    def __init__(self):
        super(CompensatedIntegrator, self).__init__(
            "Compensated Integrator",   # Name
            CellType.LOW_PASS.value,    # Type
            "app/images/compensated_integrator.png"     # Circuit path
        )

        self.options = {
            "inverter": True,
            "canGain": True,
            "canUnityGain": True,
            "canAttenuate": True
        }

        self.components = {
            "R1": None,
            "R2": None,
            "C1": None
        }

    # -------------- #
    # Public Methods #
    # -------------- #
    def design_components(self, zeros: dict, poles: dict, gain: float, stop_at_first=False) -> dict:
        if "wp" not in poles.keys() or gain >= 0 or poles["wp"] <= 0:
            raise CellError(CellErrorCodes.INVALID_PARAMETERS)
        else:
            # Declaring and cleaning
            self.results = []

            # First, compute possible R2 values based on C1 targetting the Wp value
            r2_c1_options = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Capacitor,
                lambda c1: 1 / (c1 * poles["wp"]),
                self.error
            )

            # With the given values of R2, targetting K gain, calculates R1
            r1_r2_options = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Resistor,
                lambda r2: - r2 / gain,
                self.error,
                fixed_two_values=[r2_option for r2_option, _ in r2_c1_options]
            )

            # Cross selection of possible values of components [ (R1, R2), (R1, R2) ] [(R2, C1), (R2, C1)]
            self.results = nexpand_component_list(self.results, r1_r2_options, "R1", "R2")
            self.results = nexpand_component_list(self.results, r2_c1_options, "R2", "C1")
            self.flush_results()
            self.choose_random_result()

    def get_parameters(self) -> tuple:
        poles = {"wp": self.wp()}
        gain = self.k()
        return {}, poles, gain

    def get_sensitivities(self) -> dict:
        return {
            "k": {
                "R1": -1,
                "R2": 1,
                "C1": 0
            },
            "wp": {
                "R1": 0,
                "R2": -1,
                "C1": -1
            }
        }

    # -------------- #
    # Static Methods #
    # -------------- #
    def load_variables(self):
        return (
            self.components["R1"],
            self.components["R2"],
            self.components["C1"]
        )

    def wp(self):
        R1, R2, C1 = self.load_variables()
        return 1 / (R2 * C1)

    def k(self):
        R1, R2, C1 = self.load_variables()
        return - R2 / R1
