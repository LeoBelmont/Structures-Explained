import math
import numpy
from StructuresExplained.solutions import functions
from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr
from pylatex import Document, Section, Subsection, Figure, Alignat, NoEscape, Subsubsection, \
    LineBreak
from StructuresExplained.pdfconfig import header
from StructuresExplained.pdfconfig.translations.structure_strings import translate_PDF_structure


class pdf_generator:
    def __init__(self):
        self.language = None
        self.target_dir = None

    def generatePDF(self):
        doc = Document(document_options="a4paper,12pt", documentclass="article")
        doc.preamble.append(NoEscape(header.PDFsettings))
    
        tpdf = translate_PDF_structure(self.language)
    
        doc.append(NoEscape(header.makeCover(tpdf.title, self.language)))
    
        with doc.create(Section(tpdf.step_figure_image)):
    
            with doc.create(Figure(position='H')) as fig_estrutura:
                fig_estrutura.add_image("figs\\structure", width='500px')
                fig_estrutura.add_caption(NoEscape(tpdf.step_figure_image_label))
    
        with doc.create(Section(tpdf.step_free_body_diagram_0)):
            with doc.create(Figure(position='H')) as fig_corpolivre:
                if self.hinged and self.roll:
                    fig_corpolivre.add_image("figs\\diagram1", width='500px')
                elif self.fixed:
                    fig_corpolivre.add_image("figs\\diagram2", width='500px')
                fig_corpolivre.add_caption(NoEscape(tpdf.free_body_diagram_0_label))
    
        with doc.create(Section(tpdf.step_supports_reaction)):
    
            if self.fixed:
                with doc.create(Subsection(tpdf.step_supports_fixed)):
                    with doc.create(Alignat(numbering=False, escape=False)) as sum_M:
                        sum_M.append(r'\sum{M} &= 0 \\')
                        sum_M.append(r'M &= F \cdot d \\')
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(
                    f'{self.moment_sum + self.moment_sum_from_forces} {self.get_signal(self.fixed_reaction_moment)} M = 0 \\\\'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(f'M = {abs(float(self.fixed_reaction_moment))}'))
                doc.append(NoEscape(r'\end{dmath*}'))
    
                with doc.create(Subsection(tpdf.fixed_EFY)):
                    with doc.create(Alignat(escape=False, numbering=False)) as sum_Fy:
                        sum_Fy.append(r'\sum{Fy} = 0 \\')
                        sum_Fy.append(
                            f'{self.total_point_load_y + self.total_q_load_y} {self.get_signal(self.fixed_reaction_y)} Fy = 0' r'\\')
                        sum_Fy.append(f'Fy = {abs(float(self.fixed_reaction_y))}')
    
                with doc.create(Subsection(tpdf.fixed_EFX)):
                    with doc.create(Alignat(escape=False, numbering=False)) as sum_Fx:
                        sum_Fx.append(r'\sum{Fx} = 0 \\')
                        sum_Fx.append(
                            f'{self.total_point_load_x + self.total_q_load_x} {self.get_signal(self.fixed_reaction_x)} Fx = 0' r'\\')
                        sum_Fx.append(f'Fx = {abs(float(self.fixed_reaction_x))}')
    
            elif self.hinged and self.roll:
                roll_angle = self.roll_direction.get(self.idr)
                with doc.create(Subsection(tpdf.fixed_moment)):
                    with doc.create(Alignat(numbering=False, escape=False)) as sum_M:
                        sum_M.append(r'\sum{M} &= 0 \\')
                        sum_M.append(r'M &= F \cdot d')
                    if roll_angle == math.pi / 2:
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(self.symbol_filter(
                            f'{self.moment_sum + self.moment_sum_from_forces} {self.get_signal(self.roll_reaction_x)} Bx \cdot {self.roll_dist_y} = 0 \\\\')))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(f'Bx = {abs(float(self.roll_reaction_x))}'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                    elif roll_angle == 0:
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(self.symbol_filter(
                            f'{self.moment_sum + self.moment_sum_from_forces} {self.get_signal(self.roll_reaction_y)} By \cdot {self.roll_dist_x} = 0 \\\\')))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(f'By = {abs(float(self.roll_reaction_y))}'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                    else:
                        rangle = round(self.roll_direction.get(self.idr) * 180 / math.pi, 2)
                        Bangle = round(float(self.roll_reaction_x) / math.sin(rangle * math.pi / 180), 2)
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(self.symbol_filter(
                            f'{self.moment_sum + self.moment_sum_from_forces} {self.get_signal(self.roll_reaction_y)} B_{{{rangle}\degree}} \cdot cos({rangle}\degree) \cdot {self.roll_dist_x} {self.get_signal(self.roll_reaction_x)} B_{{{rangle}\degree}} \cdot sen({rangle}\degree) \cdot {self.roll_dist_y} = 0 \\\\')))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(f'B_{{{rangle}\degree}} = {Bangle}'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(f'B_x = {Bangle} * sen({rangle}\degree)'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(f'B_x = {round(float(self.roll_reaction_x), 2)}'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(f'B_y = {Bangle} * cos({rangle}\degree)'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(f'B_y = {round(float(self.roll_reaction_y), 2)}'))
                        doc.append(NoEscape(r'\end{dmath*}'))
    
                with doc.create(Section(tpdf.step_free_body_diagram_1)):
                    with doc.create(Figure(position='H')) as fig_corpolivre:
                        fig_corpolivre.add_image("figs\\diagram2", width='500px')
                        fig_corpolivre.add_caption(NoEscape(tpdf.free_body_diagram_1_label))
    
                with doc.create(Subsection(tpdf.hinged_EFY)):
                    with doc.create(Alignat(escape=False, numbering=False)) as sum_Fy:
                        sum_Fy.append(r'\sum{Fy} = 0 \\')
                        if round(float(self.roll_reaction_y), 2) != 0:
                            sum_Fy.append(self.symbol_filter(
                                f'{self.total_point_load_y}{self.total_q_load_y} + {float(self.roll_reaction_y):.2f} {self.get_signal(self.hinged_reaction_y)} Ay = 0' r'\\'))
                        else:
                            sum_Fy.append(self.symbol_filter(
                                f'{self.total_point_load_y}{self.total_q_load_y} {self.get_signal(self.hinged_reaction_y)} Ay = 0' r'\\'))
                        sum_Fy.append(f'Ay = {abs(float(self.hinged_reaction_y))}')
    
                with doc.create(Subsection(tpdf.hinged_EFX)):
                    with doc.create(Alignat(escape=False, numbering=False)) as sum_Fx:
                        sum_Fx.append(r'\sum{Fx} = 0 \\')
                        if float(f'{float(self.roll_reaction_x):.2f}') != 0:
                            sum_Fx.append(self.symbol_filter(
                                f'{self.total_point_load_x}{self.total_q_load_x} + {float(self.roll_reaction_x):.2f} {self.get_signal(self.hinged_reaction_x)} Ax = 0' r'\\'))
                        else:
                            sum_Fx.append(self.symbol_filter(
                                f'{self.total_point_load_x}{self.total_q_load_x} {self.get_signal(self.hinged_reaction_x)} Ax = 0' r'\\'))
                        sum_Fx.append(f'Ax = {abs(float(self.hinged_reaction_x))}')
    
            with doc.create(Subsection(tpdf.step_drawing_reactions)):
                with doc.create(Figure(position='H')) as fig_apoios:
                    fig_apoios.add_image("figs\\supports", width='500px')
                    fig_apoios.add_caption(NoEscape(tpdf.drawing_reactions_label))
    
        with doc.create(Section(tpdf.step_internal_stress)):
    
            doc.append(tpdf.bending_moment_tip)
            doc.append(LineBreak())
            doc.append(tpdf.constant_tip)
            doc.append(LineBreak())
    
            eq = self.eq
            x = symbols("x")
            if self.hinged and self.roll:
                self.idh = self.hinged[0].id
                self.idr = self.roll[0].id
            elif self.fixed:
                self.idf = self.fixed[0].id
    
            for c in range(len(eq)):
    
                vx = ''
                vy = ''
                vx = self.symbol_filter(self.shear_equation_x[c])
                vy = self.symbol_filter(self.shear_equation_y[c])
                V = ''
                M = ''
                const = ''
    
                if self.hinged and self.roll:
                    if c + 1 >= self.idh:
                        _, _, _, fx, fy, _ = self.fetcher(self.node_map.get(self.idh))
                        if float(fx) != 0:
                            vx += f' + {-fx:.2f}'
                        if float(fy) != 0:
                            vy += f' + {-fy:.2f}'
    
                    if c + 1 >= self.idr:
                        _, _, _, fx, fy, _ = self.fetcher(self.node_map.get(self.idr))
                        if fx != 0:
                            vx += f' + {-fx:.2f}'
                        if fy != 0:
                            vy += f' + {-fy:.2f}'
    
                elif self.fixed:
                    if c + 1 >= float(self.idf):
                        _, _, _, fx, fy, _ = self.fetcher(self.node_map.get(self.idf))
                        if fx != 0:
                            vx += f' + {-fx:.2f}'
                        if fy != 0:
                            vy += f' + {-fy:.2f}'
    
                if c != 0:
                    _, xi, yi, _, _, _ = self.fetcher(self.node_map.get(c))
                    _, xf, yf, _, _, _ = self.fetcher(self.node_map.get(c + 1))
                    pos = ((xf - xi) ** 2 + (yf - yi) ** 2) ** 0.5
    
                vxc = vx
                vyc = vy
                if not vxc:
                    vxc = "0"
                if not vyc:
                    vyc = "0"
    
                if (abs(self.angle[c]) != 0) and (abs(self.angle[c]) != (math.pi / 2)):
                    # signals = self.get_signal_vectors(numpy.radians(90) - self.angle[c], vxc, vyc)
                    signals = self.get_signal_vectors(functions.n[c], vxc, vyc, self.angle[c], "cos")
                    vy = f'{signals[0]} ({vyc}) \cdot {tpdf.cos}({90 - (self.angle[c] * 180 / math.pi):.2f}\degree) {signals[1]} ({vxc}) \cdot {tpdf.cos}({self.angle[c] * 180 / math.pi:.2f}\degree)'
                    signals = self.get_signal_vectors(functions.eq[c][2], vxc, vyc, self.angle[c], "sin")
                    vx = f'{signals[0]} ({vyc}) \cdot {tpdf.sin}({90 - (self.angle[c] * 180 / math.pi):.2f}\degree) {signals[1]} ({vxc}) \cdot {tpdf.sin}({self.angle[c] * 180 / math.pi:.2f}\degree)'
                    vxc = f'{signals[0]} (({vyc}) * {math.sin(numpy.radians(90) - self.angle[c])}) {signals[1]} (({vxc}) * {math.sin(self.angle[c])})'
    
                if vxc == '':
                    vxc = '0'
    
                if round(float(parse_expr(self.symbol_filter(vxc))), 2) == -round(functions.n[c], 2):
                    n = vx
                    v = vy
                else:
                    n = vy
                    v = vx
    
                if round(eq[c][0], 2) != 0:
                    M += f'{-eq[c][0]:.2f}x^3'
                    V += f'{-eq[c][0] * 3: .2f}x^2'
    
                if round(eq[c][1], 2) != 0:
                    M += f'+{-eq[c][1]:.2f}x^2'
                    V += f'+{-eq[c][1] * 2:.2f}x'
    
                if round(eq[c][2], 2) != 0:
                    M += f'+{-eq[c][2]:.2f}x'
                    V += f'+{-eq[c][2]:.2f}'
    
                if round(eq[c][3], 2) != 0:
                    M += f'+{-eq[c][3]:.2f}'
    
                if V == '':
                    V = '0'
    
                if M == '':
                    M = '0'
    
                if c != 0:
                    const += f"{-eq[c - 1][0]:.2f} \cdot {pos:.2f}^3"
                    const += f" + {-eq[c - 1][1]:.2f} \cdot {pos:.2f}^2"
                    const += f" + {-eq[c - 1][2]:.2f} \cdot {pos:.2f}"
                    const += f" + {-eq[c - 1][3]:.2f}"
                    numeric_const = (-eq[c - 1][0] * pos ** 3) + (-eq[c - 1][1] * pos ** 2) + (-eq[c - 1][2] * pos) + - \
                        eq[c - 1][3]
    
                with doc.create(Subsection(f'{tpdf.step_cutting_section} {c + 1}')):
                    with doc.create(Figure(position='H')) as fig_secoes:
                        fig_secoes.add_image(f"figs\\structure{c + 1}", width='500px')
                        fig_secoes.add_caption(NoEscape(tpdf.step_cutting_section_label_1 +
                                                        f"{tpdf.step_cutting_section_label_2} {c + 1}"))
    
                    with doc.create(Subsubsection(tpdf.step_normal_stress)):
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'\sum{Fx} = 0 \\'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'{} + N = 0'.format(self.symbol_filter(n))))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'N = {:.2f}'.format(float(functions.n[c]))))
                        doc.append(NoEscape(r'\end{dmath*}'))
    
                    with doc.create(Subsubsection(tpdf.step_shear_stress)):
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'\sum{Fy} = 0 \\'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        if c + 1 in self.q_load.keys() and self.eq_load.get(c + 1) is not None:
                            doc.append(
                                NoEscape(r'{} - V = 0'.format(self.symbol_filter(f'{self.eq_load.get(c + 1)} {v}'))))
                        else:
                            doc.append(NoEscape(r'{} - V = 0'.format(self.symbol_filter(v))))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'V = {}'.format(self.symbol_filter(V))))
                        doc.append(NoEscape(r'\end{dmath*}'))
    
                    with doc.create(Subsubsection(tpdf.step_bending_stress)):
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(f'M = \\int{self.symbol_filter(V)}  dx'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{flushleft}'))
                        doc.append(f'{tpdf.constant_at} {c + 1}:')
                        doc.append(NoEscape(r'\end{flushleft}'))
                        if c != 0:
                            doc.append(NoEscape(r'\begin{dmath*}'))
                            if f'{c + 1}: ' in str(self.moment):
                                doc.append(NoEscape(self.symbol_filter(
                                    f"c = {const} + {self.get_signal_constant(self.moment.get(c + 1), -eq[c][3], numeric_const):.2f}")))
                            else:
                                doc.append(NoEscape(self.symbol_filter(f"c = {const}")))
                            doc.append(NoEscape(r'\end{dmath*}'))
                        elif c == 0 and f'{c + 1}: ' in str(self.moment):
                            doc.append(NoEscape(r'\begin{dmath*}'))
                            doc.append(self.symbol_filter(
                                NoEscape(f'c = {self.get_signal_constant(self.moment.get(c + 1), -eq[c][3]):.2f}')))
                            doc.append(NoEscape(r'\end{dmath*}'))
                        else:
                            doc.append(NoEscape(r'\begin{center}'))
                            doc.append(NoEscape(f'{tpdf.no_moment_at_1} {c + 1}, {tpdf.no_moment_at_2}'))
                            doc.append(NoEscape(r'\end{center}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'M = {}'.format(self.symbol_filter(M))))
                        doc.append(NoEscape(r'\end{dmath*}'))
    
        with doc.create(Section(tpdf.step_internal_diagrams)):
            with doc.create(Subsection(tpdf.step_internal_diagrams_normal)):
                with doc.create(Figure(position='H')) as fig_normais:
                    fig_normais.add_image("figs\\axial", width='500px')
                    fig_normais.add_caption(NoEscape(tpdf.internal_diagrams_normal_label))
    
            with doc.create(Subsection(tpdf.step_internal_diagrams_shear)):
                with doc.create(Figure(position='H')) as fig_cortante:
                    fig_cortante.add_image("figs\\shear", width='500px')
                    fig_cortante.add_caption(NoEscape(tpdf.internal_diagrams_shear_label))
    
            with doc.create(Subsection(tpdf.step_internal_diagrams_moment)):
                with doc.create(Figure(position='H')) as fig_momentofletor:
                    fig_momentofletor.add_image("figs\\moment", width='500px')
                    fig_momentofletor.add_caption(NoEscape(tpdf.internal_diagrams_moment_label))
    
        doc.generate_pdf(r'tmp\resolucao',
                         compiler='pdflatex',
                         win_no_console=True,
                         compiler_args=["-enable-installer"])

    def get_signal(self, fixed_reaction_moment):
        pass

    def symbol_filter(self, param):
        pass

    def fetcher(self, param):
        pass

    def get_signal_vectors(self, param, vxc, vyc, param1, param2):
        pass

    def get_signal_constant(self, param, param1):
        pass
