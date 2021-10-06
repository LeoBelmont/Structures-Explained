import numpy
from pylatex import Document, Section, Subsection, Figure, NoEscape
from sympy import Symbol, latex, simplify
from StructuresExplained.pdfconfig import header
from StructuresExplained.pdfconfig.translations.mohr_strings import translate_PDF_Mohr
from StructuresExplained.utils.util import add_to_pdf


class pdf_generator:

    def __init__(self, manager, results):
        self.mng = manager
        self.res = results

    def setup_pdf(self, language):
        self.doc = Document(document_options="a4paper,12pt", documentclass="article")
        self.doc.preamble.append(NoEscape(header.PDFsettings))

        self.language = language

        self.pdf = add_to_pdf(self.doc)

        self.tpdf = translate_PDF_Mohr(self.language)

    def generate_pdf_plain_state(self, language, pdf_path, filename):
        self.setup_pdf(language)

        append_plain_state(self, self.mng, self.res).append_all()

        self.doc.generate_pdf(fr'{pdf_path}\{filename}',
                              compiler='pdflatex',
                              win_no_console=True,
                              compiler_args=["-enable-installer"])

    def generate_pdf_triple_state(self, language, pdf_path, filename):
        self.setup_pdf(language)

        append_triple_state(self, self.mng, self.res).append_all()

        self.doc.generate_pdf(fr'{pdf_path}\{filename}',
                              compiler='pdflatex',
                              win_no_console=True,
                              compiler_args=["-enable-installer"])


class append_plain_state:
    def __init__(self, generator, manager, results):
        self.gen = generator
        self.mng = manager
        self.res = results

    def append_all(self):
        self.make_cover()
        self.append_main_stresses()
        self.append_main_stresses()
        self.append_center()
        self.append_angle()
        self.append_result_drawing()

    def make_cover(self):
        self.gen.doc.append(NoEscape(header.makeCover(self.gen.tpdf.title_2d, self.gen.language)))

    def append_radius_and_max_shear(self):
        with self.gen.doc.create(Section(self.gen.tpdf.radius_and_max_shear)):
            with self.gen.doc.create(Subsection(self.gen.tpdf.radius_and_max_shear_formula)):
                self.gen.pdf.add_equation(
                    self.gen.tpdf.radius_var + r' \sqrt{(\frac{\sigma_x-\sigma_y}{2})^2 + \tau_xy ^ 2)}')
            with self.gen.doc.create(Subsection(self.gen.tpdf.radius_and_max_shear_solving)):
                self.gen.pdf.add_equation(
                    self.gen.tpdf.radius_var + r' \sqrt{(\frac{' + fr'{self.res.sigma_x}-{self.res.sigma_y}' +
                    '}{2})^2 +' + f'{self.res.tau_xy}' + '^ 2)}')
                self.gen.pdf.add_equation(self.gen.tpdf.radius_var + f'{self.res.max_shear}')

    def append_main_stresses(self):
        with self.gen.doc.create(Section(self.gen.tpdf.main_stress_calculation)):
            with self.gen.doc.create(Subsection(self.gen.tpdf.main_stress_formula)):
                self.gen.pdf.add_equation(
                    r'\sigma_{1,2} = \sqrt{\frac{\sigma_x + \sigma_y}{2} \pm (\frac{\sigma_x - \sigma_y}{2}) ^ 2 +'
                    r' {\tau_{xy}} ^ 2}')

            with self.gen.doc.create(Subsection(self.gen.tpdf.sigma_1_solving)):
                self.gen.pdf.add_equation(
                    r'\sigma_1 = \sqrt{\frac{' + f'{self.res.sigma_x}' + f'+ {self.res.sigma_y}' + r'}{2} + (\frac{'
                    + f'{self.res.sigma_x}' + ' - ' + f'{self.res.sigma_y}' + '}{2}) ^ 2 + ' + f'{self.res.tau_xy}'
                    + ' ^ 2}')
                self.gen.pdf.add_equation(f'\\sigma_1 = {self.res.sigma_1}')

            with self.gen.doc.create(Subsection(self.gen.tpdf.sigma_2_solving)):
                self.gen.pdf.add_equation(
                    r'\sigma_2 = \sqrt{\frac{' + f'{self.res.sigma_x}' + f'+ {self.res.sigma_y}' + r'}{2} - (\frac{' +
                    f'{self.res.sigma_x}' + ' - ' + f'{self.res.sigma_y}' + '}{2}) ^ 2 + ' + f'{self.res.tau_xy}' +
                    ' ^ 2}')
                self.gen.pdf.add_equation(f'\\sigma_2 = {self.res.sigma_2}')

    def append_center(self):
        with self.gen.doc.create(Section(self.gen.tpdf.center_solving)):
            with self.gen.doc.create(Subsection(self.gen.tpdf.center_formula)):
                self.gen.pdf.add_equation(self.gen.tpdf.center + r' = \frac{\sigma_x + \sigma_y}{2}')

            with self.gen.doc.create(Subsection(self.gen.tpdf.center_solving)):
                self.gen.pdf.add_equation(
                        self.gen.tpdf.center + r' = \frac{' + f'{self.res.sigma_x} +' + f'{self.res.sigma_y}' + '}{2}')
                self.gen.pdf.add_equation(f'{self.gen.tpdf.center} = {(self.res.sigma_x + self.res.sigma_y) / 2}')

    def append_angle(self):
        with self.gen.doc.create(Section(self.gen.tpdf.angle_solving)):
            with self.gen.doc.create(Subsection(self.gen.tpdf.angle_formula)):
                self.gen.pdf.add_equation(r'\theta = \frac{arctan(\frac{\tau_{xy}}{\sigma_x - ' +
                                          f'{self.gen.tpdf.center} ' + '})}{2}')

            with self.gen.doc.create(Subsection(self.gen.tpdf.doing_math)):
                self.gen.pdf.add_equation(
                    r'\theta = \frac{arctan(\frac{' + f'{self.res.tau_xy}' + '}{' + f'{self.res.sigma_x}' +
                    f' - {(self.res.sigma_x + self.res.sigma_y) / 2}' + '}' + ')}{2}')
                self.gen.pdf.add_equation(f'\\theta = {abs(self.res.angle * 180 / numpy.pi)}')
                self.gen.doc.append(NoEscape(self.gen.tpdf.angle_tip))
                self.gen.pdf.add_equation(f'\\theta = {abs(self.res.angle * 90 / numpy.pi)}')

    def append_result_drawing(self):
        with self.gen.doc.create(Section(self.gen.tpdf.drawing_circle_2d)):
            with self.gen.doc.create(Figure(position='H')) as fig_mohrleft:
                fig_mohrleft.add_image("figs\\mohrfig", width='500px')
                fig_mohrleft.add_caption(NoEscape(self.gen.tpdf.circle_label))


class append_triple_state:
    def __init__(self, generator, manager, results):
        self.gen = generator
        self.mng = manager
        self.res = results

    def append_all(self):
        self.make_cover()
        self.append_formulas()
        self.append_matrix_calculation()
        self.append_results()
        self.append_result_drawing()

    def make_cover(self):
        self.gen.doc.append(NoEscape(header.makeCover(self.gen.tpdf.title_3d, self.gen.language)))

    def append_formulas(self):
        with self.gen.doc.create(Section(self.gen.tpdf.formula_for_math)):
            with self.gen.doc.create(Subsection(self.gen.tpdf.main_stress_formula)):
                self.gen.doc.append(NoEscape(self.gen.tpdf.main_stress_tip))
                self.gen.pdf.add_equation(r'det(M - I\lambda) = 0')

                self.gen.doc.append(NoEscape(r'\[det('))
                self.gen.doc.append(NoEscape(r'\begin{bmatrix}'))
                self.gen.doc.append(NoEscape(
                    r'\sigma_x & \tau_{xy} & \tau_{xz}\\ \tau_{xy} & \sigma_y & \tau_{yz}\\' +
                    r' \tau_{xz} & \tau_{yz} & \sigma_z'
                ))
                self.gen.doc.append(NoEscape(r'\end{bmatrix}'))
                self.gen.doc.append(NoEscape(r' - '))
                self.gen.doc.append(NoEscape(r'\begin{bmatrix}'))
                self.gen.doc.append(NoEscape(r'1 & 0 & 0\\ 0 & 1 & 0\\ 0 & 0 & 1'))
                self.gen.doc.append(NoEscape(r'\end{bmatrix}'))
                self.gen.doc.append(NoEscape(r' \cdot \lambda) = 0 \Rightarrow'))
                self.gen.doc.append(NoEscape(r'\begin{vmatrix}'))
                self.gen.doc.append(NoEscape(
                    r'\sigma_x - \lambda & \tau_{xy} & \tau_{xz}\\ \tau_{xy} & \sigma_y - \lambda & \tau_{yz}\\ ' +
                    r'\tau_{xz} & \tau_{yz} & \sigma_z - \lambda'
                ))
                self.gen.doc.append(NoEscape(r'\end{vmatrix}'))
                self.gen.doc.append(NoEscape(r' = 0\]'))

            with self.gen.doc.create(Subsection(self.gen.tpdf.max_shear_formula)):
                self.gen.doc.append(NoEscape(self.gen.tpdf.max_shear_tip_head))
                self.gen.doc.append(NoEscape(r'\begin{enumerate}'))
                self.gen.doc.append(NoEscape(self.gen.tpdf.max_shear_tip_body_1))
                self.gen.doc.append(NoEscape(self.gen.tpdf.max_shear_tip_body_2))
                self.gen.doc.append(NoEscape(r'\end{enumerate}'))
                self.gen.pdf.add_equation(self.gen.tpdf.radius_var + r' \frac{\sigma_1 - \sigma_3}{2}')
                self.gen.doc.append(NoEscape(r'\newpage'))

    def append_matrix_calculation(self):
        with self.gen.doc.create(Section(self.gen.tpdf.calculation)):
            with self.gen.doc.create(Subsection(self.gen.tpdf.matrix_subs)):
                self.gen.doc.append(NoEscape(r'\['))
                self.gen.doc.append(NoEscape(r'\begin{vmatrix}'))
                self.gen.doc.append(
                    NoEscape(f'{self.res.sigma_x} -' + r'\lambda' + f'& {self.res.tau_xy} & {self.res.tau_xz}' r'\\'
                             f'{self.res.tau_xy} & {self.res.sigma_y}' + r' - \lambda' + f'& {self.res.tau_yz}' r'\\'
                             f'{self.res.tau_xz} & {self.res.tau_yz} & {self.res.sigma_z}' + r' - \lambda'))
                self.gen.doc.append(NoEscape(r'\end{vmatrix}'))
                self.gen.doc.append(NoEscape(r' =0\]'))

                with self.gen.doc.create(Subsection(self.gen.tpdf.determinant_calculation)):
                    string = f"({self.res.sigma_x} -" + r'\lambda' + f") \\cdot ({self.res.sigma_y} -" + r'\lambda' + \
                             f") \\cdot ({self.res.sigma_z} -" + r'\lambda' + f") + {self.res.tau_xy} \\cdot " \
                             f"{self.res.tau_yz} \\cdot {self.res.tau_xz} + {self.res.tau_xz} \\cdot {self.res.tau_xy}" \
                             + f" \\cdot {self.res.tau_yz} - {self.res.tau_xz} \\cdot ({self.res.sigma_y} -" \
                             + r'\lambda' + f") \\cdot {self.res.tau_xz} - {self.res.tau_yz} \\cdot {self.res.tau_yz}" \
                             f" \\cdot ({self.res.sigma_x} -" + r'\lambda' + f") - ({self.res.sigma_z} -" + \
                             r'\lambda' + f") \\cdot {self.res.tau_xy} \\cdot {self.res.tau_xy}"

                    lam = Symbol(r'\lambda')
                    numeric = (self.res.sigma_x - lam) * (self.res.sigma_y - lam) * (self.res.sigma_z - lam) + \
                              self.res.tau_xy * self.res.tau_yz * self.res.tau_xz + self.res.tau_xz * \
                              self.res.tau_xy * self.res.tau_yz - self.res.tau_xz * (self.res.sigma_y - lam) * \
                              self.res.tau_xz - self.res.tau_yz * self.res.tau_yz * (self.res.sigma_x - lam) - \
                              (self.res.sigma_z - lam) * self.res.tau_xy * self.res.tau_xy

                    self.gen.pdf.add_equation('det = ' + string)
                    self.gen.pdf.add_equation('det = ' + latex(numeric))
                    self.gen.pdf.add_equation('det = ' + latex(simplify(numeric)))
                    self.gen.doc.append(NoEscape(self.gen.tpdf.subs_3_in_1))
                    self.gen.pdf.add_equation(latex(simplify(numeric)) + r'=0')

    def append_results(self):
        with self.gen.doc.create(Section(self.gen.tpdf.get_internal_results)):
            with self.gen.doc.create(Subsection(self.gen.tpdf.main_stress)):
                self.gen.doc.append(NoEscape(self.gen.tpdf.main_stress_roots_tip))
                self.gen.pdf.add_equation(r"\sigma_1 = " + f"{round(self.res.sigma_1, 2)}")
                self.gen.pdf.add_equation(r"\sigma_2 = " + f"{round(self.res.sigma_2, 2)}")
                self.gen.pdf.add_equation(r"\sigma_3 = " + f"{round(self.res.sigma_3, 2)}")
            with self.gen.doc.create(Subsection(self.gen.tpdf.max_shear)):
                self.gen.doc.append(NoEscape(self.gen.tpdf.subs_1_in_3))
                self.gen.pdf.add_equation(
                    self.gen.tpdf.radius_var +
                    r' \frac{' + f'{round(self.res.sigma_1, 2)} - {round(self.res.sigma_3, 2)}' + r'}{2}')
                self.gen.pdf.add_equation(self.gen.tpdf.radius_var + f" {round(self.res.max_shear, 2)}")

    def append_result_drawing(self):
        self.gen.doc.append(NoEscape(r'\newpage'))
        with self.gen.doc.create(Section(self.gen.tpdf.drawing_circle_3d)):
            with self.gen.doc.create(Figure(position='H')) as fig_mohrleft:
                fig_mohrleft.add_image("figs\\mohrfig", width='500px')
                fig_mohrleft.add_caption(NoEscape(self.gen.tpdf.drawing_circle_3d_label))
