from sympy import Symbol
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from distutils.spawn import find_executable
import matplotlib.pyplot as plt
import os
import pickle
from StructuresExplained.pdfconfig.generator_thread import PDFGeneratorThread
from StructuresExplained.solutions.cross_section.manager import Manager
from StructuresExplained.utils.util import delete_folder, split_dir_filename, make_pdf_folders, rounded_result, \
    round_expr, set_axes_alpha


class connections:
    def __init__(self, main_window, main_window_functions):
        self.mw = main_window
        self.fn = main_window_functions
        self.mn = Manager()

    def set_sigma(self):
        self.mw.frame_16.setDisabled(True)
        if len(self.mn.calc.subareas_rectangle) != 0 or len(self.mn.calc.subareas_circle) != 0:
            self.mn.calculate_geometrical_properties()
            self.mw.msx.setText(f"{rounded_result(self.mn.calc.moment_x)}")
            self.mw.msy.setText(f"{rounded_result(self.mn.calc.moment_y)}")
            self.mw.mix.setText(f"{rounded_result(self.mn.calc.moment_inertia_x)}")
            self.mw.miy.setText(f"{rounded_result(self.mn.calc.moment_inertia_y)}")
            self.mw.at.setText(f"{rounded_result(self.mn.calc.total_area)}")

    def insert_sigma(self):
        self.mw.frame_16.setDisabled(False)

    def get_sigma_T(self):
        N = self.fn.filter(self.mw.tnormal.text())
        At = self.mw.at.text()
        My = self.mw.tmy.text()
        Mx = self.mw.tmz.text()
        Ix = self.mw.mix.text()
        Iy = self.mw.miy.text()
        y = Symbol('y')
        z = Symbol('z')
        if N != '' and At != '' and My != '' and Mx != '' and Ix != '' and Iy != '':
            self.check_for_user_inputs()
            if self.mw.specify_y.isChecked():
                y = self.fn.filter(self.mw.cs_y.text())
            if self.mw.specify_z.isChecked():
                z = self.fn.filter(self.mw.cs_z.text())
            normal_stress, _, _ = self.mn.calculate_normal_stress(N, y, z, self.mw.checkBox.isChecked())
            _, neutral_line, _, _ = self.mn.calculate_neutral_line(N, y, z, self.mw.checkBox.isChecked(), normal_stress)
            self.mw.tnresult.setText(f'{rounded_result(normal_stress)}')
            self.mw.tneutral.setText(f"{round_expr(neutral_line)}")
        else:
            self.fn.warning()

    def get_cis(self):
        if not self.mn.calc.subareas_circle and len(
                self.mn.calc.subareas_rectangle) >= 1 and self.mw.figureResultsButton.isChecked():
            V_text = self.mw.tshear.text()
            if V_text != "":
                self.check_for_user_inputs()
                if self.mw.cut_y.text() == '':
                    self.mw.cut_y.setText("0")
                if self.mw.twidth.text() == '':
                    self.mw.twidth.setText('0')
                V = float(self.fn.filter(V_text))
                cut_height = float(self.fn.filter(self.mw.cut_y.text()))
                t = float(self.fn.filter(self.mw.twidth.text()))
                shear_stress, Q = self.mn.calculate_shear_stress(V, t, cut_height, self.mw.checkBox_2.isChecked())
                shear_flux, _ = self.mn.calculate_shear_flux(V, cut_height, self.mw.checkBox_2.isChecked())
                self.mw.tfresult.setText(str(rounded_result(shear_stress)))
                self.mw.tsresult.setText(str(rounded_result(shear_flux)))
                self.mw.label_79.setText(str(rounded_result(Q)))
            else:
                self.fn.warning()
        else:
            msg = QMessageBox()
            msg.setWindowTitle(self.mw.shear_warning_title)
            msg.setText(self.mw.shear_warning_str)
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

    def change_table_rect(self):
        c = self.mw.rect_list.currentIndex() + 1
        rect = self.mn.calc.subareas_rectangle.get(c)
        if rect is not None:
            self.mw.rect_x1.setText(f"{rect[0]}")
            self.mw.rect_y1.setText(f"{rect[1]}")
            self.mw.rect_x2.setText(f"{rect[2]}")
            self.mw.rect_y2.setText(f"{rect[3]}")
        else:
            self.clear_rect_text()
        if self.mw.rect_visualize.isChecked():
            self.plot_sec()

    def change_table_circ(self):
        c = self.mw.circle_list.currentIndex() + 1
        circle = self.mn.calc.subareas_circle.get(c)
        if circle is not None:
            self.mw.circle_x.setText(f"{circle[0]}")
            self.mw.circle_y.setText(f"{circle[1]}")
            self.mw.circle_r.setText(f"{circle[2]}")
            self.mw.circle_ai.setText(f"{circle[3]}")
            # self.mw.circle_af.setText(f"{self.mw.sig.sub_areas_cir[c][4]}")
        else:
            self.clear_cir_text()
        if self.mw.circle_visualize.isChecked():
            self.plot_sec()

    def plot_sec(self):
        p = d = None
        if self.mw.rect_visualize.isChecked():
            p = self.mw.rect_list.currentIndex() + 1
        if self.mw.circle_visualize.isChecked():
            d = self.mw.circle_list.currentIndex() + 1
        if self.mn.calc.subareas_circle or self.mn.calc.subareas_rectangle:
            fig = self.mn.show_cross_section(False, p, d, self.mw.MplWidget.canvas.figure)
            self.mw.MplWidget.setGrid(self.mw.gridBox.isChecked())
            self.mw.MplWidget.plot(fig)
            self.mw.last_figure = self.mw.show_sec
        else:
            self.mw.MplWidget.plot(has_grid=self.mw.gridBox.isChecked())
            self.mw.last_figure = None
        self.fn.figurefix()
        self.mw.MplWidget.set_background_alpha()
        set_axes_alpha(self.mw.MplWidget.canvas.figure)

    def add_rect(self):
        if self.mn.calc.shear_flux or self.mn.calc.normal_stress:
            if self.geometry_change_prompt() == QMessageBox.Yes:
                self.mn.calc.shear_flux = ""
                self.mn.calc.normal_stress = ""
                self.update_ret()
        else:
            self.update_ret()

    def update_ret(self):
        if self.mw.rect_x1.text() != '' and self.mw.rect_y1.text() != '' and \
                self.mw.rect_x2.text() != '' and self.mw.rect_y2.text() != '':
            x1 = float(self.fn.filter(self.mw.rect_x1.text()))
            y1 = float(self.fn.filter(self.mw.rect_y1.text()))
            x2 = float(self.fn.filter(self.mw.rect_x2.text()))
            y2 = float(self.fn.filter(self.mw.rect_y2.text()))
            if y1 > y2 and x2 > x1:
                self.mn.add_rectangular_subarea((x1, y1), (x2, y2), subarea_id=self.mw.rect_list.currentIndex() + 1)
                self.finish_applying()
            else:
                msg = QMessageBox()
                msg.setWindowTitle(self.mw.warning_title)
                msg.setText(self.mw.rect_values_error)
                msg.setIcon(QMessageBox.Warning)
                x = msg.exec_()
        else:
            self.fn.warning()

    def add_rect_item(self):
        c = len(self.mw.rect_list)
        self.mw.rect_list.addItem(f"Ret. {c + 1}")
        self.mw.rect_list.setCurrentIndex(c)

    def add_cir(self):
        if self.mn.calc.shear_flux or self.mn.calc.normal_stress:
            if self.geometry_change_prompt() == QMessageBox.Yes:
                self.mn.calc.shear_flux = ""
                self.mn.calc.normal_stress = ""
                self.update_cir()
        else:
            self.update_cir()

    def update_cir(self):
        if self.mw.circle_x.text() != '' and self.mw.circle_y.text() != '' and \
                self.mw.circle_r.text() != '' and self.mw.circle_ai.text() != '':  # and self.mw.circle_af.text() != '':
            x = float(self.fn.filter(self.mw.circle_x.text()))
            y = float(self.fn.filter(self.mw.circle_y.text()))
            radius = float(self.fn.filter(self.mw.circle_r.text()))
            angle = float(self.fn.filter(self.mw.circle_ai.text()))
            self.mn.add_semicircular_subarea((x, y), radius, angle, subarea_id=self.mw.circle_list.currentIndex() + 1)
            # self.mw.circle_af.text()]})
            self.finish_applying()
        else:
            self.fn.warning()

    def add_cir_item(self):
        c = len(self.mw.circle_list)
        self.mw.circle_list.addItem(f"Cir. {c + 1}")
        self.mw.circle_list.setCurrentIndex(c)

    def finish_applying(self):
        self.mn.calculate_geometrical_properties()
        if self.mw.figureResultsButton.isChecked():
            self.set_sigma()
        self.plot_sec()

    def remove_rectangle(self):
        c = self.mw.rect_list.currentIndex() + 1
        self.mn.remove_rectangular_subarea(c)
        if self.mn.has_subareas():
            self.mn.calculate_geometrical_properties()
            if self.mw.figureResultsButton.isChecked():
                self.set_sigma()
            self.plot_sec()
            self.change_table_rect()
        else:
            self.transv_reset()

    def remove_circle(self):
        c = self.mw.circle_list.currentIndex() + 1
        self.mn.remove_semicircular_subarea(c)
        if self.mn.has_subareas():
            self.mn.calculate_geometrical_properties()
            if self.mw.figureResultsButton.isChecked():
                self.set_sigma()
            self.plot_sec()
            self.change_table_circ()
        else:
            self.transv_reset()

    def transv_reset(self):
        self.mn.calc.subareas_rectangle.clear()
        self.mn.calc.subareas_circle.clear()
        self.clear_rect_text()
        self.clear_cir_text()
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
        set_axes_alpha(plt.gcf())
        self.fn.figurefix()

    def rm_solver(self, clean=True):
        if find_executable('latex'):
            if self.mn.determine_pdf_mode() is not None:
                file, ok = QFileDialog.getSaveFileName(self.mw, self.mw.pdf_title, self.mw.pdf_text, "PDF (*.pdf)")
                if ok:
                    try:
                        self.mw.toolBox.setCurrentIndex(1)
                        self.fn.setupLoading()
                        pdf_dir, filename = split_dir_filename(file)
                        make_pdf_folders(pdf_dir)
                        thread = PDFGeneratorThread(self.mw.loadingScreen,
                                                    self.mn.generate_pdf,
                                                    self.mw.language,
                                                    pdf_path=pdf_dir,
                                                    filename=filename,
                                                    )
                        thread.start()
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

    def rm_savefig(self):
        plt.style.use('default')
        p = d = None
        if self.mw.rect_visualize.isChecked():
            p = self.mw.rect_list.currentIndex() + 1
        if self.mw.circle_visualize.isChecked():
            d = self.mw.circle_list.currentIndex() + 1
        fig = self.mn.show_cross_section(False, p, d, self.mw.MplWidget.canvas.figure)
        fig.savefig("tmp\\figs\\sectransv", transparent=True)
        plt.style.use('dark_background')
        self.mw.last_figure.click()

    def load_cross_section_aux(self, file):
        with open(f'{file}', 'rb') as f:
            _, self.mn, _ = pickle.load(f)
        if self.mn.calc.subareas_circle or self.mn.calc.subareas_rectangle:
            self.mw.rect_list.clear()
            self.mw.circle_list.clear()
            for c in range(len(self.mn.calc.subareas_rectangle)):
                self.mw.add_rect_item()
            for c in range(len(self.mn.calc.subareas_circle)):
                self.mw.add_cir_item()
            self.mn.calculate_geometrical_properties()
            if self.mw.figureResultsButton.isChecked():
                self.set_sigma()
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

    def check_for_user_inputs(self):
        if self.mw.insertDataButton.isChecked():
            self.mn.calc.moment_x = self.mw.msx.text()
            self.mn.calc.moment_y = self.mw.msy.text()
            self.mn.calc.moment_inertia_x = self.mw.mix.text()
            self.mn.calc.moment_inertia_y = self.mw.miy.text()
            self.mn.calc.total_area = self.mw.at.text()
