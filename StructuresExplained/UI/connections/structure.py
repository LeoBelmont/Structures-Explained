import pickle
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from anastruct import SystemElements
from distutils.spawn import find_executable
import os
from StructuresExplained.pdfconfig.generator_thread import PDFGeneratorThread
import matplotlib.pyplot as plt


class connections:
    def __init__(self, main_window):
        self.mw = main_window
        self.ss = SystemElements()

    def add_beam(self):
        try:
            self.mw.workaround()
            e = self.mw.elementtype.currentIndex()

            if self.mw.utilizeinfo.isChecked():
                EI = float(self.mw.filter(self.mw.beam_E.text())) * float(self.mw.filter(self.mw.beam_I.text()))
                EA = float(self.mw.filter(self.mw.beam_E.text())) * float(self.mw.filter(self.mw.beam_A.text()))
                element_types = ["beam", "truss"]
                self.ss.add_element(
                    location=[[self.mw.filter(self.mw.beam_x1.text()), self.mw.filter(self.mw.beam_y1.text())],
                              [self.mw.filter(self.mw.beam_x2.text()), self.mw.filter(self.mw.beam_y2.text())]],
                    EI=EI, EA=EA, element_type=element_types[e])

            else:
                self.ss.add_element(
                    location=[[self.mw.filter(self.mw.beam_x1.text()), self.mw.filter(self.mw.beam_y1.text())],
                              [self.mw.filter(self.mw.beam_x2.text()), self.mw.filter(self.mw.beam_y2.text())]])

            self.mw.visualize_structure()
            self.mw.states.append(pickle.dumps(self.mw.ss))
        except:
            self.mw.warning()

    def beam_info(self):
        if self.mw.utilizeinfo.isChecked():
            self.mw.frame_4.setHidden(False)
        else:
            self.mw.frame_4.setHidden(True)

    def element_type_list(self):
        if self.mw.elementtype.currentIndex() == 1:
            self.mw.beam_I.setEnabled(False)
        elif self.mw.elementtype.currentIndex() == 0:
            self.mw.beam_I.setEnabled(True)

    def add_node(self):
        try:
            if int(self.mw.node_id.text()) in self.ss.node_map.keys():
                self.mw.workaround()
                self.ss.insert_node(element_id=int(self.mw.node_id.text()),
                                    location=[self.mw.filter(self.mw.node_x.text()),
                                              self.mw.filter(self.mw.node_y.text())])
                self.mw.last_figure.click()
                self.mw.states.append(pickle.dumps(self.mw.ss))
            else:
                self.mw.invalid_id_warning()
        except:
            self.mw.warning()

    def add_support(self):
        try:
            if int(self.mw.support_pos.text()) in self.ss.node_map.keys():
                self.mw.workaround()
                if self.mw.support_hinged.isChecked():
                    self.ss.add_support_hinged(node_id=int(self.mw.support_pos.text()))
                elif self.mw.support_roll.isChecked():
                    self.ss.add_support_roll(node_id=int(self.mw.support_pos.text()),
                                             angle=float(self.mw.filter(self.mw.support_angle.text())))
                elif self.mw.support_fixed.isChecked():
                    self.ss.add_support_fixed(node_id=int(self.mw.support_pos.text()))
                elif self.mw.support_spring.isChecked():
                    self.ss.add_support_spring(node_id=int(self.mw.support_pos.text()),
                                               translation=self.mw.spring_translation.text(), k=self.mw.spring_k.text())
                elif self.mw.support_internal_hinge.isChecked():
                    pass

                self.mw.last_figure.click()
                self.mw.states.append(pickle.dumps(self.mw.ss))
                self.mw.enable_buttons()
            else:
                self.mw.invalid_id_warning()
        except:
            self.mw.warning()

    def show_support_stuff(self):
        if self.mw.support_roll.isChecked():
            self.mw.support_angle.setHidden(False)
            self.mw.label_113.setHidden(False)
            self.mw.label_27.setHidden(False)
            self.mw.label_71.setHidden(True)
            self.mw.label_73.setHidden(True)
            self.mw.spring_k.setHidden(True)
            self.mw.spring_translation.setHidden(True)
        elif self.mw.support_spring.isChecked():
            self.mw.label_71.setHidden(False)
            self.mw.label_73.setHidden(False)
            self.mw.spring_k.setHidden(False)
            self.mw.spring_translation.setHidden(False)
            self.mw.support_angle.setHidden(True)
            self.mw.label_27.setHidden(True)
            self.mw.label_127.setHidden(False)
        else:
            self.mw.support_angle.setHidden(True)
            self.mw.label_27.setHidden(True)
            self.mw.label_71.setHidden(True)
            self.mw.label_73.setHidden(True)
            self.mw.spring_k.setHidden(True)
            self.mw.label_113.setHidden(True)
            self.mw.label_127.setHidden(True)
            self.mw.spring_translation.setHidden(True)

    def add_point_load(self):
        try:
            if int(self.mw.load_pos.text()) in self.ss.node_map.keys():
                self.mw.workaround()
                if self.mw.load_moment.text() != '' and float(self.mw.load_moment.text()) != 0:
                    self.ss.moment_load(node_id=int(self.mw.load_pos.text()),
                                        Ty=float(self.mw.filter(self.mw.load_moment.text())))

                if float(self.mw.load_y.text()) == 0 and float(self.mw.load_x.text()) == 0 and float(
                        self.mw.load_angle.text()) == 0:
                    pass
                elif self.mw.load_y.text() != '' and self.mw.load_x.text() != '' and self.mw.load_angle.text() != '':
                    self.ss.point_load(node_id=int(self.mw.load_pos.text()),
                                       Fy=float(self.mw.filter(self.mw.load_y.text())),
                                       Fx=float(self.mw.filter(self.mw.load_x.text())),
                                       rotation=float(self.mw.filter(self.mw.load_angle.text())))
                self.mw.last_figure.click()
                self.mw.states.append(pickle.dumps(self.mw.ss))
                self.mw.enable_buttons()
            else:
                self.mw.invalid_id_warning()
        except:
            self.mw.warning()

    def add_q_load(self):
        try:
            if int(self.mw.qload_pos.text()) in self.ss.node_map.keys():
                if float(self.mw.qload_initial.text()) >= 0 and float(self.mw.qload_final.text()) >= 0 or \
                        float(self.mw.qload_initial.text()) <= 0 and float(self.mw.qload_final.text()) <= 0:
                    self.mw.workaround()
                    if self.mw.qload_initial.text() == '':
                        self.mw.qload_final.setText(self.mw.filter(self.mw.qload_final.text()))
                    if self.mw.qload_final.text() == '':
                        self.mw.qload_final.setText(self.mw.filter(self.mw.qload_initial.text()))
                    self.ss.q_load(element_id=int(self.mw.qload_pos.text()),
                                   q=(float(self.mw.filter(self.mw.qload_final.text())),
                                      float(self.mw.filter(self.mw.qload_initial.text()))))
                    self.mw.last_figure.click()
                    self.mw.states.append(pickle.dumps(self.mw.ss))
                    self.mw.enable_buttons()
                else:
                    msg = QMessageBox()
                    msg.setWindowTitle(self.mw.warning_title)
                    msg.setText(self.mw.qload_warning)
                    msg.setIcon(QMessageBox.Warning)
                    x = msg.exec_()
            else:
                self.mw.invalid_id_warning()
        except:
            self.mw.warning()

    def visualize_structure(self):
        if self.ss.element_map:
            self.mw.visualize(self.ss.show_structure(show=False))
            self.mw.last_figure = self.mw.show_structure
        else:
            self.mw.MplWidget.plot(has_grid=self.mw.gridBox.isChecked())
            self.mw.figurefix()
            self.mw.last_figure = None

    def visualize_diagram(self):
        self.mw.solve()
        self.mw.visualize(self.ss.show_structure(show=False, free_body_diagram=1))
        self.mw.last_figure = self.mw.show_diagram

    def visualize_supports(self):
        self.mw.solve()
        self.mw.visualize(self.ss.show_reaction_force(show=False))
        self.mw.last_figure = self.mw.show_supports

    def visualize_normal(self):
        self.mw.solve()
        self.mw.visualize(self.ss.show_axial_force(show=False))
        self.mw.last_figure = self.mw.show_normal

    def visualize_shear(self):
        self.mw.solve()
        self.mw.visualize(self.ss.show_shear_force(show=False))
        self.mw.last_figure = self.mw.show_shear

    def visualize_moment(self):
        self.mw.solve()
        self.mw.visualize(self.ss.show_bending_moment(show=False))
        self.mw.last_figure = self.mw.show_moment

    def visualize_displacement(self):
        self.mw.solve()
        self.mw.visualize(self.ss.show_displacement(show=False))
        self.mw.last_figure = self.mw.show_displacement

    def solve(self):
        self.solvetrue = True
        self.ss.solve()

    def static_solver(self):
        if find_executable('latex'):
            if self.mw.show_moment.isEnabled():
                if len(self.ss.supports_roll) == 1 and len(self.ss.supports_hinged) == 1:
                    file, ok = QFileDialog.getSaveFileName(self.mw, self.mw.pdf_title, self.mw.pdf_text, "PDF (*.pdf)")
                    if ok:
                        try:
                            self.mw.toolBox.setCurrentIndex(0)
                            self.mw.setupLoading()
                            thread = PDFGeneratorThread(self.mw.loadingScreen,
                                                        self.mw.structure_savefig,
                                                        self.mw.teach.solver,
                                                        self.mw.language,
                                                        self.mw.ss,
                                                        file)
                            thread.start()
                            self.mw.loadingScreen.exec_()
                            if not self.mw.loadingUi.userTerminated:
                                os.replace("tmp\\resolucao.pdf", f"{file}")
                                self.mw.pdf_generated_prompt()
                            self.mw.deleteTempFolder()
                        except:
                            self.mw.latex_packages_warning()
                else:
                    self.mw.static_warning()
            else:
                self.mw.warning()
        else:
            self.mw.latex_warning()

    def structure_savefig(self):
        self.makeTempFolder()

        plt.style.use('default')
        self.ss.show_structure(show=False)
        plt.savefig("tmp\\figs\\structure", transparent=True)
        self.solve()
        self.ss.show_structure(show=False, free_body_diagram=2)
        plt.savefig("tmp\\figs\\diagram2", transparent=True)
        self.ss.show_structure(show=False, free_body_diagram=3)
        plt.savefig("tmp\\figs\\diagram1", transparent=True)
        self.ss.show_reaction_force(show=False)
        plt.savefig("tmp\\figs\\supports", transparent=True)
        self.ss.show_axial_force(show=False)
        plt.savefig("tmp\\figs\\axial", transparent=True)
        self.ss.show_shear_force(show=False)
        plt.savefig("tmp\\figs\\shear", transparent=True)
        self.ss.show_bending_moment(show=False)
        plt.savefig("tmp\\figs\\moment", transparent=True)
        plt.style.use('dark_background')

    def reset_struct_elems(self):
        self.ss = pickle.loads(self.blankss)
        self.states.clear()
        self.MplWidget.plot(has_grid=self.gridBox.isChecked())
        self.figurefix()
        self.solvetrue = False
        self.disable_buttons()

    def save_structure(self):
        file, ok = QFileDialog.getSaveFileName(self, self.save_strucutre_title,
                                               self.save_strucutre_text, self.strucutre_type_str)
        if ok:
            with open(f'{file}', 'wb') as f:
                pickle.dump((self.ss, self.sig, self.mohr), f)

    def load_structure_aux(self, file):
        with open(f'{file}', 'rb') as f:
            self.ss, _, _ = pickle.load(f)
        self.struct_loaded = True

    def workaround(self):
        if self.solvetrue:
            self.ss = pickle.loads(self.states[-1])
            self.solvetrue = False

    def reset(self):
        self.workaround()
        self.ss.remove_loads()
        self.visualize(self.ss.show_structure(show=False))
        self.states.append(pickle.dumps(self.ss))
        self.disable_buttons()
