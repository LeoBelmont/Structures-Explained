class translate_PDF_Mohr:
    def __init__(self, language):
        if language == "PT":
            self.translatePT()
        elif language == "EN":
            self.translateEN()

    def translatePT(self):
        self.title_2d = r"Resolução do Estado Duplo de Tensões"
        self.radius_and_max_shear = r"Calculo do raio ou tensão de cisalhamento máxima"
        self.radius_and_max_shear_formula = r"Fórmula do raio/tensão de cisalhamento máxima"
        self.radius_and_max_shear_solving = r"Realizando a conta"
        self.main_stress_calculation = r"Calculo das tensões principais"
        self.main_stress_formula = r"Fórmula para cálculo das tensões principais"
        self.sigma_1_solving = r"Calculo de sigma 1"
        self.sigma_2_solving = r"Calculo de sigma 2"
        self.center_solving = r"Calculo do centro"
        self.center_formula = r"Fórmula do centro"
        self.center = r"centro"
        self.angle_solving = 'rCalculo do ângulo'
        self.angle_formula = r'Fórmula do ângulo'
        self.doing_math = r'Realizando a conta'
        self.angle_tip = r'Deve-se dividir o ângulo encontrado no círculo de Mohr por 2 para encontrar o ângulo' \
                         r' real, portanto:'
        self.drawing_circle_2d = r'Desenhando o estado de tensões e círculo de Mohr'
        self.circle_label = r'\label{fig:estrutura} Estado Plano de Tensões e círculo de Mohr'
        self.title_3d = r"Estado Triplo de Tensões"
        self.formula_for_math = r"Fórmulas para os cálculos"
        self.main_stress_tip = r"O cálculo das tensões principais pode ser realizado por meio do cálculo dos" \
                               r" autovalores da matriz de tensões do elemento, como mostrado na equação 1."
        self.max_shear_formula = r"Fórmula para cálculo da tensão de cisalhamento máxima"
        self.max_shear_tip_head = r"O cáculo da tensão máxima de cisalhamento pode ser realizado por meio da" \
                                  r" análise geométrica do círculo de Mohr. Dado que:"
        self.max_shear_tip_body_1 = r"\item{A distância vertical da tensão máxima de cisalhamento até a origem é" \
                                    r" sempre igual ao raio do círculo de Mohr};"
        self.max_shear_tip_body_2 = r"\item{$\sigma_1$ e $\sigma_3$ são diametralmente opostos, ou seja, $\sigma_1$" \
                                    r" - $\sigma_3$ = 2 $\cdot$ raio}."
        self.calculation = r"Cálculo"
        self.matrix_subs = r"Substituindo na matriz"
        self.determinant_calculation = r"Calculo da determinante"
        self.subs_3_in_1 = r"Substituindo a equação 3 na equação 1, temos:"
        self.results = r"Resultados"
        self.main_stress = r'Tensões Principais'
        self.main_stress_roots_tip = r"Encontrando as raízes da equação 4 descobrimos as tensões principais, lembrando" \
                                r" que $\sigma_1$ é sempre a maior tensão principal (o maior autovalor)" \
                                r" $\sigma_3$ é sempre a menor tensão principal (o menor autovalor):"
        self.max_shear = r"Tensão de Cisalhamento Máxima"
        self.subs_1_in_3 = r'Substituindo $\sigma_1$ e $\sigma_3$ na equação 2 obtemos $\tau_{max}$:'
        self.drawing_circle_3d = r"Desenhando o círculo de Mohr"
        self.drawing_circle_3d_label = r'\label{fig:estrutura} Estado Triplo de Tensões e círculo de Mohr'
        self.radius_var = r"T_{max} ="

    def translateEN(self):
        self.title_2d = r"Estado Duplo de Tensões"
        self.radius_and_max_shear = r"Calculo do raio ou tensão de cisalhamento máxima"
        self.radius_and_max_shear_formula = r"Fórmula do raio/tensão de cisalhamento máxima"
        self.radius_and_max_shear_solving = r"Realizando a conta"
        self.main_stress_calculation = r"Calculo das tensões principais"
        self.main_stress_formula = r"Fórmula para cálculo das tensões principais"
        self.sigma_1_solving = r"Calculo de sigma 1"
        self.sigma_2_solving = r"Calculo de sigma 2"
        self.center_solving = r"Calculo do centro"
        self.center_formula = r"Fórmula do centro"
        self.center = r"centro"
        self.angle_solving = 'rCalculo do ângulo'
        self.angle_formula = r'Fórmula do ângulo'
        self.doing_math = r'Realizando a conta'
        self.angle_tip = r'Deve-se dividir o ângulo encontrado no círculo de Mohr por 2 para encontrar o ângulo real, portanto:'
        self.drawing_circle_2d = r'Desenhando o estado de tensões e círculo de Mohr'
        self.circle_label = r'\label{fig:estrutura} Estado Plano de Tensões e círculo de Mohr'
        self.title_3d = r"Estado Triplo de Tensões"
        self.formula_for_math = r"Fórmulas para os cálculos"
        self.main_stress_tip = r"O cálculo das tensões principais pode ser realizado por meio do cálculo dos autovalores da " \
                          r"matriz de tensões do elemento, como mostrado na equação 1."
        self.max_shear_formula = r"Fórmula para cálculo da tensão de cisalhamento máxima"
        self.max_shear_tip_head = r"O cáculo da tensão máxima de cisalhamento pode ser realizado por meio da análise geométrica do " \
                             r"círculo de Mohr. Dado que:"
        self.max_shear_tip_body_1 = r"\item{A distância vertical da tensão máxima de cisalhamento até a origem é sempre igual" \
                               r" ao raio do círculo de Mohr};"
        self.max_shear_tip_body_2 = r"\item{$\sigma_1$ e $\sigma_3$ são diametralmente opostos, ou seja, $\sigma_1$ - $\sigma_3$ = 2 $\cdot$ raio}."
        self.calculation = r"Cálculo"
        self.matrix_subs = r"Substituindo na matriz"
        self.determinant_calculation = r"Calculo da determinante"
        self.subs_3_in_1 = r"Substituindo a equação 3 na equação 1, temos:"
        self.results = r"Resultados"
        self.main_stress = r'Tensões Principais'
        self.main_stress_roots_tip = r"Encontrando as raízes da equação 4 descobrimos as tensões principais, lembrando" \
                                r" que $\sigma_1$ é sempre a maior tensão principal (o maior autovalor)" \
                                r" $\sigma_3$ é sempre a menor tensão principal (o menor autovalor):"
        self.max_shear = r"Tensão de Cisalhamento Máxima"
        self.subs_1_in_3 = r'Substituindo $\sigma_1$ e $\sigma_3$ na equação 2 obtemos $\tau_{max}$:'
        self.drawing_circle_3d = r"Desenhando o círculo de Mohr"
        self.drawing_circle_3d_label = r'\label{fig:estrutura} Estado Triplo de Tensões e círculo de Mohr'
        self.radius_var = r"T_{max} ="
