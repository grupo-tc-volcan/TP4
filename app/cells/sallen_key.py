# Third-party modules
from sympy import *

# Python native modules

# Project modules
from app.cells.electronics import compute_commercial_by_iteration
from app.cells.electronics import build_expression_callback
from app.cells.electronics import ComponentType

from app.cells.cell import CellErrorCodes
from app.cells.cell import CellError
from app.cells.cell import CellType
from app.cells.cell import Cell


# --------------------- #
# Cell Group Definition #
# --------------------- #


# ---------------- #
# Cell Definitions #
# ---------------- #
class SallenKeyLowPass(Cell):

    def __init__(self):
        super(SallenKeyLowPass, self).__init__(
            "Sallen Key Low Pass",
            CellType.LOW_PASS.value,
            "app/images/sallen_key_low_pass.png"
        )

        self.components = {
            "R1": None,
            "R2": None,
            "C1": None,
            "C2": None,
            "Ra": None,
            "Rb": None
        }

    # -------------- #
    # Public Methods #
    # -------------- #
    def get_parameters(self) -> tuple:
        zeros = {}
        poles = {"wp": self.wp().evalf(subs=self.components), "qp": self.qp().evalf(subs=self.components)}
        gain = self.k().evalf(subs=self.components)
        return zeros, poles, gain

    def get_sensitivities(self) -> dict:
        return {
            "k": {
                "R1": 0,
                "R2": 0,
                "C1": 0,
                "C2": 0,
                "Ra": self.sens_k_ra().evalf(subs=self.components),
                "Rb": self.sens_k_rb().evalf(subs=self.components)
            },
            "wp": {
                "R1": -1/2,
                "R2": -1/2,
                "C1": -1/2,
                "C2": -1/2,
                "Ra": 0,
                "Rb": 0
            },
            "qp": {
                "R1": self.sens_q_r1().evalf(subs=self.components),
                "R2": self.sens_q_r2().evalf(subs=self.components),
                "C1": self.sens_q_c1().evalf(subs=self.components),
                "C2": self.sens_q_c1().evalf(subs=self.components),
                "Ra": self.sens_q_ra().evalf(subs=self.components),
                "Rb": self.sens_q_rb().evalf(subs=self.components)
            }
        }

    def design_components(self, zeros: dict, poles: dict, gain: float) -> dict:
        if "wp" not in poles.keys() or "qp" not in poles.keys() or gain < 1:
            raise CellError(CellErrorCodes.INVALID_PARAMETERS)
        else:
            # Declaring and cleaning
            R1, R2, C1, C2, Ra, Rb, wp, qp, k = SallenKeyLowPass.declare_symbols()
            self.results = []

            # First, calculate the easy gain resistors
            ra_rb_options = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Resistor,
                build_expression_callback(self.k(), gain, Ra),
                self.error
            )

            # Secondly, but using the relationship R1=R2, calculates C1, and C2
            expression = solve([Eq(self.qp().subs(k, gain), q), Eq(R1, R2)], [qp, R2])[0][0]
            c1_c2_options = compute_commercial_by_iteration(
                ComponentType.Capacitor, ComponentType.Capacitor,
                build_expression_callback(expression, poles["qp"], C1),
                self.error
            )

            # Finally, calculates with the previous C1, C2 values, options for R = R1 = R2

    # -------------- #
    # Static Methods #
    # -------------- #
    @staticmethod
    def declare_symbols():
        return symbols("R1 R2 C1 C2 Ra Rb wp qp k", positive=True, real=True)

    @staticmethod
    def k():
        R1, R2, C1, C2, Ra, Rb, wp, qp, k = SallenKeyLowPass.declare_symbols()
        return 1 + Rb / Ra

    @staticmethod
    def wp():
        R1, R2, C1, C2, Ra, Rb, wp, qp, k = SallenKeyLowPass.declare_symbols()
        return 1 / sqrt(R1 * R2 * C1 * C2)

    @staticmethod
    def qp():
        R1, R2, C1, C2, Ra, Rb, wp, qp, k = SallenKeyLowPass.declare_symbols()
        return (1 / sqrt(R1 * R2 * C1 * C2)) / (1 / (C1 * R1) + 1 / (C1 * R2) + (1 - k) / (R2 * C2))

    @staticmethod
    def sens_k_rb():
        return 1 - 1 / SallenKeyLowPass.k()

    @staticmethod
    def sens_k_ra():
        return (-1) * SallenKeyLowPass.sens_k_rb()

    @staticmethod
    def sens_q_r1():
        R1, R2, C1, C2 = symbols("R1 R2 C1 C2")
        return -1 / 2 + SallenKeyLowPass.qp() * sqrt((R2 * C2) / (R1 * C1))

    @staticmethod
    def sens_q_r2():
        R1, R2, C1, C2 = symbols("R1 R2 C1 C2")
        return -1 / 2 + SallenKeyLowPass.qp() * (
            sqrt((R1 * C2) / (R2 * C1)) + (1 - SallenKeyLowPass.k()) * sqrt((R1 * C1) / (R2 * C2))
        )

    @staticmethod
    def sens_q_c1():
        R1, R2, C1, C2 = symbols("R1 R2 C1 C2")
        return -1 / 2 + SallenKeyLowPass.qp() * (
            sqrt((R1 * C2) / (R2 * C1)) + sqrt((R2 * R1 * C1) / C2)
        )

    @staticmethod
    def sens_q_c2():
        R1, R2, C1, C2 = symbols("R1 R2 C1 C2")
        return (-1 / 2) * (1 - SallenKeyLowPass.k()) * SallenKeyLowPass.qp() * sqrt((R1 * C1) / (R2 * C2))

    @staticmethod
    def sens_q_rb():
        return -(1 - SallenKeyLowPass.k()) * SallenKeyLowPass.qp() * sqrt((R1 * C1) / (R2 * C2))

    @staticmethod
    def sens_q_ra():
        return (-1) * SallenKeyLowPass.sens_k_rb()


if __name__ == "__main__":
    sallen_key = SallenKeyLowPass()

    R1, R2, C1, C2, Ra, Rb, wp, qp, k = SallenKeyLowPass.declare_symbols()

    solution = solve([Eq(sallen_key.qp().subs(k, 2), qp), Eq(R1, R2)], [qp, R2])[0][0]
    print(solution)

