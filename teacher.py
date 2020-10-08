import math
import numpy
import functions
import re
import pickle
from matplotlib.pyplot import savefig
from sympy import symbols
from sympy import latex
from sympy.parsing.sympy_parser import parse_expr
from anastruct import SystemElements
from pylatex import Document, Section, Subsection, Figure, Alignat, Command, NoEscape, Package, Subsubsection, \
    LineBreak


class Teacher():

    ss = SystemElements()
    eq = functions.eq
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
            self.total_load_y = ''
        self.Ba = None
        self.Vx = []
        self.Vy = []
        self.Vxs = []
        self.angle = []
        self.eq_load = {}
        self.list_load_x = {}
        self.list_load_y = {}
        with open(f'Settings\\blank.pkl', 'rb') as f:
            self.ss, _ = pickle.load(f)

    def solver(self, hinged, roll, roll_direction, fixed, moment, point, q, qi, node_map):
        self.reset()
        if (len(hinged) == 1 and len(roll) == 1) or len(fixed) == 1:
            p = str(point)
            m = str(moment)
            df = str(q)

            # getting fixed support infos
            for c in range(len(hinged)):
                idh, _, _, _, _, _ = self.fetcher(str(hinged[0]))
                _, xh, yh, fxh, fyh, _ = self.fetcher(str(node_map.get(float(idh.group(1)))))
                self.Ax = f'{float(fxh.group(1)):.2f}'
                self.Ay = f'{float(fyh.group(1)):.2f}'

            # getting roll support infos
            for c in range(len(roll)):
                idr, _, _, _, _, _ = self.fetcher(str(roll[0]))
                _, xr, yr, fxr, fyr, _ = self.fetcher(str(node_map.get(float(idr.group(1)))))
                self.Bx = f'{float(fxr.group(1)):.2f}'
                self.By = f'{float(fyr.group(1)):.2f}'
                if abs(roll_direction.get(float(idr.group(1)))) == 0:
                    self.roll_dist = f'{float(xr.group(1)) - float(xh.group(1)):.2f}'
                    self.Ba = self.By
                elif abs(roll_direction.get(float(idr.group(1)))) == math.pi / 2:
                    self.roll_dist = f'{float(yr.group(1)) - float(yh.group(1)):.2f}'
                    self.Ba = self.Bx

            # getting fixed support infos
            for c in range(len(fixed)):
                idf, _, _, _, _, _ = self.fetcher(str(fixed[0]))
                _, xe, ye, fxe, fye, tye = self.fetcher(str(node_map.get(float(idf.group(1)))))
                self.EM = f'{float(tye.group(1)):.2f}'
                self.EFy = f'{float(fye.group(1)):.2f}'
                self.EFx = f'{float(fxe.group(1)):.2f}'

            if fixed:
                yq = ye
                xq = xe
            elif hinged and roll:
                yq = yh
                xq = xh

            for c in range(1, len(node_map)+1):
                _, xi, yi, _, _, _ = self.fetcher(str(node_map.get(c)))
                _, xf, yf, _, _, _ = self.fetcher(str(node_map.get(c + 1)))

                if xf is not None:
                    if c != len(node_map)+1:
                        self.ss.add_element([[float(xi.group(1)), float(yi.group(1))], [float(xf.group(1)), float(yf.group(1))]])
                    if (float(xf.group(1)) - float(xi.group(1))) != 0:
                        self.angle.append(numpy.arctan(
                            (float(yf.group(1)) - float(yi.group(1))) / (float(xf.group(1)) - float(xi.group(1)))))
                    elif (float(xf.group(1)) - float(xi.group(1))) == 0:
                        self.angle.append(numpy.arctan((float(yf.group(1)) - float(yi.group(1))) / 1e-100))

                if hinged and roll:
                    if f'id = {c}' in str(roll[0]):
                        self.ss.point_load(float(idr.group(1)), -float(fxr.group(1)), float(fyr.group(1)))

                    if f'id = {c}' in str(hinged[0]):
                        self.ss.point_load(float(idh.group(1)), -float(fxh.group(1)), float(fyh.group(1)))

                if fixed:
                    if f'id = {c}' in str(fixed[0]):
                        self.ss.add_support_fixed(float(idf.group(1)))

                if f'{c}: ' in p:
                    id_, x, y, _, _, _ = self.fetcher(str(node_map.get(c)))
                    ps = str(point.get(c))
                    ip = re.search(r'((-)?\d+\.\d+), ((-)?\d+\.\d+)', ps)

                    if float(ip.group(1)) > 0:
                        self.total_point_x += f' + {float(ip.group(1)):.2f}'
                    elif float(ip.group(1)) < 0:
                        self.total_point_x += f' {float(ip.group(1)):.2f}'

                    if float(y.group(1)) - float(yq.group(1)) != 0:
                        if float(ip.group(1)) > 0:
                            self.total_point += f' + {float(ip.group(1)):.2f} * {float(y.group(1)) - float(yq.group(1)):.2f}'
                        elif float(ip.group(1)) < 0:
                            self.total_point += f' {float(ip.group(1)):.2f} * {float(y.group(1)) - float(yq.group(1)):.2f}'

                    if float(ip.group(3)) > 0:
                        self.total_point_y += f' + {float(ip.group(3)):.2f}'
                    elif float(ip.group(3)) < 0:
                        self.total_point_y += f' {float(ip.group(3)):.2f}'

                    if float(x.group(1)) - float(yq.group(1)) != 0:
                        if float(ip.group(3)) > 0:
                            self.total_point += f' + {float(ip.group(3)):.2f} * {float(x.group(1)) - float(xq.group(1)):.2f}'
                        elif float(ip.group(3)) < 0:
                            self.total_point += f' {float(ip.group(3)):.2f} * {float(x.group(1)) - float(xq.group(1)):.2f}'

                    self.ss.point_load(float(id_.group(1)), float(ip.group(1)), -float(ip.group(3)))

                if f'{c}: ' in df:
                    x = symbols('x')
                    id_, xi, yi, _, _, _ = self.fetcher(str(node_map.get(c)))
                    _, xf, yf, _, _, _ = self.fetcher(str(node_map.get(c+1)))

                    pos = ((float(xf.group(1)) - float(xi.group(1))) ** 2 +
                           (float(yf.group(1)) - float(yi.group(1))) ** 2) ** 0.5
                    iload = ((float(qi.get(c)) + float(q.get(c))) * pos)/2

                    yload = math.cos(self.angle[c-1] + math.pi) * iload
                    xload = math.sin(self.angle[c-1] + math.pi) * iload
                    cg = (pos / 3) * (float(qi.get(c) + 2*float(q.get(c))) / (float(qi.get(c)) + float(q.get(c))))
                    height = math.sin(self.angle[c-1]) * cg
                    base = math.cos(self.angle[c-1]) * cg

                    if float(f'{xload:.2f}') != 0:
                        self.total_load_x += f' + {-xload:.2f}'
                        if float(f'{height + float(yi.group(1)) - float(yq.group(1)):.2f}') != 0:
                            self.total_moment += f' + {-xload:.2f} * {height + float(yi.group(1)) - float(yq.group(1)):.2f}'

                    if float(f'{yload:.2f}') != 0:
                        self.total_load_y += f' + {-yload:.2f}'
                        if float(f'{base + float(xi.group(1)) - float(yq.group(1)):.2f}') != 0:
                            self.total_moment += f' + {-yload:.2f} * {base + float(xi.group(1)) - float(yq.group(1)):.2f}'

                    self.list_load_x.update({c: self.total_load_x})
                    self.list_load_y.update({c: self.total_load_y})
                    q_part = f'{latex((-((qi.get(c) - q.get(c)) / (6 * pos)) * x ** 2) * 3 + ((qi.get(c) / 2) * x) * 2)}'
                    self.eq_load.update({c: q_part})

                    self.ss.q_load(-q.get(c), -qi.get(c), float(id_.group(1)))

                if f'{c}: ' in m:
                    id_, _, _, _, _, _ = self.fetcher(str(node_map.get(c)))
                    if -moment.get(c) > 0:
                        self.total_moment += f' + {-moment.get(c)}'
                    elif -moment.get(c) < 0:
                        self.total_moment += f' {-moment.get(c)}'
                    self.ss.moment_load(float(id_.group(1)), moment.get(c))

                self.Vy.append(self.total_point_y)
                self.Vx.append(self.total_point_x)

                if f'{c-1}: ' in df:
                    if self.list_load_y.get(c-1) is not None:
                        self.Vy[c-1] += self.list_load_y.get(c-1)
                    if self.list_load_x.get(c-1) is not None:
                        self.Vx[c-1] += self.list_load_x.get(c-1)

                if fixed:
                    if f'id = {c}' in str(fixed[0]):
                        if moment.get(c) is not None:
                            moment.update({c: moment.get(c) + -float(self.EM)})
                        else:
                            moment.update({c: -float(self.EM)})

                self.ss.show_structure()
                savefig(f'Settings\\figs\\structure{c}')

            self.savior(hinged, roll, fixed, node_map, moment, df)

    def fetcher(self, pool):
        id_ = re.search(r'id = (\d+)', pool)
        x = re.search(r' x = ((-)?\d+\.\d+(e(-)?\d+)?)', pool)
        y = re.search(r' y = ((-)?\d+\.\d+(e(-)?\d+)?)', pool)
        fx = re.search(r' Fx = ((-)?\d+\.\d+(e(-)?\d+)?)', pool)
        fy = re.search(r' Fz = ((-)?\d+\.\d+(e(-)?\d+)?)', pool)
        ty = re.search(r' Ty = ((-)?\d+\.\d+(e(-)?\d+)?)', pool)
        return id_, x, y, fx, fy, ty

    def savior(self, hinged, roll, fixed, node_map, moment, df):
        doc = Document("a4paper,top=3cm,bottom=2cm,left=3cm,right=3cm,marginparwidth=2cm")
        doc.packages.append(Package('breqn'))
        doc.packages.append(Package('amsmath'))
        doc.packages.append(Package('float'))
        doc.preamble.append(Command('title', 'Resolução'))
        doc.append(NoEscape(r'\maketitle'))
        doc.packages.append(Package('babel', options=['portuguese']))
        doc.append(NoEscape(r'\pagenumbering{gobble}'))

        with doc.create(Section('Imagem da Estrutura')):

            with doc.create(Figure(position='H')) as fig_estrutura:
                fig_estrutura.add_image("figs\\structure", width='300px')
                fig_estrutura.add_caption(NoEscape(r'\label{fig:estrutura} Imagem da estrutura com apoios e carregamentos'))

        with doc.create(Section('Fazendo o diagrama de corpo livre')):
            with doc.create(Figure(position='H')) as fig_corpolivre:
                fig_corpolivre.add_image("figs\\structure", width='300px')
                fig_corpolivre.add_caption(NoEscape(r'\label{fig:corpolivre} Diagrama de corpo livre'))

        with doc.create(Section('Calculando a reação dos apoios')):

            if fixed:
                with doc.create(Subsection('Realizando cálculo do momento no engaste')):
                    with doc.create(Alignat(numbering=False, escape=False)) as sum_M:
                        sum_M.append(r'\sum{M} &= 0 \\')
                        sum_M.append(r'M &= F * d \\')
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(f'{self.total_moment + self.total_point} + M = 0 \\\\'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(f'M = {self.EM}'))
                doc.append(NoEscape(r'\end{dmath*}'))

                with doc.create(Subsection('Fazendo a somatória das forças em Y para obter a reação em Y no engaste')):
                    with doc.create(Alignat(escape=False, numbering=False)) as sum_Fy:
                        sum_Fy.append(r'\sum{Fy} = 0 \\')
                        sum_Fy.append(f'{self.total_point_y}{self.total_load_y} + Ay = 0' r'\\')
                        sum_Fy.append(f'Ay = {-float(self.EFy)}')

                with doc.create(Subsection('Fazendo a somatória das forças em X para obter a reação em X no engaste')):
                    with doc.create(Alignat(escape=False, numbering=False)) as sum_Fx:
                        sum_Fx.append(r'\sum{Fx} = 0 \\')
                        sum_Fx.append(f'{self.total_point_x}{self.total_load_x} + Ax = 0' r'\\')
                        sum_Fx.append(f'Ax = {-float(self.EFx)}')

            elif hinged and roll:
                with doc.create(Subsection('Realizando cálculo do momento no apoio fixo')):
                    with doc.create(Alignat(numbering=False, escape=False)) as sum_M:
                        sum_M.append(r'\sum{M} &= 0 \\')
                        sum_M.append(r'M &= F * d \\')
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(f'{self.total_moment+self.total_point} + Br * {self.roll_dist} = 0 \\\\'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(f'Br = \\frac{{{float(-parse_expr(self.total_moment+self.total_point)):.2f}}}{{{float(self.roll_dist):.2f}}}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(f'Br = {-float(self.Ba)}'))
                doc.append(NoEscape(r'\end{dmath*}'))

                with doc.create(Subsection('Fazendo a somatória das forças em Y para obter a reação em Y no apoio fixo')):
                    with doc.create(Alignat(escape=False, numbering=False)) as sum_Fy:
                        sum_Fy.append(r'\sum{Fy} = 0 \\')
                        if float(f'{float(self.By):.2f}') != 0:
                            sum_Fy.append(f'{self.total_point_y}{self.total_load_y} - {float(self.By):.2f} + Ay = 0' r'\\')
                        else:
                            sum_Fy.append(f'{self.total_point_y}{self.total_load_y} + Ay = 0' r'\\')
                        sum_Fy.append(f'Ay = {-float(self.Ay)}')

                with doc.create(Subsection('Fazendo a somatória das forças em X para obter a reação em X no apoio fixo')):
                    with doc.create(Alignat(escape=False, numbering=False)) as sum_Fx:
                        sum_Fx.append(r'\sum{Fx} = 0 \\')
                        if float(f'{float(self.Bx):.2f}') != 0:
                            sum_Fx.append(f'{self.total_point_x}{self.total_load_x} - {float(self.Bx):.2f} + Ax = 0' r'\\')
                        else:
                            sum_Fx.append(f'{self.total_point_x}{self.total_load_x} + Ax = 0' r'\\')
                        sum_Fx.append(f'Ax = {-float(self.Ax)}')

            with doc.create(Subsection('Desenhando as reações dos apoios')):
                with doc.create(Figure(position='H')) as fig_apoios:
                    fig_apoios.add_image("figs\\supports", width='300px')
                    fig_apoios.add_caption(NoEscape(r'\label{fig:apoios} Reações dos apoios'))

        with doc.create(Section('Calculando os esforços internos')):

            doc.append('A partir da integral da força cortante, é obtido o momento fletor.')
            doc.append(LineBreak())
            doc.append('A constante de integração será o momento no nó final da seção anterior.')
            doc.append(LineBreak())

            with doc.create(Subsection('Cortando nas Seções')):

                eq = self.eq
                x = symbols("x")
                if hinged and roll:
                    idh = re.search(r'id = (\d+)', str(hinged[0]))
                    idr = re.search(r'id = (\d+)', str(roll[0]))
                elif fixed:
                    idf = re.search(r'id = (\d+)', str(fixed[0]))

                for c in range(len(eq)):

                    vx = self.Vx[c]
                    vy = self.Vy[c]
                    V = ''
                    M = ''
                    const = ''

                    if hinged and roll:
                        if c + 1 >= float(idh.group(1)):
                            _, _, _, fx, fy, _ = self.fetcher(str(node_map.get(float(idh.group(1)))))
                            if -float(fx.group(1)) > 0:
                                vx += f' + {-float(fx.group(1)):.2f}'
                            elif -float(fx.group(1)) < 0:
                                vx += f' {-float(fx.group(1)):.2f}'
                            if -float(fy.group(1)) > 0:
                                vy += f' + {-float(fy.group(1)):.2f}'
                            elif -float(fy.group(1)) < 0:
                                vy += f' {-float(fy.group(1)):.2f}'

                        if c + 1 >= float(idr.group(1)):
                            _, _, _, fx, fy, _ = self.fetcher(str(node_map.get(float(idr.group(1)))))
                            if -float(fx.group(1)) > 0:
                                vx += f' + {-float(fx.group(1)):.2f}'
                            elif -float(fx.group(1)) < 0:
                                vx += f' {-float(fx.group(1)):.2f}'
                            if -float(fy.group(1)) > 0:
                                vy += f' + {-float(fy.group(1)):.2f}'
                            elif -float(fy.group(1)) < 0:
                                vy += f' {-float(fy.group(1)):.2f}'

                    elif fixed:
                        if c + 1 >= float(idf.group(1)):
                            _, _, _, fx, fy, _ = self.fetcher(str(node_map.get(float(idf.group(1)))))
                            if -float(fx.group(1)) > 0:
                                vx += f' + {-float(fx.group(1)):.2f}'
                            elif -float(fx.group(1)) < 0:
                                vx += f' {-float(fx.group(1)):.2f}'
                            if -float(fy.group(1)) > 0:
                                vy += f' + {-float(fy.group(1)):.2f}'
                            elif -float(fy.group(1)) < 0:
                                vy += f' {-float(fy.group(1)):.2f}'

                    if c != 0:
                        _, xi, yi, _, _, _ = self.fetcher(str(node_map.get(c)))
                        _, xf, yf, _, _, _ = self.fetcher(str(node_map.get(c + 1)))
                        pos = ((float(xf.group(1)) - float(xi.group(1))) ** 2 +
                               (float(yf.group(1)) - float(yi.group(1))) ** 2) ** 0.5

                    vxc = vx
                    vyc = vy
                    if (abs(self.angle[c]) != 0) and (abs(self.angle[c]) != (math.pi / 2)):
                        vy = f'+({vyc}) * sen({self.angle[c] * 180 / math.pi:.2f}) - ({vxc}) * cos({self.angle[c] * 180 / math.pi:.2f})'
                        vx = f'+({vyc}) * cos({self.angle[c] * 180 / math.pi:.2f}) + ({vxc}) * sen({self.angle[c] * 180 / math.pi:.2f})'
                        vxc = f'(({vyc}) * {math.cos(self.angle[c])}) + (({vxc}) * {math.sin(self.angle[c])})'

                    if vxc == '':
                        vxc = '0'

                    if f'{float(-parse_expr(vxc)):.2f}' == functions.n[c]:
                        n = vx
                        v = vy
                    else:
                        n = vy
                        v = vx

                    if float(f'{eq[c][0]:.2f}') != 0:
                        M += f'{eq[c][0]:.2f}x^3'
                        V += f'{eq[c][0] * 3: .2f}x^2'

                    if float(f'{eq[c][1]:.2f}') > 0:
                        M += f'+{eq[c][1]:.2f}x^2'
                        V += f'+{eq[c][1] * 2: .2f}x'
                    elif float(f'{eq[c][1]:.2f}') < 0:
                        M += f'{eq[c][1]:.2f}x^2'
                        V += f'{eq[c][1] * 2: .2f}x'

                    if float(f'{eq[c][2]:.2f}') > 0:
                        M += f'+{eq[c][2]:.2f}x'
                        V += f'+{eq[c][2]: .2f}'
                    elif float(f'{eq[c][2]:.2f}') < 0:
                        M += f'{eq[c][2]:.2f}x'
                        V += f'{eq[c][2]: .2f}'

                    if float(f'{eq[c][3]:.2f}') > 0:
                        M += f'+{eq[c][3]:.2f}'
                    elif float(f'{eq[c][3]:.2f}') < 0:
                        M += f'{eq[c][3]:.2f}'

                    if V == '':
                        V = '0'

                    if M == '':
                        M = '0'

                    if c != 0:
                        if float(f'{eq[c-1][0]:.2f}') != 0:
                            const += f'{eq[c-1][0]:.2f}*{pos:.2f}^3'

                        if float(f'{eq[c-1][1]:.2f}') > 0:
                            const += f' + {eq[c - 1][1]:.2f}*{pos:.2f}^2'
                        elif float(f'{eq[c-1][1]:.2f}') < 0:
                            const += f' {eq[c-1][1]:.2f}*{pos:.2f}^2'

                        if float(f'{eq[c-1][2]:.2f}') > 0:
                            const += f' + {eq[c - 1][2]:.2f}*{pos:.2f}'
                        elif float(f'{eq[c-1][2]:.2f}') < 0:
                            const += f' {eq[c-1][2]:.2f}*{pos:.2f}'

                        if float(f'{eq[c-1][3]:.2f}') > 0:
                            const += f' + {eq[c-1][3]: .2f}'
                        elif float(f'{eq[c-1][3]:.2f}') < 0:
                            const += f' {eq[c-1][3]: .2f}'

                    with doc.create(Subsubsection(f'Cortando na Seção {c+1}')):
                        with doc.create(Figure(position='H')) as fig_secoes:
                            fig_secoes.add_image(f"figs\\structure{c+1}", width='300px')
                            fig_secoes.add_caption(NoEscape(r'\label{fig:secoes}' f"Seção {c+1}"))

                        doc.append(NoEscape(r'\begin{flushleft}'))
                        doc.append(NoEscape(r'\textbf{1) Força Normal:}'))
                        doc.append(NoEscape(r'\end{flushleft}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'\sum{Fx} = 0 \\'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'{} + N = 0'.format(latex(n))))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'N = {:.2f}'.format(float(functions.n[c]))))
                        doc.append(NoEscape(r'\end{dmath*}'))

                        doc.append(NoEscape(r'\begin{flushleft}'))
                        doc.append(NoEscape(r'\textbf{2) Força Cortante:}'))
                        doc.append(NoEscape(r'\end{flushleft}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'\sum{Fy} = 0 \\'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        if f'{c + 1}' in df and self.eq_load.get(c + 1) is not None:
                            doc.append(NoEscape(r'{} - V = 0'.format(f'{self.eq_load.get(c+1)} {v}')))
                        else:
                            doc.append(NoEscape(r'{} - V = 0'.format(latex(v))))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(r'V = {}'.format(V)))
                        doc.append(NoEscape(r'\end{dmath*}'))

                        doc.append(NoEscape(r'\begin{flushleft}'))
                        doc.append(NoEscape(r'\textbf{3) Momento Fletor:}'))
                        doc.append(NoEscape(r'\end{flushleft}'))
                        with doc.create(Alignat(escape=False, numbering=False)) as int_V:
                            int_V.append(f'M = \\int{V}  dx')
                        doc.append(NoEscape(r'\begin{flushleft}'))
                        doc.append(f'Constante no nó {c+1}:')
                        doc.append(NoEscape(r'\end{flushleft}'))
                        with doc.create(Alignat(escape=False, numbering=False)) as cons:
                            if c != 0:
                                if f'{c+1}: ' in str(moment):
                                    cons.append(f"c = {const} + {moment.get(c+1):.2f}")
                                else:
                                    cons.append(f"c = {const}")
                            elif c == 0 and f'{c+1}: ' in str(moment):
                                cons.append(f'c = {moment.get(c+1):.2f}')
                            else:
                                cons.append('c = 0')
                        with doc.create(Alignat(escape=False, numbering=False)) as mf:
                            mf.append(r'M = {}'.format(M))

                        doc.append(LineBreak())
                        doc.append(LineBreak())

        with doc.create(Section('Fazendo os diagramas de esforços internos')):
            with doc.create(Subsection('Desenhando o diagrama da força normal:')):
                with doc.create(Figure(position='H')) as fig_normais:
                    fig_normais.add_image("figs\\axial", width='300px')
                    fig_normais.add_caption(NoEscape(r'\label{fig:normais} Força normal'))

            with doc.create(Subsection('Desenhando o diagrama da força cortante:')):
                with doc.create(Figure(position='H')) as fig_cortante:
                    fig_cortante.add_image("figs\\shear", width='300px')
                    fig_cortante.add_caption(NoEscape(r'\label{fig:cortante} Força cortante'))

            with doc.create(Subsection('Desenhando o diagrama do momento fletor:')):
                with doc.create(Figure(position='H')) as fig_momentofletor:
                    fig_momentofletor.add_image("figs\\moment", width='300px')
                    fig_momentofletor.add_caption(NoEscape(r'\label{fig:momento} Momento Fletor'))

        doc.generate_pdf(f'Settings\\resolucao', compiler='pdflatex')
