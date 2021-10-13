import math


def get_signal_constant(moment, result, numeric_const=0):
    if math.isclose(round(moment + numeric_const, 2), round(result, 2), rel_tol=1e-2):
        return moment
    else:
        return -moment


def get_signal(reaction):
    if reaction < 0:
        return '-'
    else:
        return '+'
