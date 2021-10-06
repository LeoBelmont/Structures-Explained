from StructuresExplained.solutions.structure.assembler import Assembler as ia
from StructuresExplained.solutions.structure.data_fetcher import Assembler as sa
from StructuresExplained.solutions.structure.pdf_generation import pdf_generator
from StructuresExplained.solutions.structure.fig_generation import fig_generator
from StructuresExplained.utils.util import make_pdf_folder, make_figure_folder
from StructuresExplained.pdfconfig.logo import generate_logo
from anastruct import SystemElements
from enum import Enum

from typing import (
    Union,
    List,
    Dict,
)


class manager:
    def __init__(self, system_elements):
        self.ss = system_elements

    def main(self):
        self.ss.solve()
        self.ss.show_reaction_force(show=False)
        self.ss.show_structure()
        df = sa(self.ss)
        df.assemble_structure()
        ass = ia(self.ss)
        ass.assemble_structure()
        make_pdf_folder("tmp")
        make_figure_folder("tmp")
        self.gen_pdf_figures()
        generate_logo("tmp")
        gen = pdf_generator(df.results, ass.internal_results, self.ss, "PT", target_dir="tmp")
        gen.generatePDF()
        # [[print(f"section {element.id}-{sub_index + 1}: {sympify(sub_string, evaluate=False)}") for sub_index, sub_string in
        #   enumerate(string)] for element, string in ass.sections_strings.items()]
        # [print(element.id, values) for element, values in ass.sections_strings.items()]
        [print(element.id, values) for element, values in ass.internal_stresses_dict.items()]

    def gen_pdf_figures(self) -> None:
        gen = fig_generator(self.ss)
        gen.generate_figures_for_pdf()


def test_struct2():
    ss = SystemElements()
    ss.add_element([[0, 0], [1, 0]])
    ss.add_element([[1, 0], [1, 1]])
    ss.add_element([[1, 0], [2, 0]])
    ss.add_element([[2, 0], [3, 0]])
    ss.add_element([[3, 0], [4, 1]])
    ss.add_element([[4, 1], [5, 1]])
    ss.point_load(2, Fy=10)
    ss.point_load(3, Fy=-20)
    ss.point_load(4, Fy=-30)
    ss.point_load(5, Fx=-40)
    ss.moment_load(2, Ty=-9)
    ss.moment_load(1, 7)
    ss.moment_load(3, 3)
    ss.q_load(element_id=3, q=(-10, -20))
    ss.add_support_roll(4, angle=10)
    ss.add_support_hinged(5)
    # ss.add_support_fixed(3)

    mn = manager(ss)
    mn.main()


if __name__ == "__main__":
    test_struct2()
