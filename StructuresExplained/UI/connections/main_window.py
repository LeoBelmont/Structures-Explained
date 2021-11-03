import os
import inspect
import locale
import platform
import ctypes
import webbrowser
import pickle
import qdarkstyle
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

# SX files
from StructuresExplained.solutions import settings
from StructuresExplained.UI import resources
from StructuresExplained.UI import loadingPrompt, loadFilePrompt
from StructuresExplained.UI.connections.structure import connections as st_connections
from StructuresExplained.UI.connections.cross_section import connections as cs_connections
from StructuresExplained.UI.connections.stress_states import connections as ss_connections

import matplotlib

matplotlib.use("Qt5Agg")


class connections:
    def __init__(self, main_window, tenshi, app):
        self.mw = main_window
        self.tenshi = tenshi
        self.app = app

    def configUI(self):
        if platform.system() == "Windows":
            if "pt" in locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()]:
                self.retranslateUi()
            else:
                self.retranslateUiEN()
        else:
            if "pt" in os.getenv('LANG'):
                self.mw.retranslateUi()
            else:
                self.mw.retranslateUiEN()

        self.tenshi.setWindowIcon(QtGui.QIcon(r':/Figures/LogoSX.ico'))
        self.tenshi.setWindowTitle("Structures Explained")
        self.disable_unfinished()
        self.dark_theme()

        self.mw.beam_x1.setValidator(QtGui.QDoubleValidator())
        self.mw.beam_y1.setValidator(QtGui.QDoubleValidator())
        self.mw.beam_x2.setValidator(QtGui.QDoubleValidator())
        self.mw.beam_y2.setValidator(QtGui.QDoubleValidator())
        self.mw.beam_E.setValidator(QtGui.QDoubleValidator())
        self.mw.beam_A.setValidator(QtGui.QDoubleValidator())
        self.mw.beam_I.setValidator(QtGui.QDoubleValidator())
        self.mw.node_x.setValidator(QtGui.QDoubleValidator())
        self.mw.node_y.setValidator(QtGui.QDoubleValidator())
        self.mw.node_id.setValidator(QtGui.QIntValidator(1, 100))
        self.mw.support_pos.setValidator(QtGui.QIntValidator(1, 100))
        self.mw.support_angle.setValidator(QtGui.QDoubleValidator())
        self.mw.spring_k.setValidator(QtGui.QDoubleValidator())
        self.mw.spring_translation.setValidator(QtGui.QRegExpValidator())
        self.mw.load_pos.setValidator(QtGui.QIntValidator(1, 100))
        self.mw.load_y.setValidator(QtGui.QDoubleValidator())
        self.mw.load_x.setValidator(QtGui.QDoubleValidator())
        self.mw.load_angle.setValidator(QtGui.QDoubleValidator())
        self.mw.load_moment.setValidator(QtGui.QDoubleValidator())
        self.mw.qload_pos.setValidator(QtGui.QIntValidator(1, 100))
        self.mw.qload_initial.setValidator(QtGui.QDoubleValidator())
        self.mw.qload_final.setValidator(QtGui.QDoubleValidator())
        self.mw.rect_x1.setValidator(QtGui.QDoubleValidator())
        self.mw.rect_y1.setValidator(QtGui.QDoubleValidator())
        self.mw.rect_x2.setValidator(QtGui.QDoubleValidator())
        self.mw.rect_y2.setValidator(QtGui.QDoubleValidator())
        self.mw.msx.setValidator(QtGui.QDoubleValidator())
        self.mw.msy.setValidator(QtGui.QDoubleValidator())
        self.mw.mix.setValidator(QtGui.QDoubleValidator())
        self.mw.miy.setValidator(QtGui.QDoubleValidator())
        self.mw.at.setValidator(QtGui.QDoubleValidator())
        self.mw.tnormal.setValidator(QtGui.QDoubleValidator())
        self.mw.tmy.setValidator(QtGui.QDoubleValidator())
        self.mw.tmz.setValidator(QtGui.QDoubleValidator())
        self.mw.cs_y.setValidator(QtGui.QDoubleValidator())
        self.mw.cs_z.setValidator(QtGui.QDoubleValidator())
        self.mw.cut_y.setValidator(QtGui.QDoubleValidator())
        self.mw.tshear.setValidator(QtGui.QDoubleValidator())
        self.mw.tcontact.setValidator(QtGui.QDoubleValidator())
        self.mw.twidth.setValidator(QtGui.QDoubleValidator())
        self.mw.tfos.setValidator(QtGui.QDoubleValidator())
        self.mw.sx.setValidator(QtGui.QDoubleValidator())
        self.mw.sy.setValidator(QtGui.QDoubleValidator())
        self.mw.sz.setValidator(QtGui.QDoubleValidator())
        self.mw.txy.setValidator(QtGui.QDoubleValidator())
        self.mw.txz.setValidator(QtGui.QDoubleValidator())
        self.mw.tyz.setValidator(QtGui.QDoubleValidator())

        self.connect_ui()
        # self.connect_structure()
        self.connect_cross_section()
        self.connect_stress_states()

        # self.mw.blankss = pickle.dumps(self.mw.ss)
        # self.mw.blanksig = pickle.dumps(self.mw.sig)

        # speech recognition (unfinished)
        # sr.SetupUISecretary(self)

        self.doStartUpStuff()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.mw.language = "PT"
        self.tenshi.setWindowTitle(_translate("tenshi", "Solid Mechanics Solver"))
        self.mw.toolButton_4.setToolTip(_translate("tenshi", "Adicionar apoios"))
        self.mw.toolButton.setToolTip(_translate("tenshi", "Adicionar elemento de estrutura"))
        self.mw.toolButton_3.setToolTip(_translate("tenshi", "Adicionar nó"))
        self.mw.show_structure.setToolTip(_translate("tenshi", "Visualizar estrutura"))
        self.mw.show_structure.setText(_translate("tenshi", "Estrutura"))
        self.mw.show_normal.setToolTip(_translate("tenshi", "Visualizar força normal"))
        self.mw.toolButton_6.setToolTip(_translate("tenshi", "Adicionar cargas distribuídas"))
        self.mw.show_shear.setToolTip(_translate("tenshi", "Visualizar força cortante"))
        self.mw.show_displacement.setToolTip(_translate("tenshi", "Visualizar deslocamento"))
        self.mw.label.setText(_translate("tenshi", "Construir"))
        self.mw.show_supports.setToolTip(_translate("tenshi", "Visualizar reações dos apoios"))
        self.mw.show_diagram.setText(_translate("tenshi", "Diagrama \n"
                                                          "de Corpo \n"
                                                          "Livre"))
        self.mw.show_moment.setToolTip(_translate("tenshi", "Visualizar momento fletor"))
        self.mw.label_2.setText(_translate("tenshi", "Visualizar"))
        self.mw.toolButton_5.setToolTip(_translate("tenshi", "Adicionar esforços pontuais"))
        self.mw.toolBox.setItemText(self.mw.toolBox.indexOf(self.mw.page_9), _translate("tenshi", "Estrutura"))
        self.mw.toolButton_11.setText(_translate("tenshi", "Tensão de \n"
                                                           "Cisalha-\n"
                                                           "mento\n"
                                                           "e Fluxo"))
        self.mw.toolButton_8.setToolTip(_translate("tenshi", "Adicionar semicírculos"))
        self.mw.toolButton_9.setToolTip(_translate("tenshi", "Dados / Resultados"))
        self.mw.toolButton_9.setText(_translate("tenshi", "Dados \n"
                                                          "Gerais"))
        self.mw.toolButton_7.setToolTip(_translate("tenshi", "Adicionar retângulos"))
        self.mw.label_84.setText(_translate("tenshi", "Construir"))
        self.mw.label_85.setText(_translate("tenshi", "Visualizar"))
        self.mw.toolButton_2.setText(_translate("tenshi", "Tensão\n"
                                                          "Normal"))
        self.mw.show_sec.setToolTip(_translate("tenshi", "Visualizar seção transversal"))
        self.mw.label_81.setText(_translate("tenshi", "Calcular"))
        self.mw.toolBox.setItemText(self.mw.toolBox.indexOf(self.mw.page_10), _translate("tenshi", "Seção Transversal"))
        self.mw.show_mohr.setToolTip(_translate("tenshi", "Visualizar Círculo de Mohr"))
        self.mw.show_mohr.setText(_translate("tenshi", "Visualizar"))
        self.mw.toolButton_10.setToolTip(_translate("tenshi", "Círculo de Mohr"))
        self.mw.toolButton_10.setText(_translate("tenshi", "Inserir\nDados"))
        self.mw.label_82.setText(_translate("tenshi", "Construir"))
        self.mw.label_83.setText(_translate("tenshi", "Visualizar"))
        self.mw.toolBox.setItemText(self.mw.toolBox.indexOf(self.mw.page_11), _translate("tenshi", "Círculo de Mohr"))
        self.mw.label_13.setText(_translate("tenshi", "Elemento de Estrutura"))
        self.mw.label_3.setText(_translate("tenshi", "X1"))
        self.mw.label_4.setText(_translate("tenshi", "Y1"))
        self.mw.label_6.setText(_translate("tenshi", "Y2"))
        self.mw.label_5.setText(_translate("tenshi", "X2"))
        self.mw.label_7.setText(_translate("tenshi", "Coordenadas"))
        self.mw.beam_list.setItemText(0, _translate("tenshi", "Seção 1"))
        self.mw.beam_plus.setText(_translate("tenshi", "+"))
        self.mw.label_123.setText(_translate("tenshi", "m"))
        self.mw.label_124.setText(_translate("tenshi", "m"))
        self.mw.label_125.setText(_translate("tenshi", "m"))
        self.mw.label_126.setText(_translate("tenshi", "m"))
        self.mw.utilizeinfo.setText(_translate("tenshi", "Utilizar Dados do Material"))
        self.mw.label_10.setText(_translate("tenshi", "Momento de Inércia"))
        self.mw.label_14.setText(_translate("tenshi", "Tipo de Elemento"))
        self.mw.label_9.setText(_translate("tenshi", "Módulo de Elasticidade"))
        self.mw.label_11.setText(_translate("tenshi", "Área da Seção Transversal"))
        self.mw.label_114.setText(_translate("tenshi", "m²"))
        self.mw.elementtype.setItemText(0, _translate("tenshi", "Viga"))
        self.mw.elementtype.setItemText(1, _translate("tenshi", "Treliça"))
        self.mw.label_115.setText(_translate("tenshi", "GPa"))
        self.mw.label_116.setText(_translate("tenshi", "m⁴"))
        self.mw.label_8.setText(_translate("tenshi", "Dados do Material"))
        self.mw.beam_apply.setText(_translate("tenshi", "Aplicar"))
        self.mw.beam_remove.setText(_translate("tenshi", "Remover"))
        self.mw.label_42.setText(_translate("tenshi", "Nó"))
        self.mw.node_list.setItemText(0, _translate("tenshi", "Nó 1"))
        self.mw.node_plus.setText(_translate("tenshi", "+"))
        self.mw.label_29.setText(_translate("tenshi", "Coordenadas"))
        self.mw.label_30.setText(_translate("tenshi", "X"))
        self.mw.label_31.setText(_translate("tenshi", "Y"))
        self.mw.label_129.setText(_translate("tenshi", "m"))
        self.mw.label_130.setText(_translate("tenshi", "m"))
        self.mw.label_17.setText(_translate("tenshi", "Adicionar após nó:"))
        self.mw.label_43.setText(_translate("tenshi", "ID"))
        self.mw.node_apply.setText(_translate("tenshi", "Aplicar"))
        self.mw.node_remove.setText(_translate("tenshi", "Remover"))
        self.mw.label_25.setText(_translate("tenshi", "Apoios"))
        self.mw.support_list.setItemText(0, _translate("tenshi", "Apoio 1"))
        self.mw.support_plus.setText(_translate("tenshi", "+"))
        self.mw.label_27.setText(_translate("tenshi", "Ângulo"))
        self.mw.label_26.setText(_translate("tenshi", "Posição (ID)"))
        self.mw.label_73.setText(_translate("tenshi", "K"))
        self.mw.spring_k.setText(_translate("tenshi", "1"))
        self.mw.label_71.setText(_translate("tenshi", "Translação"))
        self.mw.label_127.setText(_translate("tenshi", "N/m"))
        self.mw.spring_translation.setText(_translate("tenshi", "y"))
        self.mw.label_113.setText(_translate("tenshi", "°"))
        self.mw.support_angle.setText(_translate("tenshi", "0"))
        self.mw.support_internal_hinge.setText(_translate("tenshi", "Rótula"))
        self.mw.support_roll.setText(_translate("tenshi", "Móvel"))
        self.mw.support_fixed.setText(_translate("tenshi", "Engaste"))
        self.mw.support_hinged.setText(_translate("tenshi", "Fixo"))
        self.mw.support_spring.setText(_translate("tenshi", "Mola"))
        self.mw.support_apply.setText(_translate("tenshi", "Aplicar"))
        self.mw.support_remove.setText(_translate("tenshi", "Remover"))
        self.mw.label_28.setText(_translate("tenshi", "Esforços Pontuais"))
        self.mw.load_list.setItemText(0, _translate("tenshi", "Esforço 1"))
        self.mw.load_plus.setText(_translate("tenshi", "+"))
        self.mw.label_32.setText(_translate("tenshi", "Intensidade em Y"))
        self.mw.label_36.setText(_translate("tenshi", "Posição (ID)"))
        self.mw.label_33.setText(_translate("tenshi", "Intensidade em X"))
        self.mw.load_moment.setText(_translate("tenshi", "0"))
        self.mw.load_x.setText(_translate("tenshi", "0"))
        self.mw.label_86.setText(_translate("tenshi", "N"))
        self.mw.label_89.setText(_translate("tenshi", "Nm"))
        self.mw.label_34.setText(_translate("tenshi", "Ângulo"))
        self.mw.load_angle.setText(_translate("tenshi", "0"))
        self.mw.load_y.setText(_translate("tenshi", "0"))
        self.mw.label_87.setText(_translate("tenshi", "N"))
        self.mw.label_35.setText(_translate("tenshi", "Momento"))
        self.mw.label_88.setText(_translate("tenshi", "°"))
        self.mw.load_apply.setText(_translate("tenshi", "Aplicar"))
        self.mw.load_remove.setText(_translate("tenshi", "Remover"))
        self.mw.label_37.setText(_translate("tenshi", "Cargas Distribuídas"))
        self.mw.qload_list.setItemText(0, _translate("tenshi", "Carga 1"))
        self.mw.qload_plus.setText(_translate("tenshi", "+"))
        self.mw.label_39.setText(_translate("tenshi", "Intensidade Inicial"))
        self.mw.qload_initial.setText(_translate("tenshi", "0"))
        self.mw.label_40.setText(_translate("tenshi", "Intensidade Final"))
        self.mw.label_38.setText(_translate("tenshi", "Posição (ID)"))
        self.mw.qload_final.setText(_translate("tenshi", "0"))
        self.mw.label_90.setText(_translate("tenshi", "N"))
        self.mw.label_91.setText(_translate("tenshi", "N"))
        self.mw.qload_apply.setText(_translate("tenshi", "Aplicar"))
        self.mw.qload_remove.setText(_translate("tenshi", "Remover"))
        self.mw.label_44.setText(_translate("tenshi", "Subárea Retangular"))
        self.mw.rect_list.setItemText(0, _translate("tenshi", "Ret. 1"))
        self.mw.rect_plus.setText(_translate("tenshi", "+"))
        self.mw.rect_visualize.setText(_translate("tenshi", "Destacar Subárea"))
        self.mw.label_45.setText(_translate("tenshi", "X"))
        self.mw.label_48.setText(_translate("tenshi", "Y"))
        self.mw.label_46.setText(_translate("tenshi", "Y"))
        self.mw.label_47.setText(_translate("tenshi", "X"))
        self.mw.label_131.setText(_translate("tenshi", "m"))
        self.mw.label_132.setText(_translate("tenshi", "m"))
        self.mw.label_133.setText(_translate("tenshi", "m"))
        self.mw.label_134.setText(_translate("tenshi", "m"))
        self.mw.label_51.setText(_translate("tenshi", "Abaixo na Direita"))
        self.mw.label_49.setText(_translate("tenshi", "Coordenadas dos Vértices"))
        self.mw.label_50.setText(_translate("tenshi", "Acima na Esquerda"))
        self.mw.rect_apply.setText(_translate("tenshi", "Aplicar"))
        self.mw.rect_remove.setText(_translate("tenshi", "Remover"))
        self.mw.label_52.setText(_translate("tenshi", "Subárea Circular"))
        self.mw.circle_list.setItemText(0, _translate("tenshi", "Cir. 1"))
        self.mw.circle_plus.setText(_translate("tenshi", "+"))
        self.mw.circle_visualize.setText(_translate("tenshi", "Destacar Subárea"))
        self.mw.label_56.setText(_translate("tenshi", "Raio"))
        self.mw.label_55.setText(_translate("tenshi", "Y"))
        self.mw.label_54.setText(_translate("tenshi", "X"))
        self.mw.label_57.setText(_translate("tenshi", "Ângulo Inicial"))
        self.mw.label_58.setText(_translate("tenshi", "Ângulo Final"))
        self.mw.label_135.setText(_translate("tenshi", "m"))
        self.mw.label_136.setText(_translate("tenshi", "m"))
        self.mw.label_53.setText(_translate("tenshi", "Coordenadas do Centro"))
        self.mw.label_92.setText(_translate("tenshi", "m"))
        self.mw.label_93.setText(_translate("tenshi", "°"))
        self.mw.label_94.setText(_translate("tenshi", "°"))
        self.mw.circle_apply.setText(_translate("tenshi", "Aplicar"))
        self.mw.circle_remove.setText(_translate("tenshi", "Remover"))
        self.mw.label_128.setText(_translate("tenshi",
                                             "<html><head/><body><p align=\"center\"><span style=\" color:#ff5500;\">Adicionar semicírculos impossibilitará o cálculo da tensão de cisalhamento e fluxo.</span></p></body></html>"))
        self.mw.label_61.setText(_translate("tenshi", "Momento Estático em Y (Origem)"))
        self.mw.label_62.setText(_translate("tenshi", "Momento de Inércia em Z (CG)"))
        self.mw.label_63.setText(_translate("tenshi", "Momento de Inércia em Y (CG)"))
        self.mw.label_64.setText(_translate("tenshi", "Área Total"))
        self.mw.label_95.setText(_translate("tenshi", "m²"))
        self.mw.label_98.setText(_translate("tenshi", "m³"))
        self.mw.label_60.setText(_translate("tenshi", "Momento Estático em Z (Origem)"))
        self.mw.label_96.setText(_translate("tenshi", "m⁴"))
        self.mw.label_97.setText(_translate("tenshi", "m⁴"))
        self.mw.label_99.setText(_translate("tenshi", "m³"))
        self.mw.label_59.setText(_translate("tenshi", "Dados/Resultados"))
        self.mw.figureResultsButton.setText(_translate("tenshi", "Utilizar Resultados da Figura"))
        self.mw.insertDataButton.setText(_translate("tenshi", "Inserir Dados"))
        self.mw.label_66.setText(_translate("tenshi", "Tensão Normal"))
        self.mw.label_69.setText(_translate("tenshi", "Momento em Z"))
        self.mw.specify_y.setText(_translate("tenshi", "Especificar Y"))
        self.mw.specify_z.setText(_translate("tenshi", "Especificar Z"))
        self.mw.label_68.setText(_translate("tenshi", "Momento em Y"))
        self.mw.label_67.setText(_translate("tenshi", "Força Normal"))
        self.mw.label_100.setText(_translate("tenshi", "N"))
        self.mw.label_101.setText(_translate("tenshi", "Nm"))
        self.mw.label_102.setText(_translate("tenshi", "Nm"))
        self.mw.label_103.setText(_translate("tenshi", "m"))
        self.mw.label_104.setText(_translate("tenshi", "m"))
        self.mw.label_105.setText(_translate("tenshi", "Pa"))
        # self.mw.label_106.setText(_translate("tenshi", "m")) unidade linha neutra
        self.mw.label_70.setText(_translate("tenshi", "Tensão Normal:"))
        self.mw.label_72.setText(_translate("tenshi", "Linha Neutra:"))
        self.mw.tncalculate.setText(_translate("tenshi", "Calcular"))
        self.mw.checkBox.setText(_translate("tenshi", "Adicionar à resolução"))
        self.mw.label_74.setText(_translate("tenshi", "Tensão de Cisalhamento e Fluxo"))
        self.mw.tfosbox.setItemText(0, _translate("tenshi", "Força"))
        self.mw.tfosbox.setItemText(1, _translate("tenshi", "Espaçamento"))
        self.mw.label_75.setText(_translate("tenshi", "Força Cortante"))
        self.mw.label_41.setText(_translate("tenshi", "Altura do Corte"))
        self.mw.label_77.setText(_translate("tenshi", "Espessura (t)"))
        self.mw.label_76.setText(_translate("tenshi", "Áreas de Contato"))
        self.mw.label_107.setText(_translate("tenshi", "N"))
        self.mw.label_108.setText(_translate("tenshi", "m"))
        self.mw.label_109.setText(_translate("tenshi", "m"))
        self.mw.checkBox_2.setText(_translate("tenshi", "Adicionar à resolução"))
        self.mw.label_65.setText(_translate("tenshi", "Q:"))
        self.mw.label_78.setText(_translate("tenshi", "Tensão de Cisalhamento:"))
        self.mw.label_80.setText(_translate("tenshi", "Fluxo de Cisalhamento:"))
        self.mw.label_110.setText(_translate("tenshi", "m³"))
        self.mw.label_111.setText(_translate("tenshi", "Pa"))
        self.mw.label_112.setText(_translate("tenshi", "N/m"))
        self.mw.tscalculate.setText(_translate("tenshi", "Calcular"))
        self.mw.label_12.setText(_translate("tenshi", "Círculo de Mohr"))
        self.mw.radio_plane.setText(_translate("tenshi", "Estado Plano"))
        self.mw.radio_triple.setText(_translate("tenshi", "Estado Triplo"))
        self.mw.label_18.setText(_translate("tenshi", "τxy"))
        self.mw.label_15.setText(_translate("tenshi", "σx"))
        self.mw.label_21.setText(_translate("tenshi", "τyz"))
        self.mw.label_20.setText(_translate("tenshi", "τxz"))
        self.mw.label_19.setText(_translate("tenshi", "σz"))
        self.mw.label_16.setText(_translate("tenshi", "σy"))
        self.mw.label_117.setText(_translate("tenshi", "Pa"))
        self.mw.label_118.setText(_translate("tenshi", "Pa"))
        self.mw.label_119.setText(_translate("tenshi", "Pa"))
        self.mw.label_120.setText(_translate("tenshi", "Pa"))
        self.mw.label_121.setText(_translate("tenshi", "Pa"))
        self.mw.label_122.setText(_translate("tenshi", "Pa"))
        self.mw.mohr_apply.setText(_translate("tenshi", "Aplicar"))
        self.mw.label_22.setText(_translate("tenshi", "Precisão do Mouse (Decimais)"))
        self.mw.int_plot.setText(_translate("tenshi", "Gráfico Interativo"))
        self.mw.gridBox.setText(_translate("tenshi", "Grid"))

        self.mw.label_23.setText(_translate("tenshi", "X"))
        self.mw.label_24.setText(_translate("tenshi", "Y"))
        self.mw.menuOp_es.setTitle(_translate("tenshi", "Opções"))
        self.mw.menuResetar.setTitle(_translate("tenshi", "Resetar..."))
        self.mw.menuSe_o_Transversal.setTitle(_translate("tenshi", "Seção Transversal"))
        self.mw.menuEstrutura.setTitle(_translate("tenshi", "Estrutura"))
        self.mw.menuFonte.setTitle(_translate("tenshi", "Fonte..."))
        self.mw.translate_menu.setTitle(_translate("tenshi", "Traduzir..."))
        self.mw.menuMudar_Temas.setTitle(_translate("tenshi", "Mudar Temas"))
        self.mw.menuComo_utilizar.setTitle(_translate("tenshi", "Como utilizar"))
        self.mw.menuSalvar_e_Carregar.setTitle(_translate("tenshi", "Salvar e Carregar"))
        self.mw.menuGerar_Explica_es.setTitle(_translate("tenshi", "Gerar Resoluções"))
        self.mw.save.setText(_translate("tenshi", "Salvar Tudo"))
        self.mw.load_button.setText(_translate("tenshi", "Carregar"))
        self.mw.solvestatic.setText(_translate("tenshi", "Estrutura"))
        self.mw.solveresist.setText(_translate("tenshi", "Seção Transversal"))
        self.mw.resetloads.setText(_translate("tenshi", "Esforços"))
        self.mw.resetall.setText(_translate("tenshi", "Tudo"))
        self.mw.undo.setText(_translate("tenshi", "Ação Anterior"))
        self.mw.undo.setShortcut(_translate("tenshi", "Ctrl+Z"))
        self.mw.fontstructure.setText(_translate("tenshi", "Estrutura"))
        self.mw.fontequations.setText(_translate("tenshi", "Equações"))
        self.mw.translate_pt.setText(_translate("tenshi", "Português"))
        self.mw.translate_en.setText(_translate("tenshi", "English"))
        self.mw.translate_nihongo.setText(_translate("tenshi", "日本語"))
        self.mw.font_interface.setText(_translate("tenshi", "Interface"))
        self.mw.action.setText(_translate("tenshi", "Carregar Seção Transversal"))
        self.mw.load_mohr.setText(_translate("tenshi", "Carregar Círculo de Mohr"))
        self.mw.solvermohr.setText(_translate("tenshi", "Círculo de Mohr"))
        self.mw.light_theme_button.setText(_translate("tenshi", "Tema Claro"))
        self.mw.dark_theme_button.setText(_translate("tenshi", "Tema Escuro"))
        self.mw.aboutButton.setText(_translate("tenshi", "Sobre"))
        self.mw.showManualButton.setText(_translate("tenshi", "Mostrar Manual (requer Internet)"))
        self.mw.hideManualButton.setText(_translate("tenshi", "Esconder Manual"))
        self.mw.actionP_gina_para_Download.setText(_translate("tenshi", "Baixar Manual e Exemplos"))
        self.mw.downloadPageButton.setText(_translate("tenshi", "Baixar Manual e Exemplos"))
        self.mw.reset_cross_section.setText(_translate("tenshi", "Tudo"))
        self.mw.fullscreenButton.setText(_translate("tenshi", "Alternar Modo Tela Cheia"))

        self.mw.load_structure_str = "Carregar Arquivo"
        self.mw.strucutre_type_str = "Estrutura(*.pkl)"
        self.mw.save_strucutre_text = "Estrutura"
        self.mw.save_strucutre_title = "Salvar Estrutura"
        self.mw.static_warning_str = "Apenas disponível para estruturas estáticas " \
                                     "(que contenham um apoio móvel e um apoio fixo ou um engaste apenas)."
        self.mw.warning_str = "É necessário mais informações"
        self.mw.warning_title = "Erro"
        self.mw.qload_warning = "Os valores inicial e final precisam ter o mesmo sinal"
        self.mw.id_warning_str = "ID inválido. Esse ID não existe."
        self.mw.geometry_change_title = "Aviso"
        self.mw.geometry_change_warning = "Se fizer alterações à geometria, os cálculos adicionados à resolução previamente serão perdidos. Fazer alterações?"
        self.mw.pdf_generated_title = "Pronto!"
        self.mw.pdf_generated_str = "PDF gerado com succeso"
        self.mw.shear_warning_title = "Indisponível"
        self.mw.shear_warning_str = "Seções transversal não foi desenhada, contém setores circulares ou os resultados não foram obtidos da figura."
        self.mw.latex_error_str = "É necessário ter o Miktex instalado para gerar a resolução."
        self.mw.packages_error_str = "Algo deu errado. É provavel que você não tenha os pacotes do Latex instalados."
        self.mw.font_size_str = "Tamanho da Fonte"
        self.mw.font_strucuture_str = "Fonte da Estrutura:"
        self.mw.font_equations_str = "Fonte das Equações:"
        self.mw.rect_values_error = "Valores inválidos. Provavelmente valores foram invertidos."
        self.mw.pdf_title = "Gerar resolução"
        self.mw.pdf_text = "Resolução"
        self.mw.close_title = "Sair sem Salvar?"
        self.mw.close_text = "Tem certeza que deseja sair? É possível que haja estruturas não salvas."
        self.mw.howtouse_title = "Como Utilizar"
        self.mw.howtouse_text = ("Manual de utilização: link aqui\n"
                                 "Exemplos de utilização: link aqui")
        self.mw.about_title = "Sobre"
        self.mw.about_text = ("Desenvolvido como trabalho de Iniciação Científica na EESC-USP em 2020.\n"
                              "\n"
                              "Desenvolvido por Leonardo de Souza Bornia\n"
                              "\n"
                              "Agradecimentos:\n"
                              "Eng. Me. Henrique Borges Garcia\n"
                              "Prof. Me. Gustavo Lahr\n"
                              "Prof. Dr. Glauco Augusto de Paula Caurin\n"
                              "Fundação de Apoio à Física e à Química\n")

    def retranslateUiEN(self):
        _translate = QtCore.QCoreApplication.translate
        self.mw.language = "EN"
        self.tenshi.setWindowTitle(_translate("tenshi", "Solid Mechanics Solver"))
        self.mw.toolButton_4.setToolTip(_translate("tenshi", "Add supports"))
        self.mw.toolButton.setToolTip(_translate("tenshi", "Add structure element"))
        self.mw.toolButton_3.setToolTip(_translate("tenshi", "Add node"))
        self.mw.show_structure.setToolTip(_translate("tenshi", "Visualize structure"))
        self.mw.show_structure.setText(_translate("tenshi", "Structure"))
        self.mw.show_normal.setToolTip(_translate("tenshi", "Visualize normal force"))
        self.mw.toolButton_6.setToolTip(_translate("tenshi", "Add distributed loads"))
        self.mw.show_shear.setToolTip(_translate("tenshi", "Visualize shear force"))
        self.mw.show_displacement.setToolTip(_translate("tenshi", "Visualize displacement"))
        self.mw.label.setText(_translate("tenshi", "Build"))
        self.mw.show_supports.setToolTip(_translate("tenshi", "Visualize support reactions"))
        self.mw.show_diagram.setText(_translate("tenshi", "Free \n"
                                                          "Body \n"
                                                          "Diagram"))
        self.mw.show_moment.setToolTip(_translate("tenshi", "Visualize bending moment"))
        self.mw.label_2.setText(_translate("tenshi", "Visualize"))
        self.mw.toolButton_5.setToolTip(_translate("tenshi", "Add point loads"))
        self.mw.toolBox.setItemText(self.mw.toolBox.indexOf(self.mw.page_9), _translate("tenshi", "Structure"))
        self.mw.toolButton_11.setText(_translate("tenshi", "Shear\n"
                                                           "Stress\n"
                                                           "and\n"
                                                           "Flow"))
        self.mw.toolButton_8.setToolTip(_translate("tenshi", "Add circular sectors"))
        self.mw.toolButton_9.setToolTip(_translate("tenshi", "Data / Results"))
        self.mw.toolButton_9.setText(_translate("tenshi", "General \n"
                                                          "Data"))
        self.mw.toolButton_7.setToolTip(_translate("tenshi", "Add rectangles"))
        self.mw.label_84.setText(_translate("tenshi", "Build"))
        self.mw.label_85.setText(_translate("tenshi", "Visualize"))
        self.mw.toolButton_2.setText(_translate("tenshi", "Normal\n"
                                                          "Stress"))
        self.mw.show_sec.setToolTip(_translate("tenshi", "Visualize cross sections"))
        self.mw.label_81.setText(_translate("tenshi", "Calculate"))
        self.mw.toolBox.setItemText(self.mw.toolBox.indexOf(self.mw.page_10), _translate("tenshi", "Cross Section"))
        self.mw.show_mohr.setToolTip(_translate("tenshi", "Visualize Mohr's Circle"))
        self.mw.show_mohr.setText(_translate("tenshi", "Visualize"))
        self.mw.toolButton_10.setToolTip(_translate("tenshi", "Mohr's Circle"))
        self.mw.toolButton_10.setText(_translate("tenshi", "Build"))
        self.mw.label_82.setText(_translate("tenshi", "Build"))
        self.mw.label_83.setText(_translate("tenshi", "Visualize"))
        self.mw.toolBox.setItemText(self.mw.toolBox.indexOf(self.mw.page_11), _translate("tenshi", "Mohr's Circle"))
        self.mw.label_13.setText(_translate("tenshi", "Structure Element"))
        self.mw.label_3.setText(_translate("tenshi", "X1"))
        self.mw.label_4.setText(_translate("tenshi", "Y1"))
        self.mw.label_6.setText(_translate("tenshi", "Y2"))
        self.mw.label_5.setText(_translate("tenshi", "X2"))
        self.mw.label_7.setText(_translate("tenshi", "Coordinates"))
        self.mw.beam_list.setItemText(0, _translate("tenshi", "Section 1"))
        self.mw.beam_plus.setText(_translate("tenshi", "+"))
        self.mw.label_123.setText(_translate("tenshi", "m"))
        self.mw.label_124.setText(_translate("tenshi", "m"))
        self.mw.label_125.setText(_translate("tenshi", "m"))
        self.mw.label_126.setText(_translate("tenshi", "m"))
        self.mw.utilizeinfo.setText(_translate("tenshi", "Specify Material"))
        self.mw.label_10.setText(_translate("tenshi", "Moment of Inertia"))
        self.mw.label_14.setText(_translate("tenshi", "Element Type"))
        self.mw.label_9.setText(_translate("tenshi", "Modulus of Elasticity"))
        self.mw.label_11.setText(_translate("tenshi", "Cross Section Area"))
        self.mw.label_114.setText(_translate("tenshi", "m²"))
        self.mw.elementtype.setItemText(0, _translate("tenshi", "Beam"))
        self.mw.elementtype.setItemText(1, _translate("tenshi", "Truss"))
        self.mw.label_115.setText(_translate("tenshi", "GPa"))
        self.mw.label_116.setText(_translate("tenshi", "m⁴"))
        self.mw.label_8.setText(_translate("tenshi", "Material Information"))
        self.mw.beam_apply.setText(_translate("tenshi", "Apply"))
        self.mw.beam_remove.setText(_translate("tenshi", "Remove"))
        self.mw.label_42.setText(_translate("tenshi", "Node"))
        self.mw.node_list.setItemText(0, _translate("tenshi", "Node 1"))
        self.mw.node_plus.setText(_translate("tenshi", "+"))
        self.mw.label_29.setText(_translate("tenshi", "Coordinates"))
        self.mw.label_30.setText(_translate("tenshi", "X"))
        self.mw.label_31.setText(_translate("tenshi", "Y"))
        self.mw.label_129.setText(_translate("tenshi", "m"))
        self.mw.label_130.setText(_translate("tenshi", "m"))
        self.mw.label_17.setText(_translate("tenshi", "Add after node:"))
        self.mw.label_43.setText(_translate("tenshi", "ID"))
        self.mw.node_apply.setText(_translate("tenshi", "Apply"))
        self.mw.node_remove.setText(_translate("tenshi", "Remove"))
        self.mw.label_25.setText(_translate("tenshi", "Supports"))
        self.mw.support_list.setItemText(0, _translate("tenshi", "Support 1"))
        self.mw.support_plus.setText(_translate("tenshi", "+"))
        self.mw.label_27.setText(_translate("tenshi", "Angle"))
        self.mw.label_26.setText(_translate("tenshi", "Position (ID)"))
        self.mw.label_73.setText(_translate("tenshi", "K"))
        self.mw.spring_k.setText(_translate("tenshi", "1"))
        self.mw.label_71.setText(_translate("tenshi", "Translation"))
        self.mw.label_127.setText(_translate("tenshi", "N/m"))
        self.mw.spring_translation.setText(_translate("tenshi", "y"))
        self.mw.label_113.setText(_translate("tenshi", "°"))
        self.mw.support_angle.setText(_translate("tenshi", "0"))
        self.mw.support_internal_hinge.setText(_translate("tenshi", "Internal Hinge"))
        self.mw.support_roll.setText(_translate("tenshi", "Roll"))
        self.mw.support_fixed.setText(_translate("tenshi", "Fixed"))
        self.mw.support_hinged.setText(_translate("tenshi", "Hinged"))
        self.mw.support_spring.setText(_translate("tenshi", "Spring"))
        self.mw.support_apply.setText(_translate("tenshi", "Apply"))
        self.mw.support_remove.setText(_translate("tenshi", "Remove"))
        self.mw.label_28.setText(_translate("tenshi", "Point Loads"))
        self.mw.load_list.setItemText(0, _translate("tenshi", "Load 1"))
        self.mw.load_plus.setText(_translate("tenshi", "+"))
        self.mw.label_32.setText(_translate("tenshi", "Y Intensity"))
        self.mw.label_36.setText(_translate("tenshi", "Position (ID)"))
        self.mw.label_33.setText(_translate("tenshi", "X Intensity"))
        self.mw.load_moment.setText(_translate("tenshi", "0"))
        self.mw.load_x.setText(_translate("tenshi", "0"))
        self.mw.label_86.setText(_translate("tenshi", "N"))
        self.mw.label_89.setText(_translate("tenshi", "Nm"))
        self.mw.label_34.setText(_translate("tenshi", "Angle"))
        self.mw.load_angle.setText(_translate("tenshi", "0"))
        self.mw.load_y.setText(_translate("tenshi", "0"))
        self.mw.label_87.setText(_translate("tenshi", "N"))
        self.mw.label_35.setText(_translate("tenshi", "Moment"))
        self.mw.label_88.setText(_translate("tenshi", "°"))
        self.mw.load_apply.setText(_translate("tenshi", "Apply"))
        self.mw.load_remove.setText(_translate("tenshi", "Remove"))
        self.mw.label_37.setText(_translate("tenshi", "Distributed Loads"))
        self.mw.qload_list.setItemText(0, _translate("tenshi", "Load 1"))
        self.mw.qload_plus.setText(_translate("tenshi", "+"))
        self.mw.label_39.setText(_translate("tenshi", "Initial Intensity"))
        self.mw.qload_initial.setText(_translate("tenshi", "0"))
        self.mw.label_40.setText(_translate("tenshi", "Final Intensity"))
        self.mw.label_38.setText(_translate("tenshi", "Position (ID)"))
        self.mw.qload_final.setText(_translate("tenshi", "0"))
        self.mw.label_90.setText(_translate("tenshi", "N"))
        self.mw.label_91.setText(_translate("tenshi", "N"))
        self.mw.qload_apply.setText(_translate("tenshi", "Apply"))
        self.mw.qload_remove.setText(_translate("tenshi", "Remove"))
        self.mw.label_44.setText(_translate("tenshi", "Rectangular Subarea"))
        self.mw.rect_list.setItemText(0, _translate("tenshi", "Ret. 1"))
        self.mw.rect_plus.setText(_translate("tenshi", "+"))
        self.mw.rect_visualize.setText(_translate("tenshi", "Highlight Subarea"))
        self.mw.label_45.setText(_translate("tenshi", "X"))
        self.mw.label_48.setText(_translate("tenshi", "Y"))
        self.mw.label_46.setText(_translate("tenshi", "Y"))
        self.mw.label_47.setText(_translate("tenshi", "X"))
        self.mw.label_131.setText(_translate("tenshi", "m"))
        self.mw.label_132.setText(_translate("tenshi", "m"))
        self.mw.label_133.setText(_translate("tenshi", "m"))
        self.mw.label_134.setText(_translate("tenshi", "m"))
        self.mw.label_51.setText(_translate("tenshi", "Down Right"))
        self.mw.label_49.setText(_translate("tenshi", "Vertices Coordinates"))
        self.mw.label_50.setText(_translate("tenshi", "Up Left"))
        self.mw.rect_apply.setText(_translate("tenshi", "Apply"))
        self.mw.rect_remove.setText(_translate("tenshi", "Remove"))
        self.mw.label_52.setText(_translate("tenshi", "Circular Subarea"))
        self.mw.circle_list.setItemText(0, _translate("tenshi", "Cir. 1"))
        self.mw.circle_plus.setText(_translate("tenshi", "+"))
        self.mw.circle_visualize.setText(_translate("tenshi", "Highlight Subarea"))
        self.mw.label_56.setText(_translate("tenshi", "Radius"))
        self.mw.label_55.setText(_translate("tenshi", "Y"))
        self.mw.label_54.setText(_translate("tenshi", "X"))
        self.mw.label_57.setText(_translate("tenshi", "Initial Angle"))
        self.mw.label_57.setText("Angle (bisectrix)")
        self.mw.label_58.setText(_translate("tenshi", "Final Angle"))
        self.mw.label_135.setText(_translate("tenshi", "m"))
        self.mw.label_136.setText(_translate("tenshi", "m"))
        self.mw.label_53.setText(_translate("tenshi", "Center Coordinates"))
        self.mw.label_92.setText(_translate("tenshi", "m"))
        self.mw.label_93.setText(_translate("tenshi", "°"))
        self.mw.label_94.setText(_translate("tenshi", "°"))
        self.mw.circle_apply.setText(_translate("tenshi", "Apply"))
        self.mw.circle_remove.setText(_translate("tenshi", "Remove"))
        self.mw.label_128.setText(_translate("tenshi",
                                             "<html><head/><body><p align=\"center\"><span style=\" color:#ff5500;\">Adding semicircles will unable calculations of the shear stress and flux.</span></p></body></html>"))
        self.mw.label_59.setText(_translate("tenshi", "Data/Results"))
        self.mw.figureResultsButton.setText(_translate("tenshi", "Get Results from Figure"))
        self.mw.insertDataButton.setText(_translate("tenshi", "Insert Data"))
        self.mw.label_95.setText(_translate("tenshi", "m²"))
        self.mw.label_96.setText(_translate("tenshi", "m⁴"))
        self.mw.label_97.setText(_translate("tenshi", "m⁴"))
        self.mw.label_98.setText(_translate("tenshi", "m³"))
        self.mw.label_99.setText(_translate("tenshi", "m³"))
        self.mw.label_60.setText(_translate("tenshi", "Z Static Moment (Origin)"))
        self.mw.label_61.setText(_translate("tenshi", "Y Static Moment (Origin)"))
        self.mw.label_62.setText(_translate("tenshi", "Z Moment of Inertia (Centroid)"))
        self.mw.label_63.setText(_translate("tenshi", "Y Moment of Inertia (Centroid)"))
        self.mw.label_64.setText(_translate("tenshi", "Total Area"))
        self.mw.label_66.setText(_translate("tenshi", "Normal Stress"))
        self.mw.label_69.setText(_translate("tenshi", "Z Moment"))
        self.mw.specify_y.setText(_translate("tenshi", "Specify Y"))
        self.mw.checkBox.setText(_translate("tenshi", "Add to PDF"))
        self.mw.specify_z.setText(_translate("tenshi", "Specify Z"))
        self.mw.label_68.setText(_translate("tenshi", "Y Moment"))
        self.mw.label_67.setText(_translate("tenshi", "Normal Force"))
        self.mw.label_100.setText(_translate("tenshi", "N"))
        self.mw.label_101.setText(_translate("tenshi", "Nm"))
        self.mw.label_102.setText(_translate("tenshi", "Nm"))
        self.mw.label_103.setText(_translate("tenshi", "m"))
        self.mw.label_104.setText(_translate("tenshi", "m"))
        self.mw.label_105.setText(_translate("tenshi", "Pa"))
        # self.mw.label_106.setText(_translate("tenshi", "m")) neutral line unity
        self.mw.label_70.setText(_translate("tenshi", "Normal Stress:"))
        self.mw.label_72.setText(_translate("tenshi", "Neutral Line:"))
        self.mw.tncalculate.setText(_translate("tenshi", "Calculate"))
        self.mw.label_74.setText(_translate("tenshi", "Shear Stress and Flow"))
        self.mw.tfosbox.setItemText(0, _translate("tenshi", "Force"))
        self.mw.tfosbox.setItemText(1, _translate("tenshi", "Spacing"))
        self.mw.label_75.setText(_translate("tenshi", "Shear Force"))
        self.mw.label_41.setText(_translate("tenshi", "Cut Height"))
        self.mw.tscalculate.setText(_translate("tenshi", "Calculate"))
        self.mw.label_77.setText(_translate("tenshi", "Thickness (t)"))
        self.mw.label_76.setText(_translate("tenshi", "Contact Areas"))
        self.mw.label_107.setText(_translate("tenshi", "N"))
        self.mw.label_108.setText(_translate("tenshi", "m"))
        self.mw.label_109.setText(_translate("tenshi", "m"))
        self.mw.checkBox_2.setText(_translate("tenshi", "Add to PDF"))
        self.mw.label_65.setText(_translate("tenshi", "Q:"))
        self.mw.label_78.setText(_translate("tenshi", "Shear Stress:"))
        self.mw.label_80.setText(_translate("tenshi", "Shear Flow:"))
        self.mw.label_110.setText(_translate("tenshi", "m³"))
        self.mw.label_111.setText(_translate("tenshi", "Pa"))
        self.mw.label_112.setText(_translate("tenshi", "N/m"))
        self.mw.label_12.setText(_translate("tenshi", "Mohr's Cricle"))
        self.mw.radio_plane.setText(_translate("tenshi", "Plane State"))
        self.mw.radio_triple.setText(_translate("tenshi", "Triple State"))
        self.mw.label_18.setText(_translate("tenshi", "τxy"))
        self.mw.label_15.setText(_translate("tenshi", "σx"))
        self.mw.label_21.setText(_translate("tenshi", "τyz"))
        self.mw.mohr_apply.setText(_translate("tenshi", "Apply"))
        self.mw.label_20.setText(_translate("tenshi", "τxz"))
        self.mw.label_19.setText(_translate("tenshi", "σz"))
        self.mw.label_16.setText(_translate("tenshi", "σy"))
        self.mw.label_117.setText(_translate("tenshi", "Pa"))
        self.mw.label_118.setText(_translate("tenshi", "Pa"))
        self.mw.label_119.setText(_translate("tenshi", "Pa"))
        self.mw.label_120.setText(_translate("tenshi", "Pa"))
        self.mw.label_121.setText(_translate("tenshi", "Pa"))
        self.mw.label_122.setText(_translate("tenshi", "Pa"))
        self.mw.label_22.setText(_translate("tenshi", "Mouse Precision (Decimals)"))
        self.mw.int_plot.setText(_translate("tenshi", "Interactive Graph"))

        self.mw.label_23.setText(_translate("tenshi", "X"))
        self.mw.label_24.setText(_translate("tenshi", "Y"))
        self.mw.menuOp_es.setTitle(_translate("tenshi", "Options"))
        self.mw.menuResetar.setTitle(_translate("tenshi", "Reset..."))
        self.mw.menuFonte.setTitle(_translate("tenshi", "Font..."))
        self.mw.translate_menu.setTitle(_translate("tenshi", "Translate..."))
        self.mw.menuMudar_Temas.setTitle(_translate("tenshi", "Change Background"))
        self.mw.menuSalvar_e_Carregar.setTitle(_translate("tenshi", "Save and Load"))
        self.mw.menuGerar_Explica_es.setTitle(_translate("tenshi", "Generate PDF"))
        self.mw.save.setText(_translate("tenshi", "Save All"))
        self.mw.load_button.setText(_translate("tenshi", "Load"))
        self.mw.menuComo_utilizar.setTitle(_translate("tenshi", "How to Use"))
        self.mw.solvestatic.setText(_translate("tenshi", "Structure"))
        self.mw.solveresist.setText(_translate("tenshi", "Cross Section"))
        self.mw.resetloads.setText(_translate("tenshi", "Stress"))
        self.mw.resetall.setText(_translate("tenshi", "Elements"))
        self.mw.undo.setText(_translate("tenshi", "Previous Action"))
        self.mw.undo.setShortcut(_translate("tenshi", "Ctrl+Z"))
        self.mw.fontstructure.setText(_translate("tenshi", "Structure"))
        self.mw.fontequations.setText(_translate("tenshi", "Equations"))
        self.mw.translate_pt.setText(_translate("tenshi", "Português"))
        self.mw.translate_en.setText(_translate("tenshi", "English"))
        self.mw.translate_nihongo.setText(_translate("tenshi", "日本語"))
        self.mw.reset_cross_section.setText(_translate("tenshi", "Cross Section"))
        self.mw.font_interface.setText(_translate("tenshi", "Interface"))
        self.mw.action.setText(_translate("tenshi", "Load Cross Section"))
        self.mw.load_mohr.setText(_translate("tenshi", "Load Mohr's Circle"))
        self.mw.solvermohr.setText(_translate("tenshi", "Mohr's Circle"))
        self.mw.light_theme_button.setText(_translate("tenshi", "Light Theme"))
        self.mw.dark_theme_button.setText(_translate("tenshi", "Dark Theme"))
        self.mw.aboutButton.setText(_translate("tenshi", "About"))
        self.mw.showManualButton.setText(_translate("tenshi", "Show Manual (requires Internet)"))
        self.mw.hideManualButton.setText(_translate("tenshi", "Hide Manual"))
        self.mw.actionP_gina_para_Download.setText(_translate("tenshi", "Download Manual and Examples"))
        self.mw.downloadPageButton.setText(_translate("tenshi", "Download Manual and Examples"))
        self.mw.fullscreenButton.setText(_translate("tenshi", "Toggle Fullscreen Mode"))
        self.mw.gridBox.setText(_translate("tenshi", "Grid"))

        self.mw.load_structure_str = "Load Structure"
        self.mw.strucutre_type_str = "Structure(*.pkl)"
        self.mw.save_strucutre_text = "Structure"
        self.mw.save_strucutre_title = "Save Structure"
        self.mw.static_warning_str = "Only available for static structures (which contain a roll and hinged supports or a fixed support only)."
        self.mw.warning_str = "More information is required"
        self.mw.warning_title = "Error"
        self.mw.qload_warning = "Initial and final values must have the same signal"
        self.mw.id_warning_str = "Invalid ID. This ID doesn't exist."
        self.mw.geometry_change_title = "Warning"
        self.mw.geometry_change_warning = "If you make changes to the geometry, calculations previously added to the PDF will be lost. Continue?"
        self.mw.pdf_generated_title = "Done!"
        self.mw.pdf_generated_str = "PDF successfully generated"
        self.mw.shear_warning_title = "Unavailable"
        self.mw.shear_warning_str = "Cross section wasn't drawn, contains circular sectors or results weren't calculated from figure."
        self.mw.latex_error_str = "Please install Miktex to generate resolutions."
        self.mw.packages_error_str = "Something went wrong. It's likely you don't have the Latex packages installed."
        self.mw.font_size_str = "Font Size"
        self.mw.font_strucuture_str = "Structure Font:"
        self.mw.font_equations_str = "Equations Font:"
        self.mw.rect_values_error = "Invalid Values. Values were likely inverted."
        self.mw.pdf_title = "Generate resolution"
        self.mw.pdf_text = "resolution"
        self.mw.close_title = "Quit without saving?"
        self.mw.close_text = "Are you sure you want to quit? It's possible there are unsaved structures."
        self.mw.howtouse_title = "How to Use"
        self.mw.howtouse_text = "User Manual and Utilization Examples available at:"
        self.mw.about_title = "About"
        self.mw.about_text = ("Developed as a Scientific Initiation work at EESC-USP (Brazil) in 2020.\n"
                              "\n"
                              "Developed by Leonardo de Souza Bornia\n"
                              "\n"
                              "Acknowledgements:\n"
                              "Eng. Me. Henrique Borges Garcia\n"
                              "Prof. Me. Gustavo Lahr\n"
                              "Prof. Dr. Glauco Augusto de Paula Caurin\n"
                              "Fundação de Apoio à Física e à Química\n")

    def visualize(self, figure=None):
        self.mw.MplWidget.setGrid(self.mw.gridBox.isChecked())
        self.mw.MplWidget.plot(figure)
        self.mw.MplWidget.set_background_alpha()
        self.figurefix()
        if self.mw.last_figure == self.mw.show_mohr:
            self.mw.MplWidget.fix_plot_scale()

    def visualizeCurrentIndex(self, index):
        if index == 0:
            self.mw.show_structure.click()
            self.mw.stackedWidget.setCurrentIndex(0)
        elif index == 1:
            self.mw.show_sec.click()
            self.mw.stackedWidget.setCurrentIndex(5)
        elif index == 2:
            self.mw.show_mohr.click()
            self.mw.stackedWidget.setCurrentIndex(10)

    def visualize_mohr(self, figure=None):
        if self.mw.mohr.sx is not None:
            if not figure:
                figure = self.mw.mohr.state(self.mw.MplWidget.canvas.figure)
            self.visualize(figure)
            self.mw.last_figure = self.mw.show_mohr
            self.mw.MplWidget.set_background_alpha(0)
        else:
            self.mw.MplWidget.plot(has_grid=self.mw.gridBox.isChecked())
            self.figurefix()
            self.mw.last_figure = None

    def load_file(self):
        file, ok = QFileDialog.getOpenFileName(self, self.mw.load_structure_str, "", self.mw.strucutre_type_str)
        if ok:
            struct, cross, mohr = self.mw.get_prompt_values()
            if struct:
                self.mw.load_structure_aux(file)
            if cross:
                self.mw.load_cross_section_aux(file)
            if mohr:
                self.mw.load_mohr_aux(file)
            self.mw.states.append(pickle.dumps(self.mw.ss))
            self.mw.enable_buttons()
            self.mw.change_to_loaded_figure()

    def change_to_loaded_figure(self):
        if self.mw.struct_loaded:
            if self.mw.toolBox.currentIndex() != 0:
                self.mw.toolBox.setCurrentIndex(0)
            else:
                self.mw.show_structure.click()
                self.mw.stackedWidget.setCurrentIndex(0)
        elif self.mw.cross_loaded:
            if self.mw.toolBox.currentIndex() != 1:
                self.mw.toolBox.setCurrentIndex(1)
            else:
                self.mw.show_sec.click()
                self.mw.stackedWidget.setCurrentIndex(5)
        elif self.mw.mohr_loaded:
            if self.mw.toolBox.currentIndex() != 2:
                self.mw.toolBox.setCurrentIndex(2)
            else:
                self.mw.show_mohr.click()
                self.mw.stackedWidget.setCurrentIndex(10)
        self.mw.struct_loaded = False
        self.mw.cross_loaded = False
        self.mw.mohr_loaded = False

    def warning(self):
        msg = QMessageBox()
        msg.setWindowTitle(self.mw.warning_title)
        msg.setText(self.mw.warning_str)
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def invalid_id_warning(self):
        msg = QMessageBox()
        msg.setWindowTitle(self.mw.warning_title)
        msg.setText(self.mw.id_warning_str)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def static_warning(self):
        msg = QMessageBox()
        msg.setWindowTitle(self.mw.warning_title)
        msg.setText(self.mw.static_warning_str)
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def latex_warning(self):
        msg = QMessageBox()
        msg.setWindowTitle(self.mw.warning_title)
        msg.setText(self.mw.latex_error_str)
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def latex_packages_warning(self):
        msg = QMessageBox()
        msg.setWindowTitle(self.mw.warning_title)
        msg.setText(self.mw.packages_error_str)
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def pdf_generated_prompt(self):
        msg = QMessageBox()
        msg.setWindowTitle(self.mw.pdf_generated_title)
        msg.setText(self.mw.pdf_generated_str)
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def figurefix(self):
        x = self.mw.MplWidget.size().width()
        y = self.mw.MplWidget.size().height()
        self.mw.MplWidget.resize(x + 1, y + 1)
        self.mw.MplWidget.resize(x, y)

    def enable_buttons(self):
        if (len(self.mw.ss.supports_roll) + len(self.mw.ss.supports_hinged) + len(self.mw.ss.supports_spring_x) +
            len(self.mw.ss.supports_spring_z) + len(self.mw.ss.supports_spring_y) >= 2 or len(
                    self.mw.ss.supports_fixed) >= 1) \
                and (len(self.mw.ss.loads_point) + len(self.mw.ss.loads_q) + len(self.mw.ss.loads_moment)) >= 1:
            self.mw.show_diagram.setEnabled(True)
            self.mw.show_supports.setEnabled(True)
            self.mw.show_normal.setEnabled(True)
            self.mw.show_shear.setEnabled(True)
            self.mw.show_moment.setEnabled(True)
            self.mw.show_displacement.setEnabled(True)
        else:
            self.mw.disable_buttons()

    def disable_buttons(self):
        self.mw.show_diagram.setEnabled(False)
        self.mw.show_supports.setEnabled(False)
        self.mw.show_normal.setEnabled(False)
        self.mw.show_shear.setEnabled(False)
        self.mw.show_moment.setEnabled(False)
        self.mw.show_displacement.setEnabled(False)

    def undo_previous(self):
        if self.mw.last_figure != self.mw.show_sec and self.mw.last_figure != self.mw.show_mohr:
            if len(self.mw.states) != 0:
                del self.mw.states[-1]
            if len(self.mw.states) != 0:
                self.mw.ss = pickle.loads(self.mw.states[-1])
                self.mw.visualize(self.mw.ss.show_structure(show=False, figure=self.mw.MplWidget.canvas.figure))
                self.mw.enable_buttons()
                if self.mw.solvetrue == True:
                    self.mw.solvetrue = False
            else:
                self.mw.reset_struct_elems()

    def fontstruct(self):
        i = settings.size
        i, okPressed = QInputDialog.getInt(self, self.mw.font_size_str, self.mw.font_strucuture_str, i, 1, 100, 1)
        if okPressed:
            settings.size = i
            self.mw.last_figure.click()

    def fonteq(self):
        i = settings.eqsize
        i, okPressed = QInputDialog.getInt(self, self.mw.font_size_str, self.mw.font_equations_str, i, 1, 100, 1)
        if okPressed:
            settings.eqsize = i
            self.mw.last_figure.click()

    def UI_font(self):
        font, ok = QtWidgets.QFontDialog.getFont()
        if ok:
            for name, obj in inspect.getmembers(self):
                if isinstance(obj, QtWidgets.QLabel):
                    obj.setFont(font)

    def toggle_presentation_mode(self):
        if self.mw.isPresenting:
            self.mw.exit_presentation_mode()
        else:
            self.mw.enter_presentation_mode()

    def enter_presentation_mode(self):
        self.mw.isPresenting = True
        # self.mw.menubar.setHidden(True)
        self.mw.stackedWidget.setHidden(True)
        self.mw.frame_6.setHidden(True)
        self.tenshi.showFullScreen()

    def exit_presentation_mode(self):
        self.mw.isPresenting = False
        # self.mw.menubar.setHidden(False)
        self.mw.stackedWidget.setHidden(False)
        self.mw.frame_6.setHidden(False)
        self.tenshi.showNormal()

    def filter(self, string):
        return string.replace(",", ".")

    def onclick(self, event):
        if self.mw.int_plot.isChecked():
            if self.mw.deadzone_x.text() == '':
                self.mw.deadzone_x.setText('0')
            if self.mw.deadzone_y.text() == '':
                self.mw.deadzone_y.setText('0')
            px = int(self.mw.deadzone_x.text())
            py = int(self.mw.deadzone_y.text())
            if self.mw.last_figure == self.mw.show_mohr:
                if 'RIGHT' in str(event.button) and self.mw.mohr.sz is not None:
                    self.mw.plot_to_ui(
                        self.mw.mohr.calculate(self.mw.mohr.sx, self.mw.mohr.sy, self.mw.mohr.sz, self.mw.mohr.txy,
                                               self.mw.mohr.txz, self.mw.mohr.tyz,
                                               self.mw.MplWidget.canvas.figure))
            elif self.mw.stackedWidget.currentIndex() == 0:
                if 'LEFT' in str(event.button):
                    self.mw.beam_x1.setText(str(round(event.xdata, px)))
                    self.mw.beam_y1.setText(str(round(event.ydata, py)))
                elif 'RIGHT' in str(event.button):
                    self.mw.beam_x2.setText(str(round(event.xdata, px)))
                    self.mw.beam_y2.setText(str(round(event.ydata, py)))
            elif self.mw.stackedWidget.currentIndex() == 1:
                if 'LEFT' in str(event.button):
                    self.mw.node_x.setText(str(round(event.xdata, px)))
                    self.mw.node_y.setText(str(round(event.ydata, py)))
                elif 'RIGHT' in str(event.button):
                    distance = 1e20
                    id = ""
                    for keys, values in self.mw.ss.node_map.items():
                        id_, x, y, _, _, _ = self.mw.teach.fetcher(self.mw.ss.node_map.get(keys))
                        xdistance = event.xdata - x
                        ydistance = event.ydata - y
                        new_distance = np.sqrt(xdistance ** 2 + ydistance ** 2)
                        if new_distance <= distance:
                            distance = new_distance
                            id = id_
                    self.mw.node_id.setText(str(id))
            elif self.mw.stackedWidget.currentIndex() == 2:
                distance = 1e20
                id = ""
                for keys, values in self.mw.ss.node_map.items():
                    id_, x, y, _, _, _ = self.mw.teach.fetcher(self.mw.ss.node_map.get(keys))
                    xdistance = event.xdata - x
                    ydistance = event.ydata - y
                    new_distance = np.sqrt(xdistance ** 2 + ydistance ** 2)
                    if new_distance < distance:
                        distance = new_distance
                        id = id_
                self.mw.support_pos.setText(str(id))
            elif self.mw.stackedWidget.currentIndex() == 3:
                distance = 1e20
                id = ""
                for keys, values in self.mw.ss.node_map.items():
                    id_, x, y, _, _, _ = self.mw.teach.fetcher(self.mw.ss.node_map.get(keys))
                    xdistance = event.xdata - x
                    ydistance = event.ydata - y
                    new_distance = np.sqrt(xdistance ** 2 + ydistance ** 2)
                    if new_distance < distance:
                        distance = new_distance
                        id = id_
                self.mw.load_pos.setText(str(id))
            elif self.mw.stackedWidget.currentIndex() == 4:

                def find_nearest(xarray, yarray, xvalue, yvalue):
                    nearestDistance = 1e20
                    for index in range(len(xarray)):
                        pointDistance = (((xarray[index] - xvalue) ** 2 + (yarray[index] - yvalue) ** 2) ** .5)
                        if pointDistance < nearestDistance:
                            nearestDistance = pointDistance
                    return abs(nearestDistance)

                nearest = 1e20
                for keys, values in self.mw.ss.element_map.items():
                    _, xi, yi, _, _, _ = self.mw.teach.fetcher(
                        self.mw.ss.node_map.get(self.mw.ss.element_map.get(keys).node_id1))
                    id_, xf, yf, _, _, _ = self.mw.teach.fetcher(
                        self.mw.ss.node_map.get(self.mw.ss.element_map.get(keys).node_id2))
                    xarray = np.linspace(xi, xf, 11)
                    yarray = np.linspace(yi, yf, 11)
                    newNearest = find_nearest(xarray, yarray, event.xdata, event.ydata)
                    if newNearest < nearest:
                        nearest = newNearest
                        self.mw.qload_pos.setText(str(self.mw.ss.element_map.get(keys).id))
                    if keys == len(self.mw.ss.node_map) - 1:
                        break

            elif self.mw.stackedWidget.currentIndex() == 5:
                if 'LEFT' in str(event.button):
                    self.mw.rect_x1.setText(str(round(event.xdata, px)))
                    self.mw.rect_y1.setText(str(round(event.ydata, py)))
                elif 'RIGHT' in str(event.button):
                    self.mw.rect_x2.setText(str(round(event.xdata, px)))
                    self.mw.rect_y2.setText(str(round(event.ydata, py)))
            elif self.mw.stackedWidget.currentIndex() == 6:
                if 'LEFT' in str(event.button):
                    self.mw.circle_x.setText(str(round(event.xdata, px)))
                    self.mw.circle_y.setText(str(round(event.ydata, py)))

    def on_release(self, event):
        if self.mw.int_plot.isChecked():
            if self.mw.last_figure == self.mw.show_mohr and 'RIGHT' not in str(
                    event.button) and self.mw.MplWidget.canvas.figure.gca().name == "3d":
                self.ss.plot_to_ui(self.ss.on_release(self.mw.MplWidget.canvas.figure))

    def get_prompt_values(self):
        prompt = loadFilePrompt.Ui_load_prompt()
        load_prompt = QtWidgets.QDialog()
        prompt.setupUi(load_prompt, self.mw.language)
        load_prompt.exec_()
        return prompt.struct, prompt.cross, prompt.mohr

    def disable_unfinished(self):
        self.mw.frame_19.setHidden(True)
        self.mw.frame_21.setHidden(True)
        self.mw.frame_22.setHidden(True)
        self.mw.frame_23.setHidden(True)
        self.mw.frame_24.setHidden(True)
        self.mw.label_76.setHidden(True)
        self.mw.tcontact.setHidden(True)
        self.mw.tfosbox.setHidden(True)
        self.mw.tfos.setHidden(True)
        self.mw.translate_nihongo.setVisible(False)
        self.mw.beam_remove.setHidden(True)
        self.mw.node_remove.setHidden(True)
        self.mw.support_remove.setHidden(True)
        self.mw.load_remove.setHidden(True)
        self.mw.qload_remove.setHidden(True)
        self.mw.qload_remove.setHidden(True)
        self.mw.label_58.setHidden(True)
        self.mw.label_94.setHidden(True)
        self.mw.circle_af.setHidden(True)
        self.mw.support_internal_hinge.setHidden(True)
        self.mw.support_spring.setHidden(True)
        self.mw.menuMudar_Temas.setEnabled(False)

    def light_theme(self):
        self.app.setStyleSheet("")

    def dark_theme(self):
        self.app.setStyleSheet(qdarkstyle.load_stylesheet())
        self.mw.MplWidget.set_background_alpha()

    def change_interactive_mode(self):
        if self.mw.int_plot.isChecked():
            self.mw.MplWidget.interactive_mode(0)
        else:
            self.mw.MplWidget.interactive_mode(1)

    def aboutDialog(self):
        QMessageBox.about(self, self.mw.about_title, self.mw.about_text)

    def showDownloadPage(self):
        webbrowser.open("https://github.com/LeoBelmont/Structures-Explained/releases")

    def replotGrid(self):
        self.mw.MplWidget.setGrid(self.mw.gridBox.isChecked())
        self.mw.MplWidget.canvas.draw()

    def scientific_format(self, number):
        var = '%E' % number
        return var.split('E')[0].rstrip('0').rstrip('.') + 'E' + var.split('E')[1]

    def doStartUpStuff(self):
        self.disable_buttons()
        self.mw.frame_4.setHidden(True)
        self.mw.support_angle.setHidden(True)
        self.mw.label_27.setHidden(True)
        self.mw.label_71.setHidden(True)
        self.mw.label_73.setHidden(True)
        self.mw.spring_k.setHidden(True)
        self.mw.label_113.setHidden(True)
        self.mw.label_127.setHidden(True)
        self.mw.spring_translation.setHidden(True)
        self.mw.cs_y.setEnabled(False)
        self.mw.cs_z.setEnabled(False)
        self.mw.radio_plane.setChecked(True)
        self.mw.frame_16.setDisabled(True)
        self.mw.label_83.setHidden(True)
        self.mw.label_85.setHidden(True)
        self.mw.label_128.setHidden(True)
        self.mw.show_mohr.setHidden(True)
        self.mw.show_sec.setHidden(True)
        self.mw.line_3.setHidden(True)
        self.mw.line_10.setHidden(True)
        self.mw.line_13.setHidden(True)
        self.mw.line_4.setHidden(True)
        self.ss.switch_states_plane()
        self.change_interactive_mode()
        self.mw.sx.setText("10")
        self.mw.sy.setText("20")
        self.mw.txy.setText("30")
        # self.visualize_structure()
        # self.mw.last_figure = self.st.show_structure

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.HoverEnter:
            self.mw.label_128.setHidden(False)
            return True

        if event.type() == QtCore.QEvent.HoverLeave:
            self.mw.label_128.setHidden(True)
            return True

        return False

    def setupLoading(self):
        self.mw.loadingScreen = QtWidgets.QDialog()
        self.mw.loadingUi = loadingPrompt.Ui_loading_prompt(self.mw.language, self.mw.loadingScreen)
        self.mw.loadingUi.setupUi()

    def connect_ui(self):
        self.mw.toolButton.clicked.connect(lambda: self.mw.stackedWidget.setCurrentIndex(0))
        self.mw.toolButton_3.clicked.connect(lambda: self.mw.stackedWidget.setCurrentIndex(1))
        self.mw.toolButton_4.clicked.connect(lambda: self.mw.stackedWidget.setCurrentIndex(2))
        self.mw.toolButton_5.clicked.connect(lambda: self.mw.stackedWidget.setCurrentIndex(3))
        self.mw.toolButton_6.clicked.connect(lambda: self.mw.stackedWidget.setCurrentIndex(4))
        self.mw.toolButton_7.clicked.connect(lambda: self.mw.stackedWidget.setCurrentIndex(5))
        self.mw.toolButton_8.clicked.connect(lambda: self.mw.stackedWidget.setCurrentIndex(6))
        self.mw.toolButton_9.clicked.connect(lambda: self.mw.stackedWidget.setCurrentIndex(7))
        self.mw.toolButton_2.clicked.connect(lambda: self.mw.stackedWidget.setCurrentIndex(8))
        self.mw.toolButton_11.clicked.connect(lambda: self.mw.stackedWidget.setCurrentIndex(9))
        self.mw.toolButton_10.clicked.connect(lambda: self.mw.stackedWidget.setCurrentIndex(10))

        self.mw.toolBox.currentChanged.connect(self.visualizeCurrentIndex)

        self.mw.load_button.triggered.connect(self.load_file)
        self.mw.undo.triggered.connect(self.undo_previous)
        self.mw.translate_pt.triggered.connect(self.retranslateUi)
        self.mw.translate_en.triggered.connect(self.retranslateUiEN)

        self.mw.fontstructure.triggered.connect(self.fontstruct)
        self.mw.fontequations.triggered.connect(self.fonteq)
        self.mw.font_interface.triggered.connect(self.UI_font)

        self.mw.MplWidget.canvas.mpl_connect('button_press_event', self.onclick)
        self.mw.MplWidget.canvas.mpl_connect('button_release_event', self.on_release)
        self.mw.int_plot.stateChanged.connect(self.change_interactive_mode)
        self.mw.gridBox.stateChanged.connect(self.replotGrid)
        # self.mw.deadzone_x.textEdited.connect(lambda: self.mw.MplWidget.setXTicks(self.mw.deadzone_x.text()))
        # self.mw.deadzone_y.textEdited.connect(lambda: self.mw.MplWidget.setYTicks(self.mw.deadzone_y.text()))

        self.mw.light_theme_button.triggered.connect(self.light_theme)
        self.mw.dark_theme_button.triggered.connect(self.dark_theme)
        self.mw.aboutButton.triggered.connect(self.aboutDialog)
        self.mw.downloadPageButton.triggered.connect(self.showDownloadPage)
        self.mw.fullscreenButton.triggered.connect(self.toggle_presentation_mode)

    def connect_structure(self):
        self.st = st_connections(self.mw)
        self.mw.beam_apply.clicked.connect(self.st.add_beam)
        self.mw.utilizeinfo.stateChanged.connect(self.st.beam_info)
        self.mw.elementtype.currentIndexChanged.connect(self.st.element_type_list)
        self.mw.node_apply.clicked.connect(self.st.add_node)
        self.mw.support_apply.clicked.connect(self.st.add_support)
        self.mw.support_roll.clicked.connect(self.st.show_support_stuff)
        self.mw.support_hinged.clicked.connect(self.st.show_support_stuff)
        self.mw.support_fixed.clicked.connect(self.st.show_support_stuff)
        self.mw.support_spring.clicked.connect(self.st.show_support_stuff)
        self.mw.support_internal_hinge.clicked.connect(self.st.show_support_stuff)
        self.mw.load_apply.clicked.connect(self.st.add_point_load)
        self.mw.qload_apply.clicked.connect(self.st.add_q_load)
        self.mw.show_structure.clicked.connect(self.st.visualize_structure)
        self.mw.show_diagram.clicked.connect(self.st.visualize_diagram)
        self.mw.show_supports.clicked.connect(self.st.visualize_supports)
        self.mw.show_normal.clicked.connect(self.st.visualize_normal)
        self.mw.show_shear.clicked.connect(self.st.visualize_shear)
        self.mw.show_moment.clicked.connect(self.st.visualize_moment)
        self.mw.show_displacement.clicked.connect(self.st.visualize_displacement)
        self.mw.solvestatic.triggered.connect(self.st.static_solver)
        self.mw.resetloads.triggered.connect(self.st.reset)
        self.mw.resetall.triggered.connect(self.st.reset_struct_elems)
        self.mw.save.triggered.connect(self.st.save_structure)

    def connect_cross_section(self):
        self.cs = cs_connections(self.mw, self)
        self.mw.solveresist.triggered.connect(self.cs.rm_solver)
        self.mw.rect_apply.clicked.connect(self.cs.add_rect)
        self.mw.circle_apply.clicked.connect(self.cs.add_cir)
        self.mw.tncalculate.clicked.connect(self.cs.get_sigma_T)
        self.mw.tscalculate.clicked.connect(self.cs.get_cis)
        self.mw.circle_apply.installEventFilter(self.mw)

        self.mw.figureResultsButton.clicked.connect(self.cs.set_sigma)
        self.mw.insertDataButton.clicked.connect(self.cs.insert_sigma)
        self.mw.rect_list.currentIndexChanged.connect(self.cs.change_table_rect)
        self.mw.rect_plus.clicked.connect(self.cs.add_rect_item)
        self.mw.circle_plus.clicked.connect(self.cs.add_cir_item)
        self.mw.circle_list.currentIndexChanged.connect(self.cs.change_table_circ)
        self.mw.rect_visualize.stateChanged.connect(self.cs.plot_sec)
        self.mw.circle_visualize.stateChanged.connect(self.cs.plot_sec)
        self.mw.rect_remove.clicked.connect(self.cs.remove_rectangle)
        self.mw.circle_remove.clicked.connect(self.cs.remove_circle)
        self.mw.reset_cross_section.triggered.connect(self.cs.transv_reset)
        self.mw.specify_y.stateChanged.connect(self.cs.cs_y_enabler)
        self.mw.specify_z.stateChanged.connect(self.cs.cs_z_enabler)

        self.mw.show_sec.clicked.connect(self.cs.plot_sec)

    def connect_stress_states(self):
        self.ss = ss_connections(self.mw, self, self.visualize)
        self.mw.radio_plane.clicked.connect(self.ss.switch_states_plane)
        self.mw.radio_triple.clicked.connect(self.ss.switch_states_triple)
        self.mw.mohr_apply.clicked.connect(self.ss.draw_stress_state)

        self.mw.show_mohr.clicked.connect(self.ss.draw_stress_state)
        self.mw.solvermohr.triggered.connect(self.ss.generator_thread)
