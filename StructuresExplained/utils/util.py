import matplotlib.pyplot as plt
import numpy as np
from pylatex import NoEscape
from os import path, mkdir, makedirs
from shutil import rmtree
import re

from typing import (
    Optional,
    Union
)

from sympy import latex, sympify, parse_expr


def get_arrow_patch_values(Fx, Fz, coordinates, h):
    """
    :param Fx: (float)
    :param Fz: (float)
    :param coordinates: (tuple)
    :param h: (float) Is a scale variable
    :return: Variables for the matplotlib plotter
    """

    F = (Fx ** 2 + Fz ** 2) ** 0.5
    len_x = Fx / F * h
    len_y = -Fz / F * h
    x = coordinates[0] - len_x * 1.2
    y = coordinates[1] - len_y * 1.2

    return x, y, len_x, len_y, F


def get_relative_element_by_coordinates(system, rel_system, element_id):
    ss_element = system.element_map.get(element_id)
    x_1 = ss_element.vertex_1.x
    y_1 = ss_element.vertex_1.y
    x_2 = ss_element.vertex_2.x
    y_2 = ss_element.vertex_2.y
    for element in rel_system.element_map.values():
        if x_1 == element.vertex_1.x and x_2 == element.vertex_2.x and \
                y_1 == element.vertex_1.y and y_2 == element.vertex_2.y:
            return element.id
    return None


def round_expr(expr: str):
    if not isinstance(expr, str):
        expr = str(expr)

    search = re.findall(r'(\d+([.,]\d+)?(e[-+]\d+)?)', expr)
    for index in search:
        expr = re.sub(index[0], determine_round_format(index[0]), expr, count=1)
    return expr


def determine_round_format(number: str):
    try:
        number = float(number)
    except ValueError:
        print(number, "wasn't formatted")
        return number

    if number < 1e-11:
        return "0"
    elif number < 0.01 or number > 10000:
        return scientific_notation_formatting(number)
    else:
        return str(round(number, 2))


def scientific_notation_formatting(number):
    a = '%E' % number
    return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]


def save_figure(figure: plt.Figure, fig_path: str, transparent: Optional[bool] = True):
    figure.savefig(fig_path, transparent=transparent)


def make_pdf_folder(pdf_path: str):
    if not path.isdir(pdf_path):
        mkdir(pdf_path)


def make_figure_folder(pdf_path: str):
    if not path.isdir(pdf_path + r"\figs"):
        makedirs(pdf_path + r"\figs")


def delete_folder(pdf_path: str):
    if path.isdir(pdf_path):
        rmtree(pdf_path)


class add_to_pdf:
    def __init__(self, document):
        self.document = document

    def add_equation(self, equation):
        self.document.append(NoEscape(r'\begin{dmath*}'))
        self.document.append(NoEscape(equation))
        self.document.append(NoEscape(r'\end{dmath*}'))


def append_step(equation):
    if "degree" in str(equation):
        from sympy.physics.units import degree
        equation = re.sub(r"degree", r"degrees", str(equation))
        subs = {"degrees": degree}
        return latex(sympify(round_expr(equation), evaluate=False).subs(subs))

    return latex(sympify(round_expr(equation), evaluate=False))


def append_result(equation: str):
    if not isinstance(equation, str):
        equation = str(equation)

    if "degree" in str(equation):
        equation = re.sub(r"(\d+[.,]\d+)\*degree", r"rad(\1)", str(equation))

    return latex(sympify(round_expr(equation)).evalf())


def get_value_from_points(result, element_length, mul_value=None, polynomial_degree=3):
    if mul_value is None:
        mul_value = element_length
    iteration_factor = np.linspace(0, 1, len(result))
    x = iteration_factor * element_length
    coefficients = np.polyfit(x, result, polynomial_degree)
    value = 0
    for degree, index in zip(range(polynomial_degree, -1, -1), range(polynomial_degree+1)):
        value += coefficients[index] * mul_value ** degree
    return value
