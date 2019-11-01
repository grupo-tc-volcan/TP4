# Third-party modules

# Python native modules
from math import *

# Project modules
from app.cells.electronics import compute_commercial_by_iteration
from app.cells.electronics import matches_commercial_values
from app.cells.electronics import nexpand_component_list
from app.cells.electronics import random_commercial
from app.cells.electronics import ComponentType

from app.cells.cell import CellErrorCodes
from app.cells.cell import CellGroup
from app.cells.cell import CellError
from app.cells.cell import CellType
from app.cells.cell import Cell


# --------------------- #
# Cell Group Definition #
# --------------------- #
class FleischerTow(CellGroup):

    def __init__(self):
        super(FleischerTow, self).__init__(
            "Fleischer Tow",
            {
                CellType.LOW_PASS.value: FleischerTowLowPass,
                CellType.HIGH_PASS.value: FleischerTowHighPass,
                CellType.BAND_PASS.value: FleischerTowBandPass,
                CellType.BAND_STOP.value: FleischerTowBandStop
            }
        )


# ---------------- #
# Cell Definitions #
# ---------------- #
class FleischerTowBandStop(Cell):

    def __init__(self):
        super(FleischerTowBandStop, self).__init__(
            "Fleischer Tow Band Stop",
            CellType.BAND_STOP.value,
            "app/images/fleischer_tow_band_stop.png"
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
            "R3": None,
            "R4": None,
            "R5": None,
            "R6": None,
            "R7": None,
            "R8": None,
            "C1": None,
            "C2": None
        }

    # -------------- #
    # Public Methods #
    # -------------- #
    def get_parameters(self) -> tuple:
        zeros = {"wz": self.wz(), "nz": 2}
        poles = {"wp": self.wp(), "qp": self.qp()}
        gain = self.k()
        return zeros, poles, gain

    def get_sensitivities(self) -> dict:
        return {
            "k": {
                "R1": 0,
                "R2": 1,
                "R3": 0,
                "R4": 0,
                "R5": -1,
                "R6": 0,
                "R7": 0,
                "R8": 0,
                "C1": 0,
                "C2": 0,
            },
            "wz": {
                "R1": 0,
                "R2": 0,
                "R3": -1/2,
                "R4": 0,
                "R5": -1/2,
                "R6": 1/2,
                "R7": -1/2,
                "R8": 0,
                "C1": -1/2,
                "C2": -1/2,
            },
            "wp": {
                "R1": 0,
                "R2": -1/2,
                "R3": -1/2,
                "R4": 0,
                "R5": 0,
                "R6": 0,
                "R7": -1/2,
                "R8": -1/2,
                "C1": -1/2,
                "C2": -1/2,
            },
            "qp": {
                "R1": 1,
                "R2": -1/2,
                "R3": -1/2,
                "R4": 0,
                "R5": 0,
                "R6": 0,
                "R7": -1/2,
                "R8": 1/2,
                "C1": 1/2,
                "C2": -1/2,
            },
        }

    def design_components(self, zeros: dict, poles: dict, gain: float, stop_at_first=False) -> dict:
        if "wp" not in poles.keys() or "wz" not in zeros.keys() or "qp" not in poles.keys() or gain >= 0:
            raise CellError(CellErrorCodes.INVALID_PARAMETERS)
        else:
            self.results = []

            # Starts calculating R2=R3 with R5 relationship of gain
            r2_r5 = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Resistor,
                lambda r5: gain * (-r5),
                self.error
            )
            r2_r3_r5 = [(r2, r2, r5) for r2, r5 in r2_r5]

            # To get the desired Q value, calculate R1 for that
            r1_r2 = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Resistor,
                lambda r2: poles["qp"] * r2,
                self.error,
                fixed_two_values=[r2 for r2, r3, r5 in r2_r3_r5]
            )

            # Calculating the capacitors for the pole frequency
            c_r2 = compute_commercial_by_iteration(
                ComponentType.Capacitor, ComponentType.Resistor,
                lambda r2: 1 / (r2 * poles["wp"]),
                self.error,
                fixed_two_values=[r2 for r2, r3, r5 in r2_r3_r5]
            )
            c1_c2_r3 = [(c, c, r2) for c, r2 in c_r2]

            r1_r4_c1_r3 = []
            r7_r8_r6_c1_r3 = []
            for c1, c2, r3 in c1_c2_r3:
                r4_r1 = compute_commercial_by_iteration(
                    ComponentType.Resistor, ComponentType.Resistor,
                    lambda r1: r1 * (((zeros["wz"]**2) * (c1**2) * (r3**2) )/ (-gain)),
                    self.error
                )
                r1_r4_c1_r3 += [(r1, r4, c1, r3) for r4, r1 in r4_r1]

                r6_r7 = compute_commercial_by_iteration(
                    ComponentType.Resistor, ComponentType.Resistor,
                    lambda r7: r7 * ((zeros["wz"]**2) * (c1**2) * (r3**2) / (-gain)),
                    self.error
                )
                r7_r8_r6_c1_r3 += [(r7, r7, r6, c1, r3) for r6, r7 in r6_r7]

            self.results = nexpand_component_list(self.results, r2_r3_r5, "R2", "R3", "R5")
            self.results = nexpand_component_list(self.results, r1_r2, "R1", "R2")
            self.results = nexpand_component_list(self.results, c1_c2_r3, "C1", "C2", "R3")
            self.results = nexpand_component_list(self.results, r1_r4_c1_r3, "R1", "R4", "C1", "R3")
            self.results = nexpand_component_list(self.results, r7_r8_r6_c1_r3, "R7", "R8", "R6", "C1", "R3")
            self.flush_results()
            self.choose_random_result()

    # --------------- #
    # Private Methods #
    # --------------- #
    def load_variables(self):
        return (
            self.components["R1"],
            self.components["R2"],
            self.components["R3"],
            self.components["R4"],
            self.components["R5"],
            self.components["R6"],
            self.components["R7"],
            self.components["R8"],
            self.components["C1"],
            self.components["C2"]
        )

    def k(self):
        R1, R2, R3, R4, R5, R6, R7, R8, C1, C2 = self.load_variables()
        return -R2 / R5

    def wz(self):
        R1, R2, R3, R4, R5, R6, R7, R8, C1, C2 = self.load_variables()
        return sqrt(R6 / (R3 * R5 * R7 * C1 * C2))

    def wp(self):
        R1, R2, R3, R4, R5, R6, R7, R8, C1, C2 = self.load_variables()
        return sqrt(R8 / (R2 * R3 * R7 * C1 * C2))

    def qp(self):
        R1, R2, R3, R4, R5, R6, R7, R8, C1, C2 = self.load_variables()
        return R1 * C1 * self.wp()


class FleischerTowBandPass(Cell):

    def __init__(self):
        super(FleischerTowBandPass, self).__init__(
            "Fleischer Tow Band Pass",
            CellType.BAND_PASS.value,
            "app/images/fleischer_tow_band_pass.png"
        )

        self.options = {
            "inverter": False,
            "canGain": True,
            "canUnityGain": True,
            "canAttenuate": True
        }

        self.components = {
            "R1": None,
            "R2": None,
            "R3": None,
            "R4": None,
            "R7": None,
            "R8": None,
            "C1": None,
            "C2": None
        }

    # -------------- #
    # Public Methods #
    # -------------- #
    def get_parameters(self) -> tuple:
        zeros = {}
        poles = {"wp": self.wp(), "qp": self.qp()}
        gain = self.k()
        return zeros, poles, gain

    def get_sensitivities(self) -> dict:
        return {
            "k": {
                "R1": 1,
                "R2": 0,
                "R3": 0,
                "R4": -1,
                "R5": 0,
                "R6": 0,
                "R7": -1,
                "R8": 1,
                "C1": 0,
                "C2": 0,
            },
            "wp": {
                "R1": 0,
                "R2": -1/2,
                "R3": -1/2,
                "R4": 0,
                "R5": 0,
                "R6": 0,
                "R7": -1/2,
                "R8": -1/2,
                "C1": -1/2,
                "C2": -1/2,
            },
            "qp": {
                "R1": 1,
                "R2": -1/2,
                "R3": -1/2,
                "R4": 0,
                "R5": 0,
                "R6": 0,
                "R7": -1/2,
                "R8": 1/2,
                "C1": 1/2,
                "C2": -1/2,
            },
        }

    def design_components(self, zeros: dict, poles: dict, gain: float, stop_at_first=False) -> dict:
        if "wp" not in poles.keys() or "qp" not in poles.keys() or gain <= 0:
            raise CellError(CellErrorCodes.INVALID_PARAMETERS)
        else:
            self.results = []

            # Random values... why not?
            r7 = r8 = random_commercial(ComponentType.Resistor)

            # Calculate R1 and R4 to verify the gain of the filter
            r1_r4 = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Resistor,
                lambda r4: gain * r4,
                self.error
            )

            # Using the previous R1 values, get the R = R2 = R3 values
            r_r1 = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Resistor,
                lambda r1: r1 / poles["qp"],
                self.error,
                fixed_two_values=[r1 for r1, r4 in r1_r4]
            )
            r1_r2_r3 = [(r1, r, r) for r, r1 in r_r1]

            # Using that C=C1=C2 then calculate with the previous values of R
            c_r = compute_commercial_by_iteration(
                ComponentType.Capacitor, ComponentType.Resistor,
                lambda r: 1 / (poles["wp"] * r),
                self.error,
                fixed_two_values=[r for r, r1 in r_r1]
            )
            c1_c2_r2 = [(c, c, r) for c, r in c_r]

            self.results = nexpand_component_list(self.results, c1_c2_r2, "C1", "C2", "R2")
            self.results = nexpand_component_list(self.results, r1_r2_r3, "R1", "R2", "R3")
            self.results = nexpand_component_list(self.results, r1_r4, "R1", "R4")
            self.results = nexpand_component_list(self.results, [(r7, r8)], "R7", "R8")
            self.flush_results()
            self.choose_random_result()

    # --------------- #
    # Private Methods #
    # --------------- #
    def load_variables(self):
        return (
            self.components["R1"],
            self.components["R2"],
            self.components["R3"],
            self.components["R4"],
            self.components["R7"],
            self.components["R8"],
            self.components["C1"],
            self.components["C2"]
        )

    def k(self):
        R1, R2, R3, R4, R7, R8, C1, C2 = self.load_variables()
        return (R1 * R8) / (R4 * R7)

    def wp(self):
        R1, R2, R3, R4, R7, R8, C1, C2 = self.load_variables()
        return sqrt(R8 / (R2 * R3 * R7 * C1 * C2))

    def qp(self):
        R1, R2, R3, R4, R7, R8, C1, C2 = self.load_variables()
        return R1 * C1 * self.wp()


class FleischerTowHighPass(Cell):

    def __init__(self):
        super(FleischerTowHighPass, self).__init__(
            "Fleischer Tow High Pass",
            CellType.HIGH_PASS.value,
            "app/images/fleischer_tow_high_pass.png"
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
            "R3": None,
            "R4": None,
            "R6": None,
            "R7": None,
            "R8": None,
            "C1": None,
            "C2": None
        }

    # -------------- #
    # Public Methods #
    # -------------- #
    def get_parameters(self) -> tuple:
        zeros = {"wz": 0, "nz": 2}
        poles = {"wp": self.wp(), "qp": self.qp()}
        gain = self.k()
        return zeros, poles, gain

    def get_sensitivities(self) -> dict:
        return {
            "k": {
                "R1": 0,
                "R2": 0,
                "R3": 0,
                "R4": 0,
                "R5": 0,
                "R6": -1,
                "R7": 0,
                "R8": 1,
                "C1": 0,
                "C2": 0,
            },
            "wp": {
                "R1": 0,
                "R2": -1/2,
                "R3": -1/2,
                "R4": 0,
                "R5": 0,
                "R6": 0,
                "R7": -1/2,
                "R8": -1/2,
                "C1": -1/2,
                "C2": -1/2,
            },
            "qp": {
                "R1": 1,
                "R2": -1/2,
                "R3": -1/2,
                "R4": 0,
                "R5": 0,
                "R6": 0,
                "R7": -1/2,
                "R8": 1/2,
                "C1": 1/2,
                "C2": -1/2,
            },
        }

    def design_components(self, zeros: dict, poles: dict, gain: float, stop_at_first=False) -> dict:
        if "wp" not in poles.keys() or "qp" not in poles.keys() or gain >= 0:
            raise CellError(CellErrorCodes.INVALID_PARAMETERS)
        else:
            self.results = []

            # Using the gain, we calculate R6, R7 and R8, using that R7 = R8
            r8_r6 = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Resistor,
                lambda r6: gain * (- r6),
                self.error
            )
            r8_r7_r6 = [(r8, r8, r6) for r8, r6 in r8_r6]

            # Using R = R2 = R3 and C = C1 = C2 to calculate values
            r_c = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Capacitor,
                lambda c: 1 / (poles["wp"] * c),
                self.error
            )
            r2_r3_c1_c2 = [(r, r, c, c) for r, c in r_c]

            # Calculate R1 and R4
            r1_r2 = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Resistor,
                lambda r2: r2 * poles["qp"],
                self.error,
                fixed_two_values=[r2 for r2, r3, c1, c2 in r2_r3_c1_c2]
            )

            r4_r1 = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Resistor,
                lambda r1: -r1 / gain,
                self.error,
                fixed_two_values=[r1 for r1, r2 in r1_r2]
            )

            self.results = nexpand_component_list(self.results, r4_r1, "R4", "R1")
            self.results = nexpand_component_list(self.results, r1_r2, "R1", "R2")
            self.results = nexpand_component_list(self.results, r2_r3_c1_c2, "R2", "R3", "C1", "C2")
            self.results = nexpand_component_list(self.results, r8_r7_r6, "R8", "R7", "R6")
            self.flush_results()
            self.choose_random_result()

    # --------------- #
    # Private Methods #
    # --------------- #
    def load_variables(self):
        return (
            self.components["R1"],
            self.components["R2"],
            self.components["R3"],
            self.components["R4"],
            self.components["R6"],
            self.components["R7"],
            self.components["R8"],
            self.components["C1"],
            self.components["C2"]
        )

    def k(self):
        R1, R2, R3, R4, R6, R7, R8, C1, C2 = self.load_variables()
        return -R8 / R6

    def wp(self):
        R1, R2, R3, R4, R6, R7, R8, C1, C2 = self.load_variables()
        return sqrt(R8 / (R2 * R3 * R7 * C1 * C2))

    def qp(self):
        R1, R2, R3, R4, R6, R7, R8, C1, C2 = self.load_variables()
        return R1 * C1 * self.wp()


class FleischerTowLowPass(Cell):

    def __init__(self):
        super(FleischerTowLowPass, self).__init__(
            "Fleischer Tow Low Pass",
            CellType.LOW_PASS.value,
            "app/images/fleischer_tow_low_pass.png"
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
            "R3": None,
            "R5": None,
            "R7": None,
            "R8": None,
            "C1": None,
            "C2": None
        }

    # -------------- #
    # Public Methods #
    # -------------- #
    def get_parameters(self) -> tuple:
        zeros = {}
        poles = {"wp": self.wp(), "qp": self.qp()}
        gain = self.k()
        return zeros, poles, gain

    def get_sensitivities(self) -> dict:
        return {
            "k": {
                "R1": 0,
                "R2": 1,
                "R3": 0,
                "R4": 0,
                "R5": -1,
                "R6": 0,
                "R7": 0,
                "R8": 0,
                "C1": 0,
                "C2": 0,
            },
            "wp": {
                "R1": 0,
                "R2": -1/2,
                "R3": -1/2,
                "R4": 0,
                "R5": 0,
                "R6": 0,
                "R7": -1/2,
                "R8": -1/2,
                "C1": -1/2,
                "C2": -1/2,
            },
            "qp": {
                "R1": 1,
                "R2": -1/2,
                "R3": -1/2,
                "R4": 0,
                "R5": 0,
                "R6": 0,
                "R7": -1/2,
                "R8": 1/2,
                "C1": 1/2,
                "C2": -1/2,
            },
        }

    def design_components(self, zeros: dict, poles: dict, gain: float, stop_at_first=False) -> dict:
        if "wp" not in poles.keys() or "qp" not in poles.keys() or gain >= 0:
            raise CellError(CellErrorCodes.INVALID_PARAMETERS)
        else:
            self.results = []

            # Using the gain calculates posible values for R2 and R5
            r2_r5 = compute_commercial_by_iteration(
                ComponentType.Resistor, ComponentType.Resistor,
                lambda r5: gain * (-r5),
                self.error
            )

            # Random values for R7 and R8
            r7 = r8 = random_commercial(ComponentType.Resistor)

            # Using R2 values, get possible values for R3 and C=C1=C2
            r3_c1_c2_r2_r1 = []
            for r2, r5 in r2_r5:
                r3_c = compute_commercial_by_iteration(
                    ComponentType.Resistor, ComponentType.Capacitor,
                    lambda c: 1 / ((poles["wp"] ** 2) * (c ** 2) * r2),
                    self.error
                )
                for r3, c in r3_c:
                    r1 = poles["qp"] * sqrt(r2 * r3)
                    matches, commercial = matches_commercial_values(ComponentType.Resistor, r1, self.error)
                    if matches:
                        r3_c1_c2_r2_r1.append((r3, c, c, r2, commercial))

            # Cross selection
            self.results = nexpand_component_list(self.results, r3_c1_c2_r2_r1, "R3", "C1", "C2", "R2", "R1")
            self.results = nexpand_component_list(self.results, r2_r5, "R2", "R5")
            self.results = nexpand_component_list(self.results, [(r7, r8)], "R7", "R8")
            self.flush_results()
            self.choose_random_result()

    # --------------- #
    # Private Methods #
    # --------------- #
    def load_variables(self):
        return (
            self.components["R1"],
            self.components["R2"],
            self.components["R3"],
            self.components["R5"],
            self.components["R7"],
            self.components["R8"],
            self.components["C1"],
            self.components["C2"]
        )

    def k(self):
        R1, R2, R3, R5, R7, R8, C1, C2 = self.load_variables()
        return -R2 / R5

    def wp(self):
        R1, R2, R3, R5, R7, R8, C1, C2 = self.load_variables()
        return sqrt(R8 / (R2 * R3 * R7 * C1 * C2))

    def qp(self):
        R1, R2, R3, R5, R7, R8, C1, C2 = self.load_variables()
        return R1 * C1 * self.wp()
