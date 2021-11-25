import numpy as np
from anastruct.fem.elements import Element
from sympy import Symbol
from sympy.physics.units import degree

from StructuresExplained.solutions.structure.internal_stresses.tools import get_signal_vectors


class Stresses_Stack:
    fx = ""
    fy = ""
    fy_symbolic = ""
    fx_angular = ""
    fy_angular = ""
    is_symbolic = False
    is_angular = False
    _force_map = None
    _distributed_force_map = None
    _reactions_map = None

    def __init__(self, node: int, element: [Element]):
        self.node = node
        self.determine_internal_forces(node, element)

    @classmethod
    def system(cls, system):
        cls._force_map = system.loads_point
        cls._moment_map = system.loads_moment
        cls._distributed_force_map = system.loads_q
        cls._reactions_map = system.reaction_forces

    @property
    def axes_forces(self):
        if self.is_angular:
            self.is_angular = False
            # symbolic flag also set to false because angular strings will include symbolic strings
            self.is_symbolic = False
            return [self.fx_angular, self.fy_angular]
        if self.is_symbolic:
            self.is_symbolic = False
            return [self.fx, self.fy_symbolic]
        return [self.fx, self.fy]

    def determine_internal_forces(self, node, element):
        forces = self._force_map.get(node)
        reactions = self._reactions_map.get(node)
        if forces:
            if round(forces[0], 13):
                self.fx += f"+{forces[0]}"
            if round(forces[1], 13):
                self.fy += f"+{-forces[1]}"
        if reactions:
            if round(reactions.Fx, 13):
                self.fx += f"+{reactions.Fx}"
            if round(reactions.Fz, 13):
                self.fy += f"+{-reactions.Fz}"
        if element:
            q_loads = self._distributed_force_map.get(element.id)
            if q_loads:
                if round(q_loads[0][0], 13) and round(q_loads[1][0], 13):
                    x = Symbol('x')
                    xi = element.vertex_1.x
                    yi = element.vertex_1.y
                    xf = element.vertex_2.x
                    yf = element.vertex_2.y
                    base = ((xf - xi) ** 2 + (yf - yi) ** 2) ** 0.5
                    self.fy_symbolic = self.fy
                    self.fy += f"+{((q_loads[0][0] + q_loads[1][0]) * base) / 2}"
                    self.fy_symbolic += f"+{((((-q_loads[0][0] - -q_loads[1][0]) / (6 * base)) * x ** 2) * 3 - ((-q_loads[0][0] / 2) * x) * 2)}"
                    self.is_symbolic = True

            if abs(element.angle) != 0 and abs(element.angle) != (np.pi / 2) and \
                    abs(element.angle) != np.pi and abs(element.angle) != (3 * np.pi) / 2:

                if self.is_symbolic:
                    fy = self.fy_symbolic
                else:
                    fy = self.fy

                signals = get_signal_vectors(element.axial_force, self.fx, self.fy, element, "cos")
                self.fy_angular = f'{signals[0]} ({fy if fy else "0"}) * cos({90 - (element.angle * 180 / np.pi)}' \
                                  f' * {degree}) {signals[1]} ({self.fx if self.fx else "0"})' \
                                  f' * cos({element.angle * 180 / np.pi} * {degree})'

                signals = get_signal_vectors(element.shear_force, self.fx, self.fy, element, "sin")
                self.fx_angular = f'{signals[0]} ({fy if fy else "0"}) * sin({90 - (element.angle * 180 / np.pi)}' \
                                  f' * {degree}) {signals[1]} ({self.fx if self.fx else "0"})' \
                                  f' * sin({element.angle * 180 / np.pi} * {degree})'
                self.is_angular = True

    def extend_results(self, results):
        if results[0]:
            self.fx += str(results[0])
            self.fx_angular += str(results[0])
        if results[1]:
            self.fy += str(results[1])
            self.fy_symbolic += str(results[1])
            self.fy_angular += str(results[1])
