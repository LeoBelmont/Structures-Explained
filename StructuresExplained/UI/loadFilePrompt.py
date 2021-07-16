from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_load_prompt(object):

    struct = False
    cross = False
    mohr = False

    def setupUi(self, load_prompt, language):
        load_prompt.setObjectName("load_prompt")
        load_prompt.resize(202, 138)
        self.gridLayout_2 = QtWidgets.QGridLayout(load_prompt)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(load_prompt)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.check_struct = QtWidgets.QCheckBox(self.frame)
        self.check_struct.setObjectName("check_struct")
        self.gridLayout.addWidget(self.check_struct, 0, 0, 1, 1)
        self.check_cross = QtWidgets.QCheckBox(self.frame)
        self.check_cross.setObjectName("check_cross")
        self.gridLayout.addWidget(self.check_cross, 1, 0, 1, 1)
        self.check_mohr = QtWidgets.QCheckBox(self.frame)
        self.check_mohr.setObjectName("check_mohr")
        self.gridLayout.addWidget(self.check_mohr, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(load_prompt)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)
        
        if language == "PT":
            self.retranslateUi(load_prompt)
        elif language == "EN":
            self.retranslateUIEN(load_prompt)

        self.buttonBox.accepted.connect(load_prompt.accept)
        self.buttonBox.rejected.connect(load_prompt.reject)
        QtCore.QMetaObject.connectSlotsByName(load_prompt)

        self.buttonBox.accepted.connect(self.submit)

    def retranslateUi(self, load_prompt):
        _translate = QtCore.QCoreApplication.translate
        load_prompt.setWindowTitle(_translate("load_prompt", "Prompt"))
        self.check_struct.setText(_translate("load_prompt", "Carregar Estrutura"))
        self.check_cross.setText(_translate("load_prompt", "Carregar seção transversal"))
        self.check_mohr.setText(_translate("load_prompt", "Carregar círculo de Mohr"))

    def retranslateUIEN(self, load_prompt):
        _translate = QtCore.QCoreApplication.translate
        load_prompt.setWindowTitle(_translate("load_prompt", "Prompt"))
        self.check_struct.setText(_translate("load_prompt", "Load Structure"))
        self.check_cross.setText(_translate("load_prompt", "Load Cross Section"))
        self.check_mohr.setText(_translate("load_prompt", "Load Mohr's Circle"))

    def submit(self):
        self.struct = self.check_struct.isChecked()
        self.cross = self.check_cross.isChecked()
        self.mohr = self.check_mohr.isChecked()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    load_prompt = QtWidgets.QDialog()
    ui = Ui_load_prompt()
    ui.setupUi(load_prompt)
    load_prompt.show()
    sys.exit(app.exec_())
