# Third-party modules
from sympy import *

# Python native modules

# Project modules
from app.cells.electronics import compute_commercial_by_iteration
from app.cells.electronics import matches_commercial_values
from app.cells.electronics import build_expression_callback
from app.cells.electronics import nexpand_component_list
from app.cells.electronics import ComponentType

from app.cells.cell import CellErrorCodes
from app.cells.cell import CellError
from app.cells.cell import CellType
from app.cells.cell import CellMode
from app.cells.cell import Cell


# --------------------- #
# Cell Group Definition #
# --------------------- #


# ---------------- #
# Cell Definitions #
# ---------------- #
class SallenKeyLowPassGain(Cell):

    def __init__(self):
        super(SallenKeyLowPassGain, self).__init__(
            "Sallen Key Low Pass",
            CellType.LOW_PASS.value
        )

        self.options = {
            "canGain": True,
            "canUnityGain": True,
            "canAttenuate": True
        }

        # Default declaring object status by designing mode!
        self._declare_by_mode(CellMode.GAIN)

    # -------------- #
    # Public Methods #
    # -------------- #
    def get_parameters(self) -> tuple:
        zeros = {}
        gain = self.k().evalf(subs=self.components)
        poles = {"wp": self.wp().evalf(subs=self.components), "qp": self.qp().evalf(subs={**self.components, "k": gain})}
        return zeros, poles, gain

    def get_sensitivities(self) -> dict:
        k = self.k().evalf(subs=self.components)
        qp = self.qp().evalf(subs={**self.components, "k": k})
        parameters = {**self.components, "k": k, "qp": qp}
        return {
            "k": {
                "R1": 0,
                "R2": 0,
                "C1": 0,
                "C2": 0,
                "Ra": self.sens_k_ra().evalf(subs=parameters),
                "Rb": self.sens_k_rb().evalf(subs=parameters)
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
                "R1": self.sens_q_r1().evalf(subs=parameters),
                "R2": self.sens_q_r2().evalf(subs=parameters),
                "C1": self.sens_q_c1().evalf(subs=parameters),
                "C2": self.sens_q_c1().evalf(subs=parameters),
                "Ra": self.sens_q_ra().evalf(subs=parameters),
                "Rb": self.sens_q_rb().evalf(subs=parameters)
            }
        }

    def design_components(self, zeros: dict, poles: dict, gain: float, stop_at_first=False) -> dict:
        if "wp" not in poles.keys() or "qp" not in poles.keys() or gain < 1:
            raise CellError(CellErrorCodes.INVALID_PARAMETERS)
        else:
            # Declaring and cleaning
            R1, R2, C1, C2, Ra, Rb = SallenKeyLowPass.declare_symbols()
            wp, qp, k = SallenKeyLowPass.declare_parameters()
            self.results = []

            # First, calculate the easy gain resistors
            ra_rb_options = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Resistor,
                build_expression_callback(self.k(), gain, Ra),
                self.error
            )

            # Secondly, but using the relationship R1=R2, calculates C1, and C2
            expression = solve([Eq(self.qp().subs(k, gain), qp), Eq(R1, R2)], [qp, R2])[0][0]
            expression = expression.subs(R1, 1)
            c1_c2_options = compute_commercial_by_iteration(
                ComponentType.Capacitor, ComponentType.Capacitor,
                build_expression_callback(expression, poles["qp"], C1),
                self.error
            )

            # Finally, calculates with the previous C1, C2 values, options for R = R1 = R2
            r1_r2_c1_c2_options = []
            for c1_option, c2_option in c1_c2_options[:20]:
                expression = solve([Eq(R1, R2), Eq(wp, self.wp())], [R2, R1, wp])[1][0]
                r1_option = expression.evalf(subs={C1: c1_option, C2: c2_option, wp: poles["wp"]})

                matches, commercial = matches_commercial_values(ComponentType.Resistor, r1_option, self.error)
                if matches:
                    r1_r2_c1_c2_options.append((commercial, commercial, c1_option, c2_option))

            # Cross selection of possible values of components
            self.results = nexpand_component_list(self.results, ra_rb_options, "Ra", "Rb")
            self.results = nexpand_component_list(self.results, r1_r2_c1_c2_options, "R1", "R2", "C1", "C2")
            self.flush_results()
            self.choose_random_result()

    # ------------------------ #
    # Private Internal Methods #
    # ------------------------ #
    def _declare_by_mode(self, mode: CellMode):
        self.mode = mode
        if self.mode is CellMode.GAIN:
            self.circuit = "app/images/sallen_key_low_pass.png"
            self.components = {
                "R1": None,
                "R2": None,
                "C1": None,
                "C2": None,
                "Ra": None,
                "Rb": None
            }
        elif self.mode is CellMode.UNITY_GAIN:
            self.circuit = "app/images/sallen_key_low_pass_unity.png"
            self.components = {
                "R1": None,
                "R2": None,
                "C1": None,
                "C2": None
            }
        elif self.mode is CellMode.ATTENUATION:
            self.circuit = "app/images/sallen_key_low_pass_attenuation.png"
            self.components = {
                "R1": None,
                "R2": None,
                "R3": None,
                "C1": None,
                "C2": None
            }

    @staticmethod
    def declare_parameters():
        return symbols("wp qp k")

    @staticmethod
    def declare_symbols():
        return symbols("R1 R2 C1 C2 Ra Rb")

    @staticmethod
    def k():
        R1, R2, C1, C2, Ra, Rb = SallenKeyLowPass.declare_symbols()
        wp, qp, k = SallenKeyLowPass.declare_parameters()
        return 1 + Rb / Ra

    @staticmethod
    def wp():
        R1, R2, C1, C2, Ra, Rb = SallenKeyLowPass.declare_symbols()
        wp, qp, k = SallenKeyLowPass.declare_parameters()
        return 1 / sqrt(R1 * R2 * C1 * C2)

    @staticmethod
    def qp():
        R1, R2, C1, C2, Ra, Rb = SallenKeyLowPass.declare_symbols()
        wp, qp, k = SallenKeyLowPass.declare_parameters()
        return (1 / sqrt(R1 * R2 * C1 * C2)) / (1 / (C1 * R1) + 1 / (C1 * R2) + (1 - k) / (R2 * C2))

    @staticmethod
    def sens_k_rb():
        R1, R2, C1, C2, Ra, Rb = SallenKeyLowPass.declare_symbols()
        wp, qp, k = SallenKeyLowPass.declare_parameters()
        return 1 - (1 / k)

    @staticmethod
    def sens_k_ra():
        R1, R2, C1, C2, Ra, Rb = SallenKeyLowPass.declare_symbols()
        wp, qp, k = SallenKeyLowPass.declare_parameters()
        return (-1) * SallenKeyLowPass.sens_k_rb()

    @staticmethod
    def sens_q_r1():
        R1, R2, C1, C2, Ra, Rb = SallenKeyLowPass.declare_symbols()
        wp, qp, k = SallenKeyLowPass.declare_parameters()
        return (-1 / 2) + qp * sqrt((R2 * C2) / (R1 * C1))

    @staticmethod
    def sens_q_r2():
        R1, R2, C1, C2, Ra, Rb = SallenKeyLowPass.declare_symbols()
        wp, qp, k = SallenKeyLowPass.declare_parameters()
        return (-1 / 2) + qp * (
            sqrt((R1 * C2) / (R2 * C1)) + (1 - k) * sqrt((R1 * C1) / (R2 * C2))
        )

    @staticmethod
    def sens_q_c1():
        R1, R2, C1, C2, Ra, Rb = SallenKeyLowPass.declare_symbols()
        wp, qp, k = SallenKeyLowPass.declare_parameters()
        return (-1 / 2) + qp * (
            sqrt((R1 * C1) / (R2 * C2)) + sqrt((R2 * C1) / (R1 * C2))
        )

    @staticmethod
    def sens_q_c2():
        R1, R2, C1, C2, Ra, Rb = SallenKeyLowPass.declare_symbols()
        wp, qp, k = SallenKeyLowPass.declare_parameters()
        return SallenKeyLowPass.sens_q_c1() * (-1)

    @staticmethod
    def sens_q_rb():
        R1, R2, C1, C2, Ra, Rb = SallenKeyLowPass.declare_symbols()
        wp, qp, k = SallenKeyLowPass.declare_parameters()
        return (-1) * (1 - k) * qp * sqrt((R1 * C1) / (R2 * C2))

    @staticmethod
    def sens_q_ra():
        return (-1) * SallenKeyLowPass.sens_k_rb()


class SallenKeyHighPass(SallenKeyLowPass):

    def __init__(self):
        super(SallenKeyHighPass, self).__init__()

        self.circuit = "app/image/sallen_key_high_pass.png"
        self.name = "Sallen Key High Pass"
        self.type = CellType.HIGH_PASS.value

    # -------------- #
    # Public Methods #
    # -------------- #
    def get_parameters(self) -> tuple:
        _, poles, gain = super(SallenKeyHighPass, self).get_parameters()
        zeros = {"wz": 0, "nz": 2}
        return zeros, poles, gain

    # -------------- #
    # Static Methods #
    # -------------- #
    @staticmethod
    def qp():
        R1, R2, C1, C2, Ra, Rb = SallenKeyHighPass.declare_symbols()
        wp, qp, k = SallenKeyHighPass.declare_parameters()
        return (1 / sqrt(R1 * R2 * C1 * C2)) / (1 / (C2 * R2) + 1 / (C1 * R2) + (1 - k) / (R1 * C1))
