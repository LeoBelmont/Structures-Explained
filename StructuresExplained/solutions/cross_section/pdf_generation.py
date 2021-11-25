from pylatex import Document, Section, Subsection, Subsubsection, Figure, NoEscape
from StructuresExplained.pdfconfig import header
from StructuresExplained.pdfconfig.translations.cross_sec_strings import translate_PDF_cross_section
from StructuresExplained.utils.util import add_to_pdf, round_expr, append_step, append_result


class pdf_generator:
    def __init__(self, manager, calculator):

        self.mng = manager
        self.calc = calculator

    def generate_pdf(self, language, pdf_path, filename, pdf_mode):
        doc = Document(document_options="a4paper,12pt", documentclass="article")
        doc.preamble.append(NoEscape(header.PDFsettings))

        tpdf = translate_PDF_cross_section(language)
        self.pdf = add_to_pdf(doc)

        doc.append(NoEscape(header.makeCover(tpdf.title, language)))

        if pdf_mode == "complete":

            self.append_cross_section_figure(doc, tpdf)

            self.append_static_moment(doc, tpdf)

            self.append_centroid(doc, tpdf)

            self.append_moment_inertia(doc, tpdf)

        if self.mng.normal_stress_data_list:
            self.append_normal_stress(doc, tpdf)

        if self.mng.neutral_line_data_list:
            self.append_neutral_line(doc, tpdf)

        if self.mng.shear_flux_data_list or self.mng.shear_stress_data_list:
            self.append_static_moment_for_shear_stress(doc, tpdf)

        if self.mng.shear_flux_data_list:
            self.append_shear_flux(doc, tpdf)

        if self.mng.shear_stress_data_list:
            self.append_shear_stress(doc, tpdf)

        doc.generate_pdf(f'{pdf_path}\\{filename}',
                         compiler='pdflatex',
                         win_no_console=True,
                         compiler_args=["-enable-installer"])

    def append_cross_section_figure(self, doc, tpdf):
        with doc.create(Section(tpdf.step_split)):
            with doc.create(Figure(position='H')) as fig_sectransv:
                fig_sectransv.add_image("figs\\sectransv", width='500px')
                fig_sectransv.add_caption(NoEscape(tpdf.figure_label))

    def append_static_moment(self, doc, tpdf):
        with doc.create(Section(tpdf.step_static_moment)):
            if self.calc.subareas_circle:
                doc.append(NoEscape(tpdf.centroid))
                self.pdf.add_equation(r'\frac{4 * R}{3 \cdot \pi}')

            with doc.create(Subsection(tpdf.step_static_moment_x)):
                self.pdf.add_equation(r'Ms_{x_{total}} = \sum{Ms_x} \\')
                self.pdf.add_equation(tpdf.msx_operation)
                self.pdf.add_equation(r'Ms_{{x_{{total}}}} = {}'.format(append_step(self.calc.moment_x)))
                self.pdf.add_equation(r'Ms_{{x_{{total}}}} = {}$ $m^3'.format(append_result(self.calc.moment_x)))

            with doc.create(Subsection(tpdf.step_static_moment_y)):
                self.pdf.add_equation(r'Ms_{y_{total}} = \sum{Ms_y} \\')
                self.pdf.add_equation(tpdf.msy_operation)
                self.pdf.add_equation(r'Ms_{{y_{{total}}}} = {}'.format(append_step(self.calc.moment_y)))
                self.pdf.add_equation(r'Ms_{{y_{{total}}}} = {}$ $m^3'.format(append_result(self.calc.moment_y)))

    def append_centroid(self, doc, tpdf):
        with doc.create(Section(tpdf.step_centroid)):
            with doc.create(Subsection(tpdf.centroid_x)):
                self.pdf.add_equation(r'X_{cg} = \frac{Ms_y}{A_{total}}')
                self.pdf.add_equation(r'X_{{cg}} = {}$ $m'.format(append_step(self.calc.total_cg_x)))
                self.pdf.add_equation(r'X_{{cg}} = {}$ $m'.format(append_result(self.calc.total_cg_x)))

            with doc.create(Subsection(tpdf.centroid_y)):
                self.pdf.add_equation(r'Y_{cg} = \frac{Ms_x}{A_{total}}')
                self.pdf.add_equation(r'Y_{{cg}} = {}$ $m'.format(append_step(self.calc.total_cg_y)))
                self.pdf.add_equation(r'Y_{{cg}} = {}$ $m'.format(append_result(self.calc.total_cg_y)))

    def append_moment_inertia(self, doc, tpdf):
        with doc.create(Section(tpdf.step_moment_inertia)):
            doc.append(NoEscape(tpdf.moment_inercia_tip))
            doc.append(NoEscape(tpdf.theorem_formula))

            with doc.create(Subsection(tpdf.moment_inercia_x)):
                self.pdf.add_equation(r'I_{x_{total}} = \sum{I_x}')
                if self.calc.subareas_rectangle:
                    self.pdf.add_equation(tpdf.moment_inercia_x_rect_formula)
                if self.calc.subareas_circle:
                    self.pdf.add_equation(tpdf.moment_inercia_x_circ_formula)
                self.pdf.add_equation(r'I_{{x_{{total}}}} = {}'.format(append_step(self.calc.moment_inertia_x)))
                self.pdf.add_equation(r'I_{{x_{{total}}}} = {}$ $m^4'.format(append_result(self.calc.moment_inertia_x)))

            with doc.create(Subsection(tpdf.moment_inercia_y)):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{y_{total}} = \sum{Iy}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                if self.calc.subareas_rectangle:
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.moment_inercia_y_rect_formula))
                    doc.append(NoEscape(r'\end{dmath*}'))
                if self.calc.subareas_circle:
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.moment_inercia_y_circ_formula))
                    doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(
                    r'I_{{y_{{total}}}} = {}'.format(append_step(self.calc.moment_inertia_y))))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{{y_{{total}}}} = {}$ $m^4'.format(append_result(self.calc.moment_inertia_y))))
                doc.append(NoEscape(r'\end{dmath*}'))

    def append_normal_stress(self, doc, tpdf):
        with doc.create(Section(tpdf.step_normal_stress)):
            with doc.create(Subsection(tpdf.normal_stress_formula)):
                self.pdf.add_equation(
                    tpdf.normal_stress_var + r' \frac{N}{A} - \frac{My}{Iy} \cdot z - \frac{Mz}{Iz} \cdot y')
            for i in range(len(self.mng.normal_stress_data_list)):
                with doc.create(
                        Subsection(f'{tpdf.calculating_for} N = {self.mng.normal_stress_data_list[i].normal_force} N, '
                                   f'My = {append_result(self.mng.normal_stress_data_list[i].moment_y)} Nm, '
                                   f'Mz = {append_result(self.mng.normal_stress_data_list[i].moment_x)} Nm, '
                                   f'y = {self.mng.normal_stress_data_list[i].y} m, '
                                   f'z = {self.mng.normal_stress_data_list[i].z} m')):
                    with doc.create(Subsubsection(tpdf.step_normal_stress)):
                        self.pdf.add_equation(
                            tpdf.normal_stress_var +
                            f'{append_step(self.mng.normal_stress_data_list[i].normal_stress)}')

                        self.pdf.add_equation(
                            tpdf.normal_stress_var +
                            f'{append_result(self.mng.normal_stress_data_list[i].normal_stress)}$ $Pa')

    def append_neutral_line(self, doc, tpdf):
        with doc.create(Section(tpdf.step_neutral_line)):
            with doc.create(Subsection(tpdf.neutral_line_formula)):
                doc.append(NoEscape(tpdf.neutral_line_tip))
                self.pdf.add_equation(r'0 = \frac{N}{A} - \frac{My}{Iy} \cdot z - \frac{Mz}{Iz} \cdot y')
            for i in range(len(self.mng.neutral_line_data_list)):
                with doc.create(
                        Subsection(f'{tpdf.calculating_for} N = {self.mng.neutral_line_data_list[i].normal_force} N, '
                                   f'My = {append_result(self.mng.neutral_line_data_list[i].moment_y)} Nm, '
                                   f'Mz = {append_result(self.mng.neutral_line_data_list[i].moment_x)} Nm, '
                                   f'y = {self.mng.neutral_line_data_list[i].y} m, '
                                   f'z = {self.mng.neutral_line_data_list[i].z} m')):
                    with doc.create(Subsubsection(tpdf.step_neutral_line)):
                        self.pdf.add_equation(
                            f'0 = {append_step(self.mng.neutral_line_data_list[i].normal_stress)}')
                        """neutral line specifically doesn't need/work with append_result function
                        so round_expr is called directly"""
                        self.pdf.add_equation(f'{round_expr(self.mng.neutral_line_data_list[i].neutral_line)}')

    def append_static_moment_for_shear_stress(self, doc, tpdf):
        with doc.create(Section(tpdf.step_static_moment_cut)):
            with doc.create(Subsection(tpdf.static_moment_cut_formula_above_str)):
                self.pdf.add_equation(tpdf.static_moment_cut_formula_above)

            with doc.create(Subsection(tpdf.static_moment_cut_formula_not_above_str)):
                self.pdf.add_equation(tpdf.static_moment_cut_formula_not_above)

        for i in range(len(self.mng.shear_stress_data_list)):
            with doc.create(Subsection(tpdf.step_static_moment_cut)):
                self.pdf.add_equation(
                    tpdf.static_moment_var +
                    f'{append_step(self.mng.shear_stress_data_list[i].static_moment)}')

                self.pdf.add_equation(
                    tpdf.static_moment_var +
                    f'{append_result(self.mng.shear_stress_data_list[i].static_moment)}$ $m^3')

    def append_shear_flux(self, doc, tpdf):
        with doc.create(Section(tpdf.step_shear_flux)):
            with doc.create(Subsection(tpdf.shear_flux_formula)):
                self.pdf.add_equation(tpdf.shear_flux_var + r' \frac{V \cdot Q}{I_x}')

            for i in range(len(self.mng.shear_flux_data_list)):
                with doc.create(
                        Subsection(
                            NoEscape(f'{tpdf.calculating_for} V = {self.mng.shear_flux_data_list[i].shear_force} N, '
                                     f'Q = {append_result(self.mng.shear_flux_data_list[i].static_moment)} m'
                                     + r'\textsuperscript{3}, I\textsubscript{x}' +
                                     f' = {append_result(self.mng.shear_flux_data_list[i].moment_inertia_x)}' +
                                     r' m\textsuperscript{4}'))):
                    self.pdf.add_equation(
                        tpdf.shear_flux_var +
                        f'{append_step(self.mng.shear_flux_data_list[i].shear_flux)}')

                    self.pdf.add_equation(
                        tpdf.shear_flux_var +
                        f'{append_result(self.mng.shear_flux_data_list[i].shear_flux)}' +
                        r'$ $\frac{N}{m}')

    def append_shear_stress(self, doc, tpdf):
        with doc.create(Section(tpdf.step_shear_stress)):
            with doc.create(Subsection(tpdf.shear_stress_formula_str)):
                self.pdf.add_equation(tpdf.shear_stress_var + r' \frac{V \cdot Q}{I_x \cdot t}')

            for i in range(len(self.mng.shear_stress_data_list)):
                with doc.create(Subsection(
                        NoEscape(f'{tpdf.calculating_for} V = {self.mng.shear_stress_data_list[i].shear_force} N, ' +
                                 f'Q = {append_result(self.mng.shear_stress_data_list[i].static_moment)} m'
                                 + r'\textsuperscript{3}, I\textsubscript{x}' +
                                 f' = {append_result(self.mng.shear_stress_data_list[i].moment_inertia_x)} m'
                                 + r'\textsuperscript{4}, ' + f't = {self.mng.shear_stress_data_list[i].thickness} m'
                                 ))):

                    self.pdf.add_equation(
                        tpdf.shear_stress_var +
                        f'{append_step(self.mng.shear_stress_data_list[i].shear_stress)}')

                    self.pdf.add_equation(
                        tpdf.shear_stress_var +
                        f'{append_result(self.mng.shear_stress_data_list[i].shear_stress)}' +
                        r'$ $Pa')


class normal_stress_data:
    def __init__(self,
                 normal_stress,
                 normal_force,
                 moment_y,
                 moment_x,
                 y,
                 z
                 ):

        self.normal_stress = normal_stress
        self.normal_force = normal_force
        self.moment_y = moment_y
        self.moment_x = moment_x
        self.y = y
        self.z = z


class neutral_line_data:
    def __init__(self,
                 normal_stress,
                 neutral_line,
                 normal_force,
                 moment_y,
                 moment_x,
                 y,
                 z,
                 ):

        self.normal_stress = normal_stress
        self.neutral_line = neutral_line
        self.normal_force = normal_force
        self.moment_y = moment_y
        self.moment_x = moment_x
        self.y = y
        self.z = z


class shear_flux_data:
    def __init__(self,
                 shear_flux,
                 shear_force,
                 static_moment,
                 moment_inertia_x
                 ):

        self.shear_flux = shear_flux
        self.shear_force = shear_force
        self.static_moment = static_moment
        self.moment_inertia_x = moment_inertia_x


class shear_stress_data:
    def __init__(self,
                 shear_stress,
                 shear_force,
                 static_moment,
                 moment_inertia_x,
                 thickness
                 ):

        self.shear_stress = shear_stress
        self.shear_force = shear_force
        self.static_moment = static_moment
        self.moment_inertia_x = moment_inertia_x
        self.thickness = thickness
