from PyQt5.QtCore import QThread
import StructuresExplained.pdfconfig.logo


class PDFGeneratorThread(QThread):

    def __init__(self,
                 loadingScreen,
                 PDF_generator,
                 language,
                 pdf_path: str = "pdf",
                 ss=None,
                 file=None,
                 filename: str = "solution",
                 ):
        QThread.__init__(self)
        self.loadingScreen = loadingScreen
        self.PDF_generator = PDF_generator
        self.language = language
        self.pdf_path = pdf_path
        self.filename = filename
        self.ss = ss
        self.file = file

    def __del__(self):
        self.wait()

    def run(self):
        StructuresExplained.pdfconfig.logo.generate_logo(pdf_path=self.pdf_path)
        if self.ss is None and self.file is None:
            self.PDF_generator(self.language, pdf_path=self.pdf_path, filename=self.filename)
        else:
            self.PDF_generator(self.ss.supports_hinged, self.ss.supports_roll, self.ss.inclined_roll,
                               self.ss.supports_fixed, self.ss.loads_moment, self.ss.loads_point, self.ss.loads_q,
                               self.ss.loads_qi, self.ss.system, self.file, self.language)
        self.loadingScreen.close()
