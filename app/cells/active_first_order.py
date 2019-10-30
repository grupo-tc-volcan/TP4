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
