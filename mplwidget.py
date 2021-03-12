from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib.backends.backend_qt5 as qt5agg
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import numpy as np


class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        plt.style.use('dark_background')
        figure = plt.figure()
        self.canvas = FigureCanvas(figure)
        self.canvas.figure.patch.set_alpha(0)
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.patch.set_alpha(0.2)

        #self.toolbar_buttons()
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.default_cursor = qt5agg.cursord[1]
        self.cursor = QCursor(Qt.CrossCursor)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.toolbar)
        self.vertical_layout.addWidget(self.canvas)

        self.setLayout(self.vertical_layout)
        plt.tight_layout()
        self.setGrid()

    def toolbar_buttons(self):
        backend_bases.NavigationToolbar2.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            (None, None, None, None),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),
        )

    def plot(self, new_figure=None, hasGrid=True):

        if not new_figure:
            self.canvas.figure.clear()
            self.canvas.figure.add_subplot(111)
            self.set_background_alpha()
            self.setGrid(hasGrid)
        else:
            self.canvas.figure = new_figure

        plt.tight_layout()
        self.canvas.draw()

    def clear(self):
        axes = self.canvas.figure.get_axes()
        axes.clear()

    def set_background_alpha(self, alpha=0.2):
        ax = self.canvas.figure.get_axes()
        for i in range(len(ax)):
            ax[i].patch.set_alpha(alpha)

    def set_aspect_ratio_equal(self):
        ax = self.canvas.figure.get_axes()
        for i in range(len(ax)):
            if ax[i].name != "3d":
                ax[i].set_aspect('equal', 'datalim')

    def interactive_mode(self, mode):
        if mode == 0:
            qt5agg.cursord[1] = self.cursor
        else:
            qt5agg.cursord[1] = self.default_cursor

        self.canvas.toolbar.set_cursor(1)

    def fix_plot_scale(self):
        ax = self.canvas.figure.get_axes()
        for i in range(len(ax)):
            ax[i].relim()
            ax[i].autoscale_view()

    def setGrid(self, hasGrid=True):
        ax = self.canvas.figure.get_axes()
        if hasGrid:
            for i in range(len(ax)):
                ax[i].grid(hasGrid, linestyle="--", color=(29/255,40/255,51/255))
        else:
            for i in range(len(ax)):
                ax[i].grid(False)

    def setXTicks(self, xInterval):
        if int(xInterval) in (0, 1, 2):
            ax = self.canvas.figure.get_axes()
            for i in range(len(ax)):
                start, end = ax[i].get_xlim()
                ax[i].xaxis.set_ticks(np.arange(start, end, (1*10**(-int(xInterval)))))
                ax[i].xaxis.set_major_formatter(ticker.FormatStrFormatter(f'%.{xInterval}f'))
            self.canvas.draw()

    def setYTicks(self, yInterval):
        if int(yInterval) in (0, 1, 2):
            ax = self.canvas.figure.get_axes()
            for i in range(len(ax)):
                start, end = ax[i].get_xlim()
                ax[i].yaxis.set_ticks(np.arange(start, end, (1*10**(-int(yInterval)))))
                ax[i].yaxis.set_major_formatter(ticker.FormatStrFormatter(f'%.{yInterval}f'))
            self.canvas.draw()
