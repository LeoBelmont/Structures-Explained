from collections import defaultdict
from typing import Optional, Union, List, Tuple


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
