from matplotlib import pyplot as plt
from matplotlib.pyplot import savefig
from StructuresExplained.solutions.structure.fig_generation import fig_generator

from typing import (
    Union,
    List,
    Dict,
)


class manager:
    def __init__(self):
        pass

    def assemble(self):
        if (len(self.hinged) == 1 and len(self.roll) == 1) or len(self.fixed) == 1:
            self.reset()

    def generate_figures(self):
        plt.style.use('default')
        fig_generator().draw_structure()
        plt.style.use('dark_background')
