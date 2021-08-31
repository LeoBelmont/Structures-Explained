from anastruct import SystemElements
from anastruct.fem.elements import Element
from collections import defaultdict
from typing import Optional, Union, List, Tuple


class branch:
    def __init__(self, element_group: list, junction_node_id: int, main_path=False):
        self.solved = False
        self.origin_node_id = None
        self.final_node_id = None
        self.results = ''
        self.element_group = element_group
        self.junction_node_id = junction_node_id
        self.main_path = main_path


def get_connect_elements() -> List[Tuple[int, int]]:
    connections = []
    for first_node, elements in ss.node_element_map.items():
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


class assembler:
    def __init__(self,
                 system: SystemElements
                 ):
        self.ss: SystemElements = system
        self.graph: Graph = Graph()
        self.solved_dict: dict = {e_id: False for e_id in self.ss.node_map}
        self.tip_node_ids: list = []
        self.main_path_list: list = []
        self.other_paths_list: list = []
        self.solve_order = []

    def assemble_graph(self) -> None:
        connected_elements = get_connect_elements()
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
                           random_longest_path: Optional[bool] = True
                           ) -> None:
        longest_paths = self.graph.find_longest_paths(self.tip_node_ids)
        if random_longest_path:
            import random
            self.main_path_list = random.choice(longest_paths)
        else:
            self.main_path_list = longest_paths[0]

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

    def assemble_solve_order(self) -> None:
        self.solved_dict = {e_id: False for e_id in self.ss.node_map}
        counter = 0
        branch_queue = {}
        current_branch = self.main_path_list
        while not all(self.solved_dict.values()):
            if self.is_solved(current_branch):
                last_key = list(branch_queue.keys())[-1]
                counter, current_branch = branch_queue.get(last_key)
                del branch_queue[last_key]

            current_node = current_branch[counter]
            elements = self.ss.node_element_map.get(current_node)

            if not is_branching(elements) or (is_branching(elements) and self.all_branches_solved(current_node)):
                counter += 1
                self.solve_order.append(current_node)
                self.solved_dict[current_node] = True

            else:
                for element in elements:
                    if not is_in_path(element, self.main_path_list) and not self.solved_dict[current_node]:
                        new_branch = self.get_branch(element.node_id1, element.node_id2)
                        if current_branch == new_branch or self.is_solved(new_branch):
                            continue
                        branch_queue[len(branch_queue)] = counter, current_branch
                        counter = 0
                        current_branch = new_branch
                        break

    def assemble_structure(self) -> None:
        self.find_tips()
        self.assemble_graph()
        self.assemble_main_path()
        self.assemble_other_paths()
        self.assemble_solve_order()

        print(f"main path: {self.main_path_list}, other paths: {self.other_paths_list}")
        print(f"solve order: {self.solve_order}")


class Graph(object):
    """ Graph data structure, undirected by default. """

    def __init__(self,
                 directed: Optional[bool] = False
                 ):
        self._graph = defaultdict(set)
        self._directed = directed

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


if __name__ == "__main__":
    ss = SystemElements()
    ss.add_element([[-2, 2], [-1, 0]])
    ss.add_element([[-2, 3], [-2, 2]])
    ss.add_element([[-1, 4], [-2, 3]])
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
    ss.add_element([[1, 0], [-1, 1]])
    ss.show_structure()
    ass = assembler(ss)
    ass.assemble_structure()
