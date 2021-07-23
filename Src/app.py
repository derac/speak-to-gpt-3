import os

import pyttsx3
import openai

import speech_recognition as sr

r = sr.Recognizer()
tts_engine = pyttsx3.init()

openai_api_key = os.getenv("OPENAI_API_KEY")
voices = tts_engine.getProperty("voices")
tts_engine.setProperty("voice", voices[0].id)

human_words = []
ai_words = []
chat_history = ""

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Starting talking to your computer now...\n")
    while True:
        try:
            audio = r.listen(source)
            words = r.recognize_google(audio)
            print(f"You: {words}")
            human_words.append(words)
            response = openai.Completion.create(
                engine="davinci",
                prompt=f"The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\n{chat_history}Human: {words}\nAI:",
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.6,
                stop=["\n", " Human:", " AI:"],
            )
            ai_words.append(response["choices"][0]["text"])
            human_words, ai_words = human_words[-5:], ai_words[-5:]
            chat_history = "".join(
                f"Human:{human}\nAI:{ai}\n" for human, ai in zip(human_words, ai_words)
            )
            print(f'CPU:{response["choices"][0]["text"]}')
            tts_engine.say(response["choices"][0]["text"])
            tts_engine.runAndWait()
        except:
            ...
