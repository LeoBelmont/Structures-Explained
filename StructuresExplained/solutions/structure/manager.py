from StructuresExplained.solutions.structure.assembler import Assembler as ia
from StructuresExplained.solutions.structure.data_fetcher import Assembler as sa
from StructuresExplained.solutions.structure.pdf_generation import pdf_generator
from StructuresExplained.solutions.structure.fig_generation import fig_generator
from StructuresExplained.utils.util import make_pdf_folder, make_figure_folder
from StructuresExplained.pdfconfig.logo import generate_logo
from anastruct import SystemElements


class manager:
    def __init__(self, system_elements):
        self.ss = system_elements

    def generate_pdf(self, language="PT", target_dir="tmp"):
        self.ss.solve()
        self.ss.show_structure()
        self.ss.show_reaction_force(show=True)

        make_pdf_folder(target_dir)
        make_figure_folder(target_dir)

        df = sa(self.ss)
        df.assemble_structure()

        ass = ia(self.ss)
        ass.assemble_structure(target_dir=target_dir)

        self.gen_pdf_figures(target_dir)
        generate_logo(target_dir)

        gen = pdf_generator(df.results, ass.internal_results, self.ss, language, target_dir)
        gen.generatePDF()

    def gen_pdf_figures(self, target_dir) -> None:
        gen = fig_generator(self.ss, target_dir=target_dir)
        gen.generate_figures_for_pdf()


def test_struct():
    ss = SystemElements()
    ss.add_element([[0, 0], [1, 0]])
    ss.add_element([[1, 0], [1, 1]])
    ss.add_element([[1, 0], [2, 0]])
    ss.add_element([[2, 0], [3, 0]])
    ss.add_element([[3, 0], [4, 1]])
    ss.add_element([[4, 1], [5, 1]])
    ss.point_load(2, Fy=10)
    ss.point_load(3, Fy=-20, Fx=5)
    ss.point_load(4, Fy=-30)
    ss.point_load(5, Fx=-40)
    ss.moment_load(2, Ty=-9)
    ss.moment_load(1, 7)
    ss.moment_load(3, 3)
    ss.q_load(element_id=3, q=(-10, -20))
    ss.q_load(element_id=5, q=(-10, -20))
    ss.add_support_roll(4)
    ss.add_support_hinged(5)
    # ss.add_support_fixed(3)

    mn = manager(ss)
    mn.generate_pdf(target_dir=r"C:\testfolder")


if __name__ == "__main__":
    test_struct()
