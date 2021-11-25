import numpy
from sympy import parse_expr


class calculator_plain_state:
    def __init__(self):
        self.sigma_x: float = 0
        self.sigma_y: float = 0
        self.tau_xy: float = 0
        self.sigma_1: float = 0
        self.sigma_2: float = 0
        self.center: float = 0
        self.max_shear: float = 0
        self.angle: float = 0

    def calculate(self):
        self.sigma_1 = (self.sigma_x + self.sigma_y) / 2 + (((self.sigma_x - self.sigma_y) / 2) ** 2 +
                                                            self.tau_xy ** 2) ** 0.5

        self.sigma_2 = (self.sigma_x + self.sigma_y) / 2 - (((self.sigma_x - self.sigma_y) / 2) ** 2 +
                                                            self.tau_xy ** 2) ** 0.5

        sigma_list = [self.sigma_2, self.sigma_1]

        # make sure stresses are in correct order
        sigma_list.sort()

        self.center = (sigma_list[0] + sigma_list[-1]) / 2
        self.max_shear = (((self.sigma_x - self.sigma_y) / 2) ** 2 + self.tau_xy ** 2) ** 0.5
        self.angle = (numpy.arctan(self.tau_xy / (self.sigma_x - self.center)))


class calculator_triple_state:
    def __init__(self):
        self.sigma_x: float = 0
        self.sigma_y: float = 0
        self.sigma_z: float = 0
        self.tau_xy: float = 0
        self.tau_xz: float = 0
        self.tau_yz: float = 0
        self.sigma_1: float = 0
        self.sigma_2: float = 0
        self.sigma_3: float = 0
        self.center: float = 0
        self.max_shear: float = 0

    def calculate(self):
        matrix = numpy.asarray([[self.sigma_x, self.tau_xy, self.tau_xz],
                                [self.tau_xy, self.sigma_y, self.tau_yz],
                                [self.tau_xz, self.tau_yz, self.sigma_z]])

        sigma_list, _ = numpy.linalg.eig(matrix)

        # make sure stresses are in correct order
        sigma_list.sort()

        self.sigma_1 = sigma_list[2]
        self.sigma_2 = sigma_list[1]
        self.sigma_3 = sigma_list[0]
        self.center = (sigma_list[0] + sigma_list[-1]) / 2
        self.max_shear = (sigma_list[-1] - sigma_list[0]) / 2
