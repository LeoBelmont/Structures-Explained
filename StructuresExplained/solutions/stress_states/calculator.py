import numpy


class calculator_plain_state:
    def __init__(self):
        self.sigma_x = 0
        self.sigma_y = 0
        self.tau_xy = 0
        self.sigma_1 = 0
        self.sigma_2 = 0
        self.center = 0
        self.max_shear = 0
        self.angle = 0

    def calculate(self):
        self.sigma_1 = (self.sigma_x + self.sigma_y) / 2 + (((self.sigma_x - self.sigma_y) / 2) ** 2 +
                                                            self.tau_xy ** 2) ** 0.5

        self.sigma_2 = (self.sigma_x + self.sigma_y) / 2 - (((self.sigma_x - self.sigma_y) / 2) ** 2 +
                                                            self.tau_xy ** 2) ** 0.5

        # make sure stresses are in correct order
        sigmalist = [self.sigma_1, self.sigma_2]
        sigmalist.sort()

        self.center = (sigmalist[0] + sigmalist[-1]) / 2
        self.angle = (numpy.arctan(self.tau_xy / (self.sigma_x - self.center)))
        self.max_shear = (((self.sigma_x - self.sigma_y) / 2) ** 2 + self.tau_xy ** 2) ** 0.5


class calculator_triple_state:
    def __init__(self):
        self.sigma_x = 0
        self.sigma_y = 0
        self.sigma_z = 0
        self.tau_xy = 0
        self.tau_xz = 0
        self.tau_yz = 0
        self.sigma_1 = 0
        self.sigma_2 = 0
        self.sigma_3 = 0
        self.center = 0
        self.max_shear = 0

    def calculate(self):
        matrix = numpy.asarray([[self.sigma_x, self.tau_xy, self.tau_xz],
                                [self.tau_xy, self.sigma_y, self.tau_yz],
                                [self.tau_xz, self.tau_yz, self.sigma_z]])

        sigmalist, _ = numpy.linalg.eig(matrix)

        # make sure stresses are in correct order
        sigmalist.sort()
        self.sigma_1 = sigmalist[2]
        self.sigma_2 = sigmalist[1]
        self.sigma_3 = sigmalist[0]
        self.center = (sigmalist[0] + sigmalist[-1]) / 2
        self.max_shear = (sigmalist[-1] - sigmalist[0]) / 2
