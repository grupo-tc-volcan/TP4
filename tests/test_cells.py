# third-party modules
import pytest

# python native modules

# project modules
from app.cells.active_first_order import CompensatedIntegrator
from app.cells.active_first_order import CompensatedDerivator


@pytest.fixture
def cell():
    # Change the returning cell to test it!
    return CompensatedDerivator()


def test_description(cell):
    print(cell.get_name())
    print(cell.get_type())


def test_parameters(cell):
    cell.components = {
        "R1": 1000,
        "R2": 2200,
        "C1": 100e-9
    }
    print(cell.get_parameters())


def test_sensitivities(cell):
    cell.components = {
        "R1": 1000,
        "R2": 2200,
        "C1": 100e-9
    }
    print(cell.get_sensitivities())


def test_design(cell):
    cell.set_error(0.01)

    cell.design_components(
        {},
        {"wp": 10000},
        -10
    )

    print(cell.get_components())
