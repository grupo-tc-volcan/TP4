# Third-party modules
from sympy import *

# Python native modules
from enum import Enum

import math


# ---------------- #
# Type Definitions #
# ---------------- #
class ComponentType(Enum):
    Resistor = "Resistor"
    Capacitor = "Capacitor"


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
def nexpand_component_list(current: list, new_options: list, *args):
    """ Expands a list of dictionaries describing a set of components, by matching the new options
        with already registered ones, and appending new component labels and values.
        [Parameters]
            + current: List of components [ {...} ]
            + new_options: List of n-tuple [ (...) ]
            + args: List of labels
        """
    if not current:
        for new_option in new_options:
            new_pack = {}
            for index, component in enumerate(new_option):
                new_pack[args[index]] = component
            current.append(new_pack)
    else:
        for new_option in new_options:
            for current_option in current:
                contained = False
                matches = True

                for index, component in enumerate(new_option):
                    if not contained and args[index] in current_option.keys():
                        contained = True

                    if contained and args[index] in current_option.keys():
                        if current_option[args[index]] != component:
                            matches = False
                            break

                if contained:
                    if matches:
                        for index, component in enumerate(new_option):
                            if args[index] not in current_option.keys():
                                current_option[args[index]] = component
                else:
                    for index, component in enumerate(new_option):
                        current_option[args[index]] = component
    return current


def expand_component_list(current: list, new_options: list, label_one: str, label_two: str):
    """ Expands a list of dictionaries describing a set of components, by matching the new options
        with already registered ones, and appending new component labels and values.
        [Parameters]
            + current: List of components [ {...} ]
            + new_options: List of 2-tuple with both new components. Example: [ (R1, C1) ]
            + label_one: How first component is labeled in dictionaries
            + label_two: How second component is labeled in dictionaries
        """
    if not current:
        current = [{label_one: component_one, label_two: component_two} for component_one, component_two in new_options]
    else:
        for component_one, component_two in new_options:
            for current_option in current:
                if label_one in current_option.keys():
                    if current_option[label_one] == component_one:
                        current_option[label_two] = component_two
                elif label_two in current_option.keys():
                    if current_option[label_two] == component_two:
                        current_option[label_one] = component_one
                else:
                    current_option[label_one] = component_one
                    current_option[label_two] = component_two
    return current


def compute_commercial_values(component_type: ComponentType) -> list:
    """ Returns a list of possible commercial values for the given component type.
    Returns None if non-identified component type. """

    def multiply_lists(first_list, second_list) -> list:
        new_list = []
        for first_element in first_list:
            for second_element in second_list:
                new_list.append(first_element * second_element)
        return new_list

    if component_type is ComponentType.Resistor:
        return multiply_lists(MULTIPLIER_RESISTORS, COMMERCIAL_RESISTORS)
    elif component_type is ComponentType.Capacitor:
        return multiply_lists(MULTIPLER_CAPACITORS, COMMERCIAL_CAPACITORS)
    else:
        return None


def compute_commercial_by_iteration(
        element_one: ComponentType, element_two: ComponentType,
        callback: callable, error: float,
        fixed_one_values=None,
        fixed_two_values=None) -> list:
    """ Returns [(element_one_value, element_two_value)], list of 2-tuple with possible values
    that verify the expression element_one = callback(element_two), with a relative decimal expressed error.
    Fixed list of values can be used to process the iteration.
    """
    # Loading possible choices for each element, setting up the result list
    element_one_values = compute_commercial_values(element_one) if fixed_one_values is None else fixed_one_values
    element_two_values = compute_commercial_values(element_two) if fixed_two_values is None else fixed_two_values
    results = []

    # Find for each possible element_two value, a resulting element_one and verify
    # if matches with a commercial value with the given error tolerance
    for element_two_value in element_two_values:
        element_one_target = callback(element_two_value)

        for element_one_value in element_one_values:
            if math.isclose(element_one_target, element_one_value, rel_tol=error):
                results.append((element_one_value, element_two_value))

    # Returning the results... empty or not
    return results


# ----------------------- #
# Standard callback tools #
# ----------------------- #
def build_expression_callback(expression, target, symbol):
    """ Returns a callback to get the element_one as function of element_two,
    by solving an equation for the expression = target, getting the given symbol. """
    solutions = solve(Eq(expression, target), symbol)
    symbol_expression = solutions[0]

    def callback(element_two_value: float):
        symbol = symbol_expression.free_symbols.pop()
        symbol_expression.free_symbols.add(symbol)
        return symbol_expression.evalf(subs={symbol: element_two_value})
    return callback


def build_proportional_callback(k: float):
    """ Returns a callback which operates as element_one = element_two * k """
    def callback(element_two_value: float):
        return element_two_value * k
    return callback


if __name__ == "__main__":
    test = []
    test = nexpand_component_list(test, [(1, 2, 3), (4, 5, 6)], "R1", "R2", "R3")
    test = nexpand_component_list(test, [(1, 2, 10), (4, 5, 20)], "R1", "R2", "C1")
    test = nexpand_component_list(test, [(3.15, 1.6)], "Ra", "Rb")
    print(test)
