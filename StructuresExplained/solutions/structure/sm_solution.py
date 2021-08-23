import math
import numpy
from StructuresExplained.solutions import functions
import re
import pickle
from matplotlib import pyplot as plt
from matplotlib.pyplot import savefig
from sympy import symbols, Number
from sympy import latex
from sympy.parsing.sympy_parser import parse_expr
from anastruct import SystemElements
from pylatex import Document, Section, Subsection, Figure, Alignat, NoEscape, Subsubsection, \
    LineBreak
from StructuresExplained.pdfconfig import header
from StructuresExplained.pdfconfig.translations.structure_strings import translate_PDF_structure


class Teacher:
    def __init__(self):
        self.ss = SystemElements()
        self.blank_ss = pickle.dumps(self.ss)
        self.moment_sum = ''
        self.moment_sum_from_forces = ''
        self.total_point_load_y = ''
        self.total_point_load_x = ''
        self.total_q_load_y = ''
        self.total_q_load_x = ''
        self.roll_distance = ''
        self.roll_reaction_y = ''
        self.roll_reaction_x = ''
        self.hinged_reaction_y = ''
        self.hinged_reaction_x = ''
        self.fixed_reaction_moment = ''
        self.fixed_reaction_y = ''
        self.fixed_reaction_x = ''
        self.Ba = None
        self.shear_equation_x = []
        self.shear_equation_y = []
        self.shear_equation_x_string = []
        self.angle = []
        self.eq_load = {}
        self.list_load_y = {}
        self.list_load_x = {}

    def reset(self):
        self.moment_sum = self.moment_sum_from_forces = self.total_point_load_x = self.total_point_load_y = \
            self.roll_distance = self.roll_reaction_y = self.roll_reaction_x = self.hinged_reaction_y = \
            self.hinged_reaction_x = self.fixed_reaction_moment = self.fixed_reaction_y = self.fixed_reaction_x = \
            self.total_q_load_x = self.total_q_load_y = self.Bstring = ''
        self.Ba = None
        self.shear_equation_x.clear()
        self.shear_equation_y.clear()
        self.shear_equation_x_string.clear()
        self.angle.clear()
        self.eq_load = {}
        self.list_load_x = {}
        self.list_load_y = {}
        self.ss = pickle.loads(self.blank_ss)
