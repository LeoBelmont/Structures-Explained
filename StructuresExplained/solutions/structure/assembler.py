import math
import numpy
import re
from sympy import Symbol
from sympy import latex
from sympy.parsing.sympy_parser import parse_expr

from typing import (
    Union,
    List,
    Dict,
)


class assembler:
    def __init__(self):
        self.list_load_y = None
        self.list_load_x = None
        self.eq_load = None
        self.angle = None
        self.shear_equation_y = None
        self.shear_equation_x = None
        self.eq = None
        self.hinged_reaction_x = None
        self.hinged_reaction_y = None
        self.roll_dist_x = None
        self.roll_reaction_y = None
        self.roll_dist_y = None
        self.roll_reaction_x = None
        self.idr = None
        self.fixed_reaction_x = None
        self.total_q_load_x = None
        self.total_point_load_x = None
        self.fixed_reaction_y = None
        self.total_q_load_y = None
        self.total_point_load_y = None
        self.fixed_reaction_moment = None
        self.moment_sum_from_forces = None
        self.moment_sum = None
        self.hinged = None
        self.roll = None
        self.roll_direction = None
        self.fixed = None
        self.node_map = None
        self.moment = None
        self.q_load = None
        self.node_map = None
        self.point = None
        self.relative_support_x = None
        self.relative_support_y = None
        self.element_list = None
        self.el: Union[Element, None] = None
        self.target_dir: str
        self.language: str
        self.element_counter = 0

    def assemble_structure(self):
        self.simplify_variables()

        if self.fixed:
            self.get_fixed_info()
            self.relative_support_x = self.fixed.x
            self.relative_support_y = self.fixed.y

        if self.hinged:
            self.get_hinged_info()
            self.relative_support_x = self.hinged.x
            self.relative_support_y = self.hinged.y

        if self.roll:
            self.get_roll_info()

        for self.element_counter in range(1, len(self.node_map) + 1):

            self.el = Element()

            if self.node_map.get(self.element_counter + 1):
                self.get_element_info()
            
            if self.element_counter in self.point.keys():
                self.map_loads()

            if self.element_counter in self.q_load.keys():
                self.map_q_loads()

            if self.element_counter in self.moment.keys():
                self.map_moments()

            self.shear_equation_y.append(self.total_point_load_y)
            self.shear_equation_x.append(self.total_point_load_x)

            if self.element_counter - 1 in self.q_load.keys():
                if self.list_load_y.get(self.element_counter - 1) is not None:
                    self.shear_equation_y[self.element_counter - 1] += self.list_load_y.get(self.element_counter - 1)
                if self.list_load_x.get(self.element_counter - 1) is not None:
                    self.shear_equation_x[self.element_counter - 1] += self.list_load_x.get(self.element_counter - 1)

            if self.fixed:
                if self.fixed[0].id == self.element_counter:
                    if self.moment.get(self.element_counter) is not None:
                        self.moment.update({self.element_counter: self.moment.get(self.element_counter) + float(self.fixed_reaction_moment)})
                    else:
                        self.moment.update({self.element_counter: float(self.fixed_reaction_moment)})

    def simplify_variables(self):
        self.hinged = self.hinged[0]
        self.roll = self.roll[0]
        self.fixed = self.fixed[0]

    def get_hinged_info(self):
        self.hinged_reaction_x = str(-self.hinged.Fx)
        self.hinged_reaction_y = str(-self.hinged.Fy)

    def get_roll_info(self, roll_direction=None):
        for self.element_counter in range(len(self.roll)):
            self.roll_reaction_x = str(-self.roll.x)
            self.roll_reaction_y = str(-self.roll.y)
            self.roll_dist_x = str(self.roll.x - self.hinged.x) + 'i'
            self.roll_dist_y = str(self.roll.y - self.hinged.y) + 'j'

    def get_fixed_info(self):
        id_ = self.fixed[0].id
        node = self.node_map.get(id_)
        self.fixed_reaction_moment = str(-node.Ty)
        self.fixed_reaction_y = str(-node.Fy)
        self.fixed_reaction_x = str(-node.Fx)

    def get_element_info(self):
        xi = self.node_map.get(self.element_counter).x
        yi = self.node_map.get(self.element_counter).y
        xf = self.node_map.get(self.element_counter + 1).x
        yf = self.node_map.get(self.element_counter + 1).y

        if (xf - xi) != 0:
            self.el.angle = numpy.arctan((yf - yi) / (xf - xi))
        elif (xf - xi) == 0:
            self.el.angle = numpy.arctan((yf - yi) / 1e-100)

    def map_loads(self):
        x = self.node_map.get(self.element_counter).x
        y = self.node_map.get(self.element_counter).y
        id_ = self.node_map.get(self.element_counter).id
        fx = self.point[id_][0]
        fy = -self.point[id_][1]

        if fx != 0:
            self.el.total_point_load_x = f'{self.element_list[:-1].total_point_load_x} + {fx}'

        if (y - self.relative_support_y) != 0 and fx != 0:
            self.moment_sum_from_forces += fr' + {fx}i \cdot {y - self.relative_support_y}j'

        if fy != 0:
            self.total_point_load_y += f' {fy}'

        if (x - self.relative_support_x) != 0 and fy != 0:
            self.moment_sum_from_forces += fr' + {fy}j \cdot {x - self.relative_support_x}i'

    def get_q_load_values(self, q, qi, xi, xf, yi, yf):
        pos = ((xf - xi) ** 2 + (yf - yi) ** 2) ** 0.5
        point_load = ((-qi.get(self.element_counter) + -q.get(self.element_counter)) * pos) / 2

        y_load = -(math.cos(self.angle[self.element_counter - 1] + math.pi) * point_load)
        x_load = math.sin(self.angle[self.element_counter - 1] + math.pi) * point_load
        cg = (pos / 3) * (float(qi.get(self.element_counter) + 2 * float(q.get(self.element_counter))) /
                          (float(qi.get(self.element_counter)) + float(q.get(self.element_counter))))
        height = math.sin(self.angle[self.element_counter - 1]) * cg
        base = math.cos(self.angle[self.element_counter - 1]) * cg

        return pos, point_load, y_load, x_load, cg, height, base

    def map_q_loads(self):
        qi = self.q_load.qi
        q = self.q_load.q
        xi = self.node_map.get(self.element_counter).x
        yi = self.node_map.get(self.element_counter).y
        xf = self.node_map.get(self.element_counter + 1).x
        yf = self.node_map.get(self.element_counter + 1).y
        x = Symbol('x')

        pos, point_load, y_load, x_load, cg, height, base = \
            self.get_q_load_values(q, qi, xi, xf, yi, yf)

        if round(x_load, 2) != 0:
            self.total_q_load_x += f' + {x_load}'
            if float(f'{height + yi - self.relative_support_y}') != 0:
                self.moment_sum += fr' + {x_load}i \cdot {height + yi - self.relative_support_y}j'

        if round(y_load, 2) != 0:
            self.total_q_load_y += f' + {y_load}'
            if round(base + xi - self.relative_support_x, 2) != 0:
                self.moment_sum += fr' + {y_load}j \cdot {base + xi - self.relative_support_x}i'

        self.list_load_x.update({self.element_counter: self.total_q_load_x})
        self.list_load_y.update({self.element_counter: self.total_q_load_y})

        q_part = ((((qi.get(self.element_counter) - q.get(self.element_counter)) /
                    (6 * pos)) * x ** 2) * 3 - ((qi.get(self.element_counter) / 2) * x) * 2)

        self.eq_load.update({self.element_counter: str(latex(q_part, 2))})

    def map_moments(self):
        self.moment_sum += f' + {self.moment.get(self.element_counter)}k'

    def get_signal(self, string):
        if re.search(r'(-)', string):
            return '-'
        else:
            return '+'

    def get_signal_constant(self, moment, result, numeric_const=0):
        if math.isclose(round(moment + numeric_const, 2), round(result, 2), rel_tol=1e-2):
            return moment
        else:
            return -moment

    def get_signal_vectors(self, result, fx, fy, angle, op):
        rel_value = 1e-2
        result = round(result, 2)
        fx = parse_expr(fx)
        fy = parse_expr(fy)

        if op == "sin":
            fx = fx * math.sin(angle)
            fy = fy * math.sin(numpy.radians(90) - angle)
        elif op == "cos":
            fx = fx * math.cos(angle)
            fy = fy * math.cos(numpy.radians(90) - angle)

        if math.isclose(round(-fx + fy, 2), result, rel_tol=rel_value):
            return "-", "+"

        elif math.isclose(round(fx - fy, 2), result, rel_tol=rel_value):
            return "+", "-"

        elif math.isclose(round(fx + fy, 2), result, rel_tol=rel_value):
            return "+", "+"

        else:
            return "-", "-"


class Node:
    def __init__(self):
        self.hinged: Union[List, None] = None
        self.roll: Union[List, None] = None
        self.fixed: Union[List, None] = None
        self.roll_direction: Union[float, None] = None
        self.moment = None
        self.point = None
        self.total_point_load_x = None
        self.total_point_load_y = None
        self.moment_sum_from_forces = None


class Element:
    def __init__(self):
        self.angle = None
        self.q_load = None
        self.load_x = None
        self.load_y = None
        self.eq_load = None
