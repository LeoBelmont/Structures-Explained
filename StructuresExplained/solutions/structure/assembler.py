from anastruct import SystemElements
from anastruct.fem.elements import Element
from collections import defaultdict
from StructuresExplained.solutions.structure.fig_generation import fig_generator
from enum import Enum
import re
from typing import Optional, Union, List, Tuple
from sympy import sympify, integrate, Symbol
import numpy as np
from sympy.physics.units import degree
import math
from StructuresExplained.utils.util import get_value_from_points


class Setting(Enum):
    random = "random"
    longest = "longest"


class Branch_data:
    def __init__(self, branch: List[int]):
        self.current_node_index = 0
        self.branch = branch


class Stresses_Stack:
    fx = ""
    fy = ""
    fy_symbolic = ""
    fx_angular = ""
    fy_angular = ""
    is_symbolic = False
    is_angular = False
    _force_map = None
    _distributed_force_map = None
    _reactions_map = None

    def __init__(self, node: int, element: [Element]):
        self.node = node
        self.determine_internal_forces(node, element)

    @classmethod
    def system(cls, system):
        cls._force_map = system.loads_point
        cls._moment_map = system.loads_moment
        cls._distributed_force_map = system.loads_q
        cls._reactions_map = system.reaction_forces

    @property
    def axes_forces(self):
        if self.is_angular:
            self.is_angular = False
            # symbolic flag also set to false because angular strings will include symbolic strings
            self.is_symbolic = False
            return [self.fx_angular, self.fy_angular]
        if self.is_symbolic:
            self.is_symbolic = False
            return [self.fx, self.fy_symbolic]
        return [self.fx, self.fy]

    def determine_internal_forces(self, node, element):
        forces = self._force_map.get(node)
        reactions = self._reactions_map.get(node)
        if forces:
            if round(forces[0], 13):
                self.fx += f"+{forces[0]}"
            if round(forces[1], 13):
                self.fy += f"+{-forces[1]}"
        if reactions:
            if round(reactions.Fx, 13):
                self.fx += f"+{reactions.Fx}"
            if round(reactions.Fz, 13):
                self.fy += f"+{-reactions.Fz}"
        if element:
            q_loads = self._distributed_force_map.get(element.id)
            if q_loads:
                if round(q_loads[0][0], 13) and round(q_loads[1][0], 13):
                    x = Symbol('x')
                    xi = element.vertex_1.x
                    yi = element.vertex_1.y
                    xf = element.vertex_2.x
                    yf = element.vertex_2.y
                    base = ((xf - xi) ** 2 + (yf - yi) ** 2) ** 0.5
                    self.fy_symbolic = self.fy
                    self.fy += f"+{((q_loads[0][0] + q_loads[1][0]) * base) / 2}"
                    self.fy_symbolic += f"+{((((-q_loads[0][0] - -q_loads[1][0]) / (6 * base)) * x ** 2) * 3 - ((-q_loads[0][0] / 2) * x) * 2)}"
                    self.is_symbolic = True

            if abs(element.angle) != 0 and abs(element.angle) != (np.pi / 2) and \
                    abs(element.angle) != np.pi and abs(element.angle) != (3 * np.pi) / 2:

                if self.is_symbolic:
                    fy = self.fy_symbolic
                else:
                    fy = self.fy

                signals = get_signal_vectors(element.axial_force, self.fx, self.fy, element, "cos")
                self.fy_angular = f'{signals[0]} ({fy if fy else "0"}) * cos({90 - (element.angle * 180 / np.pi)}' \
                                  f' * {degree}) {signals[1]} ({self.fx if self.fx else "0"})' \
                                  f' * cos({element.angle * 180 / np.pi} * {degree})'

                signals = get_signal_vectors(element.shear_force, self.fx, self.fy, element, "sin")
                self.fx_angular = f'{signals[0]} ({fy if fy else "0"}) * sin({90 - (element.angle * 180 / np.pi)}' \
                                  f' * {degree}) {signals[1]} ({self.fx if self.fx else "0"})' \
                                  f' * sin({element.angle * 180 / np.pi} * {degree})'
                self.is_angular = True

    def extend_results(self, results):
        if results[0]:
            self.fx += str(results[0])
            self.fx_angular += str(results[0])
        if results[1]:
            self.fy += str(results[1])
            self.fy_symbolic += str(results[1])
            self.fy_angular += str(results[1])


class Internal_Stresses:
    axial_force = ""
    shear_force = ""
    bending_moment = ""
    constant_list = []

    def __init__(self, moment_map):
        self._moment_map = moment_map

    def define_normal_shear_axes(self, element: Element, strings):
        if abs(element.angle) == 3*np.pi/2 or abs(element.angle) == np.pi/2:
            self.axial_force = strings[1]
            self.shear_force = strings[0]
        else:
            self.axial_force = strings[0]
            self.shear_force = strings[1]

    def get_moment(self, node, previous_data):
        self.bending_moment = ""
        integration_constant = [["", "", None], ""]
        self.constant_list = []
        moment = self._moment_map.get(node)
        if self.shear_force:
            copy = str(self.shear_force)
            copy = re.sub(r"(\d+\.\d+) \* degree", r"rad(\1)", copy)
            self.bending_moment += f"{integrate(sympify(copy).evalf(), Symbol('x'))}"
        for data in previous_data:
            if data[0]:
                x = Symbol('x')
                integration_constant[0][0] = f"+{data[1]}"
                integration_constant[0][1] = str(sympify(integration_constant[0][0]).subs(x, data[0].l))
                integration_constant[0][2] = data[0]
                self.bending_moment += "+" + integration_constant[0][1]
                self.constant_list.append(integration_constant)
                integration_constant = [["", "", None], ""]
        if moment:
            integration_constant[1] = f"+{moment}"
            self.bending_moment += "+" + integration_constant[1]
            if self.constant_list:
                self.constant_list[-1][1] = integration_constant[1]
            else:
                self.constant_list.append([["", "", None], integration_constant[1]])

    def get_internal_results(self, node, element, strings, previous_data):
        self.define_normal_shear_axes(element, strings)
        self.get_moment(node, previous_data)
        return [self.axial_force, self.shear_force, self.bending_moment, self.constant_list]


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


class Assembler:
    def __init__(self,
                 system: SystemElements
                 ):

        self.ss: SystemElements = system
        self.graph: Graph = Graph()
        self.solved_dict: dict = {e_id: False for e_id in self.ss.node_map}
        self.tip_node_ids: List[int] = []
        self.main_path_list: List[int] = []
        self.other_paths_list: List[List[int]] = []
        self.solve_order: List[int] = []
        self.plot_order = []
        self.sections_strings = {}
        self.internal_stresses_dict = {}

    @property
    def internal_results(self):
        return self.internal_stresses_dict

    def assemble_graph(self) -> None:
        connected_elements = assemble_element_connections(self.ss)
        for node in connected_elements:
            self.graph.add(node[0], node[1])

    def find_tips(self) -> None:
        for element_node in self.ss.node_element_map.items():
            if len(element_node[1]) == 1:
                self.tip_node_ids.append(element_node[0])

    def get_branch(self,
                   node1: int,
                   node2: int
                   ) -> Union[List[int], None]:
        for nodes in self.other_paths_list:
            if node1 in nodes and node2 in nodes:
                return nodes[:-1]
        return None

    def is_solved(self,
                  branch: List[int]
                  ) -> bool:
        for node in branch:
            if self.solved_dict[node]:
                continue
            else:
                return False
        return True

    def all_branches_solved(self,
                            node: int
                            ) -> bool:
        elements = self.ss.node_element_map.get(node)
        solved_branches_count = 0
        for element in elements:
            if self.solved_dict[element.node_id1] or self.solved_dict[element.node_id2]:
                solved_branches_count += 1
            else:
                pass
        if solved_branches_count == len(elements) - 1:
            return True
        return False

    def assemble_main_path(self,
                           main_path: Optional[Union[Setting, Tuple[int, ...]]] = Setting.longest
                           ) -> None:
        if main_path == Setting.random:
            import random
            longest_paths = self.graph.find_longest_paths(self.tip_node_ids)
            self.main_path_list = random.choice(longest_paths)

        elif main_path == Setting.longest:
            longest_paths = self.graph.find_longest_paths(self.tip_node_ids)
            self.main_path_list = longest_paths[0]

        elif isinstance(main_path, tuple):
            proper_main_path = []
            main_path = node_to_element(main_path)
            for element in main_path:
                partial_main_path = self.graph.find_path(element[0], element[1])
                for value in partial_main_path:
                    if value == partial_main_path[0] and value in proper_main_path:
                        continue
                    if value not in proper_main_path:
                        proper_main_path.append(value)
                    else:
                        raise ValueError("No path found for given nodes")
            self.main_path_list = proper_main_path

        for node in self.main_path_list:
            self.solved_dict[node] = True

    def assemble_other_paths(self) -> None:
        target_node = self.main_path_list[-1]
        for tip in self.tip_node_ids:
            if tip in self.main_path_list:
                continue

            other_path = self.graph.find_path(tip, target_node,
                                              solved_nodes=[k for k, v in self.solved_dict.items() if v])
            for node in other_path:
                self.solved_dict[node] = True

            self.other_paths_list.append(other_path)

    def plot(self, plot_order: List[list],
             show=False,
             save_figure=False,
             plotting_start_node=None,
             element_id=0,
             target_dir="tmp") -> None:

        if plotting_start_node is None:
            plotting_start_node = plot_order[0][0]
        gen = fig_generator(self.ss, self.solve_order, plot_order, target_dir=target_dir)
        gen.draw_structure(show=show,
                           save_figure=save_figure,
                           plotting_start_node=plotting_start_node,
                           element_id=element_id)

    def assemble_solve_order(self) -> None:
        self.solved_dict = {e_id: False for e_id in self.ss.node_map}
        branch_queue = []
        current_branch = Branch_data(self.main_path_list)
        pending_node = current_branch.branch[0]
        while not all(self.solved_dict.values()):
            if self.is_solved(current_branch.branch):
                current_branch = branch_queue[-1]
                del branch_queue[-1]

            current_node = current_branch.branch[current_branch.current_node_index]
            elements = self.ss.node_element_map.get(current_node)

            self.assemble_plot_sequence(pending_node, current_node)
            pending_node = current_node

            if not is_branching(elements) or (is_branching(elements) and self.all_branches_solved(current_node)):
                current_branch.current_node_index += 1
                self.solve_order.append(current_node)
                self.solved_dict[current_node] = True

            else:
                for element in elements:
                    if not is_in_path(element, self.main_path_list) and not self.solved_dict[current_node]:
                        new_branch = self.get_branch(element.node_id1, element.node_id2)
                        if current_branch.branch == new_branch or self.is_solved(new_branch):
                            continue
                        branch_queue.append(current_branch)
                        current_branch = Branch_data(new_branch)
                        break

    def assemble_plot_sequence(self, pending_node, current_node) -> None:
        if self.graph.is_connected(pending_node, current_node) \
                and [current_node, pending_node] not in self.plot_order:
            self.plot_order.append([pending_node, current_node])

    def plot_solve_order(self, show=False, save_figure=True, target_dir="tmp") -> None:
        self.solved_dict: dict = {e_id: False for e_id in self.ss.node_map}
        current_stack = None
        stacks = [self.plot_order[0][:]]
        self.plot([stacks[0]], show=show, save_figure=save_figure,
                  element_id=find_element(self.plot_order[0], self.ss.node_element_map).id, target_dir=target_dir)
        for node1, node2 in self.plot_order[1:]:
            plotted = False
            element = find_element([node1, node2], self.ss.node_element_map)

            if [node1, node2] == self.plot_order[-1]:
                self.plot(self.plot_order, show=show, save_figure=save_figure,
                          plotting_start_node=self.plot_order[-1][-1], element_id=element.id, target_dir=target_dir)
                break

            if node1 in self.tip_node_ids or node2 in self.tip_node_ids:
                current_stack = [node1, node2]
                self.plot(node_pair_to_element(current_stack), show=show, save_figure=save_figure,
                          element_id=element.id, target_dir=target_dir)
                plotted = True

            if are_stacks_connected(node1, node2, stacks):
                stacks[-1].extend([node1, node2])
                current_stack = stacks[-1]
                if not plotted:
                    self.plot(node_pair_to_element(current_stack), show=show, save_figure=save_figure,
                              plotting_start_node=current_stack[-1], element_id=element.id, target_dir=target_dir)

                if self.is_solved(current_stack):
                    del stacks[-1]
                    stacks[-1].extend(current_stack)
                    current_stack = stacks[-1]

            else:
                stacks.append(current_stack)

            self.solved_dict[node1] = True
            self.solved_dict[node2] = True

    def assemble_solve_strings(self) -> None:
        Stresses_Stack.system(self.ss)
        stacks = []
        element = find_element([self.solve_order[0], self.solve_order[1]], self.ss.node_element_map)
        current_stack = Stresses_Stack(self.solve_order[0], element)
        for node, element_nodes in zip(self.solve_order[1:-1], self.plot_order[1:]):
            self.sections_strings[element] = current_stack.axes_forces
            element = find_element(element_nodes, self.ss.node_element_map)

            if node in self.tip_node_ids:
                stacks.append(current_stack)
                current_stack = Stresses_Stack(node, element)

            elif is_branching(self.ss.node_element_map.get(node)):
                stacks.append(current_stack)
                current_stack = Stresses_Stack(node, element)
                for stack in stacks:
                    current_stack.extend_results(stack.axes_forces)
                stacks.clear()

            else:
                current_stack.determine_internal_forces(node, element)

        self.sections_strings[self.ss.node_element_map.get(self.solve_order[-1])[0]] = current_stack.axes_forces

        for key in self.sections_strings.keys():
            for index in range(len(self.sections_strings[key])):
                if self.sections_strings[key][index] == "":
                    self.sections_strings[key][index] = "0"

    def sort_shear_axial(self) -> None:
        inst = Internal_Stresses(self.ss.loads_moment)
        previous_data = []
        data_queue = {}
        for node, (element, string) in zip(self.solve_order, self.sections_strings.items()):

            if previous_data:
                if not self.graph.is_connected(previous_data[0][0], node):
                    data_queue.update({previous_data[0][1].id: previous_data[0]})
                    previous_data = []

            if is_branching(self.ss.node_element_map.get(node)):
                connected_elements = self.get_connected_elements(node)
                for el in connected_elements:
                    queued_element = data_queue.get(el.id)
                    if queued_element not in previous_data and queued_element is not None:
                        previous_data.append(queued_element)
                    if queued_element is not None:
                        del data_queue[el.id]

            self.internal_stresses_dict[element] = inst.get_internal_results(node, element, string,
                                                                             [data[1:] for data in previous_data])
            previous_data.clear()
            previous_data.append([node, element, self.internal_stresses_dict[element][2]])

    def get_connected_elements(self, node):
        elements = self.ss.node_element_map.get(node)
        return [element for element in elements]

    def assemble_structure(self,
                           main_path: Optional[Union[Setting, Tuple[int, ...]]] = Setting.longest,
                           target_dir: Optional[str] = "tmp"
                           ) -> None:
        self.find_tips()
        self.assemble_graph()
        self.assemble_main_path(main_path)
        self.assemble_other_paths()
        self.assemble_solve_order()
        self.plot_solve_order(target_dir=target_dir)
        self.assemble_solve_strings()
        self.sort_shear_axial()

        # print(f"main path: {self.main_path_list}, other paths: {self.other_paths_list}")
        # print(f"solve order: {self.solve_order}")


class Graph(object):
    """ Graph data structure, undirected by default. """
    """inspired on code by mVChr available on 
    https://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python"""
    """inspired on code by jedwards available on 
    https://stackoverflow.com/questions/29320556/finding-longest-path-in-a-graph"""

    def __init__(self,
                 directed: Optional[bool] = False
                 ):
        self._graph = defaultdict(set)
        self._directed = directed

    def is_connected(self, node1, node2):
        """ Is node1 directly connected to node2 """

        return node1 in self._graph and node2 in self._graph[node1]

    def add(self,
            node1: int,
            node2: int
            ) -> None:
        """ Add connection between node1 and node2 """

        self._graph[node1].add(node2)
        if not self._directed:
            self._graph[node2].add(node1)

    def find_path(self,
                  node1: int,
                  node2: int,
                  path: Optional[list] = None,
                  solved_nodes: Optional[list] = None
                  ) -> Union[List[int], None]:
        """ Find any path between node1 and node2 (may not be shortest) """

        if solved_nodes is None:
            solved_nodes = []
        if path is None:
            path = []

        path = path + [node1]
        if node1 == node2 or node1 in solved_nodes:
            return path
        if node1 not in self._graph:
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_path(node, node2, path, solved_nodes)
                if new_path:
                    return new_path
        return None

    def find_all_paths(self,
                       node: int,
                       seen: Optional[list] = None,
                       path: Optional[list] = None
                       ) -> List[Tuple[int, ...]]:
        """
        finds all possible paths in graph
        """
        if seen is None:
            seen = []
        if path is None:
            path = [node]

        seen.append(node)

        paths = []
        for t in self._graph[node]:
            if t not in seen:
                t_path = path + [t]
                paths.append(tuple(t_path))
                paths.extend(self.find_all_paths(t, seen[:], t_path))
        return paths

    def find_longest_paths(self, tip_node_ids: Optional[List[int]] = None) -> List[Tuple[int, ...]]:
        """find longest paths in the graph, pass tip nodes for optimal search"""
        if tip_node_ids:
            all_paths = [p for ps in [self.find_all_paths(n) for n in tip_node_ids] for p in ps]
        else:
            all_paths = [p for ps in [self.find_all_paths(n) for n in set(self._graph)] for p in ps]
        max_len = max(len(p) for p in all_paths)
        longest_paths = [p for p in all_paths if len(p) == max_len]

        return longest_paths


def test_struct1():
    ss = SystemElements()
    ss.add_element([[-2, 2], [-1, 0]])
    ss.add_element([[-2, 3], [-2, 2]])
    ss.add_element([[-1, 4], [-2, 3]])
    # ss.add_element([[-1, 4], [0, 5]])
    # ss.add_element([[0, 5], [1, 5]])
    # ss.add_element([[1, 5], [2, 5]])
    # ss.add_element([[2, 5], [3, 5]])
    # ss.add_element([[3, 5], [5, 2]])
    ss.add_element([[-3, 4], [-2, 3]])
    ss.add_element([[-4, 4], [-3, 4]])
    ss.add_element([[-3, 5], [-3, 4]])
    ss.add_element([[-2, 0], [-1, 0]])
    ss.add_element([[-2, 1], [-2, 0]])
    ss.add_element([[-2, -1], [-2, 0]])
    ss.add_element([[-3, 0], [-2, 0]])
    ss.add_element([[-4, 1], [-3, 0]])
    ss.add_element([[-5, 2], [-4, 1]])
    ss.add_element([[-4, -1], [-3, 0]])
    ss.add_element([[-5, -2], [-4, -1]])
    ss.add_element([[-1, 0], [0, 0]])
    ss.add_element([[0, 0], [1, 0]])
    ss.add_element([[2, 0], [3, 0]])
    ss.add_element([[1, 0], [2, 0]])
    ss.add_element([[2, 0], [3, 1]])
    ss.point_load(10, 5)
    ss.moment_load(1, 15)
    # ss.add_element([[3, 1], [4, 1]])
    # ss.add_element([[3, 1], [3, 2]])
    # ss.add_element([[4, 1], [5, 2]])
    # ss.add_element([[4, 1], [6, 2]])
    ss.add_element([[1, 0], [-1, 1]])
    ss.show_structure()
    ass = Assembler(ss)
    ass.assemble_structure(main_path=(15, 20))
    # ass.assemble_structure(main_path=(7, 13))
    # ass.plot_solve_order(ass.plot_order, show=True, save_figure=False, plotting_start_node=15)
    [[print(f"section {index + 1}-{sub_index + 1}: {sympify(sub_string, evaluate=False)}") for sub_index, sub_string in
      enumerate(string)] for index, string in enumerate(ass.sections_strings)]


def test_struct2():
    ss = SystemElements()
    ss.add_element([[0, 0], [1, 0]])
    ss.add_element([[1, 0], [1, 1]])
    ss.add_element([[1, 0], [2, 0]])
    ss.add_element([[2, 0], [3, 0]])
    ss.add_element([[3, 0], [4, 1]])
    ss.add_element([[4, 1], [5, 1]])
    ss.point_load(2, Fy=10)
    ss.point_load(3, Fy=-20)
    ss.point_load(4, Fy=-30)
    ss.point_load(5, Fx=-40)
    ss.moment_load(2, Ty=-9)
    ss.moment_load(1, 7)
    ss.moment_load(3, 3)
    ss.q_load(element_id=3, q=(-10, -20))
    ss.add_support_roll(4)
    ss.add_support_hinged(5)
    # ss.show_structure()
    ss.solve()
    ss.show_reaction_force(show=False)
    ass = Assembler(ss)
    ass.assemble_structure(main_path=Setting.longest)
    # [[print(f"section {element.id}-{sub_index + 1}: {sympify(sub_string, evaluate=False)}") for sub_index, sub_string in
    #   enumerate(string)] for element, string in ass.sections_strings.items()]
    # [print(element.id, values) for element, values in ass.sections_strings.items()]
    [print(element.id, values) for element, values in ass.internal_stresses_dict.items()]


if __name__ == "__main__":
    test_struct2()
