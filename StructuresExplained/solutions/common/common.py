from StructuresExplained.utils.util import save_figure, make_pdf_folder, make_figure_folder, delete_folder
from StructuresExplained.pdfconfig.logo import generate_logo

from typing import (
    Optional,
)


def generate_pdf(
        plot_figure,
        pdf_generator,
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

    pdfgen = pdf_generator
    figure = plot_figure

    save_figure(figure, pdf_path + r"\figs\mohrfig")
    generate_logo(pdf_path)

    self.pdfgen.generate_pdf_plain_state(language, pdf_path)

    if clear:
        delete_folder(pdf_path + r'\figs')
