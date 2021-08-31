from StructuresExplained.solutions.stress_states.calculator import calculator_plain_state, calculator_triple_state
from StructuresExplained.solutions.stress_states.fig_generation import fig_generator
from StructuresExplained.solutions.stress_states.pdf_generation import pdf_generator
from StructuresExplained.utils.util import save_figure, make_pdf_folder, make_figure_folder, delete_folder
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
                              tau_xy: float
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
                               tau_yz: float
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
                         show: Optional[bool] = False
                         ):

        fgen = fig_generator(self.plain_state, background_scheme)

        fig = fgen.plot_plain_state()

        if show:
            fig.show()
        else:
            return fig

    def plot_triple_state(self,
                          background_scheme: Optional[str] = "bright",
                          show: Optional[bool] = False
                          ):

        fgen = fig_generator(self.triple_state, background_scheme)

        fig = fgen.plot_triple_state()

        if show:
            fig.show()
        else:
            return fig

    def generate_pdf_plain_state(self,
                                 language: str,
                                 pdf_path: Optional[str] = "pdf",
                                 clear=True
                                 ):
        """
        creates a folder to generate the figure and logo into
        language: "EN" for english or "PT" for brazilian portuguese
        pdf_path: path where pdf will be generated
        clear: delete figures generated for pdf after pdf is generated
        """

        make_pdf_folder(pdf_path)
        make_figure_folder(pdf_path)

        self.pdfgen = pdf_generator(self, self.plain_state)
        figure = self.plot_plain_state()

        save_figure(figure, pdf_path + r"\figs\mohrfig")
        generate_logo(pdf_path)

        self.pdfgen.generate_pdf_plain_state(language, pdf_path)

        if clear:
            delete_folder(pdf_path + r'\figs')

    def generate_pdf_triple_state(self,
                                  language: str,
                                  pdf_path: Optional[str] = "pdf",
                                  clear=True
                                  ):
        """
        creates a folder to generate the figure and logo into
        language: "EN" for english or "PT" for brazilian portuguese
        pdf_path: path where pdf will be generated
        clear: delete figures generated for pdf after pdf is generated
        """

        make_pdf_folder(pdf_path)
        make_figure_folder(pdf_path)

        self.pdfgen = pdf_generator(self, self.triple_state)
        figure = self.plot_triple_state()

        save_figure(figure, pdf_path + r"\figs\mohrfig")
        generate_logo(pdf_path)

        self.pdfgen.generate_pdf_triple_state(language, pdf_path)

        if clear:
            delete_folder(pdf_path + r'\figs')

    def on_release(self, fig):
        if 80 < abs(float(fig.gca(projection="3d").azim)) < 100 and -10 < abs(
                float(fig.gca(projection="3d").elev)) < 10:
            fig.clear()
            return self.plain_state(self.sx, self.sy, self.txy, fig)
        elif -10 < abs(float(fig.gca(projection="3d").azim)) < 10 and -10 < abs(
                float(fig.gca(projection="3d").elev)) < 10:
            fig.clear()
            return self.plain_state(self.sz, self.sy, self.tyz, fig)
        elif -10 < abs(float(fig.gca(projection="3d").azim)) < 10 and 80 < abs(
                float(fig.gca(projection="3d").elev)) < 100:
            fig.clear()
            return self.plain_state(self.sz, self.sx, self.txz, fig)
        elif 170 < abs(float(fig.gca(projection="3d").azim)) < 190 and -10 < abs(
                float(fig.gca(projection="3d").elev)) < 10:
            fig.clear()
            return self.plain_state(self.sz, self.sy, self.tyz, fig)
        elif 80 < abs(float(fig.gca(projection="3d").azim)) < 100 and 80 < abs(
                float(fig.gca(projection="3d").elev)) < 100:
            fig.clear()
            return self.plain_state(self.sz, self.sx, self.txz, fig)
        else:
            return fig


if __name__ == "__main__":
    test = manager()
    test.calculate_plain_state(10, 20, 30)
    test.print_results_plain_state()
    test.plot_plain_state(show=True)
    test.generate_pdf_plain_state("PT")
    # test.calculate_triple_state(10, 20, 30, 40, 50, 60)
    # test.plot_triple_state()
    # test.generate_pdf_triple_state("PT")
