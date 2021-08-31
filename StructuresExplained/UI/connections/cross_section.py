from sympy import Symbol
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from distutils.spawn import find_executable
import matplotlib.pyplot as plt
import os
import pickle
from StructuresExplained.pdfconfig.generator_thread import PDFGeneratorThread


class connections:
    def __init__(self, main_window):
        self.mw = main_window

    def set_sigma(self):
        self.mw.frame_16.setDisabled(True)
        if len(self.mw.sig.subareas_rectangle) != 0 or len(self.mw.sig.subareas_circle) != 0:
            self.mw.msx.setText(f"{self.mw.sig.moment_y}")
            self.mw.msy.setText(f"{self.mw.sig.moment_x}")
            self.mw.mix.setText(f"{self.mw.sig.moment_inertia_x}")
            self.mw.miy.setText(f"{self.mw.sig.moment_inertia_y}")
            self.mw.at.setText(f"{self.mw.sig.total_area}")

    def insert_sigma(self):
        self.mw.frame_16.setDisabled(False)

    def get_sigma_T(self):
        N = self.mw.filter(self.mw.tnormal.text())
        At = self.mw.filter(self.mw.at.text())
        My = self.mw.filter(self.mw.tmy.text())
        Mx = self.mw.filter(self.mw.tmz.text())
        Ix = self.mw.filter(self.mw.mix.text())
        Iy = self.mw.filter(self.mw.miy.text())
        y = Symbol('y')
        z = Symbol('z')
        if N != '' and At != '' and My != '' and Mx != '' and Ix != '' and Iy != '':
            if self.mw.specify_y.isChecked():
                y = self.mw.filter(self.mw.cs_y.text())
            if self.mw.specify_z.isChecked():
                z = self.mw.filter(self.mw.cs_z.text())
            results = self.mw.sig.det_normal_stress(N, At, My, Mx, Ix, Iy, self.mw.checkBox.isChecked(), y, z)
            self.mw.tnresult.setText(f'{results[0]}')
            self.mw.tneutral.setText(f"{results[1]}")
        else:
            self.mw.warning()

    def get_cis(self):
        if not self.mw.sig.subareas_circle and len(
                self.mw.sig.subareas_rectangle) >= 1 and self.mw.figureResultsButton.isChecked():
            try:
                V = self.mw.filter(self.mw.tshear.text())
                if self.mw.cut_y.text() == '':
                    self.mw.cut_y.setText("0")
                Q = self.mw.sig.calculate_static_moment_for_shear(self.mw.cut_y.text())
                self.mw.label_79.setText(Q)
                if self.mw.twidth.text() == '':
                    self.mw.twidth.setText('0')
                t = self.mw.filter(self.mw.twidth.text())
                Ix = self.mw.filter(self.mw.mix.text())
                results = self.mw.sig.det_shear_tension(V, Q, t, Ix, self.mw.checkBox_2.isChecked())
                self.mw.tfresult.setText(self.mw.scientific_format(results[0]))
                self.mw.tsresult.setText(self.mw.scientific_format(results[1]))
            except:
                self.mw.warning()
        else:
            msg = QMessageBox()
            msg.setWindowTitle(self.mw.shear_warning_title)
            msg.setText(self.mw.shear_warning_str)
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

    def change_table_rect(self):
        c = self.mw.rect_list.currentIndex()
        if self.mw.sig.subareas_rectangle.get(c) is not None:
            self.mw.rect_x1.setText(f"{self.mw.sig.subareas_rectangle[c][0]}")
            self.mw.rect_y1.setText(f"{self.mw.sig.subareas_rectangle[c][1]}")
            self.mw.rect_x2.setText(f"{self.mw.sig.subareas_rectangle[c][2]}")
            self.mw.rect_y2.setText(f"{self.mw.sig.subareas_rectangle[c][3]}")
        else:
            self.mw.clear_rect_text()
        if self.mw.rect_visualize.isChecked():
            self.mw.plot_sec()

    def change_table_circ(self):
        c = self.mw.circle_list.currentIndex()
        if self.mw.sig.subareas_circle.get(c) is not None:
            self.mw.circle_x.setText(f"{self.mw.sig.subareas_circle[c][0]}")
            self.mw.circle_y.setText(f"{self.mw.sig.subareas_circle[c][1]}")
            self.mw.circle_r.setText(f"{self.mw.sig.subareas_circle[c][2]}")
            self.mw.circle_ai.setText(f"{self.mw.sig.subareas_circle[c][3]}")
            # self.mw.circle_af.setText(f"{self.mw.sig.sub_areas_cir[c][4]}")
        else:
            self.mw.clear_cir_text()
        if self.mw.circle_visualize.isChecked():
            self.mw.plot_sec()

    def plot_sec(self, savefigure=False):
        p = d = None
        if self.mw.rect_visualize.isChecked():
            p = self.mw.rect_list.currentIndex()
        if self.mw.circle_visualize.isChecked():
            d = self.mw.circle_list.currentIndex()
        if self.mw.sig.subareas_circle or self.mw.sig.subareas_rectangle:
            fig = self.mw.sig.plot(p, d, self.mw.MplWidget.canvas.figure)
            self.mw.MplWidget.setGrid(self.mw.gridBox.isChecked())
            self.mw.MplWidget.plot(fig)
            self.mw.last_figure = self.mw.show_sec
        else:
            self.mw.MplWidget.plot(has_grid=self.mw.gridBox.isChecked())
            self.mw.last_figure = None
        self.mw.figurefix()
        self.mw.MplWidget.set_background_alpha()
    
    def add_rect(self):
        if self.mw.sig.shear_flux_numeric or self.mw.sig.normal_stress_numeric:
            if self.mw.geometry_change_prompt() == QMessageBox.Yes:
                self.mw.update_ret()
        else:
            self.mw.update_ret()

    def update_ret(self):
        if self.mw.rect_x1.text() != '' and self.mw.rect_y1.text() != '' and \
                self.mw.rect_x2.text() != '' and self.mw.rect_y2.text() != '':
            x1 = self.mw.filter(self.mw.rect_x1.text())
            y1 = self.mw.filter(self.mw.rect_y1.text())
            x2 = self.mw.filter(self.mw.rect_x2.text())
            y2 = self.mw.filter(self.mw.rect_y2.text())
            if float(y1) > float(y2) and float(x2) > float(x1):
                c = self.mw.rect_list.currentIndex()
                self.mw.sig.subareas_rectangle.update({c: [float(x1), float(y1),
                                                    float(x2), float(y2)]})
                self.mw.finish_applying()
            else:
                msg = QMessageBox()
                msg.setWindowTitle(self.mw.warning_title)
                msg.setText(self.mw.rect_values_error)
                msg.setIcon(QMessageBox.Warning)
                x = msg.exec_()
        else:
            self.mw.warning()

    def add_rect_item(self):
        c = len(self.mw.rect_list)
        self.mw.rect_list.addItem(f"Ret. {c + 1}")
        self.mw.rect_list.setCurrentIndex(c)

    def add_cir(self):
        if self.mw.sig.shear_flux_numeric or self.mw.sig.normal_stress_numeric:
            if self.mw.geometry_change_prompt() == QMessageBox.Yes:
                self.mw.update_cir()
        else:
            self.mw.update_cir()

    def update_cir(self):
        if self.mw.circle_x.text() != '' and self.mw.circle_y.text() != '' and \
                self.mw.circle_r.text() != '' and self.mw.circle_ai.text() != '':  # and self.mw.circle_af.text() != '':
            x = self.mw.filter(self.mw.circle_x.text())
            y = self.mw.filter(self.mw.circle_y.text())
            r = self.mw.filter(self.mw.circle_r.text())
            ai = self.mw.filter(self.mw.circle_ai.text())
            c = self.mw.circle_list.currentIndex()
            self.mw.sig.subareas_circle.update({c: [float(x), float(y),
                                                 float(r), float(ai)]})
            # self.mw.circle_af.text()]})
            self.mw.finish_applying()
        else:
            self.mw.warning()

    def add_cir_item(self):
        c = len(self.mw.circle_list)
        self.mw.circle_list.addItem(f"Cir. {c + 1}")
        self.mw.circle_list.setCurrentIndex(c)

    def finish_applying(self):
        self.mw.sig.calculate_values()
        if self.mw.figureResultsButton.isChecked():
            self.mw.set_sigma()
        self.mw.plot_sec()

    def remove_rectangle(self):
        c = self.mw.rect_list.currentIndex()
        try:
            self.mw.sig.subareas_rectangle.pop(c, None)
            self.mw.sig.calculate_values()
            if self.mw.figureResultsButton.isChecked():
                self.mw.set_sigma()
            self.mw.plot_sec()
            self.mw.change_table_rect()
        except:
            self.mw.transv_reset()

    def remove_circle(self):
        c = self.mw.circle_list.currentIndex()
        try:
            self.mw.sig.subareas_circle.pop(c, None)
            self.mw.sig.calculate_values()
            if self.mw.figureResultsButton.isChecked():
                self.mw.set_sigma()
            self.mw.plot_sec()
            self.mw.change_table_circ()
        except:
            self.mw.transv_reset()

    def transv_reset(self):
        self.mw.sig.subareas_rectangle.clear()
        self.mw.sig.subareas_circle.clear()
        self.mw.clear_rect_text()
        self.mw.clear_cir_text()
        self.mw.at.clear()
        self.mw.mix.clear()
        self.mw.miy.clear()
        self.mw.msx.clear()
        self.mw.msy.clear()
        self.mw.tnormal.clear()
        self.mw.tmy.clear()
        self.mw.tmz.clear()
        self.mw.tnresult.clear()
        self.mw.tneutral.clear()
        self.mw.tshear.clear()
        self.mw.tcontact.clear()
        self.mw.twidth.clear()
        self.mw.tfos.clear()
        self.mw.tsresult.clear()
        self.mw.tfresult.clear()
        self.mw.rect_visualize.setChecked(False)
        self.mw.circle_visualize.setChecked(False)
        self.mw.MplWidget.plot(has_grid=self.mw.gridBox.isChecked())
        self.mw.figurefix()
    
    def rm_solver(self):
        if find_executable('latex'):
            if self.mw.sig.subareas_circle or self.mw.sig.subareas_rectangle:
                file, ok = QFileDialog.getSaveFileName(self.mw, self.mw.pdf_title, self.mw.pdf_text, "PDF (*.pdf)")
                if ok:
                    try:
                        self.mw.toolBox.setCurrentIndex(1)
                        self.mw.setupLoading()
                        thread = PDFGeneratorThread(self.mw.loadingScreen,
                                                    self.mw.rm_savefig,
                                                    self.mw.sig.generate_pdf,
                                                    self.mw.language)
                        thread.start()
                        self.mw.loadingScreen.exec_()
                        if not self.mw.loadingUi.userTerminated:
                            os.replace("tmp\\resolucaorm.pdf", f"{file}")
                            self.mw.pdf_generated_prompt()
                        self.mw.deleteTempFolder()
                    except:
                        self.mw.latex_packages_warning()
            else:
                self.mw.warning()
        else:
            self.mw.latex_warning()

    def rm_savefig(self):
        self.mw.makeTempFolder()

        plt.style.use('default')
        p = d = None
        if self.mw.rect_visualize.isChecked():
            p = self.mw.rect_list.currentIndex()
        if self.mw.circle_visualize.isChecked():
            d = self.mw.circle_list.currentIndex()
        fig = self.mw.sig.plot(p, d, self.mw.MplWidget.canvas.figure)
        fig.savefig("tmp\\figs\\sectransv", transparent=True)
        plt.style.use('dark_background')
        self.mw.last_figure.click()
        
    def load_cross_section_aux(self, file):
        with open(f'{file}', 'rb') as f:
            _, self.mw.sig, _ = pickle.load(f)
        if self.mw.sig.subareas_circle or self.mw.sig.subareas_rectangle:
            self.mw.rect_list.clear()
            self.mw.circle_list.clear()
            for c in range(len(self.mw.sig.subareas_rectangle)):
                self.mw.add_rect_item()
            for c in range(len(self.mw.sig.subareas_circle)):
                self.mw.add_cir_item()
            self.mw.sig.calculate_values()
            if self.mw.figureResultsButton.isChecked():
                self.mw.set_sigma()
            self.mw.cross_loaded = True
    
    def clear_rect_text(self):
        self.mw.rect_x1.clear()
        self.mw.rect_y1.clear()
        self.mw.rect_x2.clear()
        self.mw.rect_y2.clear()

    def clear_cir_text(self):
        self.mw.circle_x.clear()
        self.mw.circle_y.clear()
        self.mw.circle_r.clear()
        self.mw.circle_ai.clear()
        self.mw.circle_af.clear()
        
    def geometry_change_prompt(self):
        box = QMessageBox()
        box.setText(self.mw.geometry_change_warning)
        box.setWindowTitle(self.mw.geometry_change_title)
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        box.setIcon(QMessageBox.Warning)
        choice = box.exec_()
        return choice
    
    def cs_y_enabler(self):
        if self.mw.specify_y.isChecked():
            self.mw.cs_y.setEnabled(True)
        else:
            self.mw.cs_y.setEnabled(False)

    def cs_z_enabler(self):
        if self.mw.specify_z.isChecked():
            self.mw.cs_z.setEnabled(True)
        else:
            self.mw.cs_z.setEnabled(False)