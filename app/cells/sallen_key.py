# Python native modules
from math import sqrt

# Project modules
from app.cells.electronics import compute_commercial_by_iteration_list
from app.cells.electronics import compute_commercial_by_iteration
from app.cells.electronics import matches_commercial_values
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
class SallenKey(CellGroup):

    def __init__(self):
        super(SallenKey, self).__init__(
            "Sallen Key",
            {
                CellType.LOW_PASS.value: [SallenKeyLowPassAttenuation(), SallenKeyLowPassUnityGain(), SallenKeyLowPassGain()],
                CellType.HIGH_PASS.value: [SallenKeyHighPassUnityGain(), SallenKeyHighPassGain()]
            }
        )


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
            "inverter": False,
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
        gain = self.k()
        poles = {"wp": self.wp(), "qp": self.qp()}
        return zeros, poles, gain

    def get_sensitivities(self) -> dict:
        return {
            "k": {
                "R1": 0,
                "R2": 0,
                "C1": 0,
                "C2": 0,
                "Ra": self.sens_k_ra(),
                "Rb": self.sens_k_rb()
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
                "R1": self.sens_q_r1(),
                "R2": self.sens_q_r2(),
                "C1": self.sens_q_c1(),
                "C2": self.sens_q_c2(),
                "Ra": self.sens_k_ra(),
                "Rb": self.sens_q_rb()
            }
        }

    def design_components(self, zeros: dict, poles: dict, gain: float, stop_at_first=False) -> dict:
        if "wp" not in poles.keys() or "qp" not in poles.keys() or gain <= 1:
            raise CellError(CellErrorCodes.INVALID_PARAMETERS)
        else:
            # Declaring and cleaning
            self.results = []

            # First, calculate the easy gain resistors
            ra_rb = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Resistor,
                lambda rb: rb / (gain - 1),
                self.error
            )

            # Secondly, but using the relationship R1=R2, calculates C1, and C2
            c2_c1 = compute_commercial_by_iteration_list(
                ComponentType.Capacitor, ComponentType.Capacitor,
                [lambda c1: (-c1 * (4 * (1 - gain) - 1) + c1 * sqrt(1 - 8 * poles["qp"] ** 2 * (1 - gain))) / (8 * poles["qp"] ** 2),
                 lambda c1: (-c1 * (4 * (1 - gain) - 1) - c1 * sqrt(1 - 8 * poles["qp"] ** 2 * (1 - gain))) / (8 * poles["qp"] ** 2)],
                self.error
            )

            # Finally, calculates with the previous C1, C2 values, options for R = R1 = R2
            r1_r2_c1_c2 = []
            for c2, c1 in c2_c1:
                r = 1 / (poles["wp"] * sqrt(c1 * c2))
                matches, commercial = matches_commercial_values(ComponentType.Resistor, r, self.error)
                if matches:
                    r1_r2_c1_c2.append((commercial, commercial, c1, c2))

            # Cross selection of possible values of components
            self.results = nexpand_component_list(self.results, ra_rb, "Ra", "Rb")
            self.results = nexpand_component_list(self.results, r1_r2_c1_c2, "R1", "R2", "C1", "C2")
            self.flush_results()
            self.choose_random_result()

    # ------------------------ #
    # Private Internal Methods #
    # ------------------------ #
    def load_variables(self):
        return (
            self.components["R1"],
            self.components["R2"],
            self.components["C1"],
            self.components["C2"],
            self.components["Ra"],
            self.components["Rb"],
        )

    def k(self):
        R1, R2, C1, C2, Ra, Rb = self.load_variables()
        return 1 + Rb / Ra

    def wp(self):
        R1, R2, C1, C2, Ra, Rb = self.load_variables()
        return 1 / sqrt(R1 * R2 * C1 * C2)

    def qp(self):
        R1, R2, C1, C2, Ra, Rb = self.load_variables()
        k = self.k()
        return (1 / sqrt(R1 * R2 * C1 * C2)) / (1 / (C1 * R1) + 1 / (C1 * R2) + (1 - k) / (R2 * C2))

    def sens_k_rb(self):
        k = self.k()
        return 1 - (1 / k)

    def sens_k_ra(self):
        return (-1) * self.sens_k_rb()

    def sens_q_r1(self):
        R1, R2, C1, C2, Ra, Rb = self.load_variables()
        qp = self.qp()
        return (-1 / 2) + qp * sqrt((R2 * C2) / (R1 * C1))

    def sens_q_r2(self):
        R1, R2, C1, C2, Ra, Rb = self.load_variables()
        qp = self.qp()
        k = self.k()
        return (-1 / 2) + qp * (
            sqrt((R1 * C2) / (R2 * C1)) + (1 - k) * sqrt((R1 * C1) / (R2 * C2))
        )

    def sens_q_c1(self):
        R1, R2, C1, C2, Ra, Rb = self.load_variables()
        qp = self.qp()
        return (-1 / 2) + qp * (
            sqrt((R1 * C1) / (R2 * C2)) + sqrt((R2 * C1) / (R1 * C2))
        )

    def sens_q_c2(self):
        return self.sens_q_c1() * (-1)

    def sens_q_rb(self):
        R1, R2, C1, C2, Ra, Rb = self.load_variables()
        qp = self.qp()
        k = self.k()
        return (-1) * (1 - k) * qp * sqrt((R1 * C1) / (R2 * C2))

    def sens_q_ra(self):
        return (-1) * self.sens_q_rb()


class SallenKeyLowPassUnityGain(Cell):

    def __init__(self):
        super(SallenKeyLowPassUnityGain, self).__init__(
            "Sallen Key Low Pass",
            CellType.LOW_PASS.value,
            "app/images/sallen_key_low_pass_unity.png"
        )

        self.options = {
            "inverter": False,
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
    def get_parameters(self) -> tuple:
        zeros = {}
        gain = self.k()
        poles = {"wp": self.wp(), "qp": self.qp()}
        return zeros, poles, gain

    def get_sensitivities(self) -> dict:
        return {
            "k": {
                "R1": 0,
                "R2": 0,
                "C1": 0,
                "C2": 0
            },
            "wp": {
                "R1": -1/2,
                "R2": -1/2,
                "C1": -1/2,
                "C2": -1/2
            },
            "qp": {
                "R1": self.sens_q_r1(),
                "R2": self.sens_q_r2(),
                "C1": self.sens_q_c1(),
                "C2": self.sens_q_c2()
            }
        }

    def design_components(self, zeros: dict, poles: dict, gain: float, stop_at_first=False) -> dict:
        if "wp" not in poles.keys() or "qp" not in poles.keys() or gain != 1:
            raise CellError(CellErrorCodes.INVALID_PARAMETERS)
        else:
            # Declaring and cleaning
            self.results = []

            # Secondly, but using the relationship R1=R2, calculates C1, and C2
            c2_c1 = compute_commercial_by_iteration(
                ComponentType.Capacitor, ComponentType.Capacitor,
                lambda c1: c1 / (4 * poles["qp"] ** 2),
                self.error
            )

            # Finally, calculates with the previous C1, C2 values, options for R = R1 = R2
            r1_r2_c1_c2 = []
            for c2, c1 in c2_c1:
                r = 1 / (poles["wp"] * sqrt(c1 * c2))
                matches, commercial = matches_commercial_values(ComponentType.Resistor, r, self.error)
                if matches:
                    r1_r2_c1_c2.append((commercial, commercial, c1, c2))

            # Cross selection of possible values of components
            self.results = nexpand_component_list(self.results, r1_r2_c1_c2, "R1", "R2", "C1", "C2")
            self.flush_results()
            self.choose_random_result()

    # ------------------------ #
    # Private Internal Methods #
    # ------------------------ #
    def load_variables(self):
        return (
            self.components["R1"],
            self.components["R2"],
            self.components["C1"],
            self.components["C2"],
        )

    def k(self):
        return 1

    def wp(self):
        R1, R2, C1, C2 = self.load_variables()
        return 1 / sqrt(R1 * R2 * C1 * C2)

    def qp(self):
        R1, R2, C1, C2 = self.load_variables()
        return (1 / sqrt(R1 * R2 * C1 * C2)) / (1 / (C1 * R1) + 1 / (C1 * R2))

    def sens_q_r1(self):
        R1, R2, C1, C2 = self.load_variables()
        qp = self.qp()
        return (-1 / 2) + qp * sqrt((R2 * C2) / (R1 * C1))

    def sens_q_r2(self):
        R1, R2, C1, C2 = self.load_variables()
        qp = self.qp()
        return (-1 / 2) + qp * (
            sqrt((R1 * C2) / (R2 * C1))
        )

    def sens_q_c1(self):
        R1, R2, C1, C2 = self.load_variables()
        qp = self.qp()
        return (-1 / 2) + qp * (
            sqrt((R1 * C1) / (R2 * C2)) + sqrt((R2 * C1) / (R1 * C2))
        )

    def sens_q_c2(self):
        return self.sens_q_c1() * (-1)


class SallenKeyLowPassAttenuation(Cell):

    def __init__(self):
        super(SallenKeyLowPassAttenuation, self).__init__(
            "Sallen Key Low Pass",
            CellType.LOW_PASS.value,
            "app/images/sallen_key_low_pass_attenuation.png"
        )

        self.options = {
            "inverter": False,
            "canGain": False,
            "canUnityGain": False,
            "canAttenuate": True
        }

        self.components = {
            "R1A": None,
            "R1B": None,
            "R2": None,
            "C1": None,
            "C2": None
        }

    # -------------- #
    # Public Methods #
    # -------------- #
    def get_parameters(self) -> tuple:
        zeros = {}
        gain = self.k()
        poles = {"wp": self.wp(), "qp": self.qp()}
        return zeros, poles, gain

    def get_sensitivities(self) -> dict:
        return {
            "k": {
                "R1A": self.sens_k_r1a(),
                "R1B": self.sens_k_r1b(),
                "R2": 0,
                "C1": 0,
                "C2": 0
            },
            "wp": {
                "R1A": -1/2,
                "R1B": -1/2,
                "R2": -1/2,
                "C1": -1/2,
                "C2": -1/2
            },
            "qp": {
                "R1A": -1/2,
                "R1B": -1/2,
                "R2": self.sens_q_r2(),
                "C1": self.sens_q_c1(),
                "C2": self.sens_q_c2()
            }
        }

    def design_components(self, zeros: dict, poles: dict, gain: float, stop_at_first=False) -> dict:
        if "wp" not in poles.keys() or "qp" not in poles.keys() or gain >= 1:
            raise CellError(CellErrorCodes.INVALID_PARAMETERS)
        else:
            # Declaring and cleaning
            self.results = []

            # Secondly, but using the relationship R1=R2, calculates C1, and C2
            c2_c1 = compute_commercial_by_iteration(
                ComponentType.Capacitor, ComponentType.Capacitor,
                lambda c1: c1 / (4 * poles["qp"] ** 2),
                self.error
            )

            # Finally, calculates with the previous C1, C2 values, options for R = R1 = R2
            r1_r2_c1_c2 = []
            for c2, c1 in c2_c1:
                r = 1 / (poles["wp"] * sqrt(c1 * c2))
                matches, commercial = matches_commercial_values(ComponentType.Resistor, r, self.error)
                if matches:
                    r1_r2_c1_c2.append((commercial, commercial, c1, c2))

            r1a_r1b = []
            for r1, r2, c1, c2 in r1_r2_c1_c2:
                r1a = r1 / gain
                r1b = r1 / (1 - gain)
                r1a_r1b.append((r1a, r1b))

            # Cross selection of possible values of components
            self.results = nexpand_component_list(self.results, [(r2, c1, c2) for _, r2, c1, c2 in r1_r2_c1_c2], "R2", "C1", "C2")
            self.results = nexpand_component_list(self.results, r1a_r1b, "R1A", "R1B")
            self.flush_results()
            self.choose_random_result()

    # ------------------------ #
    # Private Internal Methods #
    # ------------------------ #
    def load_variables(self):
        return (
            self.components["R1A"],
            self.components["R1B"],
            self.components["R2"],
            self.components["C1"],
            self.components["C2"],
        )

    def r1(self):
        R1A, R1B, R2, C1, C2 = self.load_variables()
        return (R1A * R1B) / (R1A + R1B)

    def k(self):
        R1A, R1B, R2, C1, C2 = self.load_variables()
        return R1B / (R1A + R1B)

    def wp(self):
        R1A, R1B, R2, C1, C2 = self.load_variables()
        R1 = self.r1()
        return 1 / sqrt(R1 * R2 * C1 * C2)

    def qp(self):
        R1A, R1B, R2, C1, C2 = self.load_variables()
        R1 = self.r1()
        return (1 / sqrt(R1 * R2 * C1 * C2)) / (1 / (C1 * R1) + 1 / (C1 * R2))

    def sens_k_r1a(self):
        R1A, R1B, R2, C1, C2 = self.load_variables()
        return (-R1A) / (R1A + R1B)

    def sens_k_r1b(self):
        return (-1) * self.sens_k_r1a()

    def sens_q_r2(self):
        R1A, R1B, R2, C1, C2 = self.load_variables()
        R1 = self.r1()
        qp = self.qp()
        return (-1 / 2) + qp * (
            sqrt((R1 * C2) / (R2 * C1))
        )

    def sens_q_c1(self):
        R1A, R1B, R2, C1, C2 = self.load_variables()
        R1 = self.r1()
        qp = self.qp()
        return (-1 / 2) + qp * (
            sqrt((R1 * C1) / (R2 * C2)) + sqrt((R2 * C1) / (R1 * C2))
        )

    def sens_q_c2(self):
        return self.sens_q_c1() * (-1)


class SallenKeyHighPassGain(SallenKeyLowPassGain):

    def __init__(self):
        super(SallenKeyHighPassGain, self).__init__()

        self.circuit = "app/images/sallen_key_high_pass.png"
        self.name = "Sallen Key High Pass"
        self.type = CellType.HIGH_PASS.value

    # -------------- #
    # Public Methods #
    # -------------- #
    def get_parameters(self) -> tuple:
        _, poles, gain = super(SallenKeyHighPassGain, self).get_parameters()
        zeros = {"wz": 0, "nz": 2}
        return zeros, poles, gain

    def design_components(self, zeros: dict, poles: dict, gain: float, stop_at_first=False) -> dict:
        if "wp" not in poles.keys() or "qp" not in poles.keys() or gain <= 1:
            raise CellError(CellErrorCodes.INVALID_PARAMETERS)
        else:
            # Declaring and cleaning
            self.results = []

            # First, calculate the easy gain resistors
            ra_rb = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Resistor,
                lambda rb: rb / (gain - 1),
                self.error
            )

            # Secondly, but using the relationship C1=C2, calculates R1, and R2
            r1_r2 = compute_commercial_by_iteration_list(
                ComponentType.Resistor, ComponentType.Resistor,
                [lambda r2: (-r2 * (4 * (1 - gain) - 1) + r2 * sqrt(1 - 8 * poles["qp"] ** 2 * (1 - gain))) / (
                            8 * poles["qp"] ** 2),
                 lambda r2: (-r2 * (4 * (1 - gain) - 1) - r2 * sqrt(1 - 8 * poles["qp"] ** 2 * (1 - gain))) / (
                         8 * poles["qp"] ** 2)
                 ],
                self.error
            )

            # Finally, calculates with the previous R1, R2 values, options for C = C1 = C2
            r1_r2_c1_c2 = []
            for r1, r2 in r1_r2:
                c1 = 1 / (poles["wp"] * sqrt(r1 * r2))
                matches, commercial = matches_commercial_values(ComponentType.Capacitor, c1, self.error)
                if matches:
                    r1_r2_c1_c2.append((r1, r2, commercial, commercial))

            # Cross selection of possible values of components
            self.results = nexpand_component_list(self.results, ra_rb, "Ra", "Rb")
            self.results = nexpand_component_list(self.results, r1_r2_c1_c2, "R1", "R2", "C1", "C2")
            self.flush_results()
            self.choose_random_result()

    # -------------- #
    # Static Methods #
    # -------------- #
    def qp(self):
        R1, R2, C1, C2, Ra, Rb = self.load_variables()
        k = self.k()
        return (1 / sqrt(R1 * R2 * C1 * C2)) / (1 / (C2 * R2) + 1 / (C1 * R2) + (1 - k) / (R1 * C1))


class SallenKeyHighPassUnityGain(SallenKeyLowPassUnityGain):

    def __init__(self):
        super(SallenKeyHighPassUnityGain, self).__init__()

        self.circuit = "app/images/sallen_key_high_pass_unity.png"
        self.name = "Sallen Key High Pass"
        self.type = CellType.HIGH_PASS.value

    # -------------- #
    # Public Methods #
    # -------------- #
    def get_parameters(self) -> tuple:
        _, poles, gain = super(SallenKeyHighPassUnityGain, self).get_parameters()
        zeros = {"wz": 0, "nz": 2}
        return zeros, poles, gain

    # -------------- #
    # Static Methods #
    # -------------- #
    def qp(self):
        R1, R2, C1, C2 = self.load_variables()
        return (1 / sqrt(R1 * R2 * C1 * C2)) / (1 / (C2 * R2) + 1 / (C1 * R2))
