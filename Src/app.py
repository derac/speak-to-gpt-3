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
bot_explanation = "The following is a conversation with Socrates. Socrates was a Greek philosopher from Athens who is credited as a founder of Western philosophy and the first moral philosopher of the Western ethical tradition of thought."
bot_name = "Socrates"
start_prompt = f"{bot_explanation}\n\nHuman: Hello, who are you?\n{bot_name}: I am Socrates. You can ask me anything.\n"

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print(start_prompt)
    while True:
        try:
            audio = r.listen(source)
            words = r.recognize_google(audio)
            print(f"Human: {words}")
            human_words.append(words)
            response = openai.Completion.create(
                engine="davinci",
                prompt=f"{start_prompt}{chat_history}Human: {words}\nAI:",
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.6,
                stop=["\n", " Human:", f" {bot_name}:"],
            )
            ai_words.append(response["choices"][0]["text"])
            human_words, ai_words = human_words[-5:], ai_words[-5:]
            chat_history = "".join(
                f"Human:{human}\n{bot_name}:{ai}\n"
                for human, ai in zip(human_words, ai_words)
            )
            print(f'{bot_name}:{response["choices"][0]["text"]}\n')
            tts_engine.say(response["choices"][0]["text"])
            tts_engine.runAndWait()
        except:
            ...
