import math
from sympy import symbols, solve, sympify
from pylatex import Document, Section, Subsection, Figure, NoEscape, Subsubsection, LineBreak
from StructuresExplained.pdfconfig import header
from StructuresExplained.pdfconfig.translations.structure_strings import translate_PDF_structure
from StructuresExplained.solutions.structure.pdf_generation.tools import get_signal
from StructuresExplained.utils.util import add_to_pdf, append_step, append_result, degree_to_rad


class Generator:
    def __init__(self, support_results, internal_results, system_elements, language, target_dir, filename):
        self.sr = support_results
        self.ir = internal_results
        self.ss = system_elements
        self.language = language
        self.target_dir = target_dir
        self.filename = filename
        self.doc = Document(document_options="a4paper,12pt", documentclass="article")
        self.pdf = add_to_pdf(self.doc)
        self.tpdf = translate_PDF_structure(language)

    def generate_pdf(self):
        self.setup_pdf()

        self.add_structure_figure()

        self.add_free_body_diagram()

        self.add_supports_calculation()

        self.add_internal_calculation()

        self.add_internal_diagrams()

        self.generate()

    def setup_pdf(self):
        self.doc.preamble.append(NoEscape(header.PDFsettings))

        self.doc.append(NoEscape(header.makeCover(self.tpdf.title, self.language)))
    
    def add_structure_figure(self):
        with self.doc.create(Section(self.tpdf.step_figure_image)):

            with self.doc.create(Figure(position='H')) as fig_estrutura:
                fig_estrutura.add_image("figs\\structure", width='500px')
                fig_estrutura.add_caption(NoEscape(self.tpdf.step_figure_image_label))

    def add_free_body_diagram(self):
        with self.doc.create(Section(self.tpdf.step_free_body_diagram_0)):
            with self.doc.create(Figure(position='H')) as fig_corpolivre:
                if self.sr.hinged and self.sr.roll:
                    fig_corpolivre.add_image("figs\\diagram1", width='500px')
                elif self.sr.fixed:
                    fig_corpolivre.add_image("figs\\diagram2", width='500px')
                fig_corpolivre.add_caption(NoEscape(self.tpdf.free_body_diagram_0_label))

    def add_supports_calculation(self):
        with self.doc.create(Section(self.tpdf.step_supports_reaction)):

            if self.sr.fixed:
                self.calculations_fixed()

            elif self.sr.hinged and self.sr.roll:
                self.calculations_hinged_roll()

            with self.doc.create(Subsection(self.tpdf.step_drawing_reactions)):
                with self.doc.create(Figure(position='H')) as fig_apoios:
                    fig_apoios.add_image("figs\\supports", width='500px')
                    fig_apoios.add_caption(NoEscape(self.tpdf.drawing_reactions_label))

    def calculations_fixed(self):
        fixed_reactions = self.ss.reaction_forces.get(self.ss.supports_fixed[0].id)
        with self.doc.create(Subsection(self.tpdf.step_supports_fixed)):
            self.pdf.add_equation(r'\sum{M} = 0 \\')
            self.pdf.add_equation(r'M = F \cdot d \\')
            self.pdf.add_equation(NoEscape(
                f'{append_step(self.sr.moments_sum)}'
                f' {get_signal(fixed_reactions.Ty)} M = 0 \\\\'))
            self.pdf.add_equation(NoEscape(f'M = {append_result(abs(fixed_reactions.Ty))}'))

        with self.doc.create(Subsection(self.tpdf.fixed_EFY)):
            self.pdf.add_equation(r'\sum{Fy} = 0 \\')
            self.pdf.add_equation(
                f'{append_step(self.sr.point_sum_y)} {get_signal(fixed_reactions.Fz)} Fy = 0' r'\\')
            self.pdf.add_equation(f'Fy = {append_result(abs(fixed_reactions.Fz))}')

        with self.doc.create(Subsection(self.tpdf.fixed_EFX)):
            self.pdf.add_equation(r'\sum{Fx} = 0 \\')
            self.pdf.add_equation(
                f'{append_step(self.sr.point_sum_x)} {get_signal(fixed_reactions.Fx)} Fx = 0' r'\\')
            self.pdf.add_equation(f'Fx = {append_result(abs(fixed_reactions.Fx))}')

    def calculations_hinged_roll(self):
        hinged_reactions = self.ss.reaction_forces.get(self.ss.supports_hinged[0].id)
        roll_reactions = self.ss.reaction_forces.get(self.ss.supports_roll[0].id)
        roll_angle = self.sr.inclined_roll.get(self.sr.roll.id)
        if roll_angle is None: roll_angle = 0
        with self.doc.create(Subsection(self.tpdf.fixed_moment)):
            self.pdf.add_equation(r'\sum{M} = 0 \\')
            self.pdf.add_equation(r'M = F \cdot d')

            if roll_angle == math.pi / 2:
                self.pdf.add_equation(NoEscape(
                    f'{append_step(self.sr.moments_sum)} {get_signal(roll_reactions.Fx)} Bx'
                    f' \cdot {append_step(self.sr.roll_dists["y"])} = 0 \\\\'))
                self.pdf.add_equation(NoEscape(f'Bx = {append_result(abs(roll_reactions.Fx))}N'))

            elif roll_angle == 0:
                self.pdf.add_equation(NoEscape(
                    f'{append_step(self.sr.moments_sum)} {get_signal(roll_reactions.Fz)} By'
                    f' \cdot {append_step(self.sr.roll_dists["x"])} = 0 \\\\'))
                self.pdf.add_equation(NoEscape(f'By = {append_result(abs(roll_reactions.Fz))}N'))

            else:
                # degrees is dangerous, might need to use rad for solving
                roll_angle_deg = roll_angle * 180 / math.pi
                Bangle = roll_reactions.Fx / math.sin(roll_angle_deg * math.pi / 180)
                self.pdf.add_equation(NoEscape(
                    f'{append_step(self.sr.moments_sum)} {get_signal(roll_reactions.Fz)}'
                    f' B_{{{append_result(roll_angle_deg)}\degree}} \cdot '
                    f'cos({append_result(roll_angle_deg)}\degree) \cdot {self.sr.roll_dists["x"]}'
                    f' {get_signal(roll_reactions.Fx)} B_{{{append_result(roll_angle_deg)}\degree}}'
                    f' \cdot sen({append_result(roll_angle_deg)}\degree) \cdot '
                    f'{self.sr.roll_dists["y"]} = 0 \\\\'))

                self.pdf.add_equation(
                    NoEscape(f'B_{{{append_result(roll_angle_deg)}\degree}} = {append_result(Bangle)}'))

                self.pdf.add_equation(NoEscape(
                    f'B_x = {append_step(str(Bangle) + "* sen(" + str(roll_angle_deg) + "*degree)")}'
                ))
                self.pdf.add_equation(NoEscape(f'B_x = {append_result(roll_reactions.Fx)}N'))
                self.pdf.add_equation(NoEscape(
                    f'B_y = {append_step(str(Bangle) + "* cos(" + str(roll_angle_deg) + "*degree)")}'
                ))
                self.pdf.add_equation(NoEscape(f'B_y = {append_result(roll_reactions.Fz)}N'))

        with self.doc.create(Section(self.tpdf.step_free_body_diagram_1)):
            with self.doc.create(Figure(position='H')) as fig_corpolivre:
                fig_corpolivre.add_image("figs\\diagram2", width='500px')
                fig_corpolivre.add_caption(NoEscape(self.tpdf.free_body_diagram_1_label))

        with self.doc.create(Subsection(self.tpdf.hinged_EFY)):
            self.pdf.add_equation(r'\sum{Fy} = 0 \\')
            if round(roll_reactions.Fz, 13) != 0:
                self.pdf.add_equation(
                    f'{append_step(self.sr.point_sum_y + "+" + str(-roll_reactions.Fz))}'
                    f' {get_signal(roll_reactions.Fz)} Ay = 0' r'\\')
            else:
                self.pdf.add_equation(
                    f'{append_step(self.sr.point_sum_y)} {get_signal(hinged_reactions.Fz)} Ay = 0' r'\\')
            self.pdf.add_equation(f'Ay = {append_result(abs(hinged_reactions.Fz))}$ $N')

        with self.doc.create(Subsection(self.tpdf.hinged_EFX)):
            self.pdf.add_equation(r'\sum{Fx} = 0 \\')
            if round(roll_reactions.Fx, 13) != 0:
                self.pdf.add_equation(
                    f'{append_step(self.sr.point_sum_x + "+" + str(roll_reactions.Fx))}'
                    f' {get_signal(hinged_reactions.Fx)} Ax = 0' r'\\')
            else:
                self.pdf.add_equation(
                    f'{append_step(self.sr.point_sum_x)} {get_signal(hinged_reactions.Fx)} Ax = 0' r'\\')
            self.pdf.add_equation(f'Ax = {append_result(abs(hinged_reactions.Fx))}$ $N')

    def add_internal_calculation(self):
        with self.doc.create(Section(self.tpdf.step_internal_stress)):

            self.doc.append(self.tpdf.bending_moment_tip)
            self.doc.append(LineBreak())
            self.doc.append(self.tpdf.constant_tip)
            self.doc.append(LineBreak())

            x, s = symbols('x s')
            for element, (axial_force, shear_force, bending_moment, constant_list) in self.ir.items():

                # transform degrees into rad to be able to solve and add variable s to string just to solve for it
                # and easily find the equation with proper signals
                ax = solve(sympify(degree_to_rad(str(axial_force)) + " + s").evalf(), s)[0]
                sh = solve(sympify(degree_to_rad(str(shear_force)) + " + s").evalf(), s)[0]

                with self.doc.create(Subsection(f'{self.tpdf.step_cutting_section} {element.id}')):
                    with self.doc.create(Figure(position='H')) as fig_secoes:
                        fig_secoes.add_image(f"figs\\structure{element.id}", width='500px')
                        fig_secoes.add_caption(NoEscape(self.tpdf.step_cutting_section_label_1 +
                                                        f"{self.tpdf.step_cutting_section_label_2} "
                                                        f"{element.id}"))

                    with self.doc.create(Subsubsection(self.tpdf.step_normal_stress)):
                        self.pdf.add_equation(NoEscape(r'\sum{Fx} = 0 \\'))
                        self.pdf.add_equation(NoEscape(r'{} + N = 0'.format(append_step(axial_force))))
                        self.pdf.add_equation(NoEscape(r'N = {}$ $N'.format(append_result(
                            ax if ax else 0
                        ))))

                    with self.doc.create(Subsubsection(self.tpdf.step_shear_stress)):
                        self.pdf.add_equation(NoEscape(r'\sum{Fy} = 0 \\'))
                        self.pdf.add_equation(NoEscape(fr'{append_step(shear_force)} - V = 0'))
                        self.pdf.add_equation(NoEscape(r'V = {}$ $N'.format(append_result(
                            sh if sh else 0
                        ))))

                    with self.doc.create(Subsubsection(self.tpdf.step_bending_stress)):
                        self.pdf.add_equation(NoEscape(f'M = \\int{append_result(shear_force)} dx'))
                        string = ""

                        for integration_constant in constant_list:
                            if integration_constant[0][0]:
                                self.doc.append(NoEscape(
                                    fr"Encontrando a constante para seção {integration_constant[0][2].id}"))
                                self.pdf.add_equation(NoEscape(
                                    f'{self.tpdf.integration_constant}(x) = {append_step(integration_constant[0][0])}'
                                ))
                                self.pdf.add_equation(NoEscape(f"{self.tpdf.integration_constant}"
                                                               f"({append_result(integration_constant[0][2].l)})"
                                                               f" = {append_result(integration_constant[0][1])}"))
                                string += "+" + integration_constant[0][1]
                        if constant_list:
                            if constant_list[-1][1]:
                                self.doc.append(NoEscape(f"{self.tpdf.need_sum_moment}"))
                            self.pdf.add_equation(f"{self.tpdf.integration_constant} = "
                                                  f"{append_step((string if string else '0') + constant_list[-1][1])}")
                            self.pdf.add_equation(NoEscape(r'M = {}$ $N \cdot m'.format(append_result(bending_moment))))

    def add_internal_diagrams(self):
        with self.doc.create(Section(self.tpdf.step_internal_diagrams)):
            with self.doc.create(Subsection(self.tpdf.step_internal_diagrams_normal)):
                with self.doc.create(Figure(position='H')) as fig_normais:
                    fig_normais.add_image("figs\\axial", width='500px')
                    fig_normais.add_caption(NoEscape(self.tpdf.internal_diagrams_normal_label))

            with self.doc.create(Subsection(self.tpdf.step_internal_diagrams_shear)):
                with self.doc.create(Figure(position='H')) as fig_cortante:
                    fig_cortante.add_image("figs\\shear", width='500px')
                    fig_cortante.add_caption(NoEscape(self.tpdf.internal_diagrams_shear_label))

            with self.doc.create(Subsection(self.tpdf.step_internal_diagrams_moment)):
                with self.doc.create(Figure(position='H')) as fig_momentofletor:
                    fig_momentofletor.add_image("figs\\moment", width='500px')
                    fig_momentofletor.add_caption(NoEscape(self.tpdf.internal_diagrams_moment_label))

    def generate(self):
        self.doc.generate_pdf(fr'{self.target_dir}\{self.filename}',
                              compiler='pdflatex',
                              win_no_console=True,
                              compiler_args=["-enable-installer"])
