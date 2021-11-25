from matplotlib.pyplot import Figure
from matplotlib import pyplot as plt

from StructuresExplained.solutions.stress_states.calculator import calculator_plain_state, calculator_triple_state
from StructuresExplained.solutions.stress_states.fig_generation import fig_generator
from StructuresExplained.solutions.stress_states.pdf_generation import pdf_generator
from StructuresExplained.utils.util import save_figure, make_folder, make_figure_folder, delete_folder
from StructuresExplained.pdfconfig.logo import generate_logo

from typing import (
    Optional,
)


class manager:
    def __init__(self):
        self.plain_state = calculator_plain_state()
        self.triple_state = calculator_triple_state()

    def calculate_plain_state(self,
                              sigma_x: float,
                              sigma_y: float,
                              tau_xy: float,
                              ):

        self.plain_state.sigma_x = sigma_x
        self.plain_state.sigma_y = sigma_y
        self.plain_state.tau_xy = tau_xy
        self.plain_state.calculate()

    def calculate_triple_state(self,
                               sigma_x: float,
                               sigma_y: float,
                               sigma_z: float,
                               tau_xy: float,
                               tau_xz: float,
                               tau_yz: float,
                               ):

        self.triple_state.sigma_x = sigma_x
        self.triple_state.sigma_y = sigma_y
        self.triple_state.sigma_z = sigma_z
        self.triple_state.tau_xy = tau_xy
        self.triple_state.tau_xz = tau_xz
        self.triple_state.tau_yz = tau_yz
        self.triple_state.calculate()

    def print_results_plain_state(self):
        attrs = vars(self.plain_state)
        for key, value in attrs.items():
            print(f'{key}: {value}')

    def print_results_triple_state(self):
        attrs = vars(self.triple_state)
        for key, value in attrs.items():
            print(f'{key}: {value}')

    def plot_plain_state(self,
                         background_scheme: Optional[str] = "bright",
                         show: Optional[bool] = False,
                         fig: Optional[Figure] = plt.figure(),
                         ):

        fig.clear()
        fgen = fig_generator(self.plain_state, background_scheme)

        plot = fgen.plot_plain_state(fig)

        if show:
            plt.show()
        else:
            return plot

    def plot_triple_state(self,
                          background_scheme: Optional[str] = "bright",
                          show: Optional[bool] = False,
                          fig: Optional[Figure] = plt.figure(),
                          ):

        fig.clear()
        fgen = fig_generator(self.triple_state, background_scheme)

        plot = fgen.plot_triple_state(fig)

        if show:
            plt.show()
        else:
            return plot

    def generate_pdf_plain_state(self,
                                 language: str,
                                 pdf_path: Optional[str] = "pdf",
                                 filename: Optional[str] = "plain-state",
                                 clear=True
                                 ):
        """
        creates a folder to generate the figure and logo into
        language: "EN" for english or "PT" for brazilian portuguese
        pdf_path: path where pdf will be generated
        clear: delete figures generated for pdf after pdf is generated
        """

        make_folder(pdf_path)
        make_figure_folder(pdf_path)

        self.pdfgen = pdf_generator(self, self.plain_state)
        figure = self.plot_plain_state()

        save_figure(figure, pdf_path + r"\figs\mohrfig")
        generate_logo(pdf_path)

        self.pdfgen.generate_pdf_plain_state(language, pdf_path, filename)

        if clear:
            delete_folder(pdf_path + r'\figs')

    def generate_pdf_triple_state(self,
                                  language: str,
                                  pdf_path: Optional[str] = "pdf",
                                  filename: Optional[str] = "triple-state",
                                  clear=True
                                  ):
        """
        creates a folder to generate the figure and logo into
        language: "EN" for english or "PT" for brazilian portuguese
        pdf_path: path where pdf will be generated
        clear: delete figures generated for pdf after pdf is generated
        """

        make_folder(pdf_path)
        make_figure_folder(pdf_path)

        self.pdfgen = pdf_generator(self, self.triple_state)
        figure = self.plot_triple_state()

        save_figure(figure, pdf_path + r"\figs\mohrfig")
        generate_logo(pdf_path)

        self.pdfgen.generate_pdf_triple_state(language, pdf_path, filename)

        if clear:
            delete_folder(pdf_path + r'\figs')


if __name__ == "__main__":
    test = manager()
    test.calculate_plain_state(10, 20, 30)
    # test.print_results_plain_state()
    test.plot_plain_state(show=True)
    # test.generate_pdf_plain_state("PT")
    # test.calculate_triple_state(10, 20, 30, 40, 50, 60)
    # test.print_results_triple_state()
    # test.plot_triple_state(show=True)
    # test.generate_pdf_triple_state("PT")
