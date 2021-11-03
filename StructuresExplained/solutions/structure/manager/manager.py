from StructuresExplained.solutions.structure.internal_stresses.assembler import Assembler as ia
from StructuresExplained.utils.util import make_pdf_folders
from StructuresExplained.solutions.structure.reactions.assembler import Assembler as sa
from StructuresExplained.solutions.structure.pdf_generation.generator import Generator
from StructuresExplained.solutions.structure.fig_generation.artist import Artist
from StructuresExplained.pdfconfig.logo import generate_logo


class manager:
    def __init__(self, system_elements):
        self.ss = system_elements
        self.reactions = sa(system_elements)
        self.internal = ia(system_elements)

    def generator(self, language="PT", target_dir="tmp"):
        self.ss.solve()
        self.ss.show_structure()
        self.ss.show_reaction_force(show=True)

        make_pdf_folders(target_dir)

        self.__assemble_reactions()

        self.__assemble_internal_stresses(target_dir)

        self.__make_figures(target_dir)

        self.__generate_pdf(language, target_dir)

    def __assemble_reactions(self):
        self.reactions.assemble_structure()

    def __assemble_internal_stresses(self, target_dir):
        self.internal.assemble_structure(target_dir=target_dir)

    def __make_figures(self, target_dir):
        self.__gen_pdf_figures(target_dir)
        generate_logo(target_dir)

    def __gen_pdf_figures(self, target_dir) -> None:
        gen = Artist(self.ss, target_dir=target_dir)
        gen.generate_figures_for_pdf()

    def __generate_pdf(self, language, target_dir):
        gen = Generator(self.reactions.results, self.internal.internal_results, self.ss, language, target_dir)
        gen.generate_pdf()
