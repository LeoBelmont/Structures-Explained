import math

from anastruct import SystemElements
from matplotlib import pyplot as plt
from StructuresExplained.utils.util import get_relative_element_by_coordinates, get_arrow_patch_values
from typing import (
    Union,
    List,
    Dict,
)


def plot_arrow(subplot, reaction_force, vector_data):
    h = vector_data[0]
    scale = vector_data[1]
    x = vector_data[2][0]
    y = vector_data[2][1]
    len_x = vector_data[2][2]
    len_y = vector_data[2][3]

    subplot.arrow(
        x,
        y,
        len_x,
        len_y,
        head_width=h * 0.15,
        head_length=0.2 * scale,
        ec="b",
        fc="orange",
        zorder=11,
        # head_start_at_zero=head_start_at_zero,
    )

    subplot.text(
        x,
        y,
        f"F={round(abs(reaction_force), 2)}",
        color="k",
        fontsize=9,
        zorder=10,
    )


def plot_moment(subplot, node, reaction_force, vector_data):
    h = vector_data[0]
    if reaction_force > 0:
        subplot.plot(
            node.vertex.x,
            -node.vertex.z,
            marker=r"$\circlearrowleft$",
            ms=25,
            color="orange",
        )
    if reaction_force < 0:
        subplot.plot(
            node.vertex.x,
            -node.vertex.z,
            marker=r"$\circlearrowright$",
            ms=25,
            color="orange",
        )

    subplot.text(
        node.vertex.x + h * 0.2,
        -node.vertex.z + h * 0.2,
        f"R= {round(abs(reaction_force), 2)}",
        color="k",
        fontsize=9,
        zorder=10,
    )


class fig_generator:
    fig_counter = 0

    def __init__(self, system_elements, node_order=None, assemble_order=None, target_dir="tmp"):
        self.ss = system_elements
        self.branch_ss = SystemElements()
        self.assemble_order = assemble_order
        self.node_order = node_order
        self.target_dir = target_dir

    def draw_structure(self, show=False, save_figure=True, plotting_start_node=0, element_id=0):
        plot_iterations = False
        node_index = 0
        figure = plt.figure(figsize=(12, 8))
        subplot = figure.add_subplot(111)
        plt.tight_layout()

        for branch in self.assemble_order:
            self.draw_element(branch)
            first_node = next(i for i in self.node_order if i == branch[0] or i == branch[1])

            for roll in self.ss.supports_roll:
                if roll.id == first_node:
                    self.draw_support(first_node, subplot)

            for hinged in self.ss.supports_hinged:
                if hinged.id == first_node:
                    self.draw_support(first_node, subplot)

            for fixed in self.ss.supports_fixed:
                if fixed.id == first_node:
                    self.draw_support(first_node, subplot)

            if self.ss.loads_point.get(first_node):
                self.draw_point_load(first_node)

            if self.ss.loads_moment.get(first_node):
                self.draw_moment(first_node)

            elements_node1 = self.ss.node_element_map.get(branch[0])
            elements_node2 = self.ss.node_element_map.get(branch[1])
            for element in elements_node1:
                if element in elements_node2:
                    q_load = self.ss.loads_q.get(element.id)
                    if q_load:
                        if branch == self.assemble_order[-1]:
                            self.draw_q_load(get_relative_element_by_coordinates(self.ss, self.branch_ss, element.id),
                                             q_load)
                        else:
                            xi = element.vertex_1.x
                            yi = element.vertex_1.y
                            xf = element.vertex_2.x
                            yf = element.vertex_2.y
                            x_average = (xi + xf) / 2
                            y_average = (yi + yf) / 2
                            base = ((xf - xi) ** 2 + (yf - yi) ** 2) ** 0.5
                            load = ((-q_load[0][0] + -q_load[1][0]) * base) / 2
                            Fz = load * math.cos(element.angle)
                            Fx = load * math.cos(element.angle-(90 * math.pi / 180))
                            h = 0.2 * self.ss.plotter.max_val_structure
                            x, y, len_x, len_y, point_load = get_arrow_patch_values(Fx, Fz,
                                                                                    (x_average, y_average), h)
                            plot_arrow(subplot, point_load, [h, h, [x, y, len_x, len_y]])
                            # needs further testing
                    break

            node_index += 1
            if plotting_start_node in branch:
                plot_iterations = True
            if show and plot_iterations:
                self.branch_ss.show_structure(show=False, subplot=(figure, subplot))
                figure.show()
            if save_figure and plot_iterations:
                fig = self.branch_ss.show_structure(show=False, subplot=(figure, subplot))
                fig.savefig(fr'{self.target_dir}\figs\structure{element_id}')

    def generate_figures_for_pdf(self):
        fig = self.ss.show_structure(show=False)
        fig.savefig(fr'{self.target_dir}\figs\structure')
        fig = self.ss.show_structure(show=False, free_body_diagram=3)
        fig.savefig(fr'{self.target_dir}\figs\diagram1')
        fig = self.ss.show_structure(show=False, free_body_diagram=2)
        fig.savefig(fr'{self.target_dir}\figs\diagram2')
        fig = self.ss.show_reaction_force(show=False)
        fig.savefig(fr'{self.target_dir}\figs\supports')
        fig = self.ss.show_axial_force(show=False)
        fig.savefig(fr'{self.target_dir}\figs\axial')
        fig = self.ss.show_shear_force(show=False)
        fig.savefig(fr'{self.target_dir}\figs\shear')
        fig = self.ss.show_bending_moment(show=False)
        fig.savefig(fr'{self.target_dir}\figs\moment')

    def draw_support(self, node_id, subplot, roll_direction=None):
        support_node = self.ss.reaction_forces.get(node_id)
        if round(support_node.Fx, 2):
            plot_arrow(subplot, support_node.Fx, self.ss.reaction_vectors_data.get(f"{node_id}Fx"))
        if round(support_node.Fz, 2):
            plot_arrow(subplot, support_node.Fz, self.ss.reaction_vectors_data.get(f"{node_id}Fz"))
        if round(support_node.Ty, 2):
            plot_moment(subplot, self.ss.node_map.get(node_id), support_node.Ty,
                        self.ss.reaction_vectors_data.get(f"{node_id}Ty"))

    def draw_element(self, branch):
        self.add_element_to_plot(branch)

    def add_element_to_plot(self, element):
        for node in range(len(element) - 1):
            self.branch_ss.add_element([
                [
                    self.ss.node_map.get(element[node]).vertex.x,
                    self.ss.node_map.get(element[node]).vertex.y
                ],
                [
                    self.ss.node_map.get(element[node + 1]).vertex.x,
                    self.ss.node_map.get(element[node + 1]).vertex.y
                ]
            ])

    def draw_point_load(self, node_id):
        point_load = self.ss.loads_point[node_id]
        self.branch_ss.point_load(
            node_id=self.get_relative_node_by_coordinates(node_id),
            Fx=point_load[0],
            Fy=-point_load[1]
        )

    def draw_q_load(self, element_id, q_load):
        self.branch_ss.q_load(
            element_id=element_id,
            q=(
                q_load[0][0],
                q_load[1][0]
            )
        )

    def draw_moment(self, node_id):
        moment_load = self.ss.loads_moment.get(node_id)
        self.branch_ss.moment_load(
            node_id=self.get_relative_node_by_coordinates(node_id),
            Ty=moment_load
        )

    def get_relative_node_by_coordinates(self, node_id):
        coords = (self.ss.node_map.get(node_id).vertex.x, self.ss.node_map.get(node_id).vertex.y)
        for node_key in self.branch_ss.node_map:
            node = self.branch_ss.node_map.get(node_key)
            if coords[0] == node.vertex.x and coords[1] == node.vertex.y:
                return node.id
        return None
