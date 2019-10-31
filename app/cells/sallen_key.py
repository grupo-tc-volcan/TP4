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
            CellType.LOW_PASS.value,
            "app/images/sallen_key_low_pass.png"
        )

        self.options = {
            "canGain": True,
            "canUnityGain": False,
            "canAttenuate": False
        }

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
        gain = self.calculate_with_components(self.k())
        poles = {"wp": self.calculate_with_components(self.wp()), "qp": self.calculate_with_components(self.qp(), k=gain)}
        return zeros, poles, gain

    def get_sensitivities(self) -> dict:
        k = self.calculate_with_components(self.k())
        qp = self.calculate_with_components(self.qp(), k=k)
        return {
            "k": {
                "R1": 0,
                "R2": 0,
                "C1": 0,
                "C2": 0,
                "Ra": self.calculate_with_components(self.sens_k_ra(), k=k, qp=qp),
                "Rb": self.calculate_with_components(self.sens_k_rb(), k=k, qp=qp)
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
                "R1": self.calculate_with_components(self.sens_q_r1(), k=k, qp=qp),
                "R2": self.calculate_with_components(self.sens_q_r2(), k=k, qp=qp),
                "C1": self.calculate_with_components(self.sens_q_c1(), k=k, qp=qp),
                "C2": self.calculate_with_components(self.sens_q_c2(), k=k, qp=qp),
                "Ra": self.calculate_with_components(self.sens_k_ra(), k=k, qp=qp),
                "Rb": self.calculate_with_components(self.sens_q_rb(), k=k, qp=qp)
            }
        }

    def design_components(self, zeros: dict, poles: dict, gain: float, stop_at_first=False) -> dict:
        if "wp" not in poles.keys() or "qp" not in poles.keys() or gain <= 1:
            raise CellError(CellErrorCodes.INVALID_PARAMETERS)
        else:
            # Declaring and cleaning
            R1, R2, C1, C2, Ra, Rb = self.declare_symbols()
            wp, qp, k = self.declare_parameters()
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
    @staticmethod
    def declare_parameters():
        return symbols("wp qp k")

    @staticmethod
    def declare_symbols():
        return symbols("R1 R2 C1 C2 Ra Rb")

    def k(self):
        R1, R2, C1, C2, Ra, Rb = self.declare_symbols()
        wp, qp, k = self.declare_parameters()
        return 1 + Rb / Ra

    def wp(self):
        R1, R2, C1, C2, Ra, Rb = self.declare_symbols()
        wp, qp, k = self.declare_parameters()
        return 1 / sqrt(R1 * R2 * C1 * C2)

    def qp(self):
        R1, R2, C1, C2, Ra, Rb = self.declare_symbols()
        wp, qp, k = self.declare_parameters()
        return (1 / sqrt(R1 * R2 * C1 * C2)) / (1 / (C1 * R1) + 1 / (C1 * R2) + (1 - k) / (R2 * C2))

    def sens_k_rb(self):
        R1, R2, C1, C2, Ra, Rb = self.declare_symbols()
        wp, qp, k = self.declare_parameters()
        return 1 - (1 / k)

    def sens_k_ra(self):
        R1, R2, C1, C2, Ra, Rb = self.declare_symbols()
        wp, qp, k = self.declare_parameters()
        return (-1) * self.sens_k_rb()

    def sens_q_r1(self):
        R1, R2, C1, C2, Ra, Rb = self.declare_symbols()
        wp, qp, k = self.declare_parameters()
        return (-1 / 2) + qp * sqrt((R2 * C2) / (R1 * C1))

    def sens_q_r2(self):
        R1, R2, C1, C2, Ra, Rb = self.declare_symbols()
        wp, qp, k = self.declare_parameters()
        return (-1 / 2) + qp * (
            sqrt((R1 * C2) / (R2 * C1)) + (1 - k) * sqrt((R1 * C1) / (R2 * C2))
        )

    def sens_q_c1(self):
        R1, R2, C1, C2, Ra, Rb = self.declare_symbols()
        wp, qp, k = self.declare_parameters()
        return (-1 / 2) + qp * (
            sqrt((R1 * C1) / (R2 * C2)) + sqrt((R2 * C1) / (R1 * C2))
        )

    def sens_q_c2(self):
        R1, R2, C1, C2, Ra, Rb = self.declare_symbols()
        wp, qp, k = self.declare_parameters()
        return self.sens_q_c1() * (-1)

    def sens_q_rb(self):
        R1, R2, C1, C2, Ra, Rb = self.declare_symbols()
        wp, qp, k = self.declare_parameters()
        return (-1) * (1 - k) * qp * sqrt((R1 * C1) / (R2 * C2))

    def sens_q_ra(self):
        return (-1) * self.sens_k_rb()


class SallenKeyLowPassUnityGain(SallenKeyLowPassGain):

    def __init__(self):
        super(SallenKeyLowPassUnityGain, self).__init__()
        self.circuit = "app/image/sallen_key_low_pass_unity.png"

        self.options = {
            "canGain": False,
            "canUnityGain": True,
            "canAttenuate": False
        }

        self.components = {
            "R1": None,
            "R2": None,
            "C1": None,
            "C2": None
        }

    # -------------- #
    # Public Methods #
    # -------------- #
    def get_sensitivities(self) -> dict:
        sensitivities = super(SallenKeyLowPassUnityGain, self).get_sensitivities()
        for value in sensitivities.values():
            del value["Ra"]
            del value["Rb"]
        return sensitivities

    def design_components(self, zeros: dict, poles: dict, gain: float, stop_at_first=False) -> dict:
        if "wp" not in poles.keys() or "qp" not in poles.keys() or gain != 1:
            raise CellError(CellErrorCodes.INVALID_PARAMETERS)
        else:
            # Declaring and cleaning
            R1, R2, C1, C2, _, _ = self.declare_symbols()
            wp, qp, k = self.declare_parameters()
            self.results = []

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
            self.results = nexpand_component_list(self.results, r1_r2_c1_c2_options, "R1", "R2", "C1", "C2")
            self.flush_results()
            self.choose_random_result()

    # ------------------------ #
    # Private Internal Methods #
    # ------------------------ #
    def k(self):
        return 1


class SallenKeyHighPassGain(SallenKeyLowPassGain):

    def __init__(self):
        super(SallenKeyHighPassGain, self).__init__()

        self.circuit = "app/image/sallen_key_high_pass.png"
        self.name = "Sallen Key High Pass"
        self.type = CellType.HIGH_PASS.value

    # -------------- #
    # Public Methods #
    # -------------- #
    def get_parameters(self) -> tuple:
        _, poles, gain = super(SallenKeyHighPassGain, self).get_parameters()
        zeros = {"wz": 0, "nz": 2}
        return zeros, poles, gain

    # -------------- #
    # Static Methods #
    # -------------- #
    def qp(self):
        R1, R2, C1, C2, Ra, Rb = self.declare_symbols()
        wp, qp, k = self.declare_parameters()
        return (1 / sqrt(R1 * R2 * C1 * C2)) / (1 / (C2 * R2) + 1 / (C1 * R2) + (1 - k) / (R1 * C1))
