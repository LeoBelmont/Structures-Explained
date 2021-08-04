class translate_PDF_cross_section:
    def __init__(self, language):
        if language == "PT":
            self.translatePT()
        elif language == "EN":
            self.translateEN()

    def translatePT(self):
        self.title = r"Resolução da Seção Transversal"
        self.step_split = r"Subdividir a geometria da seção transversal em formas geométricas (subáreas) de " \
                          r"propriedades conhecidas"
        self.figure_label = r"\label{fig:estrutura} Estrutura com subáreas contornadas de preto"
        self.step_static_moment = r"Calcular os momentos estáticos em relação ao eixo de interesse"
        self.centroid = r"Centroide da semi-circunferência:"
        self.step_static_moment_x = r"Cálculo do momento estático em relação ao eixo X:"
        self.msx_operation = r"Ms_x = Área_{(subárea)} \cdot \overline{Y} \\"
        self.step_static_moment_y = r"Cálculo do momento estático em relação ao eixo Y:"
        self.msy_operation = r"Ms_y = Area_{(subárea)} \cdot \overline{X} \\"
        self.step_centroid = r"Calcular os centroides em relação ao eixo de interesse"
        self.centroid_x = r"Cálculo do centroide em relação ao eixo X:"
        self.centroid_y = r"Cálculo do centroide em relação ao eixo Y:"
        self.step_moment_inertia = r"Calcular os momentos de inércia em relação aos eixos de interesse"
        self.moment_inercia_tip = r"Quando necessário (ou, na dúvida, sempre), aplicar o teorema dos eixos paralelos \\"
        self.theorem_formula = r"Teorema dos eixos paralelos: I' = I + A * d² \\"
        self.moment_inercia_x = r"Cálculo do Momento de Inércia em relação a X:"
        self.moment_inercia_x_rect_formula = r"I_{x_{(retângulos)}} = \frac{base \cdot altura^3}{12}"
        self.moment_inercia_x_circ_formula = r"I_{x_{(semi-circunferência)}} = \frac{\pi \cdot raio^4}{8}"
        self.moment_inercia_y = r"Cálculo do Momento de Inércia em relação a Y:"
        self.moment_inercia_y_rect_formula = r"I_{y_{(retângulos)}} = \frac{base^3 \cdot altura}{12}"
        self.moment_inercia_y_circ_formula = r"I_{y_{(semi-circunferência)}} = \frac{\pi \cdot raio^4}{8}"
        self.step_normal_stress = r"Calcular a Tensão Normal"
        self.step_neutral_line = r"Calcular a Linha Neutra"
        self.normal_stress_formula = r"Fórmula da Tensão Normal"
        self.neutral_line_formula = r"Fórmula da Linha Neutra"
        self.neutral_line_tip = r"A linha neutra se encontra onde a Tensão Normal é 0, portanto para encontrar" \
                                r" a posição da linha neutra (y) substituímos T por 0."
        self.calculating_for = r"Cálculo para"
        self.normal_stress_var = r"T_{normal} ="
        self.step_normal_stress = r"Cálculo da Tensão Normal"
        self.step_neutral_line = r"Cálculo da Linha Neutra"
        self.step_static_moment_cut = r"Calcular o Momento Estático no corte"
        self.static_moment_cut_formula_above_str = r"Fórmula do Momento Estático para corte sobre a subárea"
        self.static_moment_cut_formula_above = r"M_{estático_{corte}} = Área_{subárea} \cdot (centroide_{subárea} - " \
                                               r"centroide_{figura}) "
        self.static_moment_cut_formula_not_above_str = r"Fórmula do Momento Estático para corte acima ou abaixo da " \
                                                       r"subárea"
        self.static_moment_cut_formula_not_above = r"M_{estático_{corte}} = (\frac{altura}{2} + centroide_{subárea}" \
                                                   r"- corte_y) \cdot base \cdot ((\frac{altura}{2} + centroide_{" \
                                                   r"subárea} - corte_y) \cdot 0.5 + corte_y - centroide_{figura}) "
        self.static_moment_var = r"M_{estático_{corte}} ="
        self.step_shear_flux = r"Calcular o Fluxo de Cisalhamento"
        self.shear_flux_formula = r"Fórmula do Fluxo de Cisalhamento"
        self.shear_flux_var = r"f_{cisalhamento} ="
        self.step_shear_stress = r"Calcular a Tensão de Cisalhamento"
        self.shear_stress_formula_str = r"Fórmula da Tensão de Cisalhamento"
        self.shear_stress_var = r"T_{cisalhamento} ="

    def translateEN(self):
        self.title = r"Seção Transversal"
        self.step_split = r"Subdividir a geometria da seção transversal em formas geométricas (subáreas) de " \
                          r"propriedades conhecidas"
        self.figure_label = r"\label{fig:estrutura} Estrutura com subáreas contornadas de preto"
        self.step_static_moment = r"Calcular os momentos estáticos em relação ao eixo de interesse"
        self.centroid = r"Centroide da semi-circunferência:"
        self.step_static_moment_x = r"Cálculo do momento estático em relação ao eixo X:"
        self.msx_operation = r"Ms_x = Área_{(subárea)} \cdot \overline{Y} \\"
        self.step_static_moment_y = r"Cálculo do momento estático em relação ao eixo Y:"
        self.msy_operation = r"Ms_y = Area_{(subárea)} \cdot \overline{X} \\"
        self.step_centroid = r"Calcular os centroides em relação ao eixo de interesse"
        self.centroid_x = r"Cálculo do centroide em relação ao eixo X:"
        self.centroid_y = r"Cálculo do centroide em relação ao eixo Y:"
        self.step_moment_inertia = r"Calcular os momentos de inércia em relação aos eixos de interesse"
        self.moment_inertia_tip = r"Quando necessário (ou, na dúvida, sempre), aplicar o teorema dos eixos paralelos \\"
        self.theorem_formula = r"Teorema dos eixos paralelos: I' = I + A * d² \\"
        self.moment_inertia_x = r"Cálculo do Momento de Inércia em relação a X:"
        self.moment_inertia_x_rect_formula = r"I_{x_{(retângulos)}} = \frac{base \cdot altura^3}{12}"
        self.moment_inertia_x_circ_formula = r"I_{x_{(semi-circunferência)}} = \frac{\pi \cdot raio^4}{8}"
        self.moment_inertia_y = r"Cálculo do Momento de Inércia em relação a Y:"
        self.moment_inertia_y_rect_formula = r"I_{y_{(retângulos)}} = \frac{base^3 \cdot altura}{12}"
        self.moment_inertia_y_circ_formula = r"I_{y_{(semi-circunferência)}} = \frac{\pi \cdot raio^4}{8}"
        self.step_normal_stress_neutral_line = r"Calcular a Tensão Normal e Linha Neutra"
        self.normal_stress_formula = r"Fórmula da Tensão Normal"
        self.neutral_line_formula = r"Fórmula da Linha Neutra"
        self.neutral_line_tip = r"A linha neutra se encontra onde a Tensão Normal é 0, portanto para encontrar" \
                                r" a posição da linha neutra (y) substituímos T por 0."
        self.calculating_for = r"Cálculo para"
        self.normal_stress_var = r"T_{normal} ="
        self.step_normal_stress = r"Cálculo da Tensão Normal"
        self.step_neutral_line = r"Cálculo da Linha Neutra"
        self.step_static_moment_cut = r"Calcular o Momento Estático no corte"
        self.static_moment_cut_formula_above_str = r"Fórmula do Momento Estático para corte sobre a subárea"
        self.static_moment_cut_formula_above = r"M_{estático_{corte}} = Área_{subárea} \cdot (centroide_{subárea} - " \
                                               r"centroide_{figura}) "
        self.static_moment_cut_formula_not_above_str = r"Fórmula do Momento Estático para corte acima ou abaixo da " \
                                                       r"subárea"
        self.static_moment_cut_formula_not_above = r"M_{estático_{corte}} = (\frac{altura}{2} + centroide_{subárea}" \
                                                   r"- corte_y) \cdot base \cdot ((\frac{altura}{2} + centroide_{" \
                                                   r"subárea} - corte_y) \cdot 0.5 + corte_y - centroide_{figura}) "
        self.static_moment_var = r"M_{estático_{corte}} ="
        self.step_shear_flux = r"Calcular o Fluxo de Cisalhamento"
        self.shear_flux_formula = r"Fórmula do Fluxo de Cisalhamento"
        self.shear_flux_var = r"f_{cisalhamento} ="
        self.step_shear_stress = r"Calcular a Tensão de Cisalhamento"
        self.shear_stress_formula_str = r"Fórmula da Tensão de Cisalhamento"
        self.shear_stress_var = r"T_{cisalhamento} ="
