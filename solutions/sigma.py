import math
import sympy
from sympy import Number
from sympy.parsing.sympy_parser import parse_expr
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Wedge
from solutions import functions
from pylatex import Document, Section, Subsection, Subsubsection, Figure, NoEscape
import numpy as np


class sigma():

    T_string = []
    T_numeric = []
    points_values = []
    nl_numeric = []
    nl_string = []
    shear_numeric = []
    shear_string = []
    flux_numeric = []
    flux_string = []
    points_values_flux = []
    points_values_shear = []
    Qc_numeric = []
    Qc_string = []
    Qc_s = ''
    bbox_setting = dict(boxstyle="round,pad=0.1", fc="grey", ec="black", lw=1)

    def __init__(self):
        self.sub_areas_rect = {}
        self.sub_areas_cir = {}
        self.Mx = ''
        self.My = ''
        self.At = ''
        self.Ix = ''
        self.Iy = ''
        self.Qc = ''
        self.T = ''
        self.nl = ''
        self.flux = ''
        self.Tcis = ''
        self.Iys = ''
        self.Ixs = ''
        self.xg = 0
        self.yg = 0

    def det_values(self):
        self.reset_values()
        self.sm_rect()
        self.sm_cir()
        self.yg = float(parse_expr(f'({self.Mx}) / ({self.At})'))
        self.xg = float(parse_expr(f'({self.My}) / ({self.At})'))
        self.im_rect()
        self.im_cir()

    def sm_rect(self):
        for key, (x1, y1, x2, y2) in self.sub_areas_rect.items():
            b, h, c, d, A, dc = self.ret_values(x1, y1, x2, y2)

            self.At += f'+ {A:.2f}'
            self.Mx += f'+ {A:.2f} * {c:.2f}'
            self.My += f'+ {A:.2f} * {d:.2f}'

    def sm_cir(self):
        for key, (x, y, r, a) in self.sub_areas_cir.items():
            A, cgy, cgx = self.cir_values(a, r)

            self.At += f'+ {A:.2f}'
            if float(f'{cgy:.2f}') > 0:
                self.Mx += f'+ {A:.2f} * ({y:.2f} + {cgy:.2f})'
            elif float(f'{cgy:.2f}') < 0:
                self.Mx += f'+ {A:.2f} * ({y:.2f} {cgy:.2f})'
            elif float(f'{cgy:.2f}') == 0:
                self.Mx += f'+ {A:.2f} * {y:.2f}'
            if float(f'{cgx:.2f}') > 0:
                self.My += f'+ {A:.2f} * ({x:.2f} + {cgx:.2f})'
            elif float(f'{cgx:.2f}') < 0:
                self.My += f'+ {A:.2f} * ({x:.2f} {cgx:.2f})'
            elif float(f'{cgx:.2f}') == 0:
                self.My += f'+ {A:.2f} * {x:.2f}'

    def im_rect(self):
        for key, (x1, y1, x2, y2) in self.sub_areas_rect.items():
            b, h, c, d, A, dc = self.ret_values(x1, y1, x2, y2)

            self.Iy += f'+((({b:.2f} ** 3) * {h:.2f}) / 12) + ({A:.2f} * (({self.xg:.2f} - {d:.2f}) ** 2))'
            self.Iys += r'+ \frac' + '{' + f'{b:.2f}^3 * {h:.2f}' + '}' + r'{12}'
            if A * (self.xg - d)**2 != 0:
                self.Iys += f'+ {A:.2f} * ({self.xg:.2f} - {d:.2f})^2'

            self.Ix += f'+(({b:.2f} * ({h:.2f} ** 3)) / 12) + ({A:.2f} * (({self.yg:.2f} - {c:.2f}) ** 2))'
            self.Ixs += r'+ \frac' + '{' + f'{b:.2f} * {h:.2f}^3' + '}' + r'{12}'
            if A * (self.yg - c)**2 != 0:
                self.Ixs += f'+ {A:.2f} * ({self.yg:.2f} - {c:.2f})^2'

    def im_cir(self):
        for key, (x, y, r, a) in self.sub_areas_cir.items():
            A, cgy, cgx = self.cir_values(a, r)

            I = f'+({math.pi:.2f} * {r:.2f} ** 4) / 8'
            Is = r'+ \frac' + '{' + f'{math.pi:.2f} * {r:.2f}^4' + '}' + r'{8}'

            self.Iy += f'{I} + {A:.2f} * (({self.xg:.2f} - {x+cgx:.2f})**2)'
            self.Iys += Is
            if A * ((self.xg - x) ** 2) != 0:
                self.Iys += f'+ {A:.2f} * ({self.xg:.2f} - {x+cgx:.2f})^2'

            self.Ix += f'{I} + {A:.2f} * (({self.yg:.2f} - {y+cgy:.2f})**2)'
            self.Ixs += Is
            if A * ((self.yg - y) ** 2) != 0:
                self.Ixs += f'+ {A:.2f} * ({self.yg:.2f} - {y+cgy:.2f})^2'

    def full_sm(self, cut_y):
        self.Qc_s = ''
        self.Qc = 0
        for key, (x1, y1, x2, y2) in self.sub_areas_rect.items():
            b, h, c, d, A, dc = self.ret_values(x1, y1, x2, y2)

            half_height = h / 2
            dist_do_corte = cut_y - c

            if dist_do_corte <= -half_height:
                self.Qc += A * (c - self.yg)
                self.Qc_s += f'+ {A} \cdot ({c} - {self.yg}) '

            elif np.abs(dist_do_corte) <= half_height:
                self.Qc += (h / 2 + c - cut_y) * b * (((h / 2 + c - cut_y) * .5 + cut_y) - self.yg)
                self.Qc_s += f'+ (' + r'\frac{' + f'{h}' + r'}{' + f'{2}' + r'} + ' + f'{c} - {cut_y}) \cdot {b} \cdot ' \
                        r'(((\frac{' + f'{h}' + r'}{' + f'{2}' \
                             + r'} + ' + f'{c} - {cut_y}) \cdot 0.5 + {cut_y}) - {self.yg}) '

        return self.Qc

        # values for circular sectors
        # for key, (x, y, r, a) in self.sub_areas_cir.items():
        #     A, cgy, cgx = self.cir_values(a, r)
        #
        #     Ac = r**2 * np.arccos((cut_y-y)/r) - cut_y-y * (r**2 - d**2)**.5
        #     self.Qc += Ac * (y + cgy - self.yg)

    def ret_values(self, x1, y1, x2, y2):
        b = x2 - x1
        h = y1 - y2
        c = (y1 + y2) / 2
        d = (x1 + x2) / 2
        A = b * h
        dc = c - self.yg
        return b, h, c, d, A, dc

    def cir_values(self, a, r):
        A = (math.pi * r ** 2) / 2
        cgy = math.cos(a * math.pi / 180) * ((4 * r) / (3 * math.pi))
        cgx = math.sin(a * math.pi / 180) * ((4 * r) / (3 * math.pi))
        return A, cgy, cgx

    def det_normal_tension(self, N, At, My, Mz, Ix, Iy, append_to_pdf, y, z):
        T_n = f'({N}/{At}) - (({My}/{Iy}) * {z}) - (({Mz}/{Ix}) * {y})'
        T_s = NoEscape(r'\frac{' + f'{N}' + r'}{' + f'{At}' + r'} - \frac{' + f'{My}' + r'}{' + f'{Iy}'
                       + r'} \cdot' + f' {z} -' + r'\frac{' + f'{Mz}' + r'}{' + f'{Ix}' + r'} \cdot' + f' {y}')

        if (My != "0" and type(z) != str) and (type(y) == str or Mz == "0"):
            self.nl = f"z = {self.round_expr(sympy.solve(T_n, z)[0], 2)}"
        elif (My == "0" and Mz == "0") or (type(y) == str and type(z) == str):
            self.nl = "Não há linha neutra"
        else:
            self.nl = f"y = {self.round_expr(sympy.solve(T_n, y)[0], 2)}"

        nl_s = NoEscape(r'0 = \frac{' + f'{N}' + r'}{' + f'{At}' + r'} - \frac{' + f'{My}' + r'}{' + f'{Iy}'
                        + r'} \cdot z -' + r'\frac{' + f'{Mz}' + r'}{' + f'{Ix}' + r'} \cdot y')
        if append_to_pdf:
            self.append_for_pdf(T_n, T_s, N, My, Mz, y, z, self.nl, nl_s)
        return self.round_expr(parse_expr(T_n), 2), self.nl

    def det_cis(self, V, Q, t, Ix, append_to_pdf):
        self.flux = f'{V} * {Q} / {Ix}'
        flux_s = r'\frac{' + f'{V} \cdot {Q}' + r'}{' + f'{Ix}' + r'}'
        if float(t) != 0:
            self.Tcis = f'({V} * {Q}) / ({Ix} * {t})'
            Tcis_s = r'\frac{' + f'{V} \cdot {Q}' + r'}{' + f'{Ix} \cdot {t}' + r'}'
            if append_to_pdf:
                self.append_for_pdf_shear(self.flux, flux_s, V, Q, Ix, self.Tcis, Tcis_s, t)
            return float(parse_expr(self.flux)), float(parse_expr(self.Tcis))
        else:
            if append_to_pdf:
                self.append_for_pdf_shear(self.flux, flux_s, V, Q, Ix)
            return float(parse_expr(self.flux)), 0

    def det_color(self, c, p):
        if c == p:
            color = 'r'
        else:
            color = 'dodgerblue'
        return color

    def plot_rect(self, p):
        for key, (x1, y1, x2, y2) in self.sub_areas_rect.items():
            b = x2 - x1
            h = y1 - y2
            self.one_fig.text(x1, y1, f'({x1},{y1})', size=functions.size, ha='center', va='bottom', bbox=self.bbox_setting)
            self.one_fig.plot(x1, y1, 'ro')
            self.one_fig.text(x2, y2, f'({x2},{y2})', size=functions.size, ha='center', va='bottom', bbox=self.bbox_setting)
            self.one_fig.plot(x2, y2, 'ro')
            color = self.det_color(key, p)
            self.one_fig.add_patch(Rectangle((x1, y2), b, h, linewidth=5, edgecolor=(10/255,60/255,100/255), facecolor=color, alpha=1))

    def plot_cir(self, p):
        for key, (x, y, r, a) in self.sub_areas_cir.items():
            self.one_fig.plot(x, y, 'ro')
            self.one_fig.text(x, y, f'({x},{y})', size=functions.size, ha='center', va='bottom', bbox=self.bbox_setting)
            color = self.det_color(key, p)
            self.one_fig.add_patch(Wedge((x, y), r, -a, -a-180, linewidth=5, edgecolor='black', facecolor=color))

    def plot(self, p, d, fig=None):
        if fig is None:
            fig = plt.figure()
        else:
            fig.clear()

        self.one_fig = fig.add_subplot(111)

        self.plot_rect(p)
        self.plot_cir(d)

        self.one_fig.plot(self.xg, self.yg, 'ro')
        self.one_fig.text(self.xg, self.yg, f"CG ({self.xg:.1f},{self.yg:.1f})", size=functions.size, ha='center',
                          va='bottom', bbox=self.bbox_setting)

        plt.tight_layout()
        self.one_fig.set_aspect('equal', 'datalim')
        self.one_fig.set_alpha(0.2)
        return fig

    def solver(self):
        doc = Document(document_options="a4paper,12pt", documentclass="article")
        doc.preamble.append(NoEscape(r"""
                \usepackage[left=1.5cm,right=1.5cm,top=2cm,bottom=2cm]{geometry}
                \usepackage{setspace}
                \onehalfspacing
                \usepackage[portuguese]{babel}
                \usepackage{indentfirst}
                \usepackage{graphicx}
                \usepackage{caption}
                \usepackage{amsmath}
                \usepackage{multicol}
                \usepackage[colorlinks=true,linkcolor=black,anchorcolor=black,citecolor=black,filecolor=black,menucolor=black,runcolor=black,urlcolor=black]{hyperref}
                \usepackage{cals, ragged2e, lmodern}
                \usepackage{pdflscape}
                \usepackage{float}
                \usepackage{breqn}

                \title{Cálculos da Seção Transversal}
                \author{}
                """))

        doc.append(NoEscape(r"""
                \maketitle
                """))

        with doc.create(Section(r'Subdividir a geometria da seção transversal em formas geométricas (subáreas) de '
                                r'propriedades conhecidas')):
            with doc.create(Figure(position='H')) as fig_sectransv:
                fig_sectransv.add_image("figs\\sectransv", width='500px')
                fig_sectransv.add_caption(NoEscape(r'\label{fig:estrutura} Estrutura com subáreas contornadas de preto'))

        with doc.create(Section('Calcular os momentos estáticos em relação ao eixo de interesse')):
            if self.sub_areas_cir:
                doc.append(NoEscape(r'Centroide da semi-circunferência:'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'\frac{4 * R}{3 \cdot \pi}'))
                doc.append(NoEscape(r'\end{dmath*}'))

            with doc.create(Subsection('Cálculo do momento estático em relação ao eixo X:')):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{x_{total}} = \sum{Ms_x} \\'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_x = Area_{(sub-área)} \cdot \overline{Y} \\'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{{x_{{total}}}} = {}'.format(self.Mx)))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{{x_{{total}}}} = {:.2f}$ $m^3'.format(parse_expr(self.Mx))))
                doc.append(NoEscape(r'\end{dmath*}'))

            with doc.create(Subsection('Cálculo do momento estático em relação ao eixo Y:')):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{y_{total}} = \sum{Ms_y} \\'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_y = Area_{(sub-área)} \cdot \overline{X} \\'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{{y_{{total}}}} = {}'.format(self.My)))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{{y_{{total}}}} = {:.2f}$ $m^3'.format(parse_expr(self.My))))
                doc.append(NoEscape(r'\end{dmath*}'))

        with doc.create(Section('Calcular os centroides em relação ao eixo de interesse')):
            with doc.create(Subsection('Cálculo do centroide em relação ao eixo X:')):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'X_{cg} = \frac{Ms_y}{A_{total}}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(f'X_{{cg}} = \\frac{{{parse_expr(self.My):.2f}}}{{{self.At}}}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'X_{{cg}} = {:.2f}$ $m'.format(self.xg)))
                doc.append(NoEscape(r'\end{dmath*}'))

            with doc.create(Subsection('Cálculo do centroide em relação ao eixo Y:')):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Y_{cg} = \frac{Ms_x}{A_{total}}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(f'Y_{{cg}} = \\frac{{{parse_expr(self.Mx):.2f}}}{{{self.At}}}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Y_{{cg}} = {:.2f}$ $m'.format(self.yg)))
                doc.append(NoEscape(r'\end{dmath*}'))

        with doc.create(Section('Calcular os momentos de inércia em relação aos eixos de interesse')):
            doc.append(NoEscape(r'Quando necessário (ou, na dúvida, sempre), aplicar o teorema dos eixos paralelos \\'))
            doc.append(NoEscape(r"Teorema dos eixos paralelos: I' = I + A * d² \\"))

            with doc.create(Subsection(r'Cálculo do Momento de Inércia em relação a X:')):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{x_{total}} = \sum{I_x}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                if self.sub_areas_rect:
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'I_{x_{(retângulos)}} = \frac{base \cdot altura^3}{12}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                if self.sub_areas_cir:
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'I_{x_{(semi-circunferência)}} = \frac{\pi \cdot raio^4}{8}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{{x_{{total}}}} = {}'.format(self.Ixs)))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{{x_{{total}}}} = {:.2f}$ $m^4'.format(parse_expr(self.Ix))))
                doc.append(NoEscape(r'\end{dmath*}'))

            with doc.create(Subsection(r'Cálculo do Momento de Inércia em relação a Y:')):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{y_{total}} = \sum{Iy}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                if self.sub_areas_rect:
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'I_{y_{(retângulos)}} = \frac{base^3 \cdot altura}{12}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                if self.sub_areas_cir:
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'I_{y_{(semi-circunferência)}} = \frac{\pi \cdot raio^4}{8}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{{y_{{total}}}} = {}'.format(self.Iys)))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{{y_{{total}}}} = {:.2f}$ $m^4'.format(parse_expr(self.Iy))))
                doc.append(NoEscape(r'\end{dmath*}'))

        if self.T_string:
            with doc.create(Section('Calcular a Tensão Normal e Linha Neutra')):
                with doc.create(Subsection('Fórmula da Tensão Normal')):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'T_{normal} = \frac{N}{A} - \frac{My}{Iy} \cdot z - \frac{Mz}{Iz} \cdot y'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                with doc.create(Subsection('Fórmula da Linha Neutra')):
                    doc.append(NoEscape(r'A linha neutra se encontra onde a Tensão Normal é 0, portanto para encontrar'
                                        r' a posição da linha neutra (y) substituímos T por 0.'))
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'0 = \frac{N}{A} - \frac{My}{Iy} \cdot z - \frac{Mz}{Iz} \cdot y'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                for i in range(len(self.T_string)):
                    with doc.create(Subsection(f'Cálculo para N = {self.points_values[i][0]} N, '
                                               f'My = {self.points_values[i][1]} Nm, Mz = {self.points_values[i][2]} Nm, '
                                               f'y = {self.points_values[i][3]} m, '
                                               f'z = {self.points_values[i][4]} m')):
                        with doc.create(Subsubsection('Cálculo da Tensão Normal')):
                            doc.append(NoEscape(r'\begin{dmath*}'))
                            doc.append(NoEscape(r'T_{normal} =' + f'{self.T_string[i]}'))
                            doc.append(NoEscape(r'\end{dmath*}'))
                            doc.append(NoEscape(r'\begin{dmath*}'))
                            doc.append(NoEscape(r'T_{normal} =' + f'{self.round_expr(parse_expr(self.T_numeric[i]), 2)}$ $Pa'))
                            doc.append(NoEscape(r'\end{dmath*}'))
                        with doc.create(Subsubsection('Cálculo da Linha Neutra')):
                            doc.append(NoEscape(r'\begin{dmath*}'))
                            doc.append(NoEscape(f'{self.nl_string[i]}'))
                            doc.append(NoEscape(r'\end{dmath*}'))
                            doc.append(NoEscape(r'\begin{dmath*}'))
                            doc.append(NoEscape(r'y =' + f'{self.round_expr(self.nl_numeric[i], 2)}'))
                            doc.append(NoEscape(r'\end{dmath*}'))

        if self.flux_string or self.shear_string:
            with doc.create(Section('Calcular o Momento Estático no corte')):

                with doc.create(Subsection('Fórmula do Momento Estático para corte sobre a subárea')):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'M_{estático_{corte}} = Área_{subárea} \cdot (centroide_{subárea} - centroide_{figura})'))
                    doc.append(NoEscape(r'\end{dmath*}'))

                with doc.create(Subsection('Fórmula do Momento Estático para corte acima ou abaixo da subárea')):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'M_{estático_{corte}} = (\frac{altura}{2} + centroide_{subárea} - corte_y) \cdot'
                                        r' base \cdot ((\frac{altura}{2} + centroide_{subárea} - corte_y) \cdot 0.5 + '
                                        r'corte_y - centroide_{figura})'))
                    doc.append(NoEscape(r'\end{dmath*}'))

            for i in range(len(self.Qc_string)):
                    with doc.create(Subsection('Calcular o Momento Estático no corte')):
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'M_{estático_{corte}} =' + f'{self.Qc_string[i]}'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'M_{estático_{corte}} =' + f'{round(self.Qc_numeric[i], 2)}$ $m^3'))
                        doc.append(NoEscape(r'\end{dmath*}'))

        if self.flux_string:
            with doc.create(Section('Calcular o Fluxo de Cisalhamento')):
                with doc.create(Subsection('Fórmula do Fluxo de Cisalhamento')):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'f_{cisalhamento} = \frac{V \cdot Q}{I_x}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                for i in range(len(self.flux_string)):
                    with doc.create(Subsection(NoEscape(f'Cálculo para V = {self.points_values_flux[i][0]} N, '
                                               f'Q = {self.points_values_flux[i][1]} m' + r'\textsuperscript{3}, '
                                               r'I\textsubscript{x}' + f' = {self.points_values_flux[i][2]} m' + r'\textsuperscript{4}'))):
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'f_{cisalhamento} =' + f'{self.flux_string[i]}'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'f_{cisalhamento} =' + f'{self.round_expr(parse_expr(self.flux_numeric[i]), 2)}' + r'$ $\frac{N}{m}'))
                        doc.append(NoEscape(r'\end{dmath*}'))

        if self.shear_string:
            with doc.create(Section('Calcular a Tensão de Cisalhamento')):
                with doc.create(Subsection('Fórmula da Tensão de Cisalhamento')):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'T_{cisalhamento} = \frac{V \cdot Q}{I_x \cdot t}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                for i in range(len(self.shear_string)):
                    with doc.create(Subsection(NoEscape(f'Cálculo para V = {self.points_values_shear[i][0]} N, '
                                               f'Q = {self.points_values_shear[i][1]} m' + r'\textsuperscript{3}, '
                                               r'I\textsubscript{x}' + f' = {self.points_values_shear[i][2]} m' + r'\textsuperscript{4}, '
                                               f't = {self.points_values_shear[i][3]} m'))):
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'T_{cisalhamento} =' + f'{self.shear_string[i]}'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'T_{cisalhamento} =' + f'{self.round_expr(parse_expr(self.shear_numeric[i]), 2)}'+ r'$ $Pa'))
                        doc.append(NoEscape(r'\end{dmath*}'))

        doc.generate_pdf('tmp\\resolucaorm',
                         compiler = 'pdflatex',
                         win_no_console=True,
                         compiler_args=["-enable-installer"])
        #doc.generate_tex('tmp\\resolucaorm')

    def append_for_pdf(self, T_n, T_s, N, My, Mx, y, z, nl_n, nl_s):
        if T_n not in self.T_numeric:
            self.T_numeric.append(T_n)
            self.T_string.append(T_s)
            self.points_values.append([N, My, Mx, y, z])
            self.nl_numeric.append(nl_n)
            self.nl_string.append(nl_s)

    def append_for_pdf_shear(self, flux_n, flux_s, V, Q, Ix, T_n=None, T_s=None, t=None):
        self.flux_numeric.append(flux_n)
        self.flux_string.append(flux_s)
        self.points_values_flux.append([V, Q, Ix])
        self.Qc_numeric.append(self.Qc)
        self.Qc_string.append(self.Qc_s)
        if T_n is not None:
            self.points_values_shear.append([V, Q, Ix, t])
            self.shear_numeric.append(T_n)
            self.shear_string.append(T_s)

    def round_expr(self, expr, num_digits):
        return expr.xreplace({n: round(n, num_digits) for n in expr.atoms(Number)})

    def reset_values(self):
        self.At = self.Mx = self.My = self.Iy = self.Ix = self.Iys = self.Ixs = self.Qc = ''
        self.Qc = self.yg = self.xg = 0
        self.T_string.clear()
        self.T_numeric.clear()
        self.points_values.clear()
        self.nl_numeric.clear()
        self.nl_string.clear()
        self.shear_numeric.clear()
        self.shear_string.clear()
        self.flux_numeric.clear()
        self.flux_string.clear()
        self.points_values_flux.clear()
        self.points_values_shear.clear()
        self.Qc_numeric.clear()
        self.Qc_string.clear()