from matplotlib import pyplot as plt
from anastruct import SystemElements

from typing import (
    Union,
    List,
    Dict,
)


class fig_generator:
    def __init__(self):
        self.ss = SystemElements()
        self.hinged: Union[List, None] = None
        self.roll: Union[List, None] = None
        self.fixed: Union[List, None] = None
        self.roll_direction: Union[float, None] = None
        self.moment = None
        self.point = None
        self.q_load = None
        self.node_map: Union[Dict, None] = None
        self.element_counter: int = 1

    def draw_structure(self):

        for self.element_counter in range(1, len(self.node_map) + 1):
            if self.node_map.get(self.element_counter + 1):
                if self.element_counter != len(self.node_map) + 1:
                    self.draw_element()

            if self.roll:
                if self.roll[0].id == self.element_counter:
                    self.draw_roll_support()

            if self.hinged:
                if self.hinged[0].id == self.element_counter:
                    self.draw_hinged_support()

            if self.fixed:
                if self.fixed[0].id == self.element_counter:
                    self.draw_fixed_support()

            if self.element_counter in self.point.keys():
                self.draw_point_load()

            if self.element_counter in self.q_load.keys():
                self.draw_q_load()

            if self.element_counter in self.moment.keys():
                self.draw_moment()

            fig = self.ss.show_structure(show=False)
            fig.savefig(f'tmp\\figs\\structure{self.element_counter}')

    def draw_roll_support(self, roll_direction=None):
        self.ss.point_load(
            node_id=self.roll[0].id,
            Fx=-self.roll[0].Fx,
            Fy=-self.roll[0].Fy
        )

    def draw_hinged_support(self):
        self.ss.point_load(
            node_id=self.hinged[0].id,
            Fx=-self.hinged[0].Fx,
            Fy=-self.hinged[0].Fy
        )

    def draw_fixed_support(self):
        self.ss.point_load(
            node_id=self.fixed[0].id,
            Fx=-self.fixed[0].Fx,
            Fy=-self.fixed[0].Fy
        )

        self.ss.moment_load(
            node_id=self.fixed[0].id,
            Ty=self.fixed[0].Ty
        )

    def draw_element(self):
        self.ss.add_element([
            [
                self.node_map.get(self.element_counter).x,
                self.node_map.get(self.element_counter).y
            ],
            [
                self.node_map.get(self.element_counter + 1).x,
                self.node_map.get(self.element_counter + 1).y
            ]
        ])

    def draw_point_load(self):
        id_ = self.node_map.get(self.element_counter).id
        self.ss.point_load(
            node_id=id_,
            Fx=self.point[id_][0],
            Fy=-self.point[id_][1]
        )

    def draw_q_load(self):
        self.ss.q_load(
            element_id=self.node_map.get(self.element_counter).id,
            q=(
                -self.q_load.get(self.element_counter).qi,
                -self.q_load.get(self.element_counter).q
            )
        )

    def draw_moment(self):
        self.ss.moment_load(
            node_id=self.node_map.get(self.element_counter).id,
            Ty=self.moment.get(self.element_counter)
        )
