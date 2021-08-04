import math
import sympy
from sympy.parsing.sympy_parser import parse_expr
from pylatex import NoEscape
import numpy as np
from StructuresExplained.utils.util import round_expr
from StructuresExplained.utils.util import simplify_signals

from typing import (
    Union,
    List,
    Dict,
    Any,
    Optional
)


class calculator:
    def __init__(self):

        self.subareas_rectangle: Dict[int, list] = {}
        self.subareas_circle: Dict[int, List[Union[float, Any]]] = {}
        self.total_area: str = ""
        self.moment_x: str = ""
        self.moment_y: str = ""
        self.total_cg_x: float = 0
        self.total_cg_y: float = 0
        self.moment_inertia_x: str = ""
        self.moment_inertia_x_latex: str = ""
        self.moment_inertia_y: str = ""
        self.moment_inertia_y_latex: str = ""
        self.static_moment_for_shear: str = ""

    def calculate_values(self):
        self.det_static_moment_rectangle()
        self.det_static_moment_circle()
        self.det_center_of_gravity()
        self.det_moment_of_inertia_rectangle()
        self.det_moment_of_inertia_circle()

    def det_static_moment_rectangle(self):
        # calculate static moment for rectangular subareas. this function only appends
        # values to a string so they can be displayed step by step in the pdf later.
        # the result is later calculated using the parse_expr function from sympy

        for key, (x1, y1, x2, y2) in self.subareas_rectangle.items():
            _, _, partial_cg_y, partial_cg_x, partial_area, _ = self.get_rectangle_values(x1, y1, x2, y2)

            self.total_area += f'+ {partial_area}'
            self.moment_x += f'+ {partial_area} * {partial_cg_y}'
            self.moment_y += f'+ {partial_area} * {partial_cg_x}'

    def det_static_moment_circle(self):
        # calculate static moment for semi-circular subareas. this function only appends
        # values to a string so they can be displayed step by step in the pdf later
        # the result is later calculated using the parse_expr function from sympy

        for key, (x, y, radius, angle) in self.subareas_circle.items():
            partial_area, partial_cg_y, partial_cg_x = self.get_circle_values(angle, radius)

            self.total_area += f'+ {partial_area}'
            self.moment_x += f'+ {partial_area} * ({y} + {partial_cg_y})'
            self.moment_y += f'+ {partial_area} * ({x} + {partial_cg_x})'

    def det_center_of_gravity(self):
        # calculates the center of gravity to be displayed in the generated figure

        self.total_cg_y = float(parse_expr(f'({self.moment_x}) / ({self.total_area})'))
        self.total_cg_x = float(parse_expr(f'({self.moment_y}) / ({self.total_area})'))

    def det_moment_of_inertia_rectangle(self):
        # calculate moment of inertia for rectangle subareas.
        # this function makes two strings, one for the results and displaying in the UI
        # and the other for the step by step solution.

        for key, (x1, y1, x2, y2) in self.subareas_rectangle.items():
            base, height, partial_cg_y, partial_cg_x, area, _ = self.get_rectangle_values(x1, y1, x2, y2)

            self.moment_inertia_x += f'+(({base} * ({height} ** 3)) / 12) + ({area} * (({self.total_cg_y} - {partial_cg_y}) ** 2))'
            self.moment_inertia_x_latex += r'+ \frac' + '{' + f'{base} \\cdot {height}^3' + '}' + r'{12}'
            if area * (self.total_cg_y - partial_cg_y) ** 2 != 0:
                # appends parallel axis theorem if necessary
                self.moment_inertia_x_latex += f'+ {area} \\cdot ({self.total_cg_y} - {partial_cg_y})^2'

            self.moment_inertia_y += f'+((({base} ** 3) * {height}) / 12) + ({area} * (({self.total_cg_x} - {partial_cg_x}) ** 2))'
            self.moment_inertia_y_latex += r'+ \frac' + '{' + f'{base}^3 \\cdot {height}' + '}' + r'{12}'
            if area * (self.total_cg_x - partial_cg_x) ** 2 != 0:
                # appends parallel axis theorem if necessary
                self.moment_inertia_y_latex += f'+ {area} \\cdot ({self.total_cg_x} - {partial_cg_x})^2'

    def det_moment_of_inertia_circle(self):
        # calculate moment of inertia for semi-circular subareas.
        # this function makes two strings, one for the results and displaying in the UI
        # and the other for the step by step solution.

        for key, (x, y, radius, angle) in self.subareas_circle.items():
            area, partial_cg_y, partial_cg_x = self.get_circle_values(angle, radius)

            moment_inertia = f'+({math.pi} * {radius} ** 4) / 8'
            moment_inertia_latex = r'+ \frac' + '{' + f'{math.pi} \\cdot {radius}^4' + '}' + r'{8}'

            self.moment_inertia_x += f'{moment_inertia} + {area} * (({self.total_cg_y} - {y + partial_cg_y})**2)'

            self.moment_inertia_x_latex += moment_inertia_latex
            if area * ((partial_cg_y - y) ** 2) != 0:
                # appends parallel axis theorem if necessary
                self.moment_inertia_x_latex += f'+ {area} \\cdot ({self.total_cg_y} - {y + partial_cg_y})^2'

            self.moment_inertia_y += f'{moment_inertia} + {area} * (({self.total_cg_x} - {x + partial_cg_x})**2)'

            self.moment_inertia_y_latex += moment_inertia_latex
            if area * ((self.total_cg_x - x) ** 2) != 0:
                # appends parallel axis theorem if necessary
                self.moment_inertia_y_latex += f'+ {area} \\cdot ({self.total_cg_x} - {x + partial_cg_x})^2'

    def calculate_static_moment_for_shear(self,
                                          cut_height: float
                                          ):
        # calculate static moment on the cut given by the user. only for rectangle subareas currently
        if self.subareas_circle:
            raise ValueError(
                "Calculating static moment for shear stress and flux for semicircular subareas isn't available yet"
            )

        static_moment_cut_string = ''
        static_moment_cut = 0
        for key, (x1, y1, x2, y2) in self.subareas_rectangle.items():
            base, height, partial_cg_y, _, area, _ = self.get_rectangle_values(x1, y1, x2, y2)

            half_height = height / 2
            distance_from_cut = cut_height - partial_cg_y

            if distance_from_cut <= -half_height:
                static_moment_cut += area * (partial_cg_y - self.total_cg_y)

                static_moment_cut_string += f'+ {area} \\cdot ({partial_cg_y} - {self.total_cg_y}) '

            elif np.abs(distance_from_cut) <= half_height:
                static_moment_cut += (height / 2 + partial_cg_y - cut_height) * base * \
                                     (((height / 2 + partial_cg_y - cut_height) * .5 + cut_height) - self.total_cg_y)

                static_moment_cut_string += r'+ (\frac{' + str(height) + r'}{2} + ' + str(partial_cg_y) + \
                                            f'- {cut_height}) \\cdot {base}' + r' \cdot (((\frac{' + str(height) + \
                                            r'}{2} + ' + str(partial_cg_y) + f' - {cut_height}) \\cdot 0.5 + ' \
                                                                             f'{cut_height}) - {self.total_cg_y}) '

        return self.static_moment_for_shear

        # values for circular sectors
        # for key, (x, y, r, a) in self.sub_areas_cir.items():
        #     A, cgy, cgx = self.cir_values(a, r)
        #
        #     Ac = r**2 * np.arccos((cut_y-y)/r) - cut_y-y * (r**2 - d**2)**.5
        #     self.Qc += Ac * (y + cgy - self.yg)

    def get_rectangle_values(self,
                             x1: float,
                             y1: float,
                             x2: float,
                             y2: float
                             ):
        # calculate values for rectangular subarea

        base = x2 - x1
        height = y1 - y2
        partial_cg_y = (y1 + y2) / 2
        partial_cg_x = (x1 + x2) / 2
        area = base * height
        dc = partial_cg_y - self.total_cg_y

        return base, height, partial_cg_y, partial_cg_x, area, dc

    def get_circle_values(self,
                          angle: float,
                          radius: float
                          ):
        # calculate values for semi-circular subarea

        area = (math.pi * radius ** 2) / 2
        partial_cg_y = math.cos(angle * math.pi / 180) * ((4 * radius) / (3 * math.pi))
        partial_cg_x = math.sin(angle * math.pi / 180) * ((4 * radius) / (3 * math.pi))

        return area, partial_cg_y, partial_cg_x

    def det_normal_stress(self,
                          normal_force: float,
                          y: str,
                          z: str,
                          latex_format: Optional[bool] = True
                          ):
        # calculates normal stress and neutral line.
        # two strings are necessary, one in LaTeX format to be displayed in the PDF solution and the other in the UI.

        normal_stress = f'({normal_force}/{self.total_area}) - (({self.moment_y}/{self.moment_inertia_y}) * {z}) - ' \
                        f'(({self.moment_x}/{self.moment_inertia_x}) * {y})'

        if latex_format:
            normal_stress_latex = NoEscape(
                r'\frac{' + f'{normal_force}' + r'}{' + f'{self.total_area}' + r'} - \frac{' +
                f'{self.moment_y}' + r'}{' + f'{self.moment_inertia_y_latex}' + r'} \cdot' +
                f' {z} -' + r'\frac{' + f'{self.moment_x}' + r'}{' +
                f'{self.moment_inertia_x_latex}' + r'} \cdot' + f' {y}'
                )

            return normal_stress, normal_stress_latex, self.moment_y, self.moment_x
        else:
            return normal_stress

    def det_neutral_line(self,
                         normal_force: float,
                         y: str,
                         z: str
                         ):

        normal_stress = self.det_normal_stress(normal_force, y, z, latex_format=False)

        if (self.moment_y != "0" and type(z) != str) and (type(y) == str or self.moment_x == "0"):
            self.neutral_line = f"z = {round_expr(sympy.solve(normal_stress, z)[0], 2)}"

        elif (self.moment_y == "0" and self.moment_x == "0") or (type(y) == str and type(z) == str):
            self.neutral_line = "Não há linha neutra"

        else:
            self.neutral_line = f"y = {round_expr(sympy.solve(normal_stress, y), 2)}"

        neutral_line_latex = NoEscape(r'0 = \frac{' + str(normal_force) + r'}{' + str(self.total_area) + r'} - \frac{'
                                      + str(self.moment_y) + r'}{' + str(self.moment_inertia_y_latex) + r'} \cdot '
                                      + str(z) + r' - \frac{' + str(self.moment_x) + r'}{'
                                      + str(self.moment_inertia_x_latex) + r'} \cdot ' + str(y))

        return self.neutral_line, neutral_line_latex, self.moment_y, self.moment_x

    def det_shear_flux(self,
                       shear_force: float
                       ):
        self.shear_flux = f'({shear_force} * {self.static_moment_for_shear}) / ({self.moment_inertia_x})'
        shear_flux_latex = r'\frac{' + f'{shear_force} \\cdot {self.static_moment_for_shear}' + r'}{' + \
                           f'{self.moment_inertia_x_latex}' + r'}'

        return self.shear_flux, shear_flux_latex

    def det_shear_stress(self,
                         shear_force: float,
                         thickness: float
                         ):

        if float(thickness) != 0:
            self.shear_stress = f'({shear_force} * {self.static_moment_for_shear}) / (({self.moment_inertia_x}) * {thickness})'
            shear_stress_latex = r'\frac{' + f'{shear_force} \\cdot {self.static_moment_for_shear}' + r'}{' + \
                                 f'{self.moment_inertia_x_latex} \\cdot {thickness}' + r'} '
        else:
            shear_stress_latex = None

        return self.shear_stress, shear_stress_latex

    def reset_results(self):
        self.total_area = self.moment_x = self.moment_y = self.moment_inertia_y = self.moment_inertia_x = \
            self.moment_inertia_y_latex = self.moment_inertia_x_latex = self.static_moment_for_shear = ''

        self.static_moment_for_shear = self.total_cg_y = self.total_cg_x = 0
