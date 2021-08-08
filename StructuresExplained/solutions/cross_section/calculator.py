import math
from sympy import Symbol, solve
from sympy.parsing.sympy_parser import parse_expr
import numpy as np

from typing import (
    Union,
    List,
    Dict,
    Any,
)


class calculator:
    def __init__(self):

        self.subareas_rectangle: Dict[int, list] = {}
        self.subareas_circle: Dict[int, List[Union[float, Any]]] = {}
        self.total_area: str = ""
        self.moment_x: str = ""
        self.moment_y: str = ""
        self.total_cg_x: str = ""
        self.total_cg_y: str = ""
        self.moment_inertia_x: str = ""
        self.moment_inertia_y: str = ""
        self.normal_stress: str = ""
        self.neutral_line: str = ""
        self.static_moment_for_shear: str = ""
        self.shear_flux: str = ""
        self.shear_stress: str = ""

    def calculate_values(self):
        self.det_static_moment_rectangle()
        self.det_static_moment_circle()
        self.det_center_of_gravity()
        self.det_moment_of_inertia_rectangle()
        self.det_moment_of_inertia_circle()

    def det_static_moment_rectangle(self):
        """
        calculate static moment for rectangular subareas. this function only appends
        values to a string so they can be displayed step by step in the pdf later.

        the result is later calculated using the parse_expr function from sympy
        """

        for key, (x1, y1, x2, y2) in self.subareas_rectangle.items():
            _, _, partial_cg_y, partial_cg_x, partial_area = self.get_rectangle_values(x1, y1, x2, y2)

            self.total_area += f'+ {partial_area}'
            self.moment_x += f'+ {partial_area} * {partial_cg_y}'
            self.moment_y += f'+ {partial_area} * {partial_cg_x}'

    def det_static_moment_circle(self):
        """
        calculate static moment for semi-circular subareas. this function only appends
        values to a string so they can be displayed step by step in the pdf later

        the result is later calculated using the parse_expr function from sympy
        """

        for key, (x, y, radius, angle) in self.subareas_circle.items():
            partial_area, partial_cg_y, partial_cg_x = self.get_circle_values(angle, radius)

            self.total_area += f'+ {partial_area}'
            self.moment_x += f'+ {partial_area} * ({y} + {partial_cg_y})'
            self.moment_y += f'+ {partial_area} * ({x} + {partial_cg_x})'

    def det_center_of_gravity(self):
        """calculates the center of gravity to be displayed in the generated figure"""

        self.total_cg_y = f'({self.moment_x}) / ({self.total_area})'
        self.total_cg_x = f'({self.moment_y}) / ({self.total_area})'

    def det_moment_of_inertia_rectangle(self):
        """calculate moment of inertia for rectangle subareas."""

        for key, (x1, y1, x2, y2) in self.subareas_rectangle.items():
            base, height, partial_cg_y, partial_cg_x, area = self.get_rectangle_values(x1, y1, x2, y2)

            self.moment_inertia_x += f'+ (({base} * {height} ** 3) / 12)'
            if area * (float(parse_expr(self.total_cg_y)) - partial_cg_y) ** 2 != 0:
                # appends parallel axis theorem if necessary
                self.moment_inertia_x += f"+ ({area} * (({parse_expr(self.total_cg_y)} - {partial_cg_y}) ** 2))"

            self.moment_inertia_y += f'+(({base} ** 3 * {height}) / 12)'
            if area * (float(parse_expr(self.total_cg_x)) - partial_cg_x) ** 2 != 0:
                # appends parallel axis theorem if necessary
                self.moment_inertia_y += f"+ ({area} * (({parse_expr(self.total_cg_x)} - {partial_cg_x}) ** 2))"

    def det_moment_of_inertia_circle(self):
        """calculate moment of inertia for semi-circular subareas."""

        for key, (x, y, radius, angle) in self.subareas_circle.items():
            area, partial_cg_y, partial_cg_x = self.get_circle_values(angle, radius)

            self.moment_inertia_x = self.moment_inertia_y = f'+({math.pi} * {radius} ** 4) / 8'

            if area * (float(parse_expr(self.total_cg_y) - y) ** 2) != 0:
                # appends parallel axis theorem if necessary
                self.moment_inertia_x += f'+ {area} * (({parse_expr(self.total_cg_y)} - {y + partial_cg_y})**2)'

            if area * (float(parse_expr(self.total_cg_x) - x) ** 2) != 0:
                # appends parallel axis theorem if necessary
                self.moment_inertia_y += f'+ {area} * (({parse_expr(self.total_cg_x)} - {x + partial_cg_x})**2)'

    def calculate_static_moment_for_shear(self,
                                          cut_height: float
                                          ):
        """calculate static moment on the cut given by the user. only for rectangle subareas currently"""
        if self.subareas_circle:
            raise ValueError(
                "Calculating static moment for shear stress and flux for semicircular subareas isn't available yet"
            )

        self.static_moment_for_shear = ""
        for key, (x1, y1, x2, y2) in self.subareas_rectangle.items():
            base, height, partial_cg_y, _, area = self.get_rectangle_values(x1, y1, x2, y2)

            half_height = height / 2
            distance_from_cut = cut_height - partial_cg_y

            if distance_from_cut <= -half_height:
                self.static_moment_for_shear += f" + {area} * ({partial_cg_y} - {float(parse_expr(self.total_cg_y))})"

            elif np.abs(distance_from_cut) <= half_height:
                self.static_moment_for_shear += f" + ({height} / 2 + {partial_cg_y} - {cut_height}) * {base}" \
                                                f" * ((({height} / 2 + {partial_cg_y} - {cut_height}) * 0.5 +" \
                                                f" {cut_height}) - {parse_expr(self.total_cg_y)})"

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
        """calculate values for rectangular subarea"""

        base = x2 - x1
        height = y1 - y2
        partial_cg_y = (y1 + y2) / 2
        partial_cg_x = (x1 + x2) / 2
        area = base * height

        return base, height, partial_cg_y, partial_cg_x, area

    def get_circle_values(self,
                          angle: float,
                          radius: float
                          ):
        """calculate values for semi-circular subarea"""

        area = (math.pi * radius ** 2) / 2
        partial_cg_y = math.cos(angle * math.pi / 180) * ((4 * radius) / (3 * math.pi))
        partial_cg_x = math.sin(angle * math.pi / 180) * ((4 * radius) / (3 * math.pi))

        return area, partial_cg_y, partial_cg_x

    def det_normal_stress(self,
                          normal_force: float,
                          y: Union[float, Symbol],
                          z: Union[float, Symbol],
                          ):
        """calculates normal stress"""

        self.normal_stress = f'({normal_force}/{parse_expr(self.total_area)}) - (({parse_expr(self.moment_y)}/' \
                             f'{parse_expr(self.moment_inertia_y)}) * {z})' \
                             f' - (({parse_expr(self.moment_x)}/{parse_expr(self.moment_inertia_x)}) * {y})'

        return self.normal_stress, self.moment_y, self.moment_x

    def det_neutral_line(self,
                         normal_force: float,
                         y: float,
                         z: float
                         ):

        normal_stress, _, _ = self.det_normal_stress(normal_force, y, z)

        if (self.moment_y != "0" and type(z) == Symbol) and (type(y) != Symbol or self.moment_x == "0"):
            self.neutral_line = f"z = {solve(normal_stress, z)[0]}"

        elif (self.moment_y == "0" and self.moment_x == "0") or (type(y) != Symbol and type(z) != Symbol):
            self.neutral_line = "No neutral line"

        else:
            self.neutral_line = f"y = {solve(normal_stress, y)}"

        return normal_stress, self.neutral_line, self.moment_y, self.moment_x

    def det_shear_flux(self,
                       shear_force: float
                       ):
        self.shear_flux = f'({shear_force} * {parse_expr(self.static_moment_for_shear)}) /' \
                          f' ({parse_expr(self.moment_inertia_x)})'

        return self.shear_flux

    def det_shear_stress(self,
                         shear_force: float,
                         thickness: float
                         ):

        if float(thickness) == 0:
            raise ValueError("thickness parameter must not be zero")

        self.shear_stress = f'({shear_force} * {parse_expr(self.static_moment_for_shear)}) /' \
                            f' (({parse_expr(self.moment_inertia_x)}) * {thickness})'

        return self.shear_stress

    def reset_results(self):
        self.total_area = self.moment_x = self.moment_y = self.moment_inertia_y = self.moment_inertia_x = \
            self.static_moment_for_shear = self.total_cg_y = self.total_cg_x = ''

        self.static_moment_for_shear = 0
