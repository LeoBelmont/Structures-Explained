from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Ui_loading_prompt(QWidget):
    def __init__(self, language, Dialog):
        super().__init__()

        self.Dialog = Dialog
        self.userTerminated = False
        self.language = language

    def setupUi(self):
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(300, 184)
        self.gridLayout = QtWidgets.QGridLayout(self.Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.Dialog)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.Dialog)
        self.label.setFixedSize(QtCore.QSize(160, 90))
        self.label.setText("")
        self.loadingGIF = QtGui.QMovie("../../Novapasta/load.gif")
        self.label.setMovie(self.loadingGIF)
        self.loadingGIF.start()
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        if self.language == 'PT':
            self.retranslateUi()
        elif self.language == 'EN':
            self.retranslateUiEN()
        self.buttonBox.rejected.connect(self.cancelEvent)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)
        self.Dialog.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.Dialog.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.Dialog.setWindowIcon(QtGui.QIcon(r':/Figures/LogoSX.ico'))
        # self.Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Trabalhando..."))
        self.label_2.setText(_translate("Dialog", "Sua resolução está sendo gerada. Pode demorar alguns minutos na primeira utilização."))

    def retranslateUiEN(self):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Working..."))
        self.label_2.setText(_translate("Dialog", "The resolution is being generated. It may take a few minutes if this is your first use."))

    def cancelEvent(self):
        self.Dialog.close()
        self.userTerminated = True
