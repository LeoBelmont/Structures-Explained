from PyQt5.QtWidgets import QFileDialog
from distutils.spawn import find_executable
import pickle
from StructuresExplained.pdfconfig.generator_thread import PDFGeneratorThread
from StructuresExplained.solutions.stress_states.manager import manager


class connections:
    def __init__(self, main_window, visualize):
        self.mw = main_window
        self.visualize = visualize
        self.mng = manager()

    def mohr_solver(self):
        if find_executable('latex'):
            if self.mng.plain_state.sigma_x is not None:
                file, ok = QFileDialog.getSaveFileName(self.mw, self.mw.pdf_title, self.mw.pdf_text, "PDF (*.pdf)")
                if ok:
                    # try:
                        self.mw.toolBox.setCurrentIndex(2)
                        self.mw.MplWidget.fix_plot_scale()
                        self.mw.setupLoading()
                        if self.mw.radio_plane.isChecked():
                            thread = PDFGeneratorThread(self.mw.loadingScreen,
                                                        self.mng.generate_pdf_plain_state,
                                                        self.mw.language)
                        else:
                            thread = PDFGeneratorThread(self.mw.loadingScreen,
                                                        self.mng.generate_pdf_triple_state,
                                                        self.mw.language)
                        thread.start()
                        self.mw.loadingScreen.exec_()
                        if not self.mw.loadingUi.userTerminated:
                            self.mw.pdf_generated_prompt()
                        self.mw.deleteTempFolder()
                    # except:
                    #     self.mw.latex_packages_warning()
            else:
                self.mw.warning()
        else:
            self.mw.latex_warning()
    
    def load_mohr_aux(self, file):
        with open(f'{file}', 'rb') as f:
            _, _, self.mw.mohr = pickle.load(f)
        self.mw.mohr_loaded = True

    def draw_stress_state(self):
        sx = self.mw.sx.text()
        sy = self.mw.sy.text()
        txy = self.mw.txy.text()
        sz = self.mw.sz.text()
        txz = self.mw.txz.text()
        tyz = self.mw.tyz.text()
        if self.mw.radio_plane.isChecked():
            if sx != '' and sy != '' and txy != '':
                self.draw_plain_state(sx, sy, txy)
            else:
                self.mw.warning()
        elif self.mw.radio_triple.isChecked():
            if sx != '' and sy != '' and sz != '' and txy != '' and txz != '' and tyz != '':
                self.draw_triple_state(sx, sy, sz, txy, txz, tyz)
            else:
                self.mw.warning()

    def draw_plain_state(self, sx, sy, txy):
        self.mng.calculate_plain_state(float(sx), float(sy), float(txy))
        self.plot_to_ui(
            self.mng.plot_plain_state(show=False, background_scheme="dark")
                )

    def draw_triple_state(self, sx, sy, sz, txy, txz, tyz):
        self.mng.calculate_triple_state(float(sx), float(sy), float(sz), float(txy), float(txz), float(tyz))
        self.plot_to_ui(
            self.mng.plot_triple_state(show=False, background_scheme="dark")
        )
    
    def switch_states_plane(self):
        self.mw.label_19.setHidden(True)
        self.mw.label_20.setHidden(True)
        self.mw.label_21.setHidden(True)
        self.mw.label_119.setHidden(True)
        self.mw.label_121.setHidden(True)
        self.mw.label_122.setHidden(True)
        self.mw.sz.setHidden(True)
        self.mw.txz.setHidden(True)
        self.mw.tyz.setHidden(True)

    def switch_states_triple(self):
        self.mw.label_19.setHidden(False)
        self.mw.label_20.setHidden(False)
        self.mw.label_21.setHidden(False)
        self.mw.label_119.setHidden(False)
        self.mw.label_121.setHidden(False)
        self.mw.label_122.setHidden(False)
        self.mw.sz.setHidden(False)
        self.mw.txz.setHidden(False)
        self.mw.tyz.setHidden(False)
        
    def plot_to_ui(self, figure):
        self.visualize(figure)
        self.mw.last_figure = self.mw.show_mohr
        self.mw.MplWidget.set_background_alpha(0)
