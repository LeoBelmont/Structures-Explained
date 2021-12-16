import re
from enum import Enum
from typing import List, Union, Optional, Tuple

import numpy as np
from anastruct import SystemElements
from anastruct.fem.elements import Element
from sympy import integrate, sympify, Symbol

from StructuresExplained.solutions.structure.fig_generation.artist import Artist
from StructuresExplained.solutions.structure.internal_stresses.graph import Graph
from StructuresExplained.solutions.structure.internal_stresses.stack import Stresses_Stack
from StructuresExplained.solutions.structure.internal_stresses.tools import assemble_element_connections, \
    node_to_element, is_branching, is_in_path, find_element, node_pair_to_element, are_stacks_connected


class Setting(Enum):
    random = "random"
    longest = "longest"


class Branch_data:
    def __init__(self, branch: List[int]):
        self.current_node_index = 0
        self.branch = branch


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
                if partial_main_path is None:
                    raise ValueError("No path found for given nodes")
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
        gen = Artist(self.ss, self.solve_order, plot_order, target_dir=target_dir)
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
        if main_path == "longest" or main_path == "random":
            main_path = Setting(main_path)
        self.assemble_main_path(main_path)
        self.assemble_other_paths()
        self.assemble_solve_order()
        self.plot_solve_order(target_dir=target_dir)
        self.assemble_solve_strings()
        self.sort_shear_axial()

        # print(f"main path: {self.main_path_list}, other paths: {self.other_paths_list}")
        # print(f"solve order: {self.solve_order}")
