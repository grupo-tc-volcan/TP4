# Third-party modules
from sympy import *

# Python native modules

# Project modules
from app.cells.electronics import compute_commercial_by_iteration
from app.cells.electronics import build_expression_callback
from app.cells.electronics import expand_component_list
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
            R1, R2, C1, C2, wp, k = CompensatedDerivator.declare_symbols()
            self.results = []

            # First, compute possible R2 values based on C1 targetting the Wp value
            r1_c1_options = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Capacitor,
                build_expression_callback(self.wp(), poles["wp"], R1),
                self.error
            )

            # With the given values of R2, targetting K gain, calculates R1
            r2_r1_options = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Resistor,
                build_expression_callback(self.k(), gain, R2),
                self.error,
                fixed_two_values=[r2_option for r2_option, _ in r1_c1_options]
            )

            # Collecting results!
            self.results = expand_component_list(self.results, "R2", "R1", r2_r1_options)
            self.results = expand_component_list(self.results, "R1", "C1", r1_c1_options)
            self.flush_results()
            self.choose_random_result()

    def get_parameters(self) -> tuple:
        zeros = {"wz": 0, "nz": 1}
        poles = {"wp": self.wp().evalf(subs=self.components)}
        gain = self.k().evalf(subs=self.components)
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
    @staticmethod
    def declare_symbols():
        return symbols("R1 R2 C1 C2 wp k", positive=True, real=True)

    @staticmethod
    def wp():
        R1, R2, C1, C2, wp, k = CompensatedDerivator.declare_symbols()
        return 1 / (R1 * C1)

    @staticmethod
    def k():
        R1, R2, C1, C2, wp, k = CompensatedDerivator.declare_symbols()
        return - R2 / R1


# noinspection PyPep8Naming,PyShadowingNames
class CompensatedIntegrator(Cell):

    def __init__(self):
        super(CompensatedIntegrator, self).__init__(
            "Compensated Integrator",
            CellType.LOW_PASS.value,
            "app/images/compensated_integrator.png"
        )

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
            R1, R2, C1, C2, wp, k = CompensatedIntegrator.declare_symbols()
            self.results = []

            # First, compute possible R2 values based on C1 targetting the Wp value
            r2_c1_options = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Capacitor,
                build_expression_callback(self.wp(), poles["wp"], R2),
                self.error
            )

            # With the given values of R2, targetting K gain, calculates R1
            r1_r2_options = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Resistor,
                build_expression_callback(self.k(), gain, R1),
                self.error,
                fixed_two_values=[r2_option for r2_option, _ in r2_c1_options]
            )

            # Cross selection of possible values of components
            self.results = expand_component_list(self.results, "R1", "R2", r1_r2_options)
            self.results = expand_component_list(self.results, "R2", "C1", r2_c1_options)
            self.flush_results()
            self.choose_random_result()

    def get_parameters(self) -> tuple:
        poles = {"wp": self.wp().evalf(subs=self.components)}
        gain = self.k().evalf(subs=self.components)
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
    @staticmethod
    def declare_symbols():
        return symbols("R1 R2 C1 C2 wp k")

    @staticmethod
    def wp():
        R1, R2, C1, C2, wp, k = CompensatedIntegrator.declare_symbols()
        return 1 / (R2 * C1)

    @staticmethod
    def k():
        R1, R2, C1, C2, wp, k = CompensatedIntegrator.declare_symbols()
        return - R2 / R1
