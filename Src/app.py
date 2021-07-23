import speech_recognition as sr
import pyttsx3
import open_ai_key as ../.env

r = sr.Recognizer()
tts_engine = pyttsx3.init()

voices = tts_engine.getProperty("voices")
tts_engine.setProperty("voice", voices[2].id)

# tts_engine.say("hello this is tts")
# tts_engine.runAndWait()


with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    while True:
        audio = r.listen(source)
        words = r.recognize_google(audio)
        if words:
            print(words)
            if words.lower() == "hello":
                tts_engine.say("say something")
                tts_engine.runAndWait()
                audio = r.listen(source)
                words = r.recognize_google(audio)
                if words:
                    tts_engine.say(words)
                    tts_engine.runAndWait()
            elif words == "stop":
                break
