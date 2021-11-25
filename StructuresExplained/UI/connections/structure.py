import pickle
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from anastruct import SystemElements
from distutils.spawn import find_executable
from StructuresExplained.pdfconfig.generator_thread import PDFGeneratorThread
from StructuresExplained.utils.util import make_pdf_folders, split_dir_filename, delete_folder
from StructuresExplained.solutions.structure.manager.manager import Manager
from matplotlib import pyplot as plt


class connections:
    def __init__(self, main_window, main_window_functions):
        self.mw = main_window
        self.fn = main_window_functions
        self.ss = SystemElements()
        self.ss.color_scheme = "dark"
        self.was_solved = False
        self.states = []

    def add_beam(self):
        try:
            self.workaround()
            e = self.mw.elementtype.currentIndex()

            if self.mw.utilizeinfo.isChecked():
                EI = float(self.fn.filter(self.mw.beam_E.text())) * float(self.fn.filter(self.mw.beam_I.text()))
                EA = float(self.fn.filter(self.mw.beam_E.text())) * float(self.fn.filter(self.mw.beam_A.text()))
                element_types = ["beam", "truss"]
                self.ss.add_element(
                    location=[[float(self.fn.filter(self.mw.beam_x1.text())),
                               float(self.fn.filter(self.mw.beam_y1.text()))],
                              [float(self.fn.filter(self.mw.beam_x2.text())),
                               float(self.fn.filter(self.mw.beam_y2.text()))]],
                    EI=EI, EA=EA, element_type=element_types[e])

            else:
                self.ss.add_element(
                    location=[[float(self.fn.filter(self.mw.beam_x1.text())),
                               float(self.fn.filter(self.mw.beam_y1.text()))],
                              [float(self.fn.filter(self.mw.beam_x2.text())),
                               float(self.fn.filter(self.mw.beam_y2.text()))]])

            self.visualize_structure()
            self.states.append(pickle.dumps(self.ss))
        except:
            self.fn.warning()

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
                self.workaround()
                self.ss.insert_node(element_id=int(self.mw.node_id.text()),
                                    location=[self.fn.filter(self.mw.node_x.text()),
                                              self.fn.filter(self.mw.node_y.text())])
                self.mw.last_figure.click()
                self.states.append(pickle.dumps(self.ss))
            else:
                self.fn.invalid_id_warning()
        except:
            self.fn.warning()

    def add_support(self):
        try:
            if int(self.mw.support_pos.text()) in self.ss.node_map.keys():
                self.workaround()
                if self.mw.support_hinged.isChecked():
                    self.ss.add_support_hinged(node_id=int(self.mw.support_pos.text()))
                elif self.mw.support_roll.isChecked():
                    self.ss.add_support_roll(node_id=int(self.mw.support_pos.text()),
                                             angle=float(self.fn.filter(self.mw.support_angle.text())))
                elif self.mw.support_fixed.isChecked():
                    self.ss.add_support_fixed(node_id=int(self.mw.support_pos.text()))
                elif self.mw.support_spring.isChecked():
                    self.ss.add_support_spring(node_id=int(self.mw.support_pos.text()),
                                               translation=self.mw.spring_translation.text(), k=self.mw.spring_k.text())
                elif self.mw.support_internal_hinge.isChecked():
                    pass

                self.mw.last_figure.click()
                self.states.append(pickle.dumps(self.ss))
                self.fn.enable_buttons()
            else:
                self.fn.invalid_id_warning()

        except:
            self.fn.warning()

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
                self.workaround()
                if self.mw.load_moment.text() != '' and float(self.mw.load_moment.text()) != 0:
                    self.ss.moment_load(node_id=int(self.mw.load_pos.text()),
                                        Ty=float(self.fn.filter(self.mw.load_moment.text())))

                if float(self.mw.load_y.text()) == 0 and float(self.mw.load_x.text()) == 0 and float(
                        self.mw.load_angle.text()) == 0:
                    pass
                elif self.mw.load_y.text() != '' and self.mw.load_x.text() != '' and self.mw.load_angle.text() != '':
                    self.ss.point_load(node_id=int(self.mw.load_pos.text()),
                                       Fy=float(self.fn.filter(self.mw.load_y.text())),
                                       Fx=float(self.fn.filter(self.mw.load_x.text())),
                                       rotation=float(self.fn.filter(self.mw.load_angle.text())))
                self.mw.last_figure.click()
                self.states.append(pickle.dumps(self.ss))
                self.fn.enable_buttons()
            else:
                self.fn.invalid_id_warning()
        except:
            self.fn.warning()

    def add_q_load(self):
        try:
            if int(self.mw.qload_pos.text()) in self.ss.node_map.keys():
                if float(self.mw.qload_initial.text()) >= 0 and float(self.mw.qload_final.text()) >= 0 or \
                        float(self.mw.qload_initial.text()) <= 0 and float(self.mw.qload_final.text()) <= 0:
                    self.workaround()
                    if self.mw.qload_initial.text() == '':
                        self.mw.qload_final.setText(self.fn.filter(self.mw.qload_final.text()))
                    if self.mw.qload_final.text() == '':
                        self.mw.qload_final.setText(self.fn.filter(self.mw.qload_initial.text()))
                    self.ss.q_load(element_id=int(self.mw.qload_pos.text()),
                                   q=(float(self.fn.filter(self.mw.qload_final.text())),
                                      float(self.fn.filter(self.mw.qload_initial.text()))))
                    self.mw.last_figure.click()
                    self.states.append(pickle.dumps(self.ss))
                    self.fn.enable_buttons()
                else:
                    msg = QMessageBox()
                    msg.setWindowTitle(self.mw.warning_title)
                    msg.setText(self.mw.qload_warning)
                    msg.setIcon(QMessageBox.Warning)
                    x = msg.exec_()
            else:
                self.fn.invalid_id_warning()
        except:
            self.fn.warning()

    def visualize_structure(self):
        if self.ss.element_map:
            self.mw.MplWidget.canvas.figure.clear()
            ax = self.mw.MplWidget.canvas.figure.add_subplot(111)
            self.fn.visualize(self.ss.show_structure(show=False, figure=(self.mw.MplWidget.canvas.figure, ax)))
            ax.patch.set_alpha(0.2)
            self.mw.last_figure = self.mw.show_structure
        else:
            self.mw.MplWidget.plot(has_grid=self.mw.gridBox.isChecked())
            self.fn.figurefix()
            self.mw.last_figure = None

    def visualize_diagram(self):
        self.solve()
        self.mw.MplWidget.canvas.figure.clear()
        ax = self.mw.MplWidget.canvas.figure.add_subplot(111)
        ax.patch.set_alpha(0.2)
        self.fn.visualize(self.ss.show_structure(show=False, free_body_diagram=1,
                                                 figure=(self.mw.MplWidget.canvas.figure, ax)))
        self.mw.last_figure = self.mw.show_diagram

    def visualize_supports(self):
        self.solve()
        self.mw.MplWidget.canvas.figure.clear()
        ax = self.mw.MplWidget.canvas.figure.add_subplot(111)
        ax.patch.set_alpha(0.2)
        self.fn.visualize(self.ss.show_reaction_force(show=False,
                                                      figure=(self.mw.MplWidget.canvas.figure, ax)))
        self.mw.last_figure = self.mw.show_supports

    def visualize_normal(self):
        self.solve()
        self.mw.MplWidget.canvas.figure.clear()
        ax = self.mw.MplWidget.canvas.figure.add_subplot(111)
        ax.patch.set_alpha(0.2)
        self.fn.visualize(self.ss.show_axial_force(show=False,
                                                   figure=(self.mw.MplWidget.canvas.figure, ax)))
        self.mw.last_figure = self.mw.show_normal

    def visualize_shear(self):
        self.solve()
        self.mw.MplWidget.canvas.figure.clear()
        ax = self.mw.MplWidget.canvas.figure.add_subplot(111)
        ax.patch.set_alpha(0.2)
        self.fn.visualize(self.ss.show_shear_force(show=False,
                                                   figure=(self.mw.MplWidget.canvas.figure, ax)))
        self.mw.last_figure = self.mw.show_shear

    def visualize_moment(self):
        self.solve()
        self.mw.MplWidget.canvas.figure.clear()
        ax = self.mw.MplWidget.canvas.figure.add_subplot(111)
        ax.patch.set_alpha(0.2)
        self.fn.visualize(self.ss.show_bending_moment(show=False,
                                                      figure=(self.mw.MplWidget.canvas.figure, ax)))
        self.mw.last_figure = self.mw.show_moment

    def visualize_displacement(self):
        self.solve()
        self.mw.MplWidget.canvas.figure.clear()
        ax = self.mw.MplWidget.canvas.figure.add_subplot(111)
        ax.patch.set_alpha(0.2)
        self.fn.visualize(self.ss.show_displacement(show=False,
                                                    figure=(self.mw.MplWidget.canvas.figure, ax)))
        self.mw.last_figure = self.mw.show_displacement

    def solve(self):
        self.was_solved = True
        self.ss.solve()

    def static_solver(self, clean=True):
        if find_executable('latex'):
            if self.mw.show_moment.isEnabled():
                if (len(self.ss.supports_roll) == 1 and len(self.ss.supports_hinged) == 1)\
                        or (len(self.ss.supports_fixed) == 1):
                    file, ok = QFileDialog.getSaveFileName(self.mw, self.mw.pdf_title, self.mw.pdf_text, "PDF (*.pdf)")
                    if ok:
                        try:
                            self.mw.toolBox.setCurrentIndex(0)
                            pdf_dir, filename = split_dir_filename(file)
                            make_pdf_folders(pdf_dir)

                            self.ss.color_scheme = "bright"
                            plt.style.use('default')

                            mn = Manager(self.ss)

                            pdf_generator_thread = PDFGeneratorThread(
                                mn.generate_pdf,
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
                            self.ss.color_scheme = "dark"
                            plt.style.use('dark_background')

                        except:
                            self.fn.latex_packages_warning()
                else:
                    self.fn.static_warning()
            else:
                self.fn.warning()
        else:
            self.fn.latex_warning()

    def on_finished(self):
        self.mw.loadingScreen.close()

    def reset_struct_elems(self):
        self.ss = SystemElements()
        self.ss.color_scheme = "dark"
        self.states.clear()
        self.mw.MplWidget.plot(has_grid=self.mw.gridBox.isChecked())
        self.mw.MplWidget.set_background_alpha()
        self.mw.MplWidget.set_subplot_alpha()
        self.fn.figurefix()
        self.was_solved = False
        self.fn.disable_buttons()

    def load_structure_aux(self, file):
        with open(f'{file}', 'rb') as f:
            self.ss, _, _ = pickle.load(f)
        self.mw.struct_loaded = True

    def workaround(self):
        if self.was_solved:
            self.ss = pickle.loads(self.states[-1])
            self.was_solved = False

    def reset(self):
        self.workaround()
        self.ss.remove_loads()
        self.mw.MplWidget.canvas.figure.clear()
        ax = self.mw.MplWidget.canvas.figure.add_subplot(111)
        ax.patch.set_alpha(0.2)
        self.fn.visualize(self.ss.show_structure(show=False, figure=(self.mw.MplWidget.canvas.figure, ax)))
        self.states.append(pickle.dumps(self.ss))
        self.fn.disable_buttons()
