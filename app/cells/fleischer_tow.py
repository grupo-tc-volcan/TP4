# Third-party modules

# Python native modules
from math import *

# Project modules
from app.cells.cell import CellType
from app.cells.cell import Cell


# --------------------- #
# Cell Group Definition #
# --------------------- #


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
        pass

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
        pass

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
        zeros = {}
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
        pass

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
        pass

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
