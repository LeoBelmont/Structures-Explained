from StructuresExplained.solutions.structure.internal_stresses.assembler import Assembler as ia
from StructuresExplained.utils.util import make_pdf_folders
from StructuresExplained.solutions.structure.reactions.assembler import Assembler as sa
from StructuresExplained.solutions.structure.pdf_generation.generator import Generator
from StructuresExplained.solutions.structure.fig_generation.artist import Artist
from StructuresExplained.pdfconfig.logo import generate_logo
from typing import Optional, Tuple


class Manager:
    def __init__(self, system_elements):
        self.ss = system_elements
        self.reactions = sa(system_elements)
        self.internal = ia(system_elements)

    def generate_pdf(self,
                     language: Optional[str] = "PT",
                     pdf_path: Optional[str] = "tmp",
                     filename: Optional[str] = "solution",
                     main_path: Optional[str] = None,
                     ):

        self.ss.solve()
        self.ss.show_structure(show=False)
        self.ss.show_reaction_force(show=False)

        make_pdf_folders(pdf_path)

        self.__assemble_reactions()

        self.__assemble_internal_stresses(pdf_path, main_path)

        self.__make_figures(pdf_path)

        self.__generate_pdf(language, pdf_path, filename)

    def __assemble_reactions(self):
        self.reactions.assemble_structure()

    def __assemble_internal_stresses(self, target_dir, main_path):
        if main_path:
            self.internal.assemble_structure(target_dir=target_dir, main_path=main_path),
        else:
            self.internal.assemble_structure(target_dir=target_dir)

    def __make_figures(self, target_dir):
        self.__gen_pdf_figures(target_dir)
        generate_logo(target_dir)

    def __gen_pdf_figures(self, target_dir) -> None:
        gen = Artist(self.ss, target_dir=target_dir)
        gen.generate_figures_for_pdf()

    def __generate_pdf(self, language, target_dir, filename):
        gen = Generator(self.reactions.results, self.internal.internal_results, self.ss, language, target_dir, filename)
        gen.generate_pdf()
