# Third-party modules

# Python native modules
from enum import Enum

import math


# ---------------- #
# Type Definitions #
# ---------------- #
class ComponentType(Enum):
    RESISTOR = "Resistor"
    CAPACITOR = "Capacitor"


# --------------------------- #
# Constant Values Declaration #
# --------------------------- #
COMMERCIAL_RESISTORS = [
    1, 1.1, 1.2, 1.3, 1.5, 1.8, 2, 2.2, 2.4, 2.7, 3, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1,
    5.6, 6.2, 6.8, 7.5, 8.2, 9.1
]

MULTIPLIER_RESISTORS = [10e0, 10e1, 10e2, 10e3, 10e4, 10e5]

COMMERCIAL_CAPACITORS = [
    1, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2
]

MULTIPLER_CAPACITORS = [1e-12, 10e-12, 100e-12, 1e-9, 10e-9, 100e-9, 1e-6]


# ---------------- #
# Public Functions #
# ---------------- #
def compute_commercial_values(component_type: ComponentType) -> list:
    """ Returns a list of possible commercial values for the given component type.
    Returns None if non-identified component type. """

    def multiply_lists(first_list, second_list) -> list:
        new_list = []
        for first_element in first_list:
            for second_element in second_list:
                new_list.append(first_element * second_element)
        return new_list

    if component_type is ComponentType.RESISTOR:
        return multiply_lists(MULTIPLIER_RESISTORS, COMMERCIAL_RESISTORS)
    elif component_type is ComponentType.CAPACITOR:
        return multiply_lists(MULTIPLER_CAPACITORS, COMMERCIAL_CAPACITORS)
    else:
        return None


def compute_commercial_by_iteration(
        element_one: ComponentType, element_two: ComponentType,
        k: float, error: float) -> list:
    """ Returns [(element_one_value, element_two_value)], list of 2-tuple with possible values
    that verify the expression element_one = element_two * k, with a relative decimal expressed error.
    """
    # Loading possible choices for each element, setting up the result list
    element_one_values = compute_commercial_values(element_one)
    element_two_values = compute_commercial_values(element_two)
    results = []

    # Find for each possible element_two value, a resulting element_one and verify
    # if matches with a commercial value with the given error tolerance
    for element_two_value in element_two_values:
        element_one_target = element_two_value * k

        for element_one_value in element_one_values:
            if math.isclose(element_one_target, element_one_value, rel_tol=error):
                results.append((element_one_value, element_two_value))

    # Returning the results... empty or not
    return results
