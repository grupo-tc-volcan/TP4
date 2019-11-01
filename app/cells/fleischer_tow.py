# Third-party modules

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
        pass

    def get_sensitivities(self) -> dict:
        pass

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
        pass

    def get_sensitivities(self) -> dict:
        pass

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
        pass

    def get_sensitivities(self) -> dict:
        pass

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
        pass

    def get_sensitivities(self) -> dict:
        pass

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
