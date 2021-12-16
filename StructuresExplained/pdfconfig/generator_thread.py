from PyQt5.QtCore import QThread
import StructuresExplained.pdfconfig.logo


class PDFGeneratorThread(QThread):

    def __init__(self,
                 PDF_generator,
                 language,
                 pdf_path: str = "pdf",
                 filename: str = "solution",
                 solve_path: str = None,
                 ):
        QThread.__init__(self)
        self.PDF_generator = PDF_generator
        self.language = language
        self.pdf_path = pdf_path
        self.filename = filename
        self.solve_path = solve_path

    def __del__(self):
        self.wait()

    def run(self):
        StructuresExplained.pdfconfig.logo.generate_logo(pdf_path=self.pdf_path)
        if self.solve_path:
            self.PDF_generator(self.language, pdf_path=self.pdf_path, filename=self.filename, main_path=self.solve_path)
        else:
            self.PDF_generator(self.language, pdf_path=self.pdf_path, filename=self.filename)
