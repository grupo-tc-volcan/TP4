# Third-party modules
from sympy import *

# Python native modules

# Project modules
from app.cells.cell import CellType
from app.cells.cell import Cell


# --------------------- #
# Cell Group Definition #
# --------------------- #


# ---------------- #
# Cell Definitions #
# ---------------- #
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
    def design_components(self, zeros: dict, poles: dict, gain: float) -> dict:
        pass

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
    def wp():
        R2, C1 = symbols("R2 C1")
        return 1 / (R2 * C1)

    @staticmethod
    def k():
        R1, R2 = symbols("R1 R2")
        return - R2 / R1
