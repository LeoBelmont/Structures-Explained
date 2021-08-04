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

        self.rectangle_count: int = 0
        self.semicircle_count: int = 0

        self.normal_stress_latex: list = []
        self.normal_stress_numeric: list = []

        self.normal_line_numeric: list = []
        self.normal_line_latex: list = []

        self.shear_stress_numeric: list = []
        self.shear_stress_latex: list = []

        self.shear_flux_numeric: list = []
        self.shear_flux_latex: list = []

        self.points_values: list = []
        self.points_values_shear_flux: list = []
        self.points_values_shear_stress: list = []

        self.static_moment_for_shear_numeric: list = []
        self.static_moment_for_shear_latex: list = []
        self.static_moment_for_shear_string: str = ''

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
        # calculates normal stress and appends the step by step solution to the PDF if append_to_pdf is True

        normal_stress, normal_stress_latex, neutral_line, neutral_line_latex, moment_y, moment_x = \
            self.calc.det_normal_stress(normal_force, y, z)

        if append_to_pdf:
            self.append_normal_stress(normal_stress, normal_stress_latex, normal_force, moment_y, moment_x, y, z,
                                      neutral_line, neutral_line_latex)

        if print_results:
            print(round_expr(parse_expr(normal_stress), 2), neutral_line)
        else:
            return normal_stress, neutral_line

    def calculate_shear_flux(self, shear_force, cut_height, append_to_pdf=False):
        self.calc.calculate_static_moment_for_shear(cut_height)

        shear_flux, shear_flux_latex = self.calc.det_shear_flux(shear_force)

        self.append_shear_stress(shear_flux, shear_flux_latex, shear_force, self.calc.static_moment_for_shear,
                                 self.calc.moment_inertia_x)

    def calculate_shear_stress(self, shear_force, thickness, cut_height, append_to_pdf=False):
        # calculates shear stress and appends the step by step solution to the PDF if append_to_pdf is True

        self.calc.calculate_static_moment_for_shear(cut_height)

        shear_stress, shear_stress_latex = self.calc.det_shear_stress(shear_force, thickness)

        if append_to_pdf:
            self.append_shear_stress(shear_force, self.calc.static_moment_for_shear, self.calc.moment_inertia_x,
                                     shear_stress, shear_stress_latex, thickness)

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
            # condition to prevent duplicates
            self.normal_stress_numeric.append(normal_stress)
            self.normal_stress_latex.append(normal_stress_latex)
            self.points_values.append([normal_force, moment_y, moment_x, y, z])
            self.normal_line_numeric.append(neutral_line_numeric)
            self.normal_line_latex.append(neutral_line_latex)

    def append_shear_flux(self,
                          shear_flux_numeric,
                          shear_flux_latex,
                          shear_force,
                          static_moment,
                          moment_inertia_x
                          ):

        if shear_force not in self.shear_flux_numeric:
            # condition to prevent duplicates
            self.shear_flux_numeric.append(shear_flux_numeric)
            self.shear_flux_latex.append(shear_flux_latex)
            self.points_values_shear_flux.append([shear_force, static_moment, moment_inertia_x])
            self.static_moment_for_shear_numeric.append(self.calc.static_moment_for_shear)
            self.static_moment_for_shear_latex.append(self.static_moment_for_shear_string)

    def append_shear_stress(self,
                            shear_stress_numeric,
                            shear_stress_latex,
                            shear_stress,
                            shear_force,
                            static_moment,
                            moment_inertia_x
                            ):

        if shear_stress not in shear_stress_numeric:
            # condition to prevent duplicates
            self.shear_stress_numeric.append(shear_stress_numeric)
            self.shear_stress_latex.append(shear_stress_latex)
            self.points_values_shear_stress.append([shear_force, static_moment, moment_inertia_x, shear_stress])
            self.static_moment_for_shear_numeric.append(self.calc.static_moment_for_shear)
            self.static_moment_for_shear_latex.append(self.static_moment_for_shear_string)

    def generate_pdf(self, language):
        # creates a folder to generate the figure and logo into
        make_temp_folder()

        self.pdfgen = pdf_generator(self, self.calc)
        figure = self.show_cross_section()

        save_figure(figure, "tmp\\figs\\sectransv")
        generate_logo()

        self.pdfgen.generate_pdf(language)

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
        self.static_moment_for_shear_numeric.clear()
        self.static_moment_for_shear_latex.clear()


if __name__ == "__main__":
    test = manager()
    test.add_rectangular_subarea(upper_left=(0, 10), down_right=(5, 0))
    test.add_rectangular_subarea(upper_left=(5, 10), down_right=(10, 0))
    #test.add_semicircular_subarea(center=(10, 5), radius=5, angle=90)
    test.get_geometrical_properties(print_results=False)
    test.calculate_normal_stress(normal_force=10, y="1", print_results=False, append_to_pdf=True) # default for y and z are Symbols
    test.calculate_shear_stress(shear_force=10, thickness=10, cut_height=5, append_to_pdf=True)
    #test.show_cross_section(show=True)
    test.generate_pdf("PT")
