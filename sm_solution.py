import math
import numpy
import functions
import re
import pickle
from matplotlib import pyplot as plt
from matplotlib.pyplot import savefig
from sympy import symbols, Number
from sympy import latex
from sympy.parsing.sympy_parser import parse_expr
from anastruct import SystemElements
from pylatex import Document, Section, Subsection, Figure, Alignat, Command, NoEscape, Package, Subsubsection, \
    LineBreak


class Teacher():

    ss = SystemElements()
    blankss = pickle.dumps(ss)
    eq = functions.eq
    functions.n.clear()
    total_moment = ''
    total_point = ''
    total_point_y = ''
    total_point_x = ''
    total_load_y = ''
    total_load_x = ''
    roll_dist = ''
    By = ''
    Bx = ''
    Ay = ''
    Ax = ''
    EM = ''
    EFy = ''
    EFx = ''
    Ba = None
    Vx = []
    Vy = []
    Vxs = []
    angle = []
    eq_load = {}
    list_load_y = {}
    list_load_x = {}

    def reset(self):
        self.total_moment = self.total_point = self.total_point_x = self.total_point_y = self.roll_dist = \
            self.By = self.Bx = self.Ay = self.Ax = self.EM = self.EFy = self.EFx = self.total_load_x = \
            self.total_load_y = self.Bstring = ''
        self.Ba = None
        self.Vx.clear()
        self.Vy.clear()
        self.Vxs.clear()
        self.angle.clear()
        self.eq_load = {}
        self.list_load_x = {}
        self.list_load_y = {}
        self.ss = pickle.loads(self.blankss)

    def get_hinged_info(self, hinged, node_map):
        if hinged:
            self.idh = hinged[0].id
            _, self.xh, self.yh, self.fxh, self.fyh, _ = self.fetcher(node_map.get(self.idh))
            self.Ax = f'{-self.fxh:.2f}'
            self.Ay = f'{-self.fyh:.2f}'

    def get_roll_info(self, roll, node_map, roll_direction):
        for c in range(len(roll)):
            self.idr = roll[0].id
            _, xr, yr, self.fxr, self.fyr, _ = self.fetcher(node_map.get(self.idr))
            self.Bx = f'{-self.fxr:.2f}'
            self.By = f'{-self.fyr:.2f}'
            self.roll_dist_x = f'{xr - self.xh:.2f}i'
            self.roll_dist_y = f'{yr - self.yh:.2f}j'

    def get_fixed_info(self, fixed, node_map):
        if fixed:
            self.idf = fixed[0].id
            _, self.xe, self.ye, self.fxe, self.fye, self.tye = self.fetcher(node_map.get(self.idf))
            self.EM = f'{-self.tye:.2f}'
            self.EFy = f'{-self.fye:.2f}'
            self.EFx = f'{-self.fxe:.2f}'

    def get_element_angle(self, c, node_map):
        if node_map.get(c+1):
            _, xi, yi, _, _, _ = self.fetcher(node_map.get(c))
            _, xf, yf, _, _, _ = self.fetcher(node_map.get(c + 1))

            if c != len(node_map) + 1:
                self.ss.add_element([[xi, yi], [xf, yf]])
            if (xf - xi) != 0:
                self.angle.append(numpy.arctan((yf - yi) / (xf - xi)))
            elif (xf - xi) == 0:
                self.angle.append(numpy.arctan((yf - yi) / 1e-100))

    def add_supports(self, c, hinged, roll, fixed):
        if hinged and roll:
            if roll[0].id == c:
                self.ss.point_load(self.idr, -self.fxr, -self.fyr)

            if hinged[0].id == c:
                self.ss.point_load(self.idh, -self.fxh, -self.fyh)

        if fixed:
            if fixed[0].id == c:
                self.ss.point_load(self.idf, -self.fxe, -self.fye)
                self.ss.moment_load(self.idf, self.tye)

    def map_loads(self, c, node_map, p, xq, yq):
        if c in p.keys():
            id_, x, y, _, _, _ = self.fetcher(node_map.get(c))
            fx = p[id_][0]
            fy = -p[id_][1]

            if fx != 0:
                self.total_point_x += f' {fx:.2f}'

            if y - yq != 0:
                if fx != 0:
                    self.total_point += f' + {fx:.2f}i \cdot {y - yq:.2f}j'

            if fy != 0:
                self.total_point_y += f' {fy:.2f}'

            if float(x) - float(xq) != 0:
                if fy != 0:
                    self.total_point += f' + {fy:.2f}j \cdot {x - xq:.2f}i'

            self.ss.point_load(id_, fx, fy)

    def get_qload_values(self, c, q, qi, xi, xf, yi, yf):
        pos = ((xf - xi) ** 2 + (yf - yi) ** 2) ** 0.5
        iload = ((-qi.get(c) + -q.get(c)) * pos) / 2

        yload = -(math.cos(self.angle[c - 1] + math.pi) * iload)
        xload = math.sin(self.angle[c - 1] + math.pi) * iload
        cg = (pos / 3) * (float(qi.get(c) + 2 * float(q.get(c))) / (float(qi.get(c)) + float(q.get(c))))
        height = math.sin(self.angle[c - 1]) * cg
        base = math.cos(self.angle[c - 1]) * cg

        return pos, iload, yload, xload, cg, height, base

    def map_qloads(self, c, node_map, df, xq, yq, q, qi):
        if c in df.keys():
            x = symbols('x')
            id_, xi, yi, _, _, _ = self.fetcher(node_map.get(c))
            _, xf, yf, _, _, _ = self.fetcher(node_map.get(c + 1))

            pos, iload, yload, xload, cg, height, base = self.get_qload_values(c, q, qi, xi, xf, yi, yf)

            if round(xload, 2) != 0:
                self.total_load_x += f' + {xload:.2f}'
                if float(f'{height + yi - yq:.2f}') != 0:
                    self.total_moment += f' + {xload:.2f}i \cdot {height + yi - yq:.2f}j'

            if round(yload, 2) != 0:
                self.total_load_y += f' + {yload:.2f}'
                if round(base + xi - yq, 2) != 0:
                    self.total_moment += f' + {yload:.2f}j \cdot {base + xi - xq:.2f}i'

            self.list_load_x.update({c: self.total_load_x})
            self.list_load_y.update({c: self.total_load_y})
            q_part = ((((qi.get(c) - q.get(c)) / (6 * pos)) * x ** 2) * 3 - ((qi.get(c) / 2) * x) * 2)
            self.eq_load.update({c: str(latex(self.round_expr(q_part, 2)))})

            self.ss.q_load(-q.get(c), -qi.get(c), float(id_))

    def map_moments(self, c, node_map, m, moment):
        if c in m.keys():
            id_ = node_map.get(c).id
            if moment.get(c) > 0:
                self.total_moment += f' + {moment.get(c)}k'
            elif moment.get(c) < 0:
                self.total_moment += f' {moment.get(c)}k'
            self.ss.moment_load(float(id_), moment.get(c))

    def solver(self, hinged, roll, roll_direction, fixed, moment, point, q, qi, node_map):
        self.reset()
        if (len(hinged) == 1 and len(roll) == 1) or len(fixed) == 1:
            p = point
            m = moment
            df = q

            self.get_hinged_info(hinged, node_map)

            self.get_roll_info(roll, node_map, roll_direction)

            self.get_fixed_info(fixed, node_map)

            if fixed:
                yq = self.ye
                xq = self.xe
            elif hinged and roll:
                yq = self.yh
                xq = self.xh

            plt.style.use('default')
            for c in range(1, len(node_map)+1):
                self.get_element_angle(c, node_map)

                self.add_supports(c, hinged, roll, fixed)

                self.map_loads(c, node_map, p, xq, yq)

                self.map_qloads(c, node_map, df, xq, yq, q, qi)

                self.map_moments(c, node_map, m, moment)

                self.Vy.append(self.total_point_y)
                self.Vx.append(self.total_point_x)

                if c-1 in df.keys():
                    if self.list_load_y.get(c-1) is not None:
                        self.Vy[c-1] += self.list_load_y.get(c-1)
                    if self.list_load_x.get(c-1) is not None:
                        self.Vx[c-1] += self.list_load_x.get(c-1)

                if fixed:
                    if fixed[0].id == c:
                        if moment.get(c) is not None:
                            moment.update({c: moment.get(c) + float(self.EM)})
                        else:
                            moment.update({c: float(self.EM)})

                self.ss.show_structure()
                savefig(f'Settings\\figs\\structure{c}')

            plt.style.use('dark_background')
            self.savior(hinged, roll, roll_direction, fixed, node_map, moment, df)

    def fetcher(self, pool):
        id_ = pool.id
        x = pool.vertex.x
        y = pool.vertex.y
        fx = pool.Fx
        fy = pool.Fy
        ty = pool.Ty
        return id_, x, y, fx, fy, ty

    def savior(self, hinged, roll, roll_direction, fixed, node_map, moment, df):
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
                \usepackage{gensymb}
                \usepackage{helvet}
                \renewcommand{\familydefault}{\sfdefault}

                \title{Cálculos da Estrutura}
                \author{}
                """))

        doc.append(NoEscape(r"""
                \maketitle
                """))

        self.filter_strings()

        with doc.create(Section('Imagem da Estrutura')):

            with doc.create(Figure(position='H')) as fig_estrutura:
                fig_estrutura.add_image("figs\\structure", width='500px')
                fig_estrutura.add_caption(NoEscape(r'\label{fig:estrutura} Imagem da estrutura com apoios e carregamentos'))

        with doc.create(Section('Fazendo o diagrama de corpo livre')):
            with doc.create(Figure(position='H')) as fig_corpolivre:
                if hinged and roll:
                    fig_corpolivre.add_image("figs\\diagram1", width='500px')
                elif fixed:
                    fig_corpolivre.add_image("figs\\diagram2", width='500px')
                fig_corpolivre.add_caption(NoEscape(r'\label{fig:corpolivre} Diagrama de corpo livre'))

        with doc.create(Section('Calculando a reação dos apoios')):

            if fixed:
                with doc.create(Subsection('Realizando cálculo do momento no engaste')):
                    with doc.create(Alignat(numbering=False, escape=False)) as sum_M:
                        sum_M.append(r'\sum{M} &= 0 \\')
                        sum_M.append(r'M &= F \cdot d \\')
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(f'{self.total_moment + self.total_point} {self.get_signal(self.EM)} M = 0 \\\\'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(f'M = {abs(float(self.EM))}'))
                doc.append(NoEscape(r'\end{dmath*}'))

                with doc.create(Subsection('Fazendo a somatória das forças em Y para obter a reação em Y no engaste')):
                    with doc.create(Alignat(escape=False, numbering=False)) as sum_Fy:
                        sum_Fy.append(r'\sum{Fy} = 0 \\')
                        sum_Fy.append(f'{self.total_point_y + self.total_load_y} {self.get_signal(self.EFy)} Fy = 0' r'\\')
                        sum_Fy.append(f'Fy = {abs(float(self.EFy))}')

                with doc.create(Subsection('Fazendo a somatória das forças em X para obter a reação em X no engaste')):
                    with doc.create(Alignat(escape=False, numbering=False)) as sum_Fx:
                        sum_Fx.append(r'\sum{Fx} = 0 \\')
                        sum_Fx.append(f'{self.total_point_x + self.total_load_x} {self.get_signal(self.EFx)} Fx = 0' r'\\')
                        sum_Fx.append(f'Fx = {abs(float(self.EFx))}')

            elif hinged and roll:
                roll_angle = roll_direction.get(self.idr)
                with doc.create(Subsection('Realizando cálculo do momento no apoio fixo')):
                    with doc.create(Alignat(numbering=False, escape=False)) as sum_M:
                        sum_M.append(r'\sum{M} &= 0 \\')
                        sum_M.append(r'M &= F \cdot d')
                    if roll_angle == math.pi/2:
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(self.symbol_filter(f'{self.total_moment+self.total_point} {self.get_signal(self.Bx)} Bx \cdot {self.roll_dist_y} = 0 \\\\')))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(f'Bx = {abs(float(self.Bx))}'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                    elif roll_angle == 0:
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(self.symbol_filter(f'{self.total_moment+self.total_point} {self.get_signal(self.By)} By \cdot {self.roll_dist_x} = 0 \\\\')))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(f'By = {abs(float(self.By))}'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                    else:
                        rangle = round(roll_direction.get(self.idr) * 180/math.pi, 2)
                        Bangle = round(float(self.Bx) / math.sin(rangle * math.pi/180), 2)
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(self.symbol_filter(
                            f'{self.total_moment + self.total_point} {self.get_signal(self.By)} B_{{{rangle}\degree}} \cdot cos({rangle}\degree) \cdot {self.roll_dist_x} {self.get_signal(self.Bx)} B_{{{rangle}\degree}} \cdot sen({rangle}\degree) \cdot {self.roll_dist_y} = 0 \\\\')))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(f'B_{{{rangle}\degree}} = {Bangle}'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(f'B_x = {Bangle} * sen({rangle}\degree)'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(f'B_x = {round(float(self.Bx), 2)}'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(f'B_y = {Bangle} * cos({rangle}\degree)'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(f'B_y = {round(float(self.By), 2)}'))
                        doc.append(NoEscape(r'\end{dmath*}'))

                with doc.create(Section('Refazendo o diagrama de corpo livre')):
                    with doc.create(Figure(position='H')) as fig_corpolivre:
                        fig_corpolivre.add_image("figs\\diagram2", width='500px')
                        fig_corpolivre.add_caption(NoEscape(r'\label{fig:corpolivre} Diagrama de corpo livre'))

                with doc.create(Subsection('Fazendo a somatória das forças em Y para obter a reação em Y no apoio fixo')):
                    with doc.create(Alignat(escape=False, numbering=False)) as sum_Fy:
                        sum_Fy.append(r'\sum{Fy} = 0 \\')
                        if round(float(self.By), 2) != 0:
                            sum_Fy.append(self.symbol_filter(f'{self.total_point_y}{self.total_load_y} + {float(self.By):.2f} {self.get_signal(self.Ay)} Ay = 0' r'\\'))
                        else:
                            sum_Fy.append(self.symbol_filter(f'{self.total_point_y}{self.total_load_y} {self.get_signal(self.Ay)} Ay = 0' r'\\'))
                        sum_Fy.append(f'Ay = {abs(float(self.Ay))}')

                with doc.create(Subsection('Fazendo a somatória das forças em X para obter a reação em X no apoio fixo')):
                    with doc.create(Alignat(escape=False, numbering=False)) as sum_Fx:
                        sum_Fx.append(r'\sum{Fx} = 0 \\')
                        if float(f'{float(self.Bx):.2f}') != 0:
                            sum_Fx.append(self.symbol_filter(f'{self.total_point_x}{self.total_load_x} + {float(self.Bx):.2f} {self.get_signal(self.Ax)} Ax = 0' r'\\'))
                        else:
                            sum_Fx.append(self.symbol_filter(f'{self.total_point_x}{self.total_load_x} {self.get_signal(self.Ax)} Ax = 0' r'\\'))
                        sum_Fx.append(f'Ax = {abs(float(self.Ax))}')

            with doc.create(Subsection('Desenhando as reações dos apoios')):
                with doc.create(Figure(position='H')) as fig_apoios:
                    fig_apoios.add_image("figs\\supports", width='500px')
                    fig_apoios.add_caption(NoEscape(r'\label{fig:apoios} Reações dos apoios'))

        with doc.create(Section('Calculando os esforços internos')):

            doc.append('A partir da integral da força cortante, é obtido o momento fletor.')
            doc.append(LineBreak())
            doc.append('A constante de integração será o momento no nó final da seção anterior.')
            doc.append(LineBreak())

            eq = self.eq
            x = symbols("x")
            if hinged and roll:
                self.idh = hinged[0].id
                self.idr = roll[0].id
            elif fixed:
                self.idf = fixed[0].id

            for c in range(len(eq)):

                vx = ''
                vy = ''
                vx = self.symbol_filter(self.Vx[c])
                vy = self.symbol_filter(self.Vy[c])
                V = ''
                M = ''
                const = ''

                if hinged and roll:
                    if c + 1 >= self.idh:
                        _, _, _, fx, fy, _ = self.fetcher(node_map.get(self.idh))
                        if float(fx) != 0:
                            vx += f' + {-fx:.2f}'
                        if float(fy) != 0:
                            vy += f' + {-fy:.2f}'

                    if c + 1 >= self.idr:
                        _, _, _, fx, fy, _ = self.fetcher(node_map.get(self.idr))
                        if fx != 0:
                            vx += f' + {-fx:.2f}'
                        if fy != 0:
                            vy += f' + {-fy:.2f}'

                elif fixed:
                    if c + 1 >= float(self.idf):
                        _, _, _, fx, fy, _ = self.fetcher(node_map.get(self.idf))
                        if fx != 0:
                            vx += f' + {-fx:.2f}'
                        if fy != 0:
                            vy += f' + {-fy:.2f}'

                if c != 0:
                    _, xi, yi, _, _, _ = self.fetcher(node_map.get(c))
                    _, xf, yf, _, _, _ = self.fetcher(node_map.get(c + 1))
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
                    vy = f'{signals[0]} ({vyc}) \cdot cos({90-(self.angle[c] * 180 / math.pi):.2f}\degree) {signals[1]} ({vxc}) \cdot cos({self.angle[c] * 180 / math.pi:.2f}\degree)'
                    signals = self.get_signal_vectors(functions.eq[c][2], vxc, vyc, self.angle[c], "sin")
                    vx = f'{signals[0]} ({vyc}) \cdot sen({90-(self.angle[c] * 180 / math.pi):.2f}\degree) {signals[1]} ({vxc}) \cdot sen({self.angle[c] * 180 / math.pi:.2f}\degree)'
                    vxc = f'{signals[0]} (({vyc}) * {math.sin(numpy.radians(90)-self.angle[c])}) {signals[1]} (({vxc}) * {math.sin(self.angle[c])})'

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
                    const += f"{-eq[c-1][0]:.2f} \cdot {pos:.2f}^3"
                    const += f" + {-eq[c-1][1]:.2f} \cdot {pos:.2f}^2"
                    const += f" + {-eq[c-1][2]:.2f} \cdot {pos:.2f}"
                    const += f" + {-eq[c-1][3]:.2f}"
                    numeric_const = (-eq[c-1][0] * pos**3) + (-eq[c-1][1] * pos**2) + (-eq[c-1][2] * pos) + -eq[c-1][3]

                with doc.create(Subsection(f'Cortando na Seção {c+1}')):
                    with doc.create(Figure(position='H')) as fig_secoes:
                        fig_secoes.add_image(f"figs\\structure{c+1}", width='500px')
                        fig_secoes.add_caption(NoEscape(r'\label{fig:secoes}' f"Seção {c+1}"))

                    with doc.create(Subsubsection(f"Força Normal")):
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'\sum{Fx} = 0 \\'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'{} + N = 0'.format(self.symbol_filter(n))))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'N = {:.2f}'.format(float(functions.n[c]))))
                        doc.append(NoEscape(r'\end{dmath*}'))

                    with doc.create(Subsubsection(f"Força Cortante")):
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'\sum{Fy} = 0 \\'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        if c+1 in df.keys() and self.eq_load.get(c + 1) is not None:
                            doc.append(NoEscape(r'{} - V = 0'.format(self.symbol_filter(f'{self.eq_load.get(c+1)} {v}'))))
                        else:
                            doc.append(NoEscape(r'{} - V = 0'.format(self.symbol_filter(v))))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'V = {}'.format(self.symbol_filter(V))))
                        doc.append(NoEscape(r'\end{dmath*}'))

                    with doc.create(Subsubsection(f'Momento Fletor')):
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(f'M = \\int{self.symbol_filter(V)}  dx'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{flushleft}'))
                        doc.append(f'Constante no nó {c+1}:')
                        doc.append(NoEscape(r'\end{flushleft}'))
                        if c != 0:
                            doc.append(NoEscape(r'\begin{dmath*}'))
                            if f'{c+1}: ' in str(moment):
                                doc.append(NoEscape(self.symbol_filter(f"c = {const} + {self.get_signal_constant(moment.get(c+1), numeric_const, -eq[c][3]):.2f}")))
                            else:
                                doc.append(NoEscape(self.symbol_filter(f"c = {const}")))
                            doc.append(NoEscape(r'\end{dmath*}'))
                        elif c == 0 and f'{c+1}: ' in str(moment):
                            doc.append(NoEscape(r'\begin{dmath*}'))
                            doc.append(self.symbol_filter(NoEscape(f'c = {self.get_signal_constant(moment.get(c+1), numeric_const, -eq[c][3]):.2f}')))
                            doc.append(NoEscape(r'\end{dmath*}'))
                        else:
                            doc.append(NoEscape(r'\begin{center}'))
                            doc.append(NoEscape(f'Não há momento no nó {c+1}, portanto c = 0'))
                            doc.append(NoEscape(r'\end{center}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'M = {}'.format(self.symbol_filter(M))))
                        doc.append(NoEscape(r'\end{dmath*}'))

        with doc.create(Section('Desenhando os diagramas de esforços internos')):
            with doc.create(Subsection('Desenhando o diagrama da força normal:')):
                with doc.create(Figure(position='H')) as fig_normais:
                    fig_normais.add_image("figs\\axial", width='500px')
                    fig_normais.add_caption(NoEscape(r'\label{fig:normais} Força normal'))

            with doc.create(Subsection('Desenhando o diagrama da força cortante:')):
                with doc.create(Figure(position='H')) as fig_cortante:
                    fig_cortante.add_image("figs\\shear", width='500px')
                    fig_cortante.add_caption(NoEscape(r'\label{fig:cortante} Força cortante'))

            with doc.create(Subsection('Desenhando o diagrama do momento fletor:')):
                with doc.create(Figure(position='H')) as fig_momentofletor:
                    fig_momentofletor.add_image("figs\\moment", width='500px')
                    fig_momentofletor.add_caption(NoEscape(r'\label{fig:momento} Momento Fletor'))

        doc.generate_pdf(r'Settings\resolucao', compiler='pdflatex')
        doc.generate_tex(r'Settings\resolucao')

    def filter_strings(self):
        self.total_moment = self.symbol_filter(self.total_moment)
        self.total_point = self.symbol_filter(self.total_point)
        self.total_point_y = self.symbol_filter(self.total_point_y)
        self.total_point_x = self.symbol_filter(self.total_point_x)
        self.total_load_y = self.symbol_filter(self.total_load_y)
        self.total_load_x = self.symbol_filter(self.total_load_x)

    def symbol_filter(self, string):
        string = string.replace('- -', '+')
        string = string.replace('--', '+')
        string = string.replace('+ -', '-')
        string = string.replace('+-', '-')
        #string = string.replace('+ 0.00', '')
        #string = string.replace('- 0.00', '')
        search = re.search(r'\\cdot -(\d+\.\d+)', string)
        if search:
            string = re.sub(r'\\cdot -(\d+\.\d+)', f'\\\\cdot (-{search.group(1)})', string)
        return string

    def get_signal(self, string):
        if re.search(r'(-)', string):
            return '-'
        else:
            return '+'

    def get_signal_constant(self, moment, numeric_const, result):
        if math.isclose(round(moment + numeric_const, 2), round(result, 2), rel_tol=1e-2):
            return moment
        else:
            return -moment

    def get_signal_vectors(self, result, fx, fy, angle, op):
        rel_value = 1e-2
        result = round(result, 2)
        fx = parse_expr(fx)
        fy = parse_expr(fy)

        if op == "sin":
            fx = fx * math.sin(angle)
            fy = fy * math.sin(numpy.radians(90) - angle)
        elif op == "cos":
            fx = fx * math.cos(angle)
            fy = fy * math.cos(numpy.radians(90) - angle)

        if math.isclose(round(-fx + fy, 2), result, rel_tol=rel_value):
            return "-", "+"

        elif math.isclose(round(fx - fy, 2), result, rel_tol=rel_value):
            return "+", "-"

        elif math.isclose(round(fx + fy, 2), result, rel_tol=rel_value):
            return "+", "+"

        else:
            return "-", "-"

    def round_expr(self, expr, num_digits):
        return expr.xreplace({n: round(n, num_digits) for n in expr.atoms(Number)})