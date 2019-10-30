# third-party modules
import pytest

# python native modules

# project modules
from app.cells.active_first_order import CompensatedIntegrator
from app.cells.active_first_order import CompensatedDerivator
from app.cells.active_first_order import ActiveFirstOrder

from app.cells.cell import CellErrorCodes


@pytest.fixture
def cell():
    # Change the returning cell to test it!
    return ActiveFirstOrder()


def test_group_description(cell):
    print(cell.get_name())
    print(cell.get_available_types())


def test_group_parameters(cell):
    def group_parameters_by_type(cell_type: str):
        components = {
            "R1": 1000,
            "R2": 2200,
            "C1": 100e-9
        }

        cell.set_components(cell_type, components)
        print(cell.get_parameters(cell_type))

    group_parameters_by_type("low-pass")
    group_parameters_by_type("high-pass")
    group_parameters_by_type("band-pass")
    group_parameters_by_type("band-stop")


def test_group_design(cell):
    def group_design_by_type(cell_type: str, error: float, zeros: dict, poles: dict, gain: float):
        cell.set_error(cell_type, error)
        cell.design_components(
            cell_type,
            zeros,
            poles,
            gain
        )
        print(cell.get_components(cell_type))

    group_design_by_type(
        "low-pass", 0.01,
        {},
        {"wp": 10000},
        -10
    )

    group_design_by_type(
        "high-pass", 0.01,
        {"wz": 0},
        {"wp": 10000},
        -10
    )


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
