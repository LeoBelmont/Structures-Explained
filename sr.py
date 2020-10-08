import speech_recognition as sr
import re


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


#print(Secretary().speech_recognition())
