import math
from sympy import symbols
from table import Ui_Dialog


class sigma():

    sub_areas_rect = []
    sub_areas_cir = []
    y = symbols("y")
    Mx = 0
    My = 0
    At = 0
    Ix = 0
    Iy = 0
    xg = 0
    yg = 0
    Qc = 0

    def det_static_moment_rectangle(self):
        self.At = self.Mx = self.My = 0
        for c in range(len(self.sub_areas_rect)):
            x1 = self.sub_areas_rect[c][0]
            y1 = self.sub_areas_rect[c][1]
            x2 = self.sub_areas_rect[c][2]
            y2 = self.sub_areas_rect[c][3]
            b = x2 - x1
            h = y1 - y2
            c = (y1 + y2) / 2
            d = (x1 + x2) / 2
            A = b * h
            self.At += A
            self.Mx += A * c
            self.My += A * d
            self.yg = self.Mx / self.At
            self.xg = self.My / self.At
        self.Iy = self.Ix = self.Qc = 0
        for c in range(len(self.sub_areas_rect)):
            x1 = self.sub_areas_rect[c][0]
            y1 = self.sub_areas_rect[c][1]
            x2 = self.sub_areas_rect[c][2]
            y2 = self.sub_areas_rect[c][3]
            b = x2 - x1
            h = y1 - y2
            c = (y1 + y2) / 2
            d = (x1 + x2) / 2
            A = b * h
            dc = c - self.yg
            if dc < 0:
                dc *= -1
            self.Qc += A * dc
            self.Iy += (((b ** 3) * h) / 12) + (A * ((self.xg - d) ** 2))
            self.Ix += ((b * (h ** 3)) / 12) + (A * ((self.yg - c) ** 2))

    def det_static_moment_circle(self):
        # 4R / 3PI
        c = len(self.sub_areas_cir) - 1
        x = self.sub_areas_cir[c][0]
        y = self.sub_areas_cir[c][1]
        r = self.sub_areas_cir[c][2]
        A = math.pi * r ** 2
        self.At += A
        self.Mx += A * x
        self.My += A * y
        self.yg = self.Mx / self.At
        self.xg = self.My / self.At
        self.Iy += ((math.pi * r ** 4) / 8) + (A * ((self.yg - y) ** 2))
        self.Ix += ((math.pi * r ** 4) / 8) + (A * ((self.xg - x) ** 2))

    def det_normal_tension(self, N, At, My, Mx, Ix, Iy):
        T = (N/At) + ((My/Iy) * self.y) + ((Mx/Ix) * self.y)
        return T

    def det_cis(self, V, Q, t, Ix):
        flux = V * Q / Ix
        if t != 0:
            Tcis = (V * Q) / (Ix * t)
            return flux, Tcis
        else:
            return flux, 0

    def show_list(self):
        pass
