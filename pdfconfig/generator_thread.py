from PyQt5.QtCore import QThread
import pdfconfig.logo


class PDFGeneratorThread(QThread):

    def __init__(self, loadingScreen, fig_grabber, PDF_generator, language, ss=None, file=None):
        QThread.__init__(self)
        self.loadingScreen = loadingScreen
        self.fig_grabber = fig_grabber
        self.PDF_generator = PDF_generator
        self.language = language
        self.ss = ss
        self.file = file

    def __del__(self):
        self.wait()

    def run(self):
        self.fig_grabber()
        pdfconfig.logo.generate_logo()
        if self.ss is None and self.file is None:
            self.PDF_generator(self.language)
        else:
            self.PDF_generator(self.ss.supports_hinged, self.ss.supports_roll, self.ss.inclined_roll,
                               self.ss.supports_fixed, self.ss.loads_moment, self.ss.loads_point, self.ss.loads_q,
                               self.ss.loads_qi, self.ss.node_map, self.file, self.language)
        self.loadingScreen.close()
