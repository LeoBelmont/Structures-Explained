import math
from typing import List, Tuple, Union

import numpy as np
from anastruct.fem.elements import Element
from sympy import sympify

from StructuresExplained.utils.util import get_value_from_points


def get_signal_vectors(result, fx_, fy_, element, op, rel_value=1e-12):
    result = round(get_value_from_points(result, element.l), 13)
    fx = sympify(fx_ if fx_ else "0")
    fy = sympify(fy_ if fy_ else "0")

    if op == "sin":
        fx *= np.sin(element.angle)
        fy *= np.sin(np.radians(90) - element.angle)
    elif op == "cos":
        fx *= np.cos(element.angle)
        fy *= np.cos(np.radians(90) - element.angle)

    if math.isclose(round(-fx + fy, 13), result, rel_tol=rel_value):
        return "-", "+"

    elif math.isclose(round(fx - fy, 13), result, rel_tol=rel_value):
        return "+", "-"

    elif math.isclose(round(fx + fy, 13), result, rel_tol=rel_value):
        return "+", "+"

    else:
        return "-", "-"


def assemble_element_connections(system_elements) -> List[Tuple[int, int]]:
    connections = []
    for first_node, elements in system_elements.node_element_map.items():
        for element in elements:
            if first_node in [element.node_id1, element.node_id2]:
                if first_node == element.node_id1:
                    last_node = element.node_id2
                else:
                    last_node = element.node_id1
                connections.append((first_node, last_node))
    return connections


def is_branching(elements: Union[List[Element], Element]) -> bool:
    if not isinstance(elements, list):
        return False
    elif len(elements) > 2:
        return True
    return False


def is_in_path(element: Element,
               path: List[int]
               ) -> bool:
    if element.node_id1 in path and element.node_id2 in path:
        return True
    return False


def node_to_element(node_list: Tuple[int, ...]) -> List[list]:
    element_list = []
    for index in range(len(node_list)):
        if index == len(node_list) - 1:
            break
        element_list.append([node_list[index], node_list[index + 1]])
    return element_list


def node_pair_to_element(stack):
    elements = []
    for index in range(0, len(stack), 2):
        elements.append([stack[index], stack[index + 1]])
    return elements


def are_stacks_connected(node1, node2, stacks):
    if (node1 == stacks[-1][-1] or node2 == stacks[-1][-2]) or \
            (node2 == stacks[-1][-1] or node1 == stacks[-1][-2]):
        return True
    return False


def find_element(element_nodes, node_element_map):
    node1_elements = node_element_map.get(element_nodes[0])
    node2_elements = node_element_map.get(element_nodes[1])
    for element in node1_elements:
        if element in node2_elements:
            return element
    return node1_elements[0]


class NodePathError(ValueError):
    pass
