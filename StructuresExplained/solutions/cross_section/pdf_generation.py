from sympy.parsing.sympy_parser import parse_expr
from pylatex import Document, Section, Subsection, Subsubsection, Figure, NoEscape
from StructuresExplained.pdfconfig import header
from StructuresExplained.pdfconfig.translations.cross_sec_strings import translate_PDF_cross_section
from StructuresExplained.utils.util import round_expr, add_to_pdf


class pdf_generator:
    def __init__(self, manager, calculator):

        self.mng = manager
        self.calc = calculator

    def generate_pdf(self, language):
        doc = Document(document_options="a4paper,12pt", documentclass="article")
        doc.preamble.append(NoEscape(header.PDFsettings))

        tpdf = translate_PDF_cross_section(language)
        self.pdf = add_to_pdf(doc)

        doc.append(NoEscape(header.makeCover(tpdf.title, language)))

        self.append_cross_section_figure(doc, tpdf)

        self.append_static_moment(doc, tpdf)

        self.append_centroid(doc, tpdf)

        self.append_moment_inertia(doc, tpdf)

        if self.mng.normal_stress_latex:
            self.append_normal_stress(doc, tpdf)

        if self.mng.shear_flux_latex or self.mng.shear_stress_latex:
            self.append_static_moment_for_shear_stress(doc, tpdf)

        if self.mng.shear_flux_latex:
            self.append_shear_flux(doc, tpdf)

        if self.mng.shear_stress_latex:
            self.append_shear_stress(doc, tpdf)

        doc.generate_pdf('tmp\\resolucaorm',
                         compiler='pdflatex',
                         win_no_console=True,
                         compiler_args=["-enable-installer"])
        # doc.generate_tex('tmp\\resolucaorm')

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
                self.pdf.add_equation(r'Ms_{{x_{{total}}}} = {}'.format(self.calc.moment_x))
                self.pdf.add_equation(r'Ms_{{x_{{total}}}} = {}$ $m^3'.format(parse_expr(self.calc.moment_x)))

            with doc.create(Subsection(tpdf.step_static_moment_y)):
                self.pdf.add_equation(r'Ms_{y_{total}} = \sum{Ms_y} \\')
                self.pdf.add_equation(tpdf.msy_operation)
                self.pdf.add_equation(r'Ms_{{y_{{total}}}} = {}'.format(self.calc.moment_y))
                self.pdf.add_equation(r'Ms_{{y_{{total}}}} = {}$ $m^3'.format(parse_expr(self.calc.moment_y)))

    def append_centroid(self, doc, tpdf):
        with doc.create(Section(tpdf.step_centroid)):
            with doc.create(Subsection(tpdf.centroid_x)):
                self.pdf.add_equation(r'X_{cg} = \frac{Ms_y}{A_{total}}')
                self.pdf.add_equation(f'X_{{cg}} = \\frac{{{parse_expr(self.calc.moment_y)}}}{{{self.calc.total_area}}}')
                self.pdf.add_equation(r'X_{{cg}} = {}$ $m'.format(self.calc.total_cg_x))

            with doc.create(Subsection(tpdf.centroid_y)):
                self.pdf.add_equation(r'Y_{cg} = \frac{Ms_x}{A_{total}}')
                self.pdf.add_equation(f'Y_{{cg}} = \\frac{{{parse_expr(self.calc.moment_x)}}}{{{self.calc.total_area}}}')
                self.pdf.add_equation(r'Y_{{cg}} = {}$ $m'.format(self.calc.total_cg_y))

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
                self.pdf.add_equation(r'I_{{x_{{total}}}} = {}'.format(self.calc.moment_inertia_x_latex))
                self.pdf.add_equation(r'I_{{x_{{total}}}} = {}$ $m^4'.format(parse_expr(self.calc.moment_inertia_x)))

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
                doc.append(NoEscape(r'I_{{y_{{total}}}} = {}'.format(self.calc.moment_inertia_y_latex)))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{{y_{{total}}}} = {}$ $m^4'.format(parse_expr(self.calc.moment_inertia_y))))
                doc.append(NoEscape(r'\end{dmath*}'))

    def append_normal_stress(self, doc, tpdf):
        with doc.create(Section(tpdf.step_normal_stress_neutral_line)):
            with doc.create(Subsection(tpdf.normal_stress_formula)):
                self.pdf.add_equation(
                    tpdf.normal_stress_var + r' \frac{N}{A} - \frac{My}{Iy} \cdot z - \frac{Mz}{Iz} \cdot y')
            with doc.create(Subsection(tpdf.neutral_line_formula)):
                doc.append(NoEscape(tpdf.neutral_line_tip))
                self.pdf.add_equation(r'0 = \frac{N}{A} - \frac{My}{Iy} \cdot z - \frac{Mz}{Iz} \cdot y')
            for i in range(len(self.mng.normal_stress_latex)):
                with doc.create(Subsection(f'{tpdf.calculating_for} N = {self.mng.points_values[i][0]} N, '
                                           f'My = {parse_expr(self.mng.points_values[i][1])} Nm, '
                                           f'Mz = {parse_expr(self.mng.points_values[i][2])} Nm, '
                                           f'y = {self.mng.points_values[i][3]} m, '
                                           f'z = {self.mng.points_values[i][4]} m')):
                    with doc.create(Subsubsection(tpdf.step_normal_stress)):
                        self.pdf.add_equation(tpdf.normal_stress_var + f'{self.mng.normal_stress_latex[i]}')
                        self.pdf.add_equation(
                            tpdf.normal_stress_var + f'{round_expr(parse_expr(self.mng.normal_stress_numeric[i]), 2)}$ $Pa')
                    with doc.create(Subsubsection(tpdf.step_neutral_line)):
                        self.pdf.add_equation(f'{self.mng.normal_line_latex[i]}')
                        self.pdf.add_equation(f'{self.mng.normal_line_numeric[i]}')

    def append_static_moment_for_shear_stress(self, doc, tpdf):
        with doc.create(Section(tpdf.step_static_moment_cut)):
            with doc.create(Subsection(tpdf.static_moment_cut_formula_above_str)):
                self.pdf.add_equation(tpdf.static_moment_cut_formula_above)

            with doc.create(Subsection(tpdf.static_moment_cut_formula_not_above_str)):
                self.pdf.add_equation(tpdf.static_moment_cut_formula_not_above)

        for i in range(len(self.mng.static_moment_for_shear_latex)):
            with doc.create(Subsection(tpdf.step_static_moment_cut)):
                self.pdf.add_equation(tpdf.static_moment_var + f'{self.mng.static_moment_for_shear_latex[i]}')
                self.pdf.add_equation(tpdf.static_moment_var + f'{round(self.mng.static_moment_for_shear_numeric[i], 2)}$ $m^3')

    def append_shear_flux(self, doc, tpdf):
        with doc.create(Section(tpdf.step_shear_flux)):
            with doc.create(Subsection(tpdf.shear_flux_formula)):
                self.pdf.add_equation(tpdf.shear_flux_var + r' \frac{V \cdot Q}{I_x}')
            for i in range(len(self.mng.shear_flux_latex)):
                with doc.create(
                        Subsection(NoEscape(f'{tpdf.calculating_for} V = {self.mng.points_values_shear_flux[i][0]} N, '
                                            f'Q = {self.mng.points_values_shear_flux[i][1]} m' + r'\textsuperscript{3}'
                                            r', I\textsubscript{x}' +
                                            f' = {parse_expr(self.mng.points_values_shear_flux[i][2])}' +
                                            r' m\textsuperscript{4}'))):

                    self.pdf.add_equation(tpdf.shear_flux_var + f'{self.mng.shear_flux_latex[i]}')
                    self.pdf.add_equation(
                        tpdf.shear_flux_var + f'{round_expr(parse_expr(self.mng.shear_flux_numeric[i]), 2)}' + r'$ $\frac{N}{m}')

    def append_shear_stress(self, doc, tpdf):
        with doc.create(Section(tpdf.step_shear_stress)):
            with doc.create(Subsection(tpdf.shear_stress_formula_str)):
                self.pdf.add_equation(tpdf.shear_stress_var + r' \frac{V \cdot Q}{I_x \cdot t}')
            for i in range(len(self.mng.shear_stress_latex)):
                with doc.create(Subsection(
                        NoEscape(f'{tpdf.calculating_for} V = {self.mng.points_values_shear_stress[i][0]} N, ' +
                                 f'Q = {self.mng.points_values_shear_stress[i][1]} m' + r'\textsuperscript{3}, ' +
                                 r'I\textsubscript{x}' + f' = {parse_expr(self.mng.points_values_shear_stress[i][2])} m'
                                 + r'\textsuperscript{4}, ' + f't = {self.mng.points_values_shear_stress[i][3]} m'))):

                    self.pdf.add_equation(tpdf.shear_stress_var + f'{self.mng.shear_stress_latex[i]}')
                    self.pdf.add_equation(
                        tpdf.shear_stress_var + f'{round_expr(parse_expr(self.mng.shear_stress_numeric[i]), 2)}' + r'$ $Pa')
