from matplotlib.patches import Wedge, Rectangle
import numpy
from solutions import functions
from pylatex import Document, Section, Subsection, Figure, NoEscape
from sympy import Symbol, latex, simplify
from solutions import header


class mohr_circle():

    bbox_setting = dict(boxstyle="round,pad=0.1", fc="grey", ec="black", lw=1)
    mode = None
    edgecolor = 'white'

    def __init__(self):
        self.sx = None
        self.sy = None
        self.sz = None
        self.txy = None
        self.txz = None
        self.tyz = None
        self.sigma1 = None
        self.sigma2 = None
        self.sigma3 = None
        self.Tmax = None
        self.angle = None
        self.triple = False
        self.one_fig = None
        self.fig = None

    def state(self, fig, mode=None):
        self.mode = mode
        if self.sz is None:
            return self.plain_state(self.sx, self.sy, self.txy, fig)
        else:
            return self.triple_state(self.sx, self.sy, self.sz, self.txy, self.txz, self.tyz, fig)

    def plain_state(self, sx, sy, txy, fig):
        sigma1 = (sx + sy) / 2 + (((sx - sy) / 2) ** 2 + txy ** 2) ** 0.5
        sigma2 = (sx + sy) / 2 - (((sx - sy) / 2) ** 2 + txy ** 2) ** 0.5
        center = (sx + sy) / 2
        angle = (numpy.arctan(txy/(sx - center)))
        Tmax = (((sx - sy)/2)**2 + txy**2)**0.5
        if not self.triple:
            self.save_values(sigma1, sigma2, Tmax, sx, sy, txy, angle=angle)
        return self.plot(sigma1, sigma2, angle, Tmax, sx, sy, txy, fig)

    def triple_state(self, sx, sy, sz, txy, txz, tyz, fig):
        matrix = numpy.asarray([[sx, txy, txz],
                                [txy, sy, tyz],
                                [txz, tyz, sz]])

        sigmalist, _ = numpy.linalg.eig(matrix)
        sigmalist.sort()
        sigma1 = sigmalist[0]
        sigma2 = sigmalist[1]
        sigma3 = sigmalist[2]
        Tmax = (sigma1 - sigma3) / 2
        if self.triple:
            self.save_values(sigma1, sigma2, Tmax, sx, sy, txy, sigma3, sz, txz, tyz)
        return self.plot(sigma1, sigma2, 0, Tmax, sx, sy, txy, fig, sigma3, sz, txz, tyz)

    def plot(self, sigma1, sigma2, angle, Tmax, sx, sy, txy, fig, sigma3=None, sz=None, txz=None, tyz=None):
        fig.clear()
        self.det_plot_values(sigma1, sigma2, sigma3)

        self.fig = fig
        self.one_fig = self.fig.add_subplot(122)

        self.plot_sigmas(sigma3)

        self.plot_T(Tmax)

        self.plot_circles(sigma3, Tmax)

        self.modify_axes()

        # plot angle if not triple state
        if sigma3 is None:
            self.plot_circles_angle(angle, Tmax)

        # plot square if plain state
        if sigma3 is None:
            self.one_fig = self.fig.add_subplot(121)
            self.plot_square(sy, sx, txy)
            self.plot_square_angle(angle)

        # or plot cube if triple state
        elif sigma3 is not None:
            self.one_fig = self.fig.add_subplot(121, projection='3d')
            self.plot_cube(sy, sx, sz, txy, tyz, txz)

        ax = self.fig.get_axes()
        for i in range(len(ax)):
            ax[i].patch.set_alpha(0)

        return fig

    def det_plot_values(self, sigma1, sigma2, sigma3):
        if sigma3 is not None:
            self.sigmalist = [sigma1, sigma2, sigma3]
            self.sigmalist.sort()
            self.s1 = self.sigmalist[2]
            self.s2 = self.sigmalist[1]
            self.s3 = self.sigmalist[0]
        elif sigma3 is None:
            self.sigmalist = [sigma1, sigma2]
            self.sigmalist.sort()
            self.s1 = self.sigmalist[1]
            self.s2 = self.sigmalist[0]
        self.center = (self.sigmalist[0] + self.sigmalist[-1]) / 2

    def plot_sigmas(self, sigma3):
        # sigma 1
        self.one_fig.plot(self.s1, 0, 'ro')
        self.one_fig.text(self.s1, 0, f'σ1 = {self.s1:.2f}', size=functions.size, ha='right', va='bottom', bbox=self.bbox_setting)

        # sigma 2
        self.one_fig.plot(self.s2, 0, 'ro')
        self.one_fig.text(self.s2, 0, f'σ2 = {self.s2:.2f}', size=functions.size, ha='left', va='top', bbox=self.bbox_setting)

        # sigma 3
        if sigma3 is not None:
            self.one_fig.plot(self.s3, 0, 'ro')
            self.one_fig.text(self.s3, 0, f'σ3 = {self.s3:.2f}', size=functions.size, ha='left', va='bottom', bbox=self.bbox_setting)

    def plot_T(self, Tmax):
        # Tmax
        self.one_fig.plot(self.center, Tmax, 'ro')
        self.one_fig.text(self.center, Tmax, f'τmax = {Tmax:.2f}', size=functions.size, ha='center', va='bottom', bbox=self.bbox_setting)

        # Tmin
        self.one_fig.plot(self.center, -Tmax, 'ro')
        self.one_fig.text(self.center, -Tmax, f'τmin = {-Tmax:.2f}', size=functions.size, ha='center', va='top', bbox=self.bbox_setting)

    def plot_circles(self, sigma3, Tmax):
        # circle plot
        # plt.plot(center, 0, 'ro')
        # plt.annotate(f'C({center:.2f})', (center, 0), size=functions.size, ha='center', va='top')
        edgecolor = self.edgecolor
        if self.state:
            edgecolor = self.mode
        if sigma3 is None:
            self.one_fig.add_patch(Wedge((self.center, 0), Tmax, 0, 360, linewidth=3, edgecolor=edgecolor, alpha=0.9,
                                         facecolor='black', fill=False))

        if sigma3 is not None:
            self.one_fig.add_patch(Wedge((self.center, 0), Tmax, 0, 360, linewidth=1, edgecolor=edgecolor,
                                         facecolor="royalblue", alpha=0.3))

            self.one_fig.add_patch(
                Wedge(((self.s3 + self.s2) / 2, 0), (self.s2 - self.s3) / 2, 0, 360, linewidth=1, edgecolor=edgecolor,
                      facecolor='grey', alpha=0.8))

            self.one_fig.add_patch(
                Wedge(((self.s2 + self.s1) / 2, 0), (self.s1 - self.s2) / 2, 0, 360, linewidth=1, edgecolor=edgecolor,
                      facecolor='grey', alpha=0.8))

        self.one_fig.set_aspect('equal', 'datalim')

    def modify_axes(self):
        # condition to make sure axis doesnt get out of screen
        if self.sigmalist[0] < 0 < self.sigmalist[-1]:
            self.one_fig.spines['left'].set_position('zero')
            self.one_fig.spines['right'].set_color('none')
            self.one_fig.set_xlabel('σ', fontsize=13, loc='right')

        elif self.sigmalist[-1] < 0:
            self.one_fig.spines['left'].set_position(('axes', 1))
            self.one_fig.spines['left'].set_color('none')
            self.one_fig.set_xlabel('σ', fontsize=13, loc='left')

        elif self.sigmalist[0] > 0:
            self.one_fig.spines['right'].set_color('none')
            self.one_fig.set_xlabel('σ', fontsize=13, loc='right')

        self.one_fig.set_ylabel('τ', rotation=0, fontsize=13, loc='top')
        self.one_fig.spines['top'].set_color('none')
        self.one_fig.spines['bottom'].set_position('zero')

    def plot_circles_angle(self, angle, Tmax):
        # show angle value
        if self.mode == "black": color = "black"
        else: color = "white"
        self.one_fig.text(self.center, Tmax / 8, f'θ = {abs(angle) * (180 / numpy.pi):.2f}°', size=functions.size,
                          ha='center', va='center', color=color, bbox=self.bbox_setting)

        start, finish = self.det_start_finish(angle)

        # show angle arcs
        self.one_fig.add_patch(Wedge((self.center, 0), Tmax / 5, -finish, -start, linewidth=2,
                                  edgecolor='blue', facecolor='blue', fill=True))

        self.one_fig.add_patch(
            Wedge((self.center, 0), Tmax, -finish, -start, linewidth=2, edgecolor='blue',
                  facecolor='blue', fill=False, linestyle='--'))

    def plot_square(self, sy, sx, txy):
        arrow_color_fc = 'blue'
        arrow_color_ec = 'white'
        self.one_fig.add_patch(
            Rectangle((0.25, 0.25), 0.5, 0.5, linewidth=2, edgecolor='blue', fill=False, alpha=.9))
        self.one_fig.arrow(0.5, 0.8, 0, 0.1, width=0.02, fc=arrow_color_fc, ec=arrow_color_ec)
        self.one_fig.arrow(0.5, 0.2, 0, -0.1, width=0.02, fc=arrow_color_fc, ec=arrow_color_ec)
        self.one_fig.arrow(0.8, 0.5, 0.1, 0, width=0.02, fc=arrow_color_fc, ec=arrow_color_ec)
        self.one_fig.arrow(0.2, 0.5, -0.1, 0, width=0.02, fc=arrow_color_fc, ec=arrow_color_ec)
        self.one_fig.arrow(0.75, 0.24, -0.41, 0, width=0.02, shape='right', fc=arrow_color_fc, ec=arrow_color_ec)
        self.one_fig.arrow(0.25, 0.76, 0.41, 0, width=0.02, shape='right', fc=arrow_color_fc, ec=arrow_color_ec)
        self.one_fig.arrow(0.24, 0.75, 0, -0.41, width=0.02, shape='left', fc=arrow_color_fc, ec=arrow_color_ec)
        self.one_fig.arrow(0.76, 0.25, 0, 0.41, width=0.02, shape='left', fc=arrow_color_fc, ec=arrow_color_ec)
        self.one_fig.annotate(f'σy = {sy}', (0.58, 0.9), size=functions.size, ha='left', va='top')
        self.one_fig.annotate(f'σx = {sx}', (0.82, 0.4), size=functions.size, ha='left', va='center')
        self.one_fig.annotate(f'τxy = {txy}', (0.8, 0.8), size=functions.size, ha='left', va='top')

        self.one_fig.set_aspect('equal', 'datalim')
        self.one_fig.axis('off')

    def plot_square_angle(self, angle):
        self.one_fig.annotate(f'{(abs(angle) * (180 / numpy.pi)) / 2:.2f}°', (0.5, 0.5), size=functions.size,
                              ha='center', va='bottom', color='blue')

        start, finish = self.det_start_finish(angle)

        self.one_fig.add_patch(Wedge((0.5, 0.5), 0.05, start/2, finish/2, linewidth=2,
                                  edgecolor='blue', facecolor='blue', fill=True))

        self.one_fig.add_patch(
            Wedge((0.5, 0.5), 0.245, start/2, finish/2, linewidth=2, edgecolor='blue',
                  facecolor='blue', fill=False, linestyle='--'))

    def det_start_finish(self, angle):
        if angle > 0:
            start = 0
            finish = angle * (180 / numpy.pi)

        else:
            start = angle * (180 / numpy.pi)
            finish = 0

        return start, finish

    def plot_cube(self, sy, sx, sz, txy, tyz, txz):
        points = numpy.array([[-1, -1, -1],
                              [1, -1, -1],
                              [1, 1, -1],
                              [-1, 1, -1],
                              [-1, -1, 1],
                              [1, -1, 1],
                              [1, 1, 1],
                              [-1, 1, 1]])

        r = [-1, 1]
        X, Y = numpy.meshgrid(r, r)
        one = numpy.ones(4).reshape(2, 2)
        self.one_fig.plot_wireframe(X, Y, one, alpha=0.5, color='blue')
        self.one_fig.plot_wireframe(X, Y, -one, alpha=0.5, color='blue')
        self.one_fig.plot_wireframe(X, -one, Y, alpha=0.5, color='blue')
        self.one_fig.plot_wireframe(X, one, Y, alpha=0.5, color='blue')
        self.one_fig.plot_wireframe(one, X, Y, alpha=0.5, color='blue')
        self.one_fig.plot_wireframe(-one, X, Y, alpha=0.5, color='blue')
        self.one_fig.scatter3D(points[:, 0], points[:, 1], points[:, 2])
        self.one_fig.plot_surface(X, Y, one, linewidth=0, color='blue', antialiased=False, alpha=0.2)
        self.one_fig.plot_surface(X, Y, -one, linewidth=0, color='blue', antialiased=False, alpha=0.2)
        self.one_fig.plot_surface(X, -one, Y, linewidth=0, color='blue', antialiased=False, alpha=0.2)
        self.one_fig.plot_surface(X, one, Y, linewidth=0, color='blue', antialiased=False, alpha=0.2)
        self.one_fig.plot_surface(one, X, Y, linewidth=0, color='blue', antialiased=False, alpha=0.2)
        self.one_fig.plot_surface(-one, X, Y, linewidth=0, color='blue', antialiased=False, alpha=0.2)

        # sigma
        color = "white"
        if self.mode == "black":
            color = "black"
        quiver_color = color
        text_color = color
        self.one_fig.quiver(0, 0, 1, 0, 0, 1, length=0.5, color=quiver_color)
        # self.one_fig.quiver(0, 0, -1, 0, 0, -1, length=0.5, color='black')
        # self.one_fig.quiver(0, 1, 0, 0, 1, 0, length=0.5, color='black')
        self.one_fig.quiver(0, -1, 0, 0, -1, 0, length=0.5, color=quiver_color)
        self.one_fig.quiver(1, 0, 0, 1, 0, 0, length=0.5, color=quiver_color)
        # self.one_fig.quiver(-1, 0, 0, -1, 0, 0, length=0.5, color='black')
        # self.one_fig.quiver(-1, 0, 0, -1, 0, 0, length=0.5, color='black')

        # tau
        self.one_fig.quiver(0, 0, 1, 1, 0, 0, length=0.5, color=quiver_color, normalize=True)
        self.one_fig.quiver(0, 0, 1, 0, -1, 0, length=0.5, color=quiver_color, normalize=True)
        self.one_fig.quiver(0, -1, 0, 1, 0, 0, length=0.5, color=quiver_color, normalize=True)
        self.one_fig.quiver(0, -1, 0, 0, 0, 1, length=0.5, color=quiver_color, normalize=True)
        self.one_fig.quiver(1, 0, 0, 0, -1, 0, length=0.5, color=quiver_color, normalize=True)
        self.one_fig.quiver(1, 0, 0, 0, 0, 1, length=0.5, color=quiver_color, normalize=True)

        self.one_fig.text(0.1, 0.1, 1.3, f"σy = {sy}", color=text_color, fontsize=functions.size)
        self.one_fig.text(0.1, 0.1, 1.05, f"τyx = {txy}", color=text_color, fontsize=functions.size)
        self.one_fig.text(-0.1, -0.5, 1.05, f"τyz = {tyz}", color=text_color, fontsize=functions.size)

        self.one_fig.text(0.2, -1.25, 0.5, f"τzy = {tyz}", color=text_color, fontsize=functions.size)
        self.one_fig.text(-0.15, -1.5, 0.1, f"σz = {sz}", color=text_color, fontsize=functions.size)
        self.one_fig.text(0.2, -1.25, 0.1, f"τzx = {txz}", color=text_color, fontsize=functions.size)

        self.one_fig.text(1, 0.1, 0.4, f"τxy = {txy}", color=text_color, fontsize=functions.size)
        self.one_fig.text(1, -0.6, 0.1, f"τxz = {txz}", color=text_color, fontsize=functions.size)
        self.one_fig.text(1.25, 0.1, 0.05, f"σx = {sx}", color=text_color, fontsize=functions.size)

        # set viewing angle if returning from 2D plot
        #if self.azim is not None:
            #Axes3D(fig).view_init(elev=self.elev, azim=self.azim)

        self.one_fig.axis('off')

    def save_values(self, sigma1, sigma2, Tmax, sx, sy, txy, sigma3=None, sz=None, txz=None, tyz=None, angle=None):
        self.sx = sx
        self.sy = sy
        self.sz = sz
        self.txy = txy
        self.txz = txz
        self.tyz = tyz
        self.sigma1 = sigma1
        self.sigma2 = sigma2
        self.sigma3 = sigma3
        self.Tmax = Tmax
        self.angle = angle

    def on_release(self, fig):
        if 80 < abs(float(fig.gca(projection="3d").azim)) < 100 and -10 < abs(float(fig.gca(projection="3d").elev)) < 10:
            fig.clear()
            return self.plain_state(self.sx, self.sy, self.txy, fig)
        elif -10 < abs(float(fig.gca(projection="3d").azim)) < 10 and -10 < abs(float(fig.gca(projection="3d").elev)) < 10:
            fig.clear()
            return self.plain_state(self.sz, self.sy, self.tyz, fig)
        elif -10 < abs(float(fig.gca(projection="3d").azim)) < 10 and 80 < abs(float(fig.gca(projection="3d").elev)) < 100:
            fig.clear()
            return self.plain_state(self.sz, self.sx, self.txz, fig)
        elif 170 < abs(float(fig.gca(projection="3d").azim)) < 190 and -10 < abs(float(fig.gca(projection="3d").elev)) < 10:
            fig.clear()
            return self.plain_state(self.sz, self.sy, self.tyz, fig)
        elif 80 < abs(float(fig.gca(projection="3d").azim)) < 100 and 80 < abs(float(fig.gca(projection="3d").elev)) < 100:
            fig.clear()
            return self.plain_state(self.sz, self.sx, self.txz, fig)
        else:
            return fig

    def solver(self):
        doc = Document(document_options="a4paper,12pt", documentclass="article")
        doc.preamble.append(NoEscape(header.PDFsettings))

        if not self.sigma3:
            doc.append(NoEscape(header.makeCover("Estado Duplo de Tensões")))
            with doc.create(Section('Calculo do raio ou tensão de cisalhamento máxima')):
                with doc.create(Subsection(r'Fórmula do raio/tensão de cisalhamento máxima')):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'T_{max} = \sqrt{(\frac{sx-sy}{2})^2 + txy ^ 2)}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                with doc.create(Subsection(r'Realizando a conta')):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'T_{max} = \sqrt{(\frac{'+f'{self.sx}'+f'-{self.sy}'+'}{2})^2 +'+f'{self.txy}'+'^ 2)}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'T_{max} ='+f'{self.Tmax:.2f}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
            with doc.create(Section('Calculo das tensões principais')):
                with doc.create(Subsection(r'Fórmula para cálculo das tensões principais')):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'sigma_{1,2} = \sqrt{\frac{s_x + s_y}{2} \pm (\frac{s_x - s_y}{2}) ^ 2 + {t_{xy}} ^ 2}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                with doc.create(Subsection('Calculo de sigma 1')):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'sigma_1 = \sqrt{\frac{'+f'{self.sx}'+f'+ {self.sy}'+r'}{2} + (\frac{'+f'{self.sx}'+' - '+f'{self.sy}'+'}{2}) ^ 2 + '+f'{self.txy}'+' ^ 2}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(f'sigma_1 = {self.sigma1:.2f}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                with doc.create(Subsection('Calculo de sigma 2')):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'sigma_2 = \sqrt{\frac{' + f'{self.sx}' + f'+ {self.sy}' + r'}{2} - (\frac{' + f'{self.sx}' + ' - ' + f'{self.sy}' + '}{2}) ^ 2 + ' + f'{self.txy}' + ' ^ 2}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(f'sigma_2 = {self.sigma2:.2f}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
            with doc.create(Section('Calculo do centro')):
                with doc.create(Subsection('Fórmula do centro')):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'centro = \frac{sx + sy}{2}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                with doc.create(Subsection('Calculo do centro')):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'centro = \frac{'+f'{self.sx} +'+f'{self.sy}'+'}{2}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(f'centro = {(self.sx + self.sy) / 2:.2f}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
            with doc.create(Section('Calculo do ângulo')):
                with doc.create(Subsection('Fórmula do ângulo')):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'\theta = \frac{arctan(\frac{txy}{sx - centro})}{2}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                with doc.create(Subsection('Realizando a conta')):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'\theta = \frac{arctan(\frac{'+f'{self.txy}'+'}{'+f'{self.sx}'+f' - {(self.sx + self.sy) / 2}'+'}'+')}{2}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(f'\\theta = {abs(self.angle * 180/numpy.pi):.2f}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                    doc.append(NoEscape(r'Deve-se dividir o ângulo encontrado no círculo de Mohr por 2 para encontrar o ângulo real, portanto:'))
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(f'\\theta = {abs(self.angle * 90 / numpy.pi):.2f}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
            with doc.create(Section('Desenhando o estado de tensões e círculo de Mohr')):
                with doc.create(Figure(position='H')) as fig_mohrleft:
                    fig_mohrleft.add_image("figs\\mohrfig", width='500px')
                    fig_mohrleft.add_caption(NoEscape(r'\label{fig:estrutura} Estado Plano de Tensões e círculo de Mohr'))

        elif self.sigma3:
            doc.append(NoEscape(header.makeCover("Estado Triplo de Tensões")))
            with doc.create(Section("Fórmulas para os cálculos")):
                with doc.create(Subsection(r'Fórmula para cálculo das tensões principais')):
                    doc.append(NoEscape(r"O cálculo das tensões principais pode ser realizado por meio do cálculo dos "
                                        r"autovalores da matriz de tensões do elemento, como mostrado na equação 1."))
                    doc.append(NoEscape(r'\begin{dmath}'))
                    doc.append(NoEscape(r'det(M - I\lambda) = 0'))
                    doc.append(NoEscape(r'\end{dmath}'))

                    doc.append(NoEscape(r'\[det('))
                    doc.append(NoEscape(r'\begin{bmatrix}'))
                    doc.append(NoEscape(r'\sigma_x & \tau_{xy} & \tau_{xz}\\ \tau_{xy} & \sigma_y & \tau_{yz}\\ \tau_{xz} & \tau_{yz} & \sigma_z'))
                    doc.append(NoEscape(r'\end{bmatrix}'))
                    doc.append(NoEscape(r' - '))
                    doc.append(NoEscape(r'\begin{bmatrix}'))
                    doc.append(NoEscape(r'1 & 0 & 0\\ 0 & 1 & 0\\ 0 & 0 & 1'))
                    doc.append(NoEscape(r'\end{bmatrix}'))
                    doc.append(NoEscape(r' \cdot \lambda) = 0 \Rightarrow'))
                    doc.append(NoEscape(r'\begin{vmatrix}'))
                    doc.append(NoEscape(
                        r'\sigma_x - \lambda & \tau_{xy} & \tau_{xz}\\ \tau_{xy} & \sigma_y - \lambda & \tau_{yz}\\ \tau_{xz} & \tau_{yz} & \sigma_z - \lambda'))
                    doc.append(NoEscape(r'\end{vmatrix}'))
                    doc.append(NoEscape(r' = 0\]'))

                with doc.create(Subsection(r'Fórmula para cálculo da tensão de cisalhamento máxima')):
                    doc.append(NoEscape(r'O cáculo da tensão máxima de cisalhamento pode ser realizado por meio da '
                                        r'análise geométrica do círculo de Mohr. Dado que:'))
                    doc.append(NoEscape(r'\begin{enumerate}'))
                    doc.append(NoEscape(r'\item{A distância vertical da tensão máxima de cisalhamento até a origem é '
                                        r'sempre igual ao raio do círculo de Mohr};'))
                    doc.append(NoEscape(r'\item{$\sigma_1$ e $\sigma_3$ são diametralmente opostos, ou seja, $\sigma_1$ - $\sigma_3$ = 2 $\cdot$ raio}.'))
                    doc.append(NoEscape(r'\end{enumerate}'))
                    doc.append(NoEscape(r'\begin{dmath}'))
                    doc.append(NoEscape(r'T_{max} = \frac{\sigma_1 - \sigma_3}{2}'))
                    doc.append(NoEscape(r'\end{dmath}'))
                    doc.append(NoEscape(r'\newpage'))

            with doc.create(Section(r'Cálculo')):
                with doc.create(Subsection(r'Substituindo na matriz')):
                    doc.append(NoEscape(r'\['))
                    doc.append(NoEscape(r'\begin{vmatrix}'))
                    doc.append(NoEscape(f'{self.sx} -' + r'\lambda' + f'& {self.txy} & {self.txz}' r'\\'
                                        f'{self.txy} & {self.sy}' + r' - \lambda' + f'& {self.tyz}' r'\\'
                                        f'{self.txz} & {self.tyz} & {self.sz}' + r' - \lambda'))
                    doc.append(NoEscape(r'\end{vmatrix}'))
                    doc.append(NoEscape(r' =0\]'))

                    with doc.create(Subsection(r'Calculo da determinante')):
                        string = f"({self.sx} -" + r'\lambda' + f") \\cdot ({self.sy} -" + r'\lambda' + f") \\cdot ({self.sz} -" + r'\lambda' + \
                            f") + {self.txy} \\cdot {self.tyz} \\cdot {self.txz} + {self.txz} \\cdot {self.txy} \\cdot {self.tyz} " \
                            f"- {self.txz} \\cdot ({self.sy} -" + r'\lambda' + f") \\cdot {self.txz} " \
                            f"- {self.tyz} \\cdot {self.tyz} \\cdot ({self.sx} -" + r'\lambda' + \
                            f") - ({self.sz} -" + r'\lambda' + f") \\cdot {self.txy} \\cdot {self.txy}"

                        lam = Symbol(r'\lambda')
                        numeric = (self.sx - lam) * (self.sy - lam) * (self.sz - lam) + self.txy * self.tyz * self.txz + \
                                  self.txz * self.txy * self.tyz - self.txz * (self.sy - lam) * self.txz - \
                                  self.tyz * self.tyz * (self.sx - lam) - (self.sz - lam) * self.txy * self.txy

                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape('det = ' + string))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape('det = ' + latex(numeric)))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath}'))
                        doc.append(NoEscape('det = ' + latex(simplify(numeric))))
                        doc.append(NoEscape(r'\end{dmath}'))
                        doc.append(NoEscape(r'Substituindo a equação 3 na equação 1, temos:'))
                        doc.append(NoEscape(r'\begin{dmath}'))
                        doc.append(NoEscape(latex(simplify(numeric)) + r'=0'))
                        doc.append(NoEscape(r'\end{dmath}'))

            with doc.create(Section(r'Resultados')):
                with doc.create(Subsection(r'Tensões Principais')):
                    doc.append(NoEscape(r"Encontrando as raízes da equação 4 descobrimos as tensões principais, "
                                        r"lembrando que $\sigma_1$ é sempre a maior tensão principal (o maior autovalor) "
                                        r"e $\sigma_3$ é sempre a menor tensão principal (o menor autovalor):"))
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r"\sigma_1 = " + f"{round(self.sigma1, 2)}"))
                    doc.append(NoEscape(r'\end{dmath*}'))
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r"\sigma_2 = " + f"{round(self.sigma2, 2)}"))
                    doc.append(NoEscape(r'\end{dmath*}'))
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r"\sigma_3 = " + f"{round(self.sigma3, 2)}"))
                    doc.append(NoEscape(r'\end{dmath*}'))
                with doc.create(Subsection(r'Tensão de Cisalhamento Máxima')):
                    doc.append(NoEscape(r'Substituindo $\sigma_1$ e $\sigma_3$ na equação 2 obtemos $\tau_{max}$:'))
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'T_{max} = \frac{' + f'{round(self.sigma1, 2)} - {round(self.sigma3, 2)}' + r'}{2}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r"T_{max} = " + f"{round(self.Tmax, 2)}"))
                    doc.append(NoEscape(r'\end{dmath*}'))

            doc.append(NoEscape(r'\newpage'))
            with doc.create(Section(r'Desenhando o círculo de Mohr')):
                with doc.create(Figure(position='H')) as fig_mohrleft:
                    fig_mohrleft.add_image("figs\\mohrfig", width='500px')
                    fig_mohrleft.add_caption(
                        NoEscape(r'\label{fig:estrutura} Estado Triplo de Tensões e círculo de Mohr'))

        doc.generate_tex('tmp\\resolucaomohrt')
        doc.generate_pdf('tmp\\resolucaomohr',
                         compiler='pdflatex',
                         win_no_console=True,
                         compiler_args=["-enable-installer"])
