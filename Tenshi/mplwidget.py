from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        figure = plt.figure()
        figure.add_subplot(111)
        self.canvas = FigureCanvas(figure)

        self.toolbar = NavigationToolbar(self.canvas, self)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.toolbar)
        self.vertical_layout.addWidget(self.canvas)

        self.setLayout(self.vertical_layout)
        plt.tight_layout()

    def plot(self, new_figure=None):

        if new_figure is None:
            figure = plt.figure()
            figure.add_subplot(111)
            self.canvas.figure = figure
        else:
            self.canvas.figure = new_figure

        self.canvas.draw()

