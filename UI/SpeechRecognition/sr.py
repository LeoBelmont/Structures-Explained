import speech_recognition as sr
import re
from PyQt5 import QtGui, QtWidgets, QtCore


class Secretary:
    def speech_recognition(self):
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            #print("Say something!")
            audio = r.listen(source)
            r.adjust_for_ambient_noise(source)
        try:
            print(r.recognize_google(audio, language='pt-BR'))
            return self.audio_sort(r.recognize_google(audio, language='pt-BR'))
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("not request results from Speech Recognition service; {0}".format(e))

    def audio_sort(self, audio):
        audio = re.sub('-', '', audio)
        audio = audio.replace(" ", "")
        audio = audio.replace(",", ".")
        if 'aplicar' in audio:
            return 'aplicar'
        else:
            l = re.search(r'([a-zA-Z]\d)((-)?\d+((\.)\d+)?)', audio)
            try:
                return l.group(1).capitalize(), l.group(2)
            except:
                print(l)
                return None, None


class SetupUISecretary():
    def __init__(self, tenshi):
        self.tenshi = tenshi

    def configSR(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Figures/mic_red.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tenshi.push_to_talk.setIcon(icon)
        self.tenshi.push_to_talk.repaint()
        audio = Secretary().speech_recognition()
        if audio is not None:
            if audio == 'aplicar' or audio == 'apply':
                self.tenshi.beam_apply.click()
            else:
                a, b = audio
                if a is not None and b is not None:
                    if str(a) == 'X1':
                        self.tenshi.beam_x1.setText(str(b))
                    elif str(a) == 'Y1':
                        self.tenshi.beam_y1.setText(str(b))
                    elif str(a) == r'X2':
                        self.tenshi.beam_x2.setText(str(b))
                    elif str(a) == 'Y2':
                        self.tenshi.beam_y2.setText(str(b))
        icon.addPixmap(QtGui.QPixmap(":/Figures/mic_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tenshi.push_to_talk.setIcon(icon)
        self.tenshi.push_to_talk.repaint()

    def setupSR(self):
        _translate = QtCore.QCoreApplication.translate
        self.tenshi.push_to_talk = QtWidgets.QToolButton(self.tenshi.frame_6)
        self.tenshi.push_to_talk.setMaximumSize(QtCore.QSize(25, 25))
        self.tenshi.push_to_talk.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tenshi.push_to_talk.setAutoFillBackground(False)
        self.tenshi.push_to_talk.setText("")
        self.tenshi.push_to_talk.clicked.connect(self.tenshi.listener)
        #self.tenshi.push_to_talk.setIcon(icon13)
        self.tenshi.push_to_talk.setIconSize(QtCore.QSize(25, 25))
        self.tenshi.push_to_talk.setObjectName("push_to_talk")
        self.tenshi.tenshi.setTabOrder(self.tenshi.gridBox, self.tenshi.push_to_talk)
        self.tenshi.tenshi.setTabOrder(self.tenshi.push_to_talk, self.tenshi.deadzone_x)
        self.tenshi.push_to_talk.setToolTip(_translate("tenshi", "Utilizar comandos de voz"))
        self.tenshi.push_to_talk.setShortcut(_translate("tenshi", "V"))
        self.tenshi.horizontalLayout_2.addWidget(self.tenshi.push_to_talk)

# print(Secretary().speech_recognition())
