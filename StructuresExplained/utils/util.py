from pylatex import NoEscape
from sympy import Number
from os import path, mkdir, makedirs
from shutil import rmtree
import re


def round_expr(expr, num_digits):
    return expr.xreplace({n: round(n, num_digits) for n in expr.atoms(Number)})


def simplify_signals(equation):
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


def save_figure(figure, fig_path, transparent=True):
    figure.savefig(fig_path, transparent=transparent)


def make_temp_folder():
    if not path.isdir("tmp"):
        mkdir("tmp")
    if not path.isdir("tmp\\figs"):
        makedirs("tmp\\figs")


def delete_temp_folder():
    if path.isdir("tmp"):
        rmtree('tmp')


class add_to_pdf:
    def __init__(self, document):
        self.document = document

    def add_equation(self, equation):
        self.document.append(NoEscape(r'\begin{dmath*}'))
        self.document.append(NoEscape(equation))
        self.document.append(NoEscape(r'\end{dmath*}'))
