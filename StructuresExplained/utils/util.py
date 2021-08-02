from pylatex import NoEscape
from sympy import Number
from os import path, mkdir, makedirs
from shutil import rmtree


def round_expr(expr, num_digits):
    return expr.xreplace({n: round(n, num_digits) for n in expr.atoms(Number)})


def add_equation_to_pdf(doc, equation):
    doc.append(NoEscape(r'\begin{dmath*}'))
    doc.append(NoEscape(equation))
    doc.append(NoEscape(r'\end{dmath*}'))


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
