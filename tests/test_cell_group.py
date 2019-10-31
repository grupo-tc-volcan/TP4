# Third-party modules
import pytest

# Project modules
from app.cells.sallen_key import SallenKey
from app.cells.active_first_order import ActiveFirstOrder


@pytest.fixture
def cell():
    return SallenKey()


def test_description(cell):
    print(cell.get_name())
    print(cell.get_available_types())


def test_validation(cell):
    print(cell.is_valid_gain_mode("low-pass", gain=0.5))
    print(cell.is_valid_gain_mode("low-pass", gain=1))
    print(cell.is_valid_gain_mode("low-pass", gain=5))

    print(cell.is_valid_gain_mode("high-pass", gain=0.5))
    print(cell.is_valid_gain_mode("high-pass", gain=1))
    print(cell.is_valid_gain_mode("high-pass", gain=5))

    print(cell.is_valid_gain_mode("band-pass", gain=0.5))
    print(cell.is_valid_gain_mode("band-pass", gain=1))
    print(cell.is_valid_gain_mode("band-pass", gain=5))

    print(cell.is_valid_gain_mode("band-stop", gain=0.5))
    print(cell.is_valid_gain_mode("band-stop", gain=1))
    print(cell.is_valid_gain_mode("band-stop", gain=5))


def test_set(cell):
    cell.set_cell("low-pass", gain=1)
    print(cell.get_circuit())
    print(cell.get_components())
    print(cell.get_results())


def test_parameters(cell):
    components = {
        "R1": 1200,
        "R2": 2200,
        "C1": 100e-9,
        "C2": 100e-9
    }
    cell.set_cell("low-pass", gain=1)
    cell.set_components(components)
    print(cell.get_parameters())


def test_sensitivities(cell):
    components = {
        "R1": 1200,
        "R2": 2200,
        "C1": 100e-9,
        "C2": 100e-9
    }
    cell.set_cell("low-pass", gain=1)
    cell.set_components(components)
    print(cell.get_sensitivities())


def test_design(cell):
    cell.set_cell("low-pass", gain=1)
    cell.set_error(0.05)
    cell.design_components(
        {"wz": 0},
        {"wp": 10000, "qp": 0.8},
        1
    )
    print(cell.get_components())
