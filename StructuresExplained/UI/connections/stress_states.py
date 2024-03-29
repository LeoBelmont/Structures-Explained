from PyQt5.QtWidgets import QFileDialog
from distutils.spawn import find_executable
import pickle
from StructuresExplained.pdfconfig.generator_thread import PDFGeneratorThread
from StructuresExplained.solutions.stress_states.manager import manager
from StructuresExplained.utils.util import make_pdf_folders, delete_folder, split_dir_filename


class connections:
    def __init__(self, main_window, functions, visualize):
        self.mw = main_window
        self.fn = functions
        self.visualize = visualize
        self.mng = manager()
        self.current_state = None

    def generator_thread(self, clean=True):
        if find_executable('latex'):
            if self.mng.plain_state.sigma_x is not None:
                file, ok = QFileDialog.getSaveFileName(self.mw, self.mw.pdf_title, self.mw.pdf_text, "PDF (*.pdf)")
                if ok:
                    try:
                        self.mw.toolBox.setCurrentIndex(2)
                        self.mw.MplWidget.fix_plot_scale()
                        pdf_dir, filename = split_dir_filename(file)
                        make_pdf_folders(pdf_dir)
                        if self.mw.radio_plane.isChecked():
                            pdf_generator_thread = PDFGeneratorThread(
                                self.mng.generate_pdf_plain_state,
                                self.mw.language,
                                pdf_path=pdf_dir,
                                filename=filename,
                            )
                        else:
                            pdf_generator_thread = PDFGeneratorThread(
                                self.mng.generate_pdf_triple_state,
                                self.mw.language,
                                pdf_path=pdf_dir,
                                filename=filename,
                            )

                        self.fn.setupLoading(pdf_generator_thread)

                        pdf_generator_thread.finished.connect(self.on_finished)

                        pdf_generator_thread.start()
                        self.mw.loadingScreen.exec_()

                        if not self.mw.loadingUi.userTerminated:
                            self.fn.pdf_generated_prompt()
                        if clean:
                            delete_folder(pdf_dir)
                    except:
                        self.fn.latex_packages_warning()
            else:
                self.fn.warning()
        else:
            self.fn.latex_warning()

    def on_finished(self):
        self.mw.loadingScreen.close()

    def load_mohr_aux(self, file):
        with open(f'{file}', 'rb') as f:
            _, _, self.mng = pickle.load(f)
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
                self.draw_plain_state(sx, sy, txy, self.mw.MplWidget.canvas.figure)
                self.current_state = "plane"
            else:
                self.fn.warning()
        elif self.mw.radio_triple.isChecked():
            if sx != '' and sy != '' and sz != '' and txy != '' and txz != '' and tyz != '':
                self.draw_triple_state(sx, sy, sz, txy, txz, tyz, self.mw.MplWidget.canvas.figure)
                self.current_state = "triple"
            else:
                self.fn.warning()

    def draw_plain_state(self, sx, sy, txy, figure):
        self.mng.calculate_plain_state(float(sx), float(sy), float(txy))
        self.plot_to_ui(
            self.mng.plot_plain_state(show=False, background_scheme="dark", fig=figure)
        )

    def draw_triple_state(self, sx, sy, sz, txy, txz, tyz, figure):
        self.mng.calculate_triple_state(float(sx), float(sy), float(sz), float(txy), float(txz), float(tyz))
        self.plot_to_ui(
            self.mng.plot_triple_state(show=False, background_scheme="dark", fig=figure)
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
        ax = figure.get_axes()
        for i in range(len(ax)):
            ax[i].patch.set_alpha(0)
        self.mw.last_figure = self.mw.show_mohr

    def on_release(self, fig):
        if 80 < abs(float(fig.gca(projection="3d").azim)) < 100 and -10 < abs(
                float(fig.gca(projection="3d").elev)) < 10:
            fig.clear()
            self.draw_plain_state(self.mw.sx.text(), self.mw.sy.text(), self.mw.txy.text(), fig)
        elif -10 < abs(float(fig.gca(projection="3d").azim)) < 10 and -10 < abs(
                float(fig.gca(projection="3d").elev)) < 10:
            fig.clear()
            self.draw_plain_state(self.mw.sz.text(), self.mw.sy.text(), self.mw.tyz.text(), fig)
        elif -10 < abs(float(fig.gca(projection="3d").azim)) < 10 and 80 < abs(
                float(fig.gca(projection="3d").elev)) < 100:
            fig.clear()
            self.draw_plain_state(self.mw.sz.text(), self.mw.sx.text(), self.mw.txz.text(), fig)
        elif 170 < abs(float(fig.gca(projection="3d").azim)) < 190 and -10 < abs(
                float(fig.gca(projection="3d").elev)) < 10:
            fig.clear()
            self.draw_plain_state(self.mw.sz.text(), self.mw.sy.text(), self.mw.tyz.text(), fig)
        elif 80 < abs(float(fig.gca(projection="3d").azim)) < 100 and 80 < abs(
                float(fig.gca(projection="3d").elev)) < 100:
            fig.clear()
            self.draw_plain_state(self.mw.sz.text(), self.mw.sx.text(), self.mw.txz.text(), fig)
