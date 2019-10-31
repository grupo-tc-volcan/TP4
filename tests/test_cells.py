# third-party modules
import pytest

# python native modules

# project modules
from app.cells.active_first_order import CompensatedIntegrator
from app.cells.active_first_order import CompensatedDerivator
from app.cells.active_first_order import ActiveFirstOrder

from app.cells.sallen_key import SallenKeyLowPassGain
from app.cells.sallen_key import SallenKeyLowPassUnityGain

from app.cells.sallen_key import SallenKeyHighPassGain

from app.cells.cell import CellErrorCodes


@pytest.fixture
def cell():
    # Change the returning cell to test it!
    return CompensatedDerivator()


def test_description(cell):
    print(cell.get_name())
    print(cell.get_type())
    print(cell.get_circuit())


def test_validation(cell):
    print(cell.is_valid_gain_mode(gain=0.5))
    print(cell.is_valid_gain_mode(gain=1))
    print(cell.is_valid_gain_mode(gain=5))


def test_parameters(cell):
    cell.components = {
        "R1": 1000,
        "R2": 2200,
        "C1": 100e-9,
        "C2": 10e-9
    }
    print(cell.get_parameters())


def test_sensitivities(cell):
    cell.components = {
        "R1": 1000,
        "R2": 2200,
        "C1": 100e-9,
        "C2": 10e-9,
        "Ra": 1000,
        "Rb": 100
    }
    print(cell.get_sensitivities())


def test_design(cell):
    cell.set_error(0.1)

    cell.design_components(
        {"wz": 0},
        {"wp": 10000, "qp": 0.89},
        -1
    )

    print(cell.components)
