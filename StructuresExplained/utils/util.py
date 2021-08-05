import matplotlib.pyplot as plt
from pylatex import NoEscape
from sympy import Number
from os import path, mkdir, makedirs
from shutil import rmtree
import re

from typing import (
    Optional,
)


def round_expr(expr, num_digits: int):
    return expr.xreplace({n: round(n, num_digits) for n in expr.atoms(Number)})


def simplify_signals(equation: str):
    equation = equation.replace('- -', '+')
    equation = equation.replace('--', '+')
    equation = equation.replace('+ -', '-')
    equation = equation.replace('+-', '-')
    # string = string.replace('+ 0.00', '')
    # string = string.replace('- 0.00', '')
    search = re.search(r'\\cdot -(\d+\.\d+)', equation)
    if search:
        equation = re.sub(r'\\cdot -(\d+\.\d+)', f'\\\\cdot (-{search.group(1)})', equation)
    return equation


def save_figure(figure: plt.Figure, fig_path: str, transparent: Optional[bool] = True):
    figure.savefig(fig_path, transparent=transparent)


def make_pdf_folder(pdf_path: str):
    if not path.isdir(pdf_path):
        mkdir(pdf_path)


def make_figure_folder(pdf_path: str):
    if not path.isdir(pdf_path + r"\figs"):
        makedirs(pdf_path + r"\figs")


def delete_temp_folder(pdf_path: str):
    if path.isdir(pdf_path):
        rmtree(pdf_path)


class add_to_pdf:
    def __init__(self, document):
        self.document = document

    def add_equation(self, equation):
        self.document.append(NoEscape(r'\begin{dmath*}'))
        self.document.append(NoEscape(equation))
        self.document.append(NoEscape(r'\end{dmath*}'))
