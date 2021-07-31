import math
import sympy
from sympy import Number
from sympy.parsing.sympy_parser import parse_expr
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Wedge
from StructuresExplained.solutions import functions
from pylatex import Document, Section, Subsection, Subsubsection, Figure, NoEscape
import numpy as np
from StructuresExplained.pdfconfig import header
from StructuresExplained.pdfconfig.translations.cross_sec_strings import translate_PDF_cross_section


class sigma:

    normal_stress_latex = []
    normal_stress_numeric = []
    points_values = []
    normal_line_numeric = []
    normal_line_latex = []
    shear_stress_numeric = []
    shear_stress_latex = []
    shear_flux_numeric = []
    shear_flux_latex = []
    points_values_shear_flux = []
    points_values_shear_stress = []
    static_moment_cut_numeric = []
    static_moment_cut_latex = []
    static_moment_cut_string = ''
    bbox_setting = dict(boxstyle="round,pad=0.1", fc="grey", ec="black", lw=1)

    def __init__(self):
        self.subareas_rectangle = {}
        self.subareas_circle = {}
        self.moment_x = ''
        self.moment_y = ''
        self.total_area = ''
        self.moment_inertia_x = ''
        self.moment_inertia_y = ''
        self.static_moment_cut = ''
        self.normal_stress = ''
        self.neutral_line = ''
        self.shear_flux = ''
        self.shear_stress = ''
        self.moment_inertia_y_latex = ''
        self.moment_inertia_x_latex = ''
        self.total_cg_x = 0
        self.total_cg_y = 0

    def det_values(self):
        self.reset_values()
        self.static_moment_rectangle()
        self.static_moment_circle()
        self.total_cg_y = float(parse_expr(f'({self.moment_x}) / ({self.total_area})'))
        self.total_cg_x = float(parse_expr(f'({self.moment_y}) / ({self.total_area})'))
        self.moment_inertia_rectangle()
        self.moment_inertia_circle()

    def static_moment_rectangle(self):
        # calculate static moment for rectangular subareas. this function only appends
        # values to a string so they can be displayed step by step in the pdf later
        
        for key, (x1, y1, x2, y2) in self.subareas_rectangle.items():
            _, _, partial_cg_y, partial_cg_x, partial_area, _ = self.get_rectangle_values(x1, y1, x2, y2)

            self.total_area += f'+ {partial_area}'
            self.moment_x += f'+ {partial_area} * {partial_cg_y}'
            self.moment_y += f'+ {partial_area} * {partial_cg_x}'

    def static_moment_circle(self):
        # calculate static moment for semi-circular subareas. this function only appends
        # values to a string so they can be displayed step by step in the pdf later
        
        for key, (x, y, radius, angle) in self.subareas_circle.items():
            partial_area, partial_cg_y, partial_cg_x = self.get_circle_values(angle, radius)

            self.total_area += f'+ {partial_area}'
            
            if float(f'{partial_cg_y}') > 0:
                self.moment_x += f'+ {partial_area} * ({y} + {partial_cg_y})'
            elif float(f'{partial_cg_y}') < 0:
                self.moment_x += f'+ {partial_area} * ({y} {partial_cg_y})'
            elif float(f'{partial_cg_y}') == 0:
                self.moment_x += f'+ {partial_area} * {y}'
                
            if float(f'{partial_cg_x}') > 0:
                self.moment_y += f'+ {partial_area} * ({x} + {partial_cg_x})'
            elif float(f'{partial_cg_x}') < 0:
                self.moment_y += f'+ {partial_area} * ({x} {partial_cg_x})'
            elif float(f'{partial_cg_x}') == 0:
                self.moment_y += f'+ {partial_area} * {x}'

    def moment_inertia_rectangle(self):
        # calculate moment of inertia for rectangle subareas.
        # this function makes two strings, one for the results and displaying in the UI
        # and the other for the step by step solution.
        
        for key, (x1, y1, x2, y2) in self.subareas_rectangle.items():
            base, height, partial_cg_y, partial_cg_x, area, _ = self.get_rectangle_values(x1, y1, x2, y2)

            self.moment_inertia_x += f'+(({base} * ({height} ** 3)) / 12) + ({area} * (({self.total_cg_y} - {partial_cg_y}) ** 2))'

            self.moment_inertia_x_latex += r'+ \frac' + '{' + f'{base} * {height}^3' + '}' + r'{12}'
            if area * (self.total_cg_y - partial_cg_y) ** 2 != 0:
                # appends parallel axis theorem if necessary
                self.moment_inertia_x_latex += f'+ {area} * ({self.total_cg_y} - {partial_cg_y})^2'

            self.moment_inertia_y += f'+((({base} ** 3) * {height}) / 12) + ({area} * (({self.total_cg_x} - {partial_cg_x}) ** 2))'

            self.moment_inertia_y_latex += r'+ \frac' + '{' + f'{base}^3 * {height}' + '}' + r'{12}'
            if area * (self.total_cg_x - partial_cg_x) ** 2 != 0:
                # appends parallel axis theorem if necessary
                self.moment_inertia_y_latex += f'+ {area} * ({self.total_cg_x} - {partial_cg_x})^2'

    def moment_inertia_circle(self):
        # calculate moment of inertia for semi-circular subareas.
        # this function makes two strings, one for the results and displaying in the UI
        # and the other for the step by step solution.

        for key, (x, y, radius, angle) in self.subareas_circle.items():
            area, partial_cg_y, partial_cg_x = self.get_circle_values(angle, radius)

            moment_inertia = f'+({math.pi} * {radius} ** 4) / 8'
            moment_inertia_latex = r'+ \frac' + '{' + f'{math.pi} * {radius}^4' + '}' + r'{8}'

            self.moment_inertia_x += f'{moment_inertia} + {area} * (({self.total_cg_y} - {y + partial_cg_y})**2)'

            self.moment_inertia_x_latex += moment_inertia_latex
            if area * ((partial_cg_y - y) ** 2) != 0:
                # appends parallel axis theorem if necessary
                self.moment_inertia_x_latex += f'+ {area} * ({self.total_cg_y} - {y + partial_cg_y})^2'

            self.moment_inertia_y += f'{moment_inertia} + {area} * (({self.total_cg_x} - {x + partial_cg_x})**2)'

            self.moment_inertia_y_latex += moment_inertia_latex
            if area * ((self.total_cg_x - x) ** 2) != 0:
                # appends parallel axis theorem if necessary
                self.moment_inertia_y_latex += f'+ {area} * ({self.total_cg_x} - {x + partial_cg_x})^2'

    def full_sm(self, cut_height):
        # calculate static moment on the cut given by the user. only for rectangle subareas currently

        static_moment_cut_string = ''
        static_moment_cut = 0
        for key, (x1, y1, x2, y2) in self.subareas_rectangle.items():
            base, height, partial_cg_y, _, area, _ = self.get_rectangle_values(x1, y1, x2, y2)

            half_height = height / 2
            distance_from_cut = cut_height - partial_cg_y

            if distance_from_cut <= -half_height:
                static_moment_cut += area * (partial_cg_y - self.total_cg_y)

                static_moment_cut_string += f'+ {area} \cdot ({partial_cg_y} - {self.total_cg_y}) '

            elif np.abs(distance_from_cut) <= half_height:
                static_moment_cut += (height / 2 + partial_cg_y - cut_height) * base * \
                                     (((height / 2 + partial_cg_y - cut_height) * .5 + cut_height) - self.total_cg_y)

                static_moment_cut_string += r'+ (' + r'\frac{' + f'{height}' + r'}{' + f'{2}' + r'} + ' + f'{partial_cg_y}' \
                                                                                                         f' - {cut_height}) \cdot {base} \cdot ' + r'(((\frac{' + f'{height}' + r'}{' \
                                           + f'{2}' + r'} + ' + f'{partial_cg_y} - {cut_height}) \cdot 0.5 +' \
                                                                f' {cut_height}) - {self.total_cg_y}) '

        return self.static_moment_cut

        # values for circular sectors
        # for key, (x, y, r, a) in self.sub_areas_cir.items():
        #     A, cgy, cgx = self.cir_values(a, r)
        #
        #     Ac = r**2 * np.arccos((cut_y-y)/r) - cut_y-y * (r**2 - d**2)**.5
        #     self.Qc += Ac * (y + cgy - self.yg)

    def get_rectangle_values(self, x1, y1, x2, y2):
        # calculate values for rectangular subarea

        base = x2 - x1
        height = y1 - y2
        partial_cg_y = (y1 + y2) / 2
        partial_cg_x = (x1 + x2) / 2
        area = base * height
        dc = partial_cg_y - self.total_cg_y

        return base, height, partial_cg_y, partial_cg_x, area, dc

    def get_circle_values(self, angle, radius):
        # calculate values for semi-circular subarea

        area = (math.pi * radius ** 2) / 2
        partial_cg_y = math.cos(angle * math.pi / 180) * ((4 * radius) / (3 * math.pi))
        partial_cg_x = math.sin(angle * math.pi / 180) * ((4 * radius) / (3 * math.pi))

        return area, partial_cg_y, partial_cg_x

    def det_normal_stress(self, normal_force, total_area, moment_y, moment_z, moment_inertia_x, moment_inertia_y, append_to_pdf, y, z):
        normal_stress = f'({normal_force}/{total_area}) - (({moment_y}/{moment_inertia_y}) * {z}) -' \
                         f' (({moment_z}/{moment_inertia_x}) * {y})'
        normal_stress_latex = NoEscape(r'\frac{' + f'{normal_force}' + r'}{' + f'{total_area}' + r'} - \frac{' +
                                        f'{moment_y}' + r'}{' + f'{moment_inertia_y}' + r'} \cdot' + f' {z} -' +
                                        r'\frac{' + f'{moment_z}' + r'}{' + f'{moment_inertia_x}' + r'} \cdot' + f' {y}'
                                        )

        if (moment_y != "0" and type(z) != str) and (type(y) == str or moment_z == "0"):
            self.neutral_line = f"z = {self.round_expr(sympy.solve(normal_stress, z)[0], 2)}"
        elif (moment_y == "0" and moment_z == "0") or (type(y) == str and type(z) == str):
            self.neutral_line = "Não há linha neutra"
        else:
            self.neutral_line = f"y = {self.round_expr(sympy.solve(normal_stress, y)[0], 2)}"

        neutral_line_latex = NoEscape(r'0 = \frac{' + f'{normal_force}' + r'}{' + f'{total_area}' + r'} - \frac{'
                                      + f'{moment_y}' + r'}{' + f'{moment_inertia_y}' + r'} \cdot z -' + r'\frac{'
                                      + f'{moment_z}' + r'}{' + f'{moment_inertia_x}' + r'} \cdot y')

        if append_to_pdf:
            self.append_for_pdf(normal_stress, normal_stress_latex, normal_force, moment_y, moment_z, y, z, self.neutral_line, neutral_line_latex)
        return self.round_expr(parse_expr(normal_stress), 2), self.neutral_line

    def det_shear_tension(self, shear_force, static_moment, normal_stress, moment_inertia_x, append_to_pdf):
        self.shear_flux = f'{shear_force} * {static_moment} / {moment_inertia_x}'
        shear_flux_latex = r'\frac{' + f'{shear_force} \cdot {static_moment}' + r'}{' + f'{moment_inertia_x}' + r'}'
        if float(normal_stress) != 0:
            self.shear_stress = f'({shear_force} * {static_moment}) / ({moment_inertia_x} * {normal_stress})'
            shear_stress_latex = r'\frac{' + f'{shear_force} \cdot {static_moment}' + r'}{' + f'{moment_inertia_x} \cdot {normal_stress}' + r'}'
            if append_to_pdf:
                self.append_for_pdf_shear(self.shear_flux, shear_flux_latex, shear_force, static_moment, moment_inertia_x, self.shear_stress, shear_stress_latex, normal_stress)
            return float(parse_expr(self.shear_flux)), float(parse_expr(self.shear_stress))
        else:
            if append_to_pdf:
                self.append_for_pdf_shear(self.shear_flux, shear_flux_latex, shear_force, static_moment, moment_inertia_x)
            return float(parse_expr(self.shear_flux)), 0

    def det_color(self, c, p):
        if c == p:
            color = 'r'
        else:
            color = 'dodgerblue'
        return color

    def plot_rect(self, rectangle_subarea_id):
        for key, (x1, y1, x2, y2) in self.subareas_rectangle.items():
            base = x2 - x1
            height = y1 - y2
            self.subplot.text(x1, y1, f'({x1},{y1})', size=functions.size, ha='center', va='bottom', bbox=self.bbox_setting)
            self.subplot.plot(x1, y1, 'ro')
            self.subplot.text(x2, y2, f'({x2},{y2})', size=functions.size, ha='center', va='bottom', bbox=self.bbox_setting)
            self.subplot.plot(x2, y2, 'ro')
            color = self.det_color(key, rectangle_subarea_id)
            self.subplot.add_patch(Rectangle((x1, y2), base, height, linewidth=5, edgecolor=(10 / 255, 60 / 255, 100 / 255), facecolor=color, alpha=1))

    def plot_cir(self, circle_subarea_id):
        for key, (x, y, radius, angle) in self.subareas_circle.items():
            self.subplot.plot(x, y, 'ro')
            self.subplot.text(x, y, f'({x},{y})', size=functions.size, ha='center', va='bottom', bbox=self.bbox_setting)
            color = self.det_color(key, circle_subarea_id)
            self.subplot.add_patch(Wedge((x, y), radius, -angle, -angle - 180, linewidth=5, edgecolor='black', facecolor=color))

    def plot(self, rectangle_subarea_id, circle_subarea_id, fig=None):
        if fig is None:
            fig = plt.figure()
        else:
            fig.clear()

        self.subplot = fig.add_subplot(111)

        self.plot_rect(rectangle_subarea_id)
        self.plot_cir(circle_subarea_id)

        self.subplot.plot(self.total_cg_x, self.total_cg_y, 'ro')
        self.subplot.text(self.total_cg_x, self.total_cg_y, f"CG ({self.total_cg_x:.1f},{self.total_cg_y:.1f})", size=functions.size, ha='center',
                          va='bottom', bbox=self.bbox_setting)

        plt.tight_layout()
        self.subplot.set_aspect('equal', 'datalim')
        self.subplot.set_alpha(0.2)
        return fig

    def solver(self, language):
        doc = Document(document_options="a4paper,12pt", documentclass="article")
        doc.preamble.append(NoEscape(header.PDFsettings))

        tpdf = translate_PDF_cross_section(language)

        doc.append(NoEscape(header.makeCover(tpdf.title, language)))

        with doc.create(Section(tpdf.step_split)):
            with doc.create(Figure(position='H')) as fig_sectransv:
                fig_sectransv.add_image("figs\\sectransv", width='500px')
                fig_sectransv.add_caption(NoEscape(tpdf.figure_label))

        with doc.create(Section(tpdf.step_static_moment)):
            if self.subareas_circle:
                doc.append(NoEscape(tpdf.centroid))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'\frac{4 * R}{3 \cdot \pi}'))
                doc.append(NoEscape(r'\end{dmath*}'))

            with doc.create(Subsection(tpdf.step_static_moment_x)):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{x_{total}} = \sum{Ms_x} \\'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(tpdf.msx_operation))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{{x_{{total}}}} = {}'.format(self.moment_x)))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{{x_{{total}}}} = {:.2f}$ $m^3'.format(parse_expr(self.moment_x))))
                doc.append(NoEscape(r'\end{dmath*}'))

            with doc.create(Subsection(tpdf.step_static_moment_y)):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{y_{total}} = \sum{Ms_y} \\'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(tpdf.msy_operation))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{{y_{{total}}}} = {}'.format(self.moment_y)))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Ms_{{y_{{total}}}} = {:.2f}$ $m^3'.format(parse_expr(self.moment_y))))
                doc.append(NoEscape(r'\end{dmath*}'))

        with doc.create(Section(tpdf.step_centroid)):
            with doc.create(Subsection(tpdf.centroid_x)):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'X_{cg} = \frac{Ms_y}{A_{total}}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(f'X_{{cg}} = \\frac{{{parse_expr(self.moment_y)}}}{{{self.total_area}}}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'X_{{cg}} = {:.2f}$ $m'.format(self.total_cg_x)))
                doc.append(NoEscape(r'\end{dmath*}'))

            with doc.create(Subsection(tpdf.centroid_y)):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Y_{cg} = \frac{Ms_x}{A_{total}}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(f'Y_{{cg}} = \\frac{{{parse_expr(self.moment_x)}}}{{{self.total_area}}}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'Y_{{cg}} = {:.2f}$ $m'.format(self.total_cg_y)))
                doc.append(NoEscape(r'\end{dmath*}'))

        with doc.create(Section(tpdf.step_moment_inercia)):
            doc.append(NoEscape(tpdf.moment_inercia_tip))
            doc.append(NoEscape(tpdf.theorem_formula))

            with doc.create(Subsection(tpdf.moment_inercia_x)):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{x_{total}} = \sum{I_x}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                if self.subareas_rectangle:
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.moment_inercia_x_rect_formula))
                    doc.append(NoEscape(r'\end{dmath*}'))
                if self.subareas_circle:
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.moment_inercia_x_circ_formula))
                    doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{{x_{{total}}}} = {}'.format(self.moment_inertia_x_latex)))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{{x_{{total}}}} = {:.2f}$ $m^4'.format(parse_expr(self.moment_inertia_x))))
                doc.append(NoEscape(r'\end{dmath*}'))

            with doc.create(Subsection(tpdf.moment_inercia_y)):
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{y_{total}} = \sum{Iy}'))
                doc.append(NoEscape(r'\end{dmath*}'))
                if self.subareas_rectangle:
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.moment_inercia_y_rect_formula))
                    doc.append(NoEscape(r'\end{dmath*}'))
                if self.subareas_circle:
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.moment_inercia_y_circ_formula))
                    doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{{y_{{total}}}} = {}'.format(self.moment_inertia_y_latex)))
                doc.append(NoEscape(r'\end{dmath*}'))
                doc.append(NoEscape(r'\begin{dmath*}'))
                doc.append(NoEscape(r'I_{{y_{{total}}}} = {:.2f}$ $m^4'.format(parse_expr(self.moment_inertia_y))))
                doc.append(NoEscape(r'\end{dmath*}'))

        if self.normal_stress_latex:
            with doc.create(Section(tpdf.step_normal_stress_neutral_line)):
                with doc.create(Subsection(tpdf.normal_stress_formula)):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.normal_stress_var + r' \frac{N}{A} - \frac{My}{Iy} \cdot z - \frac{Mz}{Iz} \cdot y'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                with doc.create(Subsection(tpdf.neutral_line_formula)):
                    doc.append(NoEscape(tpdf.neutral_line_tip))
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(r'0 = \frac{N}{A} - \frac{My}{Iy} \cdot z - \frac{Mz}{Iz} \cdot y'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                for i in range(len(self.normal_stress_latex)):
                    with doc.create(Subsection(f'{tpdf.calculating_for} N = {self.points_values[i][0]} N, '
                                               f'My = {self.points_values[i][1]} Nm, Mz = {self.points_values[i][2]} Nm, '
                                               f'y = {self.points_values[i][3]} m, '
                                               f'z = {self.points_values[i][4]} m')):
                        with doc.create(Subsubsection(tpdf.step_normal_stress)):
                            doc.append(NoEscape(r'\begin{dmath*}'))
                            doc.append(NoEscape(tpdf.normal_stress_var + f'{self.normal_stress_latex[i]}'))
                            doc.append(NoEscape(r'\end{dmath*}'))
                            doc.append(NoEscape(r'\begin{dmath*}'))
                            doc.append(NoEscape(tpdf.normal_stress_var + f'{self.round_expr(parse_expr(self.normal_stress_numeric[i]), 2)}$ $Pa'))
                            doc.append(NoEscape(r'\end{dmath*}'))
                        with doc.create(Subsubsection(tpdf.step_neutral_line)):
                            doc.append(NoEscape(r'\begin{dmath*}'))
                            doc.append(NoEscape(f'{self.normal_line_latex[i]}'))
                            doc.append(NoEscape(r'\end{dmath*}'))
                            doc.append(NoEscape(r'\begin{dmath*}'))
                            doc.append(NoEscape(f'{self.normal_line_numeric[i]}'))
                            doc.append(NoEscape(r'\end{dmath*}'))

        if self.shear_flux_latex or self.shear_stress_latex:
            with doc.create(Section(tpdf.step_static_moment_cut)):

                with doc.create(Subsection(tpdf.static_moment_cut_formula_above_str)):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.static_moment_cut_formula_above))
                    doc.append(NoEscape(r'\end{dmath*}'))

                with doc.create(Subsection(tpdf.static_moment_cut_formula_not_above_str)):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.static_moment_cut_formula_not_above))
                    doc.append(NoEscape(r'\end{dmath*}'))

            for i in range(len(self.static_moment_cut_latex)):
                    with doc.create(Subsection(tpdf.step_static_moment_cut)):
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(tpdf.static_moment_var + f'{self.static_moment_cut_latex[i]}'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(tpdf.static_moment_var + f'{round(self.static_moment_cut_numeric[i], 2)}$ $m^3'))
                        doc.append(NoEscape(r'\end{dmath*}'))

        if self.shear_flux_latex:
            with doc.create(Section(tpdf.step_shear_flux)):
                with doc.create(Subsection(tpdf.shear_flux_formula)):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.shear_flux_var + r' \frac{V \cdot Q}{I_x}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                for i in range(len(self.shear_flux_latex)):
                    with doc.create(Subsection(NoEscape(f'{tpdf.calculating_for} V = {self.points_values_shear_flux[i][0]} N, '
                                               f'Q = {self.points_values_shear_flux[i][1]} m' + r'\textsuperscript{3}, '
                                               r'I\textsubscript{x}' + f' = {self.points_values_shear_flux[i][2]} m' + r'\textsuperscript{4}'))):
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(tpdf.shear_flux_var + f'{self.shear_flux_latex[i]}'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(tpdf.shear_flux_var + f'{self.round_expr(parse_expr(self.shear_flux_numeric[i]), 2)}' + r'$ $\frac{N}{m}'))
                        doc.append(NoEscape(r'\end{dmath*}'))

        if self.shear_stress_latex:
            with doc.create(Section(tpdf.step_shear_stress)):
                with doc.create(Subsection(tpdf.shear_stress_formula_str)):
                    doc.append(NoEscape(r'\begin{dmath*}'))
                    doc.append(NoEscape(tpdf.shear_stress_var + r' \frac{V \cdot Q}{I_x \cdot t}'))
                    doc.append(NoEscape(r'\end{dmath*}'))
                for i in range(len(self.shear_stress_latex)):
                    with doc.create(Subsection(NoEscape(f'{tpdf.calculating_for} V = {self.points_values_shear_stress[i][0]} N, '
                                               f'Q = {self.points_values_shear_stress[i][1]} m' + r'\textsuperscript{3}, '
                                               r'I\textsubscript{x}' + f' = {self.points_values_shear_stress[i][2]} m' + r'\textsuperscript{4}, '
                                               f't = {self.points_values_shear_stress[i][3]} m'))):
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(tpdf.shear_stress_var + f'{self.shear_stress_latex[i]}'))
                        doc.append(NoEscape(r'\end{dmath*}'))
                        doc.append(NoEscape(r'\begin{dmath*}'))
                        doc.append(NoEscape(tpdf.shear_stress_var + f'{self.round_expr(parse_expr(self.shear_stress_numeric[i]), 2)}'+ r'$ $Pa'))
                        doc.append(NoEscape(r'\end{dmath*}'))

        doc.generate_pdf('tmp\\resolucaorm',
                         compiler='pdflatex',
                         win_no_console=True,
                         compiler_args=["-enable-installer"])
        #doc.generate_tex('tmp\\resolucaorm')

    def append_for_pdf(self,
                       normal_stress,
                       normal_stress_latex,
                       normal_force,
                       moment_y,
                       moment_x,
                       y,
                       z,
                       neutral_line_numeric,
                       neutral_line_latex
                       ):

        if normal_stress not in self.normal_stress_numeric:
            self.normal_stress_numeric.append(normal_stress)
            self.normal_stress_latex.append(normal_stress_latex)
            self.points_values.append([normal_force, moment_y, moment_x, y, z])
            self.normal_line_numeric.append(neutral_line_numeric)
            self.normal_line_latex.append(neutral_line_latex)

    def append_for_pdf_shear(self,
                             shear_flux_numeric,
                             shear_flux_latex,
                             shear_force,
                             static_moment,
                             moment_inertia_x,
                             normal_stress_numeric=None,
                             normal_stress_latex=None,
                             normal_stress=None
                             ):

        self.shear_flux_numeric.append(shear_flux_numeric)
        self.shear_flux_latex.append(shear_flux_latex)
        self.points_values_shear_flux.append([shear_force, static_moment, moment_inertia_x])
        self.static_moment_cut_numeric.append(self.static_moment_cut)
        self.static_moment_cut_latex.append(self.static_moment_cut_string)

        if normal_stress_numeric is not None:
            self.points_values_shear_stress.append([shear_force, static_moment, moment_inertia_x, normal_stress])
            self.shear_stress_numeric.append(normal_stress_numeric)
            self.shear_stress_latex.append(normal_stress_latex)

    def round_expr(self, expr, num_digits):
        return expr.xreplace({n: round(n, num_digits) for n in expr.atoms(Number)})

    def reset_values(self):
        self.total_area = self.moment_x = self.moment_y = self.moment_inertia_y = self.moment_inertia_x = \
            self.moment_inertia_y_latex = self.moment_inertia_x_latex = self.static_moment_cut = ''
        self.static_moment_cut = self.total_cg_y = self.total_cg_x = 0
        self.normal_stress_latex.clear()
        self.normal_stress_numeric.clear()
        self.points_values.clear()
        self.normal_line_numeric.clear()
        self.normal_line_latex.clear()
        self.shear_stress_numeric.clear()
        self.shear_stress_latex.clear()
        self.shear_flux_numeric.clear()
        self.shear_flux_latex.clear()
        self.points_values_shear_flux.clear()
        self.points_values_shear_stress.clear()
        self.static_moment_cut_numeric.clear()
        self.static_moment_cut_latex.clear()
