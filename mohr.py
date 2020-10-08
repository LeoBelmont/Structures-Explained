import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Rectangle
import numpy
import functions
from pylatex import Document, Section, Subsection, Figure, Command, NoEscape, Package
from mpl_toolkits.mplot3d import Axes3D


class mohr_circle():

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

    def state(self, fig):
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
            self.save_values(sigma1, sigma2, angle, Tmax, sx, sy, txy)
        return self.plot(sigma1, sigma2, angle, Tmax, sx, sy, txy, fig)

    def triple_state(self, sx, sy, sz, txy, txz, tyz, fig):
        I1 = sx + sy + sz
        I2 = sx * sy + sx * sz + sy * sz - txy ** 2 - txz ** 2 - tyz ** 2
        I3 = sx * sy * sz - sx * tyz ** 2 - sy * txz ** 2 - sz * txy ** 2 + 2 * txy * txz * tyz
        angle = (1/3) * numpy.arctan((2*I1**3 - 9*I1*I2 + 27*I3) / (2*((I1**2 - 3*I2)**(3/2))))
        sigma1 = I1/3 + (2/3)*((I1**2 - 3*I2)**0.5 * numpy.cos(angle))
        sigma2 = I1/3 + (2/3)*((I1**2 - 3*I2)**0.5 * numpy.cos(angle - 2.0944))
        sigma3 = I1/3 + (2/3)*((I1**2 - 3*I2)**0.5 * numpy.cos(angle - 4.18879))
        Tmax = (sigma1 - sigma3) / 2
        if self.triple:
            self.save_values(sigma1, sigma2, angle, Tmax, sx, sy, txy, sigma3, sz, txz, tyz)
        return self.plot(sigma1, sigma2, angle, Tmax, sx, sy, txy, fig, sigma3, sz, txz, tyz)

    def plot(self, sigma1, sigma2, angle, Tmax, sx, sy, txy, fig, sigma3=None, sz=None, txz=None, tyz=None):
        self.det_plot_values(sigma1, sigma2, sigma3)

        ax = plt.subplot(122)

        self.plot_sigmas(sigma3)

        self.plot_T(Tmax)

        self.plot_circles(sigma3, Tmax)

        self.modify_axes(ax)

        # plot angle if not triple state
        if sigma3 is None:
            self.plot_circles_angle(angle, Tmax)

        # plot square if plain state
        if sigma3 is None:
            self.plot_square(sy, sx, txy)
            self.plot_square_angle(angle)

        # or plot cube if triple state
        elif sigma3 is not None:
            self.plot_cube(sy, sx, sz, txy, tyz, txz, fig)

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
        plt.plot(self.s1, 0, 'ro')
        plt.annotate(f'σ1 = {self.s1:.2f}', (self.s1, 0), size=functions.size, ha='right', va='bottom')

        # sigma 2
        plt.plot(self.s2, 0, 'ro')
        plt.annotate(f'σ2 = {self.s2:.2f}', (self.s2, 0), size=functions.size, ha='left', va='bottom')

        # sigma 3
        if sigma3 is not None:
            plt.plot(self.s3, 0, 'ro')
            plt.annotate(f'σ3 = {self.s3:.2f}', (self.s3, 0), size=functions.size, ha='left', va='bottom')

    def plot_T(self, Tmax):
        # Tmax
        plt.plot(self.center, Tmax, 'ro')
        plt.annotate(f'τmax = {Tmax:.2f}', (self.center, Tmax), size=functions.size, ha='center', va='bottom')

        # Tmin
        plt.plot(self.center, -Tmax, 'ro')
        plt.annotate(f'τmin = {-Tmax:.2f}', (self.center, -Tmax), size=functions.size, ha='center', va='top')

    def plot_circles(self, sigma3, Tmax):
        # circle plot
        # plt.plot(center, 0, 'ro')
        # plt.annotate(f'C({center:.2f})', (center, 0), size=functions.size, ha='center', va='top')
        if sigma3 is None:
            plt.gca().add_patch(Wedge((self.center, 0), Tmax, 0, 360, linewidth=3, edgecolor='black', facecolor='black',
                                      fill=False))

        if sigma3 is not None:
            plt.gca().add_patch(Wedge((self.center, 0), Tmax, 0, 360, linewidth=1, edgecolor='black', facecolor='grey'))

            plt.gca().add_patch(
                Wedge(((self.s3 + self.s2) / 2, 0), (self.s2 - self.s3) / 2, 0, 360, linewidth=1, edgecolor='black',
                      facecolor='white'))

            plt.gca().add_patch(
                Wedge(((self.s2 + self.s1) / 2, 0), (self.s1 - self.s2) / 2, 0, 360, linewidth=1, edgecolor='black',
                      facecolor='white'))

    def modify_axes(self, ax):
        # condition to make sure axis doesnt get out of screen
        if self.sigmalist[0] < 0 < self.sigmalist[-1]:
            ax.spines['left'].set_position('zero')
            ax.spines['right'].set_color('none')
            plt.xlabel('σ', fontsize=13, loc='right')

        elif self.sigmalist[-1] < 0:
            ax.spines['left'].set_position(('axes', 1))
            ax.spines['left'].set_color('none')
            plt.xlabel('σ', fontsize=13, loc='left')

        elif self.sigmalist[0] > 0:
            ax.spines['right'].set_color('none')
            plt.xlabel('σ', fontsize=13, loc='right')

        plt.ylabel('τ', rotation=0, fontsize=13, loc='top')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_position('zero')

    def plot_circles_angle(self, angle, Tmax):
        # show angle value
        plt.annotate(f'{abs(angle) * (180 / numpy.pi):.2f}°', (self.center, Tmax/8), size=functions.size,
                     ha='center', va='center')

        start, finish = self.det_start_finish(angle)

        # show angle arcs
        plt.gca().add_patch(Wedge((self.center, 0), Tmax / 5, -finish, -start, linewidth=2,
                                  edgecolor='blue', facecolor='blue', fill=True))

        plt.gca().add_patch(
            Wedge((self.center, 0), Tmax, -finish, -start, linewidth=2, edgecolor='blue',
                  facecolor='blue', fill=False, linestyle='--'))

    def plot_square(self, sy, sx, txy):
        plt.subplot(121)
        plt.gca().add_patch(
            Rectangle((0.25, 0.25), 0.5, 0.5, linewidth=2, edgecolor='black', facecolor='black', fill=False))
        plt.arrow(0.5, 0.8, 0, 0.1, width=0.02)
        plt.arrow(0.5, 0.2, 0, -0.1, width=0.02)
        plt.arrow(0.8, 0.5, 0.1, 0, width=0.02)
        plt.arrow(0.2, 0.5, -0.1, 0, width=0.02)
        plt.arrow(0.75, 0.24, -0.41, 0, width=0.02, shape='right')
        plt.arrow(0.25, 0.76, 0.41, 0, width=0.02, shape='right')
        plt.arrow(0.24, 0.75, 0, -0.41, width=0.02, shape='left')
        plt.arrow(0.76, 0.25, 0, 0.41, width=0.02, shape='left')
        plt.annotate(f'σy = {sy}', (0.58, 0.9), size=functions.size, ha='left', va='top')
        plt.annotate(f'σx = {sx}', (0.82, 0.4), size=functions.size, ha='left', va='center')
        plt.annotate(f'τxy = {txy}', (0.8, 0.8), size=functions.size, ha='left', va='top')

        plt.axis('off')

    def plot_square_angle(self, angle):
        plt.annotate(f'{(abs(angle) * (180 / numpy.pi)) / 2:.2f}°', (0.5, 0.5), size=functions.size,
                     ha='center', va='bottom')

        start, finish = self.det_start_finish(angle)

        plt.gca().add_patch(Wedge((0.5, 0.5), 0.05, start/2, finish/2, linewidth=2,
                                  edgecolor='blue', facecolor='blue', fill=True))

        plt.gca().add_patch(
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

    def plot_cube(self, sy, sx, sz, txy, tyz, txz, fig):
        points = numpy.array([[-1, -1, -1],
                              [1, -1, -1],
                              [1, 1, -1],
                              [-1, 1, -1],
                              [-1, -1, 1],
                              [1, -1, 1],
                              [1, 1, 1],
                              [-1, 1, 1]])

        ax = fig.add_subplot(121, projection='3d')
        r = [-1, 1]
        X, Y = numpy.meshgrid(r, r)
        one = numpy.ones(4).reshape(2, 2)
        ax.plot_wireframe(X, Y, one, alpha=0.5, color='blue')
        ax.plot_wireframe(X, Y, -one, alpha=0.5, color='blue')
        ax.plot_wireframe(X, -one, Y, alpha=0.5, color='blue')
        ax.plot_wireframe(X, one, Y, alpha=0.5, color='blue')
        ax.plot_wireframe(one, X, Y, alpha=0.5, color='blue')
        ax.plot_wireframe(-one, X, Y, alpha=0.5, color='blue')
        ax.scatter3D(points[:, 0], points[:, 1], points[:, 2])
        ax.plot_surface(X, Y, one, linewidth=0, color='blue', antialiased=False, alpha=0.2)
        ax.plot_surface(X, Y, -one, linewidth=0, color='blue', antialiased=False, alpha=0.2)
        ax.plot_surface(X, -one, Y, linewidth=0, color='blue', antialiased=False, alpha=0.2)
        ax.plot_surface(X, one, Y, linewidth=0, color='blue', antialiased=False, alpha=0.2)
        ax.plot_surface(one, X, Y, linewidth=0, color='blue', antialiased=False, alpha=0.2)
        ax.plot_surface(-one, X, Y, linewidth=0, color='blue', antialiased=False, alpha=0.2)

        # sigma
        ax.quiver(0, 0, 1, 0, 0, 1, length=0.5, color='black')
        # ax.quiver(0, 0, -1, 0, 0, -1, length=0.5, color='black')
        # ax.quiver(0, 1, 0, 0, 1, 0, length=0.5, color='black')
        ax.quiver(0, -1, 0, 0, -1, 0, length=0.5, color='black')
        ax.quiver(1, 0, 0, 1, 0, 0, length=0.5, color='black')
        # ax.quiver(-1, 0, 0, -1, 0, 0, length=0.5, color='black')
        # ax.quiver(-1, 0, 0, -1, 0, 0, length=0.5, color='black')

        # tau
        ax.quiver(0, 0, 1, 1, 0, 0, length=0.5, color='black', normalize=True)
        ax.quiver(0, 0, 1, 0, -1, 0, length=0.5, color='black', normalize=True)
        ax.quiver(0, -1, 0, 1, 0, 0, length=0.5, color='black', normalize=True)
        ax.quiver(0, -1, 0, 0, 0, 1, length=0.5, color='black', normalize=True)
        ax.quiver(1, 0, 0, 0, -1, 0, length=0.5, color='black', normalize=True)
        ax.quiver(1, 0, 0, 0, 0, 1, length=0.5, color='black', normalize=True)

        ax.text(0.1, 0.1, 1.3, f"σy = {sy}", color='black')
        ax.text(0.1, 0.1, 1.05, f"τyx = {txy}", color='black')
        ax.text(-0.1, -0.5, 1.05, f"τyz = {tyz}", color='black')

        ax.text(0.2, -1.25, 0.5, f"τzy = {tyz}", color='black')
        ax.text(-0.15, -1.5, 0.1, f"σz = {sz}", color='black')
        ax.text(0.2, -1.25, 0.1, f"τzx = {txz}", color='black')

        ax.text(1, 0.1, 0.4, f"τxy = {txy}", color='black')
        ax.text(1, -0.6, 0.1, f"τxz = {txz}", color='black')
        ax.text(1.25, 0.1, 0.05, f"σx = {sx}", color='black')

        # set viewing angle if returning from 2D plot
        #if self.azim is not None:
            #Axes3D(fig).view_init(elev=self.elev, azim=self.azim)

        plt.axis('off')

    def save_values(self, sigma1, sigma2, angle, Tmax, sx, sy, txy, sigma3=None, sz=None, txz=None, tyz=None):
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
        doc = Document("a4paper,left=1.5cm,right=1.5cm,top=2cm,bottom=2cm")
        doc.packages.append(Package('breqn'))
        doc.packages.append(Package('amsmath'))
        doc.packages.append(Package('float'))
        doc.packages.append(Package('hyperref'))
        doc.packages.append(Package('babel', options=['portuguese']))
        doc.preamble.append(Command('title', 'Resolução'))
        doc.append(NoEscape(r'\maketitle'))
        doc.append(NoEscape(r'\tableofcontents'))
        doc.append(NoEscape(r'\pagenumbering{gobble}'))

        if self.sigma3 is None:
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
                    doc.append(NoEscape(r'Deve-se multiplicar o ângulo encontrado no círculo de Mohr por 2 para encontrar o ângulo real, portanto:'))
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(f'\\theta = {abs(self.angle * 360 / numpy.pi):.2f}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
            # with doc.create(Section('Figuras Finais')):
            #     with doc.create(Figure(position='H')) as fig_estrutura:
            #         fig_estrutura.add_image("figs\\structure", width='300px')
            #         fig_estrutura.add_caption(
            #             NoEscape(r'\label{fig:estrutura} Imagem da estrutura com apoios e carregamentos'

        doc.generate_pdf('Settings\\resolucaorm', compiler='pdflatex')
        doc.generate_tex('Settings\\resolucaorm')
