import math


def get_q_load_values(q, qi, xi, xf, yi, yf, angle):
    pos = ((xf - xi) ** 2 + (yf - yi) ** 2) ** 0.5
    point_load = ((qi + q) * pos) / 2
    cg = ((pos / 3) * (qi + 2 * q)) / (qi + q)

    y_load = math.cos(angle + math.pi) * point_load
    x_load = math.sin(angle + math.pi) * point_load
    height = math.sin(angle) * cg
    base = math.cos(angle) * cg

    return y_load, x_load, height, base
