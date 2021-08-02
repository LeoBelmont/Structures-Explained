from sympy.parsing.sympy_parser import parse_expr
from pylatex import Document, Section, Subsection, Subsubsection, Figure, NoEscape
from StructuresExplained.pdfconfig import header
from StructuresExplained.pdfconfig.translations.cross_sec_strings import translate_PDF_cross_section
from StructuresExplained.utils.util import round_expr


class pdf_generator:
    def __init__(self, manager, calculator):

        self.mng = manager
        self.calc = calculator

    def solver(self, language):
        doc = Document(document_options="a4paper,12pt", documentclass="article")
        doc.preamble.append(NoEscape(header.PDFsettings))

        tpdf = translate_PDF_cross_section(language)

        doc.append(NoEscape(header.makeCover(tpdf.title, language)))

        with doc.create(Section(tpdf.step_split)):
            with doc.create(Figure(position='H')) as fig_sectransv:
                fig_sectransv.add_image("figs\\sectransv", width='500px')
                fig_sectransv.add_caption(NoEscape(tpdf.figure_label))

        with doc.create(Section(tpdf.step_static_moment)):
            if self.calc.subareas_circle:
                doc.append(NoEscape(tpdf.centroid))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'\frac{4 * R}{3 \cdot \pi}'))
                doc.append(NoEscape(r'\end{dmath*}'))

            with doc.create(Subsection(tpdf.step_static_moment_x)):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{x_{total}} = \sum{Ms_x} \\'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(tpdf.msx_operation))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{{x_{{total}}}} = {}'.format(self.calc.moment_x)))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{{x_{{total}}}} = {:.2f}$ $m^3'.format(parse_expr(self.calc.moment_x))))
                doc.append(NoEscape(r'\end{dmath*}'))

            with doc.create(Subsection(tpdf.step_static_moment_y)):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{y_{total}} = \sum{Ms_y} \\'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(tpdf.msy_operation))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{{y_{{total}}}} = {}'.format(self.calc.moment_y)))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{{y_{{total}}}} = {:.2f}$ $m^3'.format(parse_expr(self.calc.moment_y))))
                doc.append(NoEscape(r'\end{dmath*}'))

        with doc.create(Section(tpdf.step_centroid)):
            with doc.create(Subsection(tpdf.centroid_x)):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'X_{cg} = \frac{Ms_y}{A_{total}}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(f'X_{{cg}} = \\frac{{{parse_expr(self.calc.moment_y)}}}{{{self.calc.total_area}}}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'X_{{cg}} = {:.2f}$ $m'.format(self.calc.total_cg_x)))
                doc.append(NoEscape(r'\end{dmath*}'))

            with doc.create(Subsection(tpdf.centroid_y)):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Y_{cg} = \frac{Ms_x}{A_{total}}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(f'Y_{{cg}} = \\frac{{{parse_expr(self.calc.moment_x)}}}{{{self.calc.total_area}}}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Y_{{cg}} = {:.2f}$ $m'.format(self.calc.total_cg_y)))
                doc.append(NoEscape(r'\end{dmath*}'))

        with doc.create(Section(tpdf.step_moment_inercia)):
            doc.append(NoEscape(tpdf.moment_inercia_tip))
            doc.append(NoEscape(tpdf.theorem_formula))

            with doc.create(Subsection(tpdf.moment_inercia_x)):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{x_{total}} = \sum{I_x}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                if self.calc.subareas_rectangle:
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.moment_inercia_x_rect_formula))
                    doc.append(NoEscape(r'\end{dmath*}'))
                if self.calc.subareas_circle:
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.moment_inercia_x_circ_formula))
                    doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{{x_{{total}}}} = {}'.format(self.calc.moment_inertia_x_latex)))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{{x_{{total}}}} = {:.2f}$ $m^4'.format(parse_expr(self.calc.moment_inertia_x))))
                doc.append(NoEscape(r'\end{dmath*}'))

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
                doc.append(NoEscape(r'I_{{y_{{total}}}} = {:.2f}$ $m^4'.format(parse_expr(self.calc.moment_inertia_y))))
                doc.append(NoEscape(r'\end{dmath*}'))

        if self.mng.normal_stress_latex:
            with doc.create(Section(tpdf.step_normal_stress_neutral_line)):
                with doc.create(Subsection(tpdf.normal_stress_formula)):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(
                        tpdf.normal_stress_var + r' \frac{N}{A} - \frac{My}{Iy} \cdot z - \frac{Mz}{Iz} \cdot y'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                with doc.create(Subsection(tpdf.neutral_line_formula)):
                    doc.append(NoEscape(tpdf.neutral_line_tip))
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'0 = \frac{N}{A} - \frac{My}{Iy} \cdot z - \frac{Mz}{Iz} \cdot y'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                for i in range(len(self.mng.normal_stress_latex)):
                    with doc.create(Subsection(f'{tpdf.calculating_for} N = {self.mng.points_values[i][0]} N, '
                                               f'My = {self.mng.points_values[i][1]} Nm, Mz = {self.mng.points_values[i][2]} Nm, '
                                               f'y = {self.mng.points_values[i][3]} m, '
                                               f'z = {self.mng.points_values[i][4]} m')):
                        with doc.create(Subsubsection(tpdf.step_normal_stress)):
                            doc.append(NoEscape(r'\begin{dmath*}'))
                            doc.append(NoEscape(tpdf.normal_stress_var + f'{self.mng.normal_stress_latex[i]}'))
                            doc.append(NoEscape(r'\end{dmath*}'))
                            doc.append(NoEscape(r'\begin{dmath*}'))
                            doc.append(NoEscape(
                                tpdf.normal_stress_var + f'{round_expr(parse_expr(self.mng.normal_stress_numeric[i]), 2)}$ $Pa'))
                            doc.append(NoEscape(r'\end{dmath*}'))
                        with doc.create(Subsubsection(tpdf.step_neutral_line)):
                            doc.append(NoEscape(r'\begin{dmath*}'))
                            doc.append(NoEscape(f'{self.mng.normal_line_latex[i]}'))
                            doc.append(NoEscape(r'\end{dmath*}'))
                            doc.append(NoEscape(r'\begin{dmath*}'))
                            doc.append(NoEscape(f'{self.mng.normal_line_numeric[i]}'))
                            doc.append(NoEscape(r'\end{dmath*}'))

        if self.mng.shear_flux_latex or self.mng.shear_stress_latex:
            with doc.create(Section(tpdf.step_static_moment_cut)):

                with doc.create(Subsection(tpdf.static_moment_cut_formula_above_str)):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.static_moment_cut_formula_above))
                    doc.append(NoEscape(r'\end{dmath*}'))

                with doc.create(Subsection(tpdf.static_moment_cut_formula_not_above_str)):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.static_moment_cut_formula_not_above))
                    doc.append(NoEscape(r'\end{dmath*}'))

            for i in range(len(self.calc.static_moment_cut_latex)):
                with doc.create(Subsection(tpdf.step_static_moment_cut)):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.static_moment_var + f'{self.mng.static_moment_cut_latex[i]}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(
                        NoEscape(tpdf.static_moment_var + f'{round(self.mng.static_moment_cut_numeric[i], 2)}$ $m^3'))
                    doc.append(NoEscape(r'\end{dmath*}'))

        if self.mng.shear_flux_latex:
            with doc.create(Section(tpdf.step_shear_flux)):
                with doc.create(Subsection(tpdf.shear_flux_formula)):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.shear_flux_var + r' \frac{V \cdot Q}{I_x}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                for i in range(len(self.mng.shear_flux_latex)):
                    with doc.create(
                            Subsection(NoEscape(f'{tpdf.calculating_for} V = {self.mng.points_values_shear_flux[i][0]} N, '
                                                f'Q = {self.mng.points_values_shear_flux[i][1]} m' + r'\textsuperscript{3}, '
                                                                                                 r'I\textsubscript{x}' + f' = {self.mng.points_values_shear_flux[i][2]} m' + r'\textsuperscript{4}'))):
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(tpdf.shear_flux_var + f'{self.mng.shear_flux_latex[i]}'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(
                            tpdf.shear_flux_var + f'{round_expr(parse_expr(self.mng.shear_flux_numeric[i]), 2)}' + r'$ $\frac{N}{m}'))
                        doc.append(NoEscape(r'\end{dmath*}'))

        if self.mng.shear_stress_latex:
            with doc.create(Section(tpdf.step_shear_stress)):
                with doc.create(Subsection(tpdf.shear_stress_formula_str)):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.shear_stress_var + r' \frac{V \cdot Q}{I_x \cdot t}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                for i in range(len(self.mng.shear_stress_latex)):
                    with doc.create(Subsection(
                            NoEscape(f'{tpdf.calculating_for} V = {self.mng.points_values_shear_stress[i][0]} N, ' +
                                     f'Q = {self.mng.points_values_shear_stress[i][1]} m' + r'\textsuperscript{3}, ' +
                                     r'I\textsubscript{x}' + f' = {self.mng.points_values_shear_stress[i][2]} m' +
                                     r'\textsuperscript{4}, ' + f't = {self.mng.points_values_shear_stress[i][3]} m'))):
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(tpdf.shear_stress_var + f'{self.mng.shear_stress_latex[i]}'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(
                            tpdf.shear_stress_var + f'{round_expr(parse_expr(self.mng.shear_stress_numeric[i]), 2)}' + r'$ $Pa'))
                        doc.append(NoEscape(r'\end{dmath*}'))

        doc.generate_pdf('tmp\\resolucaorm',
                         compiler='pdflatex',
                         win_no_console=True,
                         compiler_args=["-enable-installer"])
        # doc.generate_tex('tmp\\resolucaorm')
