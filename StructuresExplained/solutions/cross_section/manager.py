from sympy.parsing.sympy_parser import parse_expr
from sympy import Symbol
from StructuresExplained.solutions.cross_section.calculator import calculator
from StructuresExplained.solutions.cross_section.fig_generation import fig_generator
from StructuresExplained.solutions.cross_section.pdf_generation import pdf_generator
from StructuresExplained.utils.util import round_expr, save_figure, make_temp_folder
from StructuresExplained.pdfconfig.logo import generate_logo

from typing import (
    Union,
    List,
    Optional,
)


class manager:

    def __init__(self):
        self.calc = calculator()

        self.rectangle_count: int = 0
        self.semicircle_count: int = 0

        self.normal_stress_data_list: List[normal_stress_data] = []
        self.neutral_line_data_list: List[neutral_line_data] = []
        self.shear_flux_data_list: List[shear_flux_data] = []
        self.shear_stress_data_list: List[shear_stress_data] = []

        self.static_moment_for_shear_numeric: list = []
        self.static_moment_for_shear_latex: list = []
        self.static_moment_for_shear_string: str = ''

    def add_rectangular_subarea(self,
                                upper_left: tuple,
                                down_right: tuple
                                ):
        # upper_left: coordinate of upper left vertex of rectangle (x, y)
        # down_right: coordinate of down right vertex of rectangle (x, y)

        self.rectangle_count += 1
        self.calc.subareas_rectangle.update({self.rectangle_count: [upper_left[0], upper_left[1],
                                                                    down_right[0], down_right[1]]})

    def add_semicircular_subarea(self,
                                 center: tuple,
                                 radius: float,
                                 angle: float
                                 ):
        # center: coordinate of the semicircle center (as if it were a full circle) (x, y)
        # radius: radius of the semicircle
        # angle: angle of the semicircle relative to x axis, clockwise

        self.semicircle_count += 1
        self.calc.subareas_circle.update({self.semicircle_count: [center[0], center[1], radius, angle]})

    def get_geometrical_properties(self,
                                   print_results: bool = False
                                   ):
        # calculates geometrical properties and stores them in the calculator instance calc

        self.calc.reset_results()

        self.reset_strings()

        self.calc.calculate_values()

        if print_results:
            self.print_geometrical_properties()

    def print_geometrical_properties(self):
        attrs = vars(self.calc)
        print('\n'.join("%s: %s" % item for item in attrs.items()))

    def show_cross_section(self, show: Optional[bool] = False,
                           rectangle_subarea_id: Optional[int] = None,
                           circle_subarea_id: Optional[int] = None
                           ):
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

    def calculate_normal_stress(self,
                                normal_force: float,
                                y: Optional[Union[str, Symbol]] = Symbol('y'),
                                z: Optional[Union[str, Symbol]] = Symbol('z'),
                                append_to_pdf: bool = False,
                                print_results: bool = False
                                ):
        # calculates normal stress and appends the step by step solution to the PDF if append_to_pdf is True

        normal_stress, normal_stress_latex, moment_y, moment_x = self.calc.det_normal_stress(normal_force, y, z)

        if append_to_pdf:
            self.append_normal_stress(normal_stress, normal_stress_latex, normal_force, moment_y, moment_x, y, z)

        if print_results:
            print("Normal Stress = ", round_expr(parse_expr(normal_stress), 2))
        else:
            return normal_stress

    def calculate_neutral_line(self,
                               normal_force: float,
                               y: Optional[Union[str, Symbol]] = Symbol('y'),
                               z: Optional[Union[str, Symbol]] = Symbol('z'),
                               append_to_pdf: bool = False,
                               print_results: bool = False
                               ):
        # calculates neutral line and appends the step by step solution to the PDF if append_to_pdf is True

        neutral_line, neutral_line_latex, moment_y, moment_x = self.calc.det_neutral_line(normal_force, y, z)

        if append_to_pdf:
            self.append_neutral_line(neutral_line, neutral_line_latex, normal_force, moment_y, moment_x, y, z)

        if print_results:
            print(neutral_line)
        else:
            return neutral_line

    def calculate_shear_flux(self,
                             shear_force: float,
                             cut_height: float,
                             append_to_pdf: bool = False
                             ):
        self.calc.calculate_static_moment_for_shear(cut_height)

        shear_flux, shear_flux_latex = self.calc.det_shear_flux(shear_force)

        if append_to_pdf:
            self.append_shear_flux(shear_flux, shear_flux_latex, shear_force, self.calc.static_moment_for_shear,
                                   self.static_moment_for_shear_string, self.calc.moment_inertia_x)

    def calculate_shear_stress(self,
                               shear_force: float,
                               thickness: float,
                               cut_height: float,
                               append_to_pdf: Optional[bool] = False
                               ):
        # calculates shear stress and appends the step by step solution to the PDF if append_to_pdf is True

        self.calc.calculate_static_moment_for_shear(cut_height)

        shear_stress, shear_stress_latex = self.calc.det_shear_stress(shear_force, thickness)

        if append_to_pdf:
            self.append_shear_stress(shear_stress, shear_stress_latex, shear_stress, shear_force,
                                     self.calc.static_moment_for_shear, self.static_moment_for_shear_string,
                                     self.calc.moment_inertia_x, thickness)

    def append_normal_stress(self,
                             normal_stress: str,
                             normal_stress_latex: str,
                             normal_force: float,
                             moment_y: str,
                             moment_x: str,
                             y: Union[str, Symbol],
                             z: Union[str, Symbol]
                             ):

        self.normal_stress_data_list.append(
            normal_stress_data(
                normal_stress,
                normal_stress_latex,
                normal_force,
                moment_y,
                moment_x,
                y,
                z
            )
        )

    def append_neutral_line(self,
                            neutral_line_numeric: str,
                            neutral_line_latex: str,
                            normal_force: float,
                            moment_y: str,
                            moment_x: str,
                            y: Union[str, Symbol],
                            z: Union[str, Symbol]
                            ):

        self.neutral_line_data_list.append(
            neutral_line_data(
                normal_force,
                moment_y,
                moment_x,
                y,
                z,
                neutral_line_numeric,
                neutral_line_latex
            )
        )

    def append_shear_flux(self,
                          shear_flux_numeric: str,
                          shear_flux_latex: str,
                          shear_force: float,
                          static_moment: str,
                          static_moment_string: str,
                          moment_inertia_x: str
                          ):

        self.shear_flux_data_list.append(
            shear_flux_data(
                shear_flux_numeric,
                shear_flux_latex,
                shear_force,
                static_moment,
                static_moment_string,
                moment_inertia_x
            )
        )

    def append_shear_stress(self,
                            shear_stress_numeric: str,
                            shear_stress_latex: str,
                            shear_stress: str,
                            shear_force: float,
                            static_moment: str,
                            static_moment_latex: str,
                            moment_inertia_x: str,
                            thickness: float
                            ):

        self.shear_stress_data_list.append(
            shear_stress_data(
                shear_stress_numeric,
                shear_stress_latex,
                shear_stress,
                shear_force,
                static_moment,
                static_moment_latex,
                moment_inertia_x,
                thickness
            )
        )

    def generate_pdf(self,
                     language: str
                     ):
        # creates a folder to generate the figure and logo into
        make_temp_folder()

        self.pdfgen = pdf_generator(self, self.calc)
        figure = self.show_cross_section()

        save_figure(figure, "tmp\\figs\\sectransv")
        generate_logo()

        self.pdfgen.generate_pdf(language)

    def reset_strings(self):
        self.normal_stress_data_list.clear()
        self.neutral_line_data_list.clear()
        self.shear_flux_data_list.clear()
        self.shear_stress_data_list.clear()
        self.static_moment_for_shear_numeric.clear()
        self.static_moment_for_shear_latex.clear()


class normal_stress_data:
    def __init__(self,
                 normal_stress,
                 normal_stress_latex,
                 normal_force,
                 moment_y,
                 moment_x,
                 y,
                 z
                 ):

        self.normal_stress = normal_stress
        self.normal_stress_latex = normal_stress_latex
        self.normal_force = normal_force
        self.moment_y = moment_y
        self.moment_x = moment_x
        self.y = y
        self.z = z


class neutral_line_data:
    def __init__(self,
                 normal_force,
                 moment_y,
                 moment_x,
                 y,
                 z,
                 neutral_line_numeric,
                 neutral_line_latex
                 ):

        self.normal_force = normal_force
        self.moment_y = moment_y
        self.moment_x = moment_x
        self.y = y
        self.z = z
        self.neutral_line_numeric = neutral_line_numeric
        self.neutral_line_latex = neutral_line_latex


class shear_flux_data:
    def __init__(self,
                 shear_flux_numeric,
                 shear_flux_latex,
                 # shear_flux,
                 shear_force,
                 static_moment,
                 static_moment_latex,
                 moment_inertia_x
                 ):

        self.shear_flux_numeric = shear_flux_numeric
        self.shear_flux_latex = shear_flux_latex
        # self.shear_flux = shear_flux
        self.shear_force = shear_force
        self.static_moment = static_moment
        self.static_moment_string = static_moment_latex
        self.moment_inertia_x = moment_inertia_x


class shear_stress_data:
    def __init__(self,
                 shear_stress_numeric,
                 shear_stress_latex,
                 shear_stress,
                 shear_force,
                 static_moment,
                 static_moment_latex,
                 moment_inertia_x,
                 thickness
                 ):

        self.shear_stress_numeric = shear_stress_numeric
        self.shear_stress_latex = shear_stress_latex
        self.shear_stress = shear_stress
        self.shear_force = shear_force
        self.static_moment = static_moment
        self.static_moment_latex = static_moment_latex
        self.moment_inertia_x = moment_inertia_x
        self.thickness = thickness


if __name__ == "__main__":
    test = manager()
    test.add_rectangular_subarea(upper_left=(0, 10), down_right=(5, 0))
    test.add_rectangular_subarea(upper_left=(5, 10), down_right=(10, 0))
    # test.add_semicircular_subarea(center=(10, 5), radius=5, angle=90)
    test.get_geometrical_properties(print_results=False)
    test.calculate_normal_stress(normal_force=10, y="1", print_results=False,
                                 append_to_pdf=True)  # default for y and z are Symbols
    test.calculate_neutral_line(normal_force=10, y="1", append_to_pdf=True)
    test.calculate_shear_flux(10, 1, True)
    test.calculate_shear_stress(shear_force=10, thickness=10, cut_height=5, append_to_pdf=True)
    # test.show_cross_section(show=True)
    test.generate_pdf("PT")
