import matplotlib.pyplot as plt
from pylatex import NoEscape
from os import path, mkdir, makedirs
from shutil import rmtree
import re

from typing import (
    Optional,
)


def round_expr(expr: str):
    if not isinstance(expr, str):
        expr = str(expr)

    search = re.findall(r'(\d+[\.,]\d+)', expr)
    for index in search:
        expr = re.sub(index, determine_round_format(index), expr)
    return expr


def determine_round_format(number: str):
    try:
        number = float(number)
    except ValueError:
        print(number, "wasn't formatted")
        return number

    if number < 0.01 or number > 10000:
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
