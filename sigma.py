import math
from sympy import symbols, Number
from sympy.parsing.sympy_parser import parse_expr
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Wedge
import functions
from pylatex import Document, Section, Subsection, Figure, Command, NoEscape, Package


class sigma():

    def __init__(self):
        self.sub_areas_rect = {}
        self.sub_areas_cir = {}
        self.y = symbols("y")
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
        self.At = self.Mx = self.My = self.Iy = self.Ix = self.Iys = self.Ixs = ''
        self.Qc = self.yg = self.xg = 0
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

            self.Qc += A * abs(dc)

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

            self.Qc += A * abs(y + cgy - self.yg)

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

    def det_normal_tension(self, N, At, My, Mx, Ix, Iy):
        self.T = f'({N}/{At}) - (({My}/{Iy}) * {self.y}) - (({Mx}/{Ix}) * {self.y})'
        self.nl = f'{N}/{At}'
        if My != 0 or Mx != 0:
            self.nl += f'* (1/(({My}/{Iy}) - ({Mx}/{Ix})))'
        return self.round_expr(parse_expr(self.T), 2), float(parse_expr(self.nl))

    def det_cis(self, V, Q, t, Ix):
        self.flux = f'{V} * {Q} / {Ix}'
        if float(t) != 0:
            self.Tcis = f'({V} * {Q}) / ({Ix} * {t})'
            return float(parse_expr(self.flux)), float(parse_expr(self.Tcis))
        else:
            return float(parse_expr(self.flux)), 0

    def det_color(self, c, p):
        if c == p:
            color = 'r'
        else:
            color = 'b'
        return color

    def plot_rect(self, p):
        for key, (x1, y1, x2, y2) in self.sub_areas_rect.items():
            b = x2 - x1
            h = y1 - y2
            plt.plot(x1, y1, 'ro')
            plt.annotate(f'({x1},{y1})', (x1, y1), size=functions.size, ha='center', va='bottom')
            plt.plot(x2, y2, 'ro')
            plt.annotate(f'({x2},{y2})', (x2, y2), size=functions.size, ha='center', va='bottom')
            color = self.det_color(key, p)
            plt.gca().add_patch(Rectangle((x1, y2), b, h, linewidth=5, edgecolor='black', facecolor=color))

    def plot_cir(self, p):
        for key, (x, y, r, a) in self.sub_areas_cir.items():
            plt.plot(x, y, 'ro')
            plt.annotate(f'({x},{y})', (x, y), size=functions.size, ha='center', va='bottom')
            color = self.det_color(key, p)
            plt.gca().add_patch(Wedge((x, y), r, -a, -a-180, linewidth=5, edgecolor='black', facecolor=color))

    def plot(self, p, d, fig=None):
        if fig is None:
            fig = plt.figure()
        else:
            fig.clear()

        self.plot_rect(p)
        self.plot_cir(d)

        plt.plot(self.xg, self.yg, 'ro')
        plt.annotate(f"CG ({self.xg:.1f},{self.yg:.1f})", (self.xg, self.yg), size=functions.size, ha='center', va='bottom')

        plt.tight_layout()
        return fig

    def solver(self):
        doc = Document("a4paper,top=3cm,bottom=2cm,left=3cm,right=3cm,marginparwidth=2cm")
        doc.packages.append(Package('breqn'))
        doc.packages.append(Package('amsmath'))
        doc.packages.append(Package('float'))
        doc.preamble.append(Command('title', 'Resolução'))
        doc.append(NoEscape(r'\maketitle'))
        doc.packages.append(Package('babel', options=['portuguese']))
        doc.append(NoEscape(r'\pagenumbering{gobble}'))

        with doc.create(Section(r'Subdividir a geometria da seção transversal em formas geométricas (sub-áreas) de '
                                r'propriedades conhecidas')):
            with doc.create(Figure(position='H')) as fig_sectransv:
                fig_sectransv.add_image("figs\\sectransv", width='400px')
                fig_sectransv.add_caption(NoEscape(r'\label{fig:estrutura} Estrutura com sub-áreas contornadas de preto'))

        with doc.create(Section('Calcular os momentos estáticos em relação ao eixo de interesse')):
            if self.sub_areas_cir:
                doc.append(NoEscape(r'Centroide da semi-circunferência:'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'\frac{4 * R}{3 * \pi}'))
                doc.append(NoEscape(r'\end{dmath*}'))

            with doc.create(Subsection('Cálculo do momento estático em relação ao eixo X:')):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{x_{total}} = \sum{Ms_x} \\'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_x = Area_{(sub-área)} * \overline{Y} \\'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{{x_{{total}}}} = {}'.format(self.Mx)))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{{x_{{total}}}} = {:.2f}'.format(parse_expr(self.Mx))))
                doc.append(NoEscape(r'\end{dmath*}'))

            with doc.create(Subsection('Cálculo do momento estático em relação ao eixo Y:')):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{y_{total}} = \sum{Ms_y} \\'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_y = Area_{(sub-área)} * \overline{X} \\'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{{y_{{total}}}} = {}'.format(self.My)))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{{y_{{total}}}} = {:.2f}'.format(parse_expr(self.My))))
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
                doc.append(NoEscape(r'X_{{cg}} = {:.2f}'.format(self.xg)))
                doc.append(NoEscape(r'\end{dmath*}'))

            with doc.create(Subsection('Cálculo do centroide em relação ao eixo Y:')):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Y_{cg} = \frac{Ms_x}{A_{total}}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(f'Y_{{cg}} = \\frac{{{parse_expr(self.Mx):.2f}}}{{{self.At}}}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Y_{{cg}} = {:.2f}'.format(self.yg)))
                doc.append(NoEscape(r'\end{dmath*}'))

        with doc.create(Section('Calcular os momentos de inércia em relação aos eixos de interesse')):
            doc.append(NoEscape(r'Quando necessário (ou, na dúvida, sempre), aplicar o teorema dos eixos paralelos \\'))
            doc.append(NoEscape(r"Teorema dos eixos paralelos: I' = I + A * d² \\"))

            with doc.create(Subsection(r'Cálculo do Momento de Inércia em relação a X:')):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{x_{total}} = \sum{Ix}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                if self.sub_areas_rect:
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'I_{x_{(retângulos)}} = \frac{base * altura^3}{12}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                if self.sub_areas_cir:
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'I_{x_{(semi-circunferência)}} = \frac{\pi * raio^4}{8}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{{x_{{total}}}} = {}'.format(self.Ixs)))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{{x_{{total}}}} = {:.2f}'.format(parse_expr(self.Ix))))
                doc.append(NoEscape(r'\end{dmath*}'))

            with doc.create(Subsection(r'Cálculo do Momento de Inércia em relação a Y:')):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{y_{total}} = \sum{Iy}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                if self.sub_areas_rect:
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'I_{y_{(retângulos)}} = \frac{base^3 * altura}{12}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                if self.sub_areas_cir:
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'I_{y_{(semi-circunferência)}} = \frac{\pi * raio^4}{8}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{{y_{{total}}}} = {}'.format(self.Iys)))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{{y_{{total}}}} = {:.2f}'.format(parse_expr(self.Iy))))
                doc.append(NoEscape(r'\end{dmath*}'))

        doc.generate_pdf('Settings\\resolucaorm', compiler='pdflatex')

    def round_expr(self, expr, num_digits):
        return expr.xreplace({n: round(n, num_digits) for n in expr.atoms(Number)})
