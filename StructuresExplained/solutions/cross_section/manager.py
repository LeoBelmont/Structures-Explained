from sympy import Symbol, parse_expr
from StructuresExplained.solutions.cross_section.calculator import calculator
from StructuresExplained.solutions.cross_section.fig_generation import fig_generator
from StructuresExplained.solutions.cross_section.pdf_generation import *
from StructuresExplained.utils.util import save_figure, make_pdf_folder, make_figure_folder, delete_folder
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

    def add_rectangular_subarea(self,
                                upper_left: tuple,
                                down_right: tuple
                                ):
        """
        upper_left: coordinate of upper left vertex of rectangle (x, y)

        down_right: coordinate of down right vertex of rectangle (x, y)
        """

        self.rectangle_count += 1
        self.calc.subareas_rectangle.update({self.rectangle_count: [upper_left[0], upper_left[1],
                                                                    down_right[0], down_right[1]]})

    def add_semicircular_subarea(self,
                                 center: tuple,
                                 radius: float,
                                 angle: float
                                 ):
        """
        center: coordinate of the semicircle center (as if it were a full circle) (x, y)

        radius: radius of the semicircle

        angle: angle of the semicircle relative to x axis, clockwise
        """

        self.semicircle_count += 1
        self.calc.subareas_circle.update({self.semicircle_count: [center[0], center[1], radius, angle]})

    def calculate_geometrical_properties(self):
        """calculates geometrical properties and stores them in the calculator instance calc"""

        self.calc.reset_results()

        self.reset_pdf_data()

        self.calc.calculate_values()

    def print_results(self):
        attrs = vars(self.calc)
        for key, value in attrs.items():
            if 'subareas' not in key:
                if type(value) != str or key == "neutral_line":
                    print(f'{key}: {value}')
                else:
                    if value != "":
                        print(f'{key}: {parse_expr(value)}')

    def show_cross_section(self,
                           show: Optional[bool] = False,
                           rectangle_subarea_id: Optional[int] = None,
                           circle_subarea_id: Optional[int] = None
                           ):
        """
        you can pass a subarea ID if you want it to be highlighted in red. IDs must match the
        ones in the subarea dict
        """

        fgen = fig_generator(self.calc.subareas_rectangle,
                             self.calc.subareas_circle,
                             parse_expr(self.calc.total_cg_x),
                             parse_expr(self.calc.total_cg_y),
                             )

        fig = fgen.plot(rectangle_subarea_id, circle_subarea_id)

        if show:
            fig.show()
        else:
            return fig

    def calculate_normal_stress(self,
                                normal_force: float,
                                y: Optional[Union[float, Symbol]] = Symbol('y'),
                                z: Optional[Union[float, Symbol]] = Symbol('z'),
                                append_to_pdf: bool = False,
                                ):
        """calculates normal stress and appends the step by step solution to the PDF if append_to_pdf is True"""

        normal_stress, moment_y, moment_x = self.calc.det_normal_stress(normal_force, y, z)

        if append_to_pdf:
            self.append_normal_stress(normal_stress, normal_force, moment_y, moment_x, y, z)

    def calculate_neutral_line(self,
                               normal_force: float,
                               y: Optional[Union[float, Symbol]] = Symbol('y'),
                               z: Optional[Union[float, Symbol]] = Symbol('z'),
                               append_to_pdf: bool = False,
                               ):
        """calculates neutral line and appends the step by step solution to the PDF if append_to_pdf is True"""

        normal_stress, neutral_line, moment_y, moment_x = self.calc.det_neutral_line(normal_force, y, z)

        if append_to_pdf:
            self.append_neutral_line(normal_stress, neutral_line, normal_force, moment_y, moment_x, y, z)

    def calculate_shear_flux(self,
                             shear_force: float,
                             cut_height: float,
                             append_to_pdf: bool = False
                             ):
        self.calc.calculate_static_moment_for_shear(cut_height)

        shear_flux = self.calc.det_shear_flux(shear_force)

        if append_to_pdf:
            self.append_shear_flux(shear_flux, shear_force, self.calc.static_moment_for_shear,
                                   self.calc.moment_inertia_x)

    def calculate_shear_stress(self,
                               shear_force: float,
                               thickness: float,
                               cut_height: float,
                               append_to_pdf: Optional[bool] = False
                               ):
        """calculates shear stress and appends the step by step solution to the PDF if append_to_pdf is True"""

        self.calc.calculate_static_moment_for_shear(cut_height)

        shear_stress = self.calc.det_shear_stress(shear_force, thickness)

        if append_to_pdf:
            self.append_shear_stress(shear_stress, shear_force, self.calc.static_moment_for_shear,
                                     self.calc.moment_inertia_x, thickness)

    def append_normal_stress(self,
                             normal_stress: str,
                             normal_force: float,
                             moment_y: str,
                             moment_x: str,
                             y: Union[float, Symbol],
                             z: Union[float, Symbol]
                             ):

        self.normal_stress_data_list.append(
            normal_stress_data(
                normal_stress,
                normal_force,
                moment_y,
                moment_x,
                y,
                z
            )
        )

    def append_neutral_line(self,
                            normal_stress: str,
                            neutral_line: str,
                            normal_force: float,
                            moment_y: str,
                            moment_x: str,
                            y: Union[float, Symbol],
                            z: Union[float, Symbol]
                            ):

        self.neutral_line_data_list.append(
            neutral_line_data(
                normal_stress,
                neutral_line,
                normal_force,
                moment_y,
                moment_x,
                y,
                z,
            )
        )

    def append_shear_flux(self,
                          shear_flux: str,
                          shear_force: float,
                          static_moment: str,
                          moment_inertia_x: str
                          ):

        self.shear_flux_data_list.append(
            shear_flux_data(
                shear_flux,
                shear_force,
                static_moment,
                moment_inertia_x
            )
        )

    def append_shear_stress(self,
                            shear_stress: str,
                            shear_force: float,
                            static_moment: str,
                            moment_inertia_x: str,
                            thickness: float
                            ):

        self.shear_stress_data_list.append(
            shear_stress_data(
                shear_stress,
                shear_force,
                static_moment,
                moment_inertia_x,
                thickness
            )
        )

    def generate_pdf(self,
                     language: str,
                     pdf_path: Optional[str] = "pdf",
                     filename: Optional[str] = "cross-section",
                     clear=True
                     ):
        """
        creates a folder to generate the figure and logo into
        language: "EN" for english or "PT" for brazilian portuguese
        pdf_path: path where pdf will be generated
        clear: delete figures generated for pdf after pdf is generated
        """

        make_pdf_folder(pdf_path)
        make_figure_folder(pdf_path)

        self.pdfgen = pdf_generator(self, self.calc)
        figure = self.show_cross_section()

        save_figure(figure, pdf_path + r"\figs\sectransv")
        generate_logo(pdf_path)

        self.pdfgen.generate_pdf(language, pdf_path, filename)

        if clear:
            delete_folder(pdf_path + r'\figs')

    def reset_pdf_data(self):
        self.normal_stress_data_list.clear()
        self.neutral_line_data_list.clear()
        self.shear_flux_data_list.clear()
        self.shear_stress_data_list.clear()


if __name__ == "__main__":
    test = manager()
    test.add_rectangular_subarea(upper_left=(0, 10), down_right=(5, 0))
    test.add_rectangular_subarea(upper_left=(5, 10), down_right=(10, 0))
    # test.add_semicircular_subarea(center=(10, 5), radius=5, angle=90)
    test.calculate_geometrical_properties()
    test.calculate_normal_stress(normal_force=10, y=1, append_to_pdf=True)  # default for y and z are Symbols
    test.calculate_neutral_line(normal_force=10, y=1, append_to_pdf=True)
    test.calculate_shear_flux(10, 1, append_to_pdf=True)
    test.calculate_shear_stress(shear_force=10, thickness=10, cut_height=5, append_to_pdf=True)
    test.print_results()
    test.show_cross_section(show=True)
    test.generate_pdf("PT", "testpath")
