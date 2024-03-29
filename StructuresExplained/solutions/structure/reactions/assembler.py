from sympy import symbols

from StructuresExplained.solutions.structure.reactions.tools import get_q_load_values


class Results:
    def __init__(self):
        self.hinged = None
        self.roll = None
        self.fixed = None
        self.roll_dists = None
        self.point_sum_x = ""
        self.point_sum_y = ""
        self.moments_sum = ""


class Assembler:
    i, j, k = symbols("i j k")

    def __init__(self, system_elements):
        self.ss = system_elements
        self.res = Results()
        self.fixed = self.ss.supports_fixed
        self.hinged = self.ss.supports_hinged
        self.roll = self.ss.supports_roll
        self.loads = self.ss.loads_point
        self.q_loads = self.ss.loads_q
        self.moments = self.ss.loads_moment
        self.relative_support = None

    @property
    def results(self):
        if not self.res.moments_sum: self.res.moments_sum = "0"
        if not self.res.point_sum_x: self.res.point_sum_x = "0"
        if not self.res.point_sum_y: self.res.point_sum_y = "0"
        return self.res

    def assemble_structure(self):
        self.simplify_variables()

        if self.fixed:
            self.res.fixed = self.fixed
            self.relative_support = self.fixed

        if self.hinged:
            self.res.hinged = self.hinged
            self.relative_support = self.hinged

        if self.roll:
            self.res.roll = self.roll
            self.res.inclined_roll = self.ss.inclined_roll
            self.res.roll_dists = {"x": str((self.roll.vertex.x - self.relative_support.vertex.x) * self.i),
                                   "y": str((self.roll.vertex.y - self.relative_support.vertex.y) * self.j)}

        self.map_loads()

        self.map_q_loads()

        self.map_moments()

    def simplify_variables(self):
        if self.hinged:
            self.hinged = self.hinged[0]
        if self.roll:
            self.roll = self.roll[0]
        if self.fixed:
            self.fixed = self.fixed[0]

    def map_loads(self):
        for node_id, load in self.loads.items():
            x = self.ss.node_map.get(node_id).vertex.x
            y = self.ss.node_map.get(node_id).vertex.y
            fx = load[0]
            fy = -load[1]

            if round(fx, 13) != 0:
                self.res.point_sum_x += f'+ {fx}'

                if (y - self.relative_support.vertex.y) != 0:
                    self.res.moments_sum += fr' + {fx * self.i} * {(self.relative_support.vertex.y - y) * self.j}'

            if round(fy, 13) != 0:
                self.res.point_sum_y += f'+ {fy}'

                if (x - self.relative_support.vertex.x) != 0:
                    self.res.moments_sum += fr' + {fy * self.j} * {(self.relative_support.vertex.x - x) * self.i}'

    def map_q_loads(self):
        for element_id, q_load in self.q_loads.items():
            qi = -q_load[0][0]
            q = -q_load[1][0]
            xi = self.ss.element_map.get(element_id).vertex_1.x
            yi = self.ss.element_map.get(element_id).vertex_1.y
            xf = self.ss.element_map.get(element_id).vertex_2.x
            yf = self.ss.element_map.get(element_id).vertex_2.y
            angle = self.ss.element_map.get(element_id).angle

            y_load, x_load, height, base = \
                get_q_load_values(q, qi, xi, xf, yi, yf, angle)

            if round(x_load, 13) != 0:
                self.res.point_sum_x += f'+{x_load}'
                if round(self.relative_support.vertex.y - (height + yi), 13) != 0:
                    self.res.moments_sum += fr' + {x_load * self.i} * {(self.relative_support.vertex.y - (height + yi)) * self.j} '

            if round(y_load, 13) != 0:
                self.res.point_sum_y += f'+{y_load}'
                if round(self.relative_support.vertex.x - (base + xi), 13) != 0:
                    self.res.moments_sum += fr' + {y_load * self.j} * {(self.relative_support.vertex.x - (base + xi)) * self.i}'

    def map_moments(self):
        for node_id, moment in self.moments.items():
            self.res.moments_sum += f' + {moment * self.k}'
