class translate_PDF_structure:
    def __init__(self, language):
        if language == "PT":
            self.translatePT()
        elif language == "EN":
            self.translateEN()

    def translatePT(self):
        self.title = r"Resolução da Estrutura"
        self.step_figure_image = r"Imagem da Estrutura"
        self.step_figure_image_label = r"\label{fig:estrutura} Imagem da estrutura com apoios e carregamentos"
        self.step_free_body_diagram_0 = r"Fazendo o diagrama de corpo livre"
        self.free_body_diagram_0_label = r"\label{fig:corpolivre} Diagrama de corpo livre"
        self.step_supports_reaction = r"Calculando a reação dos apoios"
        self.step_supports_fixed = r"Realizando cálculo do momento no engaste"
        self.fixed_EFY = r"Fazendo a somatória das forças em Y para obter a reação em Y no engaste"
        self.fixed_EFX = r"Fazendo a somatória das forças em X para obter a reação em X no engaste"
        self.fixed_moment = r"Realizando cálculo do momento no apoio fixo"
        self.step_free_body_diagram_1 = r"Refazendo o diagrama de corpo livre"
        self.free_body_diagram_1_label = r"\label{fig:corpolivre} Diagrama de corpo livre"
        self.hinged_EFY = r"Fazendo a somatória das forças em Y para obter a reação em Y no apoio fixo"
        self.hinged_EFX = r"Fazendo a somatória das forças em X para obter a reação em X no apoio fixo"
        self.step_drawing_reactions = r"Desenhando as reações dos apoios"
        self.drawing_reactions_label = r"\label{fig:apoios} Reações dos apoios"
        self.step_internal_stress = r"Calculando os esforços internos"
        self.bending_moment_tip = r"A partir da integral da força cortante, é obtido o momento fletor."
        self.constant_tip = r"A constante de integração será o momento no nó final da seção anterior."
        self.sin = r"sen"
        self.cos = r"cos"
        self.step_cutting_section = r"Cortando na Seção"
        self.step_cutting_section_label_1 = r"\label{fig:secoes}"
        self.step_cutting_section_label_2 = r"\label{fig:secoes}"
        self.step_normal_stress = r"Força Normal"
        self.step_shear_stress = r"Força Cortante"
        self.step_bending_stress = r"Momento Fletor"
        self.constant_at = r"Constante no nó"
        self.no_moment_at_1 = r"Não há momento no nó"
        self.no_moment_at_2 = r"portanto c = 0"
        self.step_internal_diagrams = r"Desenhando os diagramas de esforços internos"
        self.step_internal_diagrams_normal = r"Desenhando o diagrama da força normal:"
        self.internal_diagrams_normal_label = r"\label{fig:normais} Força normal"
        self.step_internal_diagrams_shear = r"Desenhando o diagrama da força cortante:"
        self.internal_diagrams_shear_label = r"\label{fig:cortante} Força cortante"
        self.step_internal_diagrams_moment = r"Desenhando o diagrama do momento fletor:"
        self.internal_diagrams_moment_label = r"\label{fig:momento} Momento Fletor"

    def translateEN(self):
        self.title = r"Resolução da Estrutura"
        self.step_figure_image = r"Imagem da Estrutura"
        self.step_figure_image_label = r"\label{fig:estrutura} Imagem da estrutura com apoios e carregamentos"
        self.step_free_body_diagram_0 = r"Fazendo o diagrama de corpo livre"
        self.free_body_diagram_0_label = r"\label{fig:corpolivre} Diagrama de corpo livre"
        self.step_supports_reaction = r"Calculando a reação dos apoios"
        self.step_supports_fixed = r"Realizando cálculo do momento no engaste"
        self.fixed_EFY = r"Fazendo a somatória das forças em Y para obter a reação em Y no engaste"
        self.fixed_EFX = r"Fazendo a somatória das forças em X para obter a reação em X no engaste"
        self.fixed_moment = r"Realizando cálculo do momento no apoio fixo"
        self.step_free_body_diagram_1 = r"Refazendo o diagrama de corpo livre"
        self.free_body_diagram_1_label = r"\label{fig:corpolivre} Diagrama de corpo livre"
        self.hinged_EFY = r"Fazendo a somatória das forças em Y para obter a reação em Y no apoio fixo"
        self.hinged_EFX = r"Fazendo a somatória das forças em X para obter a reação em X no apoio fixo"
        self.step_drawing_reactions = r"Desenhando as reações dos apoios"
        self.drawing_reactions_label = r"\label{fig:apoios} Reações dos apoios"
        self.step_internal_stress = r"Calculando os esforços internos"
        self.bending_moment_tip = r"A partir da integral da força cortante, é obtido o momento fletor."
        self.constant_tip = r"A constante de integração será o momento no nó final da seção anterior."
        self.sin = r"sen"
        self.cos = r"cos"
        self.step_cutting_section = r"Cortando na Seção"
        self.step_cutting_section_label_1 = r"\label{fig:secoes}"
        self.step_cutting_section_label_2 = r"\label{fig:secoes}"
        self.step_normal_stress = r"Força Normal"
        self.step_shear_stress = r"Força Cortante"
        self.step_bending_stress = r"Momento Fletor"
        self.constant_at = r"Constante no nó"
        self.no_moment_at_1 = r"Não há momento no nó"
        self.no_moment_at_2 = r"portanto c = 0"
        self.step_internal_diagrams = r"Desenhando os diagramas de esforços internos"
        self.step_internal_diagrams_normal = r"Desenhando o diagrama da força normal:"
        self.internal_diagrams_normal_label = r"\label{fig:normais} Força normal"
        self.step_internal_diagrams_shear = r"Desenhando o diagrama da força cortante:"
        self.internal_diagrams_shear_label = r"\label{fig:cortante} Força cortante"
        self.step_internal_diagrams_moment = r"Desenhando o diagrama do momento fletor:"
        self.internal_diagrams_moment_label = r"\label{fig:momento} Momento Fletor"