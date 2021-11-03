import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Rectangle
import numpy
from StructuresExplained.solutions import settings
from StructuresExplained.utils.util import round_expr

from typing import (
    Optional,
    Union,
)

import matplotlib
matplotlib.use("Qt5Agg")


class fig_generator:
    bbox_setting = dict(boxstyle="round,pad=0.1", fc="grey", ec="black", lw=1)

    def __init__(self,
                 results,
                 background_scheme: Optional[str] = "black"
                 ):

        self.res = results
        self.color_scheme = color_scheme(background_scheme)
        self.fig: Union[plt.Figure, None] = None
        self.subplot: Union[plt.axes, None] = None

    def plot_plain_state(self,
                         figure: plt.Figure
                         ):

        self.plot_basics(figure)

        self.plain_state_specifics()

        self.make_transparent()

        return self.fig

    def plot_triple_state(self,
                          figure: plt.Figure
                          ):

        self.plot_basics(figure)

        self.triple_state_specifics()

        self.make_transparent()

        return self.fig

    def plot_basics(self, figure: plt.Figure):

        self.fig = figure

        self.subplot = self.fig.add_subplot(122)

        self.plot_sigma_1_and_2()

        self.plot_max_shear()

    def plain_state_specifics(self):
        self.plot_circle_plain_state()
        self.modify_axes([self.res.sigma_2, self.res.sigma_1])
        self.plot_circles_angle()
        self.subplot = self.fig.add_subplot(121)
        self.plot_square()
        self.plot_square_angle()

    def triple_state_specifics(self):
        self.plot_sigma_3()
        self.plot_circles_triple_state()
        self.modify_axes([self.res.sigma_3, self.res.sigma_2, self.res.sigma_1])
        self.subplot = self.fig.add_subplot(121, projection='3d')
        self.plot_cube()

    def plot_sigma_1_and_2(self):
        # sigma 1
        self.subplot.plot(self.res.sigma_1, 0, 'ro')
        self.subplot.text(self.res.sigma_1, 0, f'σ1 = {round_expr(self.res.sigma_1)}', size=settings.size, ha='right',
                          va='bottom', bbox=self.bbox_setting)

        # sigma 2
        self.subplot.plot(self.res.sigma_2, 0, 'ro')
        self.subplot.text(self.res.sigma_2, 0, f'σ2 = {round_expr(self.res.sigma_2)}', size=settings.size, ha='left',
                          va='top', bbox=self.bbox_setting)

    def plot_sigma_3(self):
        self.subplot.plot(self.res.sigma_3, 0, 'ro')
        self.subplot.text(self.res.sigma_3, 0, f'σ3 = {round_expr(self.res.sigma_3)}', size=settings.size, ha='left',
                          va='bottom', bbox=self.bbox_setting)

    def plot_max_shear(self):
        # Tmax
        self.subplot.plot(self.res.center, self.res.max_shear, 'ro')
        self.subplot.text(self.res.center, self.res.max_shear, f'τmax = {round_expr(self.res.max_shear)}',
                          size=settings.size, ha='center', va='bottom', bbox=self.bbox_setting)

        # Tmin
        self.subplot.plot(self.res.center, -self.res.max_shear, 'ro')
        self.subplot.text(self.res.center, -self.res.max_shear, f'τmin = {round_expr(-self.res.max_shear)}',
                          size=settings.size, ha='center', va='top', bbox=self.bbox_setting)

    def plot_circle_plain_state(self):
        self.subplot.add_patch(
            Wedge((self.res.center, 0), self.res.max_shear, 0, 360, linewidth=3, edgecolor=self.color_scheme.edgecolor,
                  alpha=0.9, facecolor='black', fill=False))

        self.subplot.set_aspect('equal', 'datalim')

    def plot_circles_triple_state(self):
        self.subplot.add_patch(Wedge((self.res.center, 0), self.res.max_shear, 0, 360, linewidth=1,
                                     edgecolor=self.color_scheme.edgecolor, facecolor="royalblue", alpha=0.3))

        self.subplot.add_patch(
            Wedge(((self.res.sigma_3 + self.res.sigma_2) / 2, 0), (self.res.sigma_2 - self.res.sigma_3) / 2, 0, 360,
                  linewidth=1, edgecolor=self.color_scheme.edgecolor, facecolor='grey', alpha=0.8))

        self.subplot.add_patch(
            Wedge(((self.res.sigma_2 + self.res.sigma_1) / 2, 0), (self.res.sigma_1 - self.res.sigma_2) / 2, 0, 360,
                  linewidth=1, edgecolor=self.color_scheme.edgecolor, facecolor='grey', alpha=0.8))

        self.subplot.set_aspect('equal', 'datalim')

    def plot_circles_angle(self):
        # plot angle value
        self.subplot.text(self.res.center, self.res.max_shear / 8,
                          f'θ = {round_expr(abs(self.res.angle) * (180 / numpy.pi))}°', size=settings.size,
                          ha='center', va='center', color=self.color_scheme.arrow_color, bbox=self.bbox_setting)

        start, finish = self.det_start_finish()

        # plot angle arcs
        self.subplot.add_patch(Wedge((self.res.center, 0), self.res.max_shear / 5, -finish, -start, linewidth=2,
                                     edgecolor='blue', facecolor='blue', fill=True))

        self.subplot.add_patch(
            Wedge((self.res.center, 0), self.res.max_shear, -finish, -start, linewidth=2, edgecolor='blue',
                  facecolor='blue', fill=False, linestyle='--'))

    def plot_square(self):
        arrow_color_fc = 'blue'
        arrow_color_ec = 'white'
        self.subplot.add_patch(
            Rectangle((0.25, 0.25), 0.5, 0.5, linewidth=2, edgecolor='blue', fill=False, alpha=.9))
        self.subplot.arrow(0.5, 0.8, 0, 0.1, width=0.02, fc=arrow_color_fc, ec=arrow_color_ec)
        self.subplot.arrow(0.5, 0.2, 0, -0.1, width=0.02, fc=arrow_color_fc, ec=arrow_color_ec)
        self.subplot.arrow(0.8, 0.5, 0.1, 0, width=0.02, fc=arrow_color_fc, ec=arrow_color_ec)
        self.subplot.arrow(0.2, 0.5, -0.1, 0, width=0.02, fc=arrow_color_fc, ec=arrow_color_ec)
        self.subplot.arrow(0.75, 0.24, -0.41, 0, width=0.02, shape='right', fc=arrow_color_fc, ec=arrow_color_ec)
        self.subplot.arrow(0.25, 0.76, 0.41, 0, width=0.02, shape='right', fc=arrow_color_fc, ec=arrow_color_ec)
        self.subplot.arrow(0.24, 0.75, 0, -0.41, width=0.02, shape='left', fc=arrow_color_fc, ec=arrow_color_ec)
        self.subplot.arrow(0.76, 0.25, 0, 0.41, width=0.02, shape='left', fc=arrow_color_fc, ec=arrow_color_ec)
        self.subplot.annotate(f'σy = {self.res.sigma_y}', (0.58, 0.9), size=settings.size, ha='left', va='top')
        self.subplot.annotate(f'σx = {self.res.sigma_x}', (0.82, 0.4), size=settings.size, ha='left', va='center')
        self.subplot.annotate(f'τxy = {self.res.tau_xy}', (0.8, 0.8), size=settings.size, ha='left', va='top')

        self.subplot.set_aspect('equal', 'datalim')
        self.subplot.axis('off')

    def plot_square_angle(self):
        self.subplot.annotate(f'{round_expr((abs(self.res.angle) * (180 / numpy.pi)) / 2)}°', (0.5, 0.5),
                              size=settings.size, ha='center', va='bottom', color='blue')

        start, finish = self.det_start_finish()

        self.subplot.add_patch(Wedge((0.5, 0.5), 0.05, start / 2, finish / 2, linewidth=2,
                                     edgecolor='blue', facecolor='blue', fill=True))

        self.subplot.add_patch(
            Wedge((0.5, 0.5), 0.245, start / 2, finish / 2, linewidth=2, edgecolor='blue',
                  facecolor='blue', fill=False, linestyle='--'))

    def det_start_finish(self):
        if self.res.angle > 0:
            start = 0
            finish = self.res.angle * (180 / numpy.pi)

        else:
            start = self.res.angle * (180 / numpy.pi)
            finish = 0

        return start, finish

    def plot_cube(self):
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
        self.subplot.plot_wireframe(X, Y, one, alpha=0.5, color='blue')
        self.subplot.plot_wireframe(X, Y, -one, alpha=0.5, color='blue')
        self.subplot.plot_wireframe(X, -one, Y, alpha=0.5, color='blue')
        self.subplot.plot_wireframe(X, one, Y, alpha=0.5, color='blue')
        self.subplot.plot_wireframe(one, X, Y, alpha=0.5, color='blue')
        self.subplot.plot_wireframe(-one, X, Y, alpha=0.5, color='blue')
        self.subplot.scatter3D(points[:, 0], points[:, 1], points[:, 2])
        self.subplot.plot_surface(X, Y, one, linewidth=0, color='blue', antialiased=False, alpha=0.2)
        self.subplot.plot_surface(X, Y, -one, linewidth=0, color='blue', antialiased=False, alpha=0.2)
        self.subplot.plot_surface(X, -one, Y, linewidth=0, color='blue', antialiased=False, alpha=0.2)
        self.subplot.plot_surface(X, one, Y, linewidth=0, color='blue', antialiased=False, alpha=0.2)
        self.subplot.plot_surface(one, X, Y, linewidth=0, color='blue', antialiased=False, alpha=0.2)
        self.subplot.plot_surface(-one, X, Y, linewidth=0, color='blue', antialiased=False, alpha=0.2)

        # sigma
        quiver_color = self.color_scheme.arrow_color
        text_color = self.color_scheme.arrow_color
        self.subplot.quiver(0, 0, 1, 0, 0, 1, length=0.5, color=quiver_color)
        # self.one_fig.quiver(0, 0, -1, 0, 0, -1, length=0.5, color='black')
        # self.one_fig.quiver(0, 1, 0, 0, 1, 0, length=0.5, color='black')
        self.subplot.quiver(0, -1, 0, 0, -1, 0, length=0.5, color=quiver_color)
        self.subplot.quiver(1, 0, 0, 1, 0, 0, length=0.5, color=quiver_color)
        # self.one_fig.quiver(-1, 0, 0, -1, 0, 0, length=0.5, color='black')
        # self.one_fig.quiver(-1, 0, 0, -1, 0, 0, length=0.5, color='black')

        # tau
        self.subplot.quiver(0, 0, 1, 1, 0, 0, length=0.5, color=quiver_color, normalize=True)
        self.subplot.quiver(0, 0, 1, 0, -1, 0, length=0.5, color=quiver_color, normalize=True)
        self.subplot.quiver(0, -1, 0, 1, 0, 0, length=0.5, color=quiver_color, normalize=True)
        self.subplot.quiver(0, -1, 0, 0, 0, 1, length=0.5, color=quiver_color, normalize=True)
        self.subplot.quiver(1, 0, 0, 0, -1, 0, length=0.5, color=quiver_color, normalize=True)
        self.subplot.quiver(1, 0, 0, 0, 0, 1, length=0.5, color=quiver_color, normalize=True)

        self.subplot.text(0.1, 0.1, 1.3, f"σy = {self.res.sigma_y}", color=text_color, fontsize=settings.size)
        self.subplot.text(0.1, 0.1, 1.05, f"τyx = {self.res.tau_xy}", color=text_color, fontsize=settings.size)
        self.subplot.text(-0.1, -0.5, 1.05, f"τyz = {self.res.tau_yz}", color=text_color, fontsize=settings.size)

        self.subplot.text(0.2, -1.25, 0.5, f"τzy = {self.res.tau_yz}", color=text_color, fontsize=settings.size)
        self.subplot.text(-0.15, -1.5, 0.1, f"σz = {self.res.sigma_z}", color=text_color, fontsize=settings.size)
        self.subplot.text(0.2, -1.25, 0.1, f"τzx = {self.res.tau_xz}", color=text_color, fontsize=settings.size)

        self.subplot.text(1, 0.1, 0.4, f"τxy = {self.res.tau_xy}", color=text_color, fontsize=settings.size)
        self.subplot.text(1, -0.6, 0.1, f"τxz = {self.res.tau_xz}", color=text_color, fontsize=settings.size)
        self.subplot.text(1.25, 0.1, 0.05, f"σx = {self.res.sigma_x}", color=text_color, fontsize=settings.size)

        # set viewing angle if returning from 2D plot
        # if self.azim is not None:
        # Axes3D(fig).view_init(elev=self.elev, azim=self.azim)

        self.subplot.axis('off')

    def modify_axes(self, sigma_list: list):
        # condition to make sure axis doesnt get out of screen
        if sigma_list[0] < 0 < sigma_list[-1]:
            self.subplot.spines['left'].set_position('zero')
            self.subplot.spines['right'].set_color('none')
            self.subplot.set_xlabel('σ', fontsize=13, loc='right')

        elif sigma_list[-1] < 0:
            self.subplot.spines['left'].set_position(('axes', 1))
            self.subplot.spines['left'].set_color('none')
            self.subplot.set_xlabel('σ', fontsize=13, loc='left')

        elif sigma_list[0] > 0:
            self.subplot.spines['right'].set_color('none')
            self.subplot.set_xlabel('σ', fontsize=13, loc='right')

        self.subplot.set_ylabel('τ', rotation=0, fontsize=13, loc='top')
        self.subplot.spines['top'].set_color('none')
        self.subplot.spines['bottom'].set_position('zero')

    def make_transparent(self):
        ax = self.fig.get_axes()
        for i in range(len(ax)):
            ax[i].patch.set_alpha(0)


class color_scheme:
    def __init__(self, background: str):
        self.arrow_color = "black"
        if background == "dark":
            self.edgecolor = "white"
        elif background == "bright":
            self.edgecolor = "black"
