from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget


class PathPrompt(QWidget):
    def __init__(self, language, dialog):
        super().__init__()
        self.language = language
        self.Dialog = dialog
        self.userTerminated = False
        self.path = None
        self.setupUi()

    def setupUi(self):
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(300, 174)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Dialog.sizePolicy().hasHeightForWidth())
        self.Dialog.setSizePolicy(sizePolicy)
        self.Dialog.setMinimumSize(QtCore.QSize(300, 174))
        self.Dialog.setMaximumSize(QtCore.QSize(300, 174))
        self.gridLayout = QtWidgets.QGridLayout(self.Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.Dialog)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.Dialog)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton(self.Dialog)
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout.addWidget(self.radioButton_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.Dialog)
        self.label.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.Dialog)
        self.lineEdit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.Dialog)
        self.label_2.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.Dialog)
        self.lineEdit_2.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        if self.language == "PT":
            self.retranslateUi()
        elif self.language == "EN":
            self.retranslateUiEN()
        self.buttonBox.accepted.connect(self.acceptEvent)
        self.buttonBox.rejected.connect(self.cancelEvent)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)
        self.Dialog.setTabOrder(self.radioButton, self.radioButton_2)
        self.Dialog.setTabOrder(self.radioButton_2, self.radioButton_3)
        self.Dialog.setTabOrder(self.radioButton_3, self.lineEdit)

        self.radioButton.toggled.connect(self.showStuff)
        self.radioButton_2.toggled.connect(self.showStuff)
        self.radioButton_3.toggled.connect(self.showStuff)
        self.Dialog.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.Dialog.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.Dialog.setWindowIcon(QtGui.QIcon(r':/Figures/LogoSX.ico'))
        self.radioButton.toggle()
        self.lineEdit.setValidator(QIntValidator())
        self.lineEdit_2.setValidator(QIntValidator())

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Escolher Caminho da Solução"))
        self.radioButton.setText(_translate("Dialog", "Fixo"))
        self.radioButton_2.setText(_translate("Dialog", "Aleatório"))
        self.radioButton_3.setText(_translate("Dialog", "Especificar Caminho dos Nós da Solução"))
        self.label.setText(_translate("Dialog", "Índice Inicial"))
        self.label_2.setText(_translate("Dialog", "Índice Final"))
        self.warning_title = "Erro"
        self.warning_str = "O campo não pode estar vazio"
        self.invalid_warning_str = "Dados inválidos. Escreva inteiros separados por hífens."

    def retranslateUiEN(self):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Choose Solution Path"))
        self.radioButton.setText(_translate("Dialog", "Fixed"))
        self.radioButton_2.setText(_translate("Dialog", "Random"))
        self.radioButton_3.setText(_translate("Dialog", "Specify Solution Node Path"))
        self.label.setText(_translate("Dialog", "Initial Index"))
        self.label_2.setText(_translate("Dialog", "Final Index"))
        self.warning_title = "Error"
        self.warning_str = "Field can't be empty"
        self.invalid_warning_str = "Invalid data. Type whole numbers separated by hyphens."

    def acceptEvent(self):
        if self.radioButton.isChecked():
            self.path = "longest"
            self.Dialog.close()

        elif self.radioButton_2.isChecked():
            self.path = "random"
            self.Dialog.close()

        elif self.radioButton_3.isChecked():
            text1 = self.lineEdit.text()
            text2 = self.lineEdit_2.text()
            if text1 != "" and text2 != "":
                try:
                    self.path = (int(text1), int(text2))
                    if len(self.path) != 2:
                        self.invalid_warning()
                    else:
                        self.Dialog.close()
                except ValueError:
                    self.invalid_warning()
            else:
                self.warning()

    def cancelEvent(self):
        self.userTerminated = True
        self.Dialog.close()

    def showStuff(self):
        if not self.radioButton_3.isChecked():
            self.label.setEnabled(False)
            self.label_2.setEnabled(False)
            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
        else:
            self.label.setEnabled(True)
            self.label_2.setEnabled(True)
            self.lineEdit.setEnabled(True)
            self.lineEdit_2.setEnabled(True)

    def warning(self):
        msg = QMessageBox()
        msg.setWindowTitle(self.warning_title)
        msg.setText(self.warning_str)
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def invalid_warning(self):
        msg = QMessageBox()
        msg.setWindowTitle(self.warning_title)
        msg.setText(self.invalid_warning_str)
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()


if __name__ == "__main__":
    import os
    import sys

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    dialog = QtWidgets.QDialog()
    ui = PathPrompt("PT", dialog)
    dialog.show()
    sys.exit(app.exec_())
