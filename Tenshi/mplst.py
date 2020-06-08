from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import sigma


class MplST(QWidget):

    sig = sigma.sigma()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.figure = plt.figure()
        self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.toolbar)
        self.vertical_layout.addWidget(self.canvas)

        self.setLayout(self.vertical_layout)
        plt.tight_layout()

    def plot(self, xg, yg, p=None):

        self.figure.clear()

        for c in range(len(self.sig.sub_areas_rect)):
            x1 = self.sig.sub_areas_rect[c][0]
            y1 = self.sig.sub_areas_rect[c][1]
            x2 = self.sig.sub_areas_rect[c][2]
            y2 = self.sig.sub_areas_rect[c][3]
            b = x2 - x1
            h = y1 - y2
            plt.plot(x1, y1, 'ro')
            plt.annotate(f'({x1},{y1})', (x1, y1), size=16, ha='center', va='bottom')
            plt.plot(x2, y2, 'ro')
            plt.annotate(f'({x2},{y2})', (x2, y2), size=16, ha='center', va='bottom')
            if c == p:
                plt.gca().add_patch(Rectangle((x1, y2), b, h, linewidth=5, edgecolor='black', facecolor='r'))
            else:
                plt.gca().add_patch(Rectangle((x1, y2), b, h, linewidth=5, edgecolor='black', facecolor='b'))

        plt.plot(xg, yg, 'ro')
        plt.annotate(f"CG ({xg:.1f},{yg:.1f})", (xg, yg), size=16, ha='center', va='bottom')

        plt.tight_layout()
        self.canvas.draw()
