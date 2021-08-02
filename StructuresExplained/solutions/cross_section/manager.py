from sympy.parsing.sympy_parser import parse_expr
from sympy import Symbol
from StructuresExplained.solutions.cross_section.calculator import calculator
from StructuresExplained.solutions.cross_section.fig_generation import fig_generator
from StructuresExplained.solutions.cross_section.pdf_generation import pdf_generator
from StructuresExplained.utils.util import round_expr, save_figure, make_temp_folder
from StructuresExplained.pdfconfig.logo import generate_logo


from typing import (
    Tuple,
    Union,
    List,
    Optional,
    Dict,
    Set,
    TYPE_CHECKING,
    Sequence,
    cast,
    Collection,
    Any,
)


class manager:

    def __init__(self):
        self.calc = calculator()
        self.rectangle_count = 0
        self.semicircle_count = 0

        self.normal_stress_latex = []
        self.normal_stress_numeric = []

        self.normal_line_numeric = []
        self.normal_line_latex = []

        self.shear_stress_numeric = []
        self.shear_stress_latex = []

        self.shear_flux_numeric = []
        self.shear_flux_latex = []

        self.points_values = []
        self.points_values_shear_flux = []
        self.points_values_shear_stress = []

        self.static_moment_cut_numeric = []
        self.static_moment_cut_latex = []
        self.static_moment_cut_string = ''

    def add_rectangular_subarea(self, upper_left: tuple, down_right: tuple):
        # upper_left: coordinate of upper left vertex of rectangle (x, y)
        # down_right: coordinate of down right vertex of rectangle (x, y)

        self.rectangle_count += 1
        self.calc.subareas_rectangle.update({self.rectangle_count: [upper_left[0], upper_left[1],
                                                                    down_right[0], down_right[1]]})

    def add_semicircular_subarea(self, center: tuple, radius: float, angle: float):
        # center: coordinate of the semicircle center (as if it were a full circle) (x, y)
        # radius: radius of the semicircle
        # angle: angle of the semicircle relative to x axis, clockwise

        self.semicircle_count += 1
        self.calc.subareas_circle.update({self.semicircle_count: [center[0], center[1], radius, angle]})

    def get_geometrical_properties(self, print_results=False):
        # calculates geometrical properties and stores them in the calculator instance calc

        self.calc.reset_results()

        self.reset_strings()

        self.calc.det_values()

        if print_results:
            self.print_geometrical_properties()

    def print_geometrical_properties(self):
        attrs = vars(self.calc)
        print('\n'.join("%s: %s" % item for item in attrs.items()))

    def show_cross_section(self, show=False, rectangle_subarea_id=None, circle_subarea_id=None):
        # you can pass a subarea ID if you want it to be highlighted in red. IDs must match the
        # ones in the subarea dict

        self.fgen = fig_generator(self.calc.subareas_rectangle,
                                  self.calc.subareas_circle,
                                  self.calc.total_cg_x,
                                  self.calc.total_cg_y,
                                  )

        fig = self.fgen.plot(rectangle_subarea_id, circle_subarea_id)

        if show:
            fig.show()
        else:
            return fig

    def calculate_normal_stress(
            self, normal_force, y=Symbol('y'), z=Symbol('z'), append_to_pdf=False, print_results=False):

        normal_stress, normal_stress_latex, neutral_line, neutral_line_latex, moment_y, moment_x = \
            self.calc.det_normal_stress(normal_force, y, z)

        if append_to_pdf:
            self.append_normal_stress(normal_stress, normal_stress_latex, normal_force, moment_y, moment_x, y, z,
                                      neutral_line, neutral_line_latex)

        if print_results:
            print(round_expr(parse_expr(normal_stress), 2), neutral_line)
        else:
            return normal_stress, neutral_line

    def calculate_shear_stress(self, shear_force, static_moment, thickness, moment_inertia_x, append_to_pdf=False):

        shear_flux, shear_stress, shear_flux_latex, shear_stress_latex = self.calc.det_shear_stress(
            shear_force, static_moment, thickness, moment_inertia_x)

        if float(thickness) != 0:
            if append_to_pdf:
                self.append_shear_stress(shear_flux, shear_flux_latex, shear_force, static_moment,
                                         moment_inertia_x, shear_stress, shear_stress_latex, thickness)

        else:
            if append_to_pdf:
                self.append_shear_stress(shear_flux, shear_flux_latex, shear_force, static_moment,
                                         moment_inertia_x)

    def append_normal_stress(self,
                             normal_stress,
                             normal_stress_latex,
                             normal_force,
                             moment_y,
                             moment_x,
                             y,
                             z,
                             neutral_line_numeric,
                             neutral_line_latex
                             ):

        if normal_stress not in self.normal_stress_numeric:
            self.normal_stress_numeric.append(normal_stress)
            self.normal_stress_latex.append(normal_stress_latex)
            self.points_values.append([normal_force, moment_y, moment_x, y, z])
            self.normal_line_numeric.append(neutral_line_numeric)
            self.normal_line_latex.append(neutral_line_latex)

    def append_shear_stress(self,
                            shear_flux_numeric,
                            shear_flux_latex,
                            shear_force,
                            static_moment,
                            moment_inertia_x,
                            normal_stress_numeric=None,
                            normal_stress_latex=None,
                            normal_stress=None
                            ):

        self.shear_flux_numeric.append(shear_flux_numeric)
        self.shear_flux_latex.append(shear_flux_latex)
        self.points_values_shear_flux.append([shear_force, static_moment, moment_inertia_x])
        self.static_moment_cut_numeric.append(self.static_moment_cut)
        self.static_moment_cut_latex.append(self.static_moment_cut_string)

        if normal_stress_numeric is not None:
            self.points_values_shear_stress.append([shear_force, static_moment, moment_inertia_x, normal_stress])
            self.shear_stress_numeric.append(normal_stress_numeric)
            self.shear_stress_latex.append(normal_stress_latex)

    def generate_pdf(self, language):
        make_temp_folder()
        self.pdfgen = pdf_generator(self, self.calc)
        figure = self.show_cross_section()
        save_figure(figure, "tmp\\figs\\sectransv")
        generate_logo()
        self.pdfgen.solver(language)

    def reset_strings(self):
        self.normal_stress_latex.clear()
        self.normal_stress_numeric.clear()
        self.points_values.clear()
        self.normal_line_numeric.clear()
        self.normal_line_latex.clear()
        self.shear_stress_numeric.clear()
        self.shear_stress_latex.clear()
        self.shear_flux_numeric.clear()
        self.shear_flux_latex.clear()
        self.points_values_shear_flux.clear()
        self.points_values_shear_stress.clear()
        self.static_moment_cut_numeric.clear()
        self.static_moment_cut_latex.clear()


if __name__ == "__main__":
    test = manager()
    test.add_rectangular_subarea((0, 10), (5, 0))
    test.add_rectangular_subarea((5, 10), (10, 0))
    test.add_semicircular_subarea((10, 5), 5, 90)
    test.get_geometrical_properties(print_results=True)
    test.calculate_normal_stress(10, print_results=True)
    test.show_cross_section(show=True, rectangle_subarea_id=None)
    test.generate_pdf("PT")
