import os
import sys
sys.stdout = open(os.devnull, 'w')
import time
import speech_recognition as sr
from gtts import gTTS
import pygame
import pyautogui
import g4f
from g4f.client import Client
from g4f.cookies import set_cookies

# set_cookies(".bing.com", {
#   "_U": "cookie value"
# })
# set_cookies(".google.com", {
#   "__Secure-1PSID": "g.a000ighQwC-BF7hBQdbXy8CWhA3dCG1DL4vKReffc1QeFB8MKMmDOf03sbKtt6A1XnXmdn0e8wACgYKAWwSAQASFQHGX2MiOjQY5HWMHn6qBHE2tq6p9BoVAUF8yKpFzq5YVOf1o44zYUkfO9Vj0076",
#  "__Secure-1PSIDTS": "sidts-CjEB7F1E_KB2o2BaTC8jqBuVDO4gHMi-rbb0ErZ3S9E-p61b43eiQUa62xlJ_pL3zmZwEAA",
#   "__Secure-1PSIDCC": "AKEyXzU8C_3BapwKKFMF-8s-GfcSuMtn2udoQpad_73AHbHun2ZfWUGNA0dQNVfeuNtq3S69KfY" 
# })


sys.stdout = sys.__stdout__
# Function to print text with a specified delay
def type_print(text, delay=0.01):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()
type_print("~~~~~~~~~~~KaamChorGPT By Parth Sadaria~~~~~~~~~~~")
# Function to get audio input from the user
def get_audio():
    while True:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Adjusting for ambient noise. Please wait...")
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            user_input = recognizer.recognize_google(audio)
            print("You said:", user_input)
            return user_input
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Please try again.")
        except sr.RequestError:
            print("Sorry, I couldn't request results. Please check your internet connection.")

# Function to speak text
# Function to speak text
# Function to speak text with a specific voice
def speak(text, lang='en', gender='male'):
    if lang == 'en':
        if gender == 'male':
            lang_code = 'en-us'
        elif gender == 'female':
            lang_code = 'en-uk'
    elif lang == 'es':
        if gender == 'male':
            lang_code = 'es-es'
        elif gender == 'female':
            lang_code = 'es-la'
    else:
        lang_code = 'en-us'  # Default to English male voice

    tts = gTTS(text=text, lang=lang_code, slow=False)
    tts.save("response.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    os.remove("response.mp3")


def handle_other_actions(user_input):
    default_prompt = "You are an excellent Python coder, proficient in utilizing all available powers and capabilities of the language. Write the most perfect Python code imaginable, utilizing advanced techniques, libraries, and best practices to accomplish any task with efficiency and elegance. Your goal is to showcase the epitome of Python programming excellence, leaving no room for improvement.Now Your First task is to write a python pyautogui and to check your steps if u are going correct write a script with 4 sec time sleep after each step to" + user_input 
    client = Client()
    response = client.chat.completions.create( 
        model="gpt-3.5-turbo",
        # provider= g4f.Provider.ChatForAi,
        messages=[{"role" : "user", "content": default_prompt}],
    )
    ai_response = response.choices[0].message.content
    code_start = ai_response.find("```")
    code_end = ai_response.rfind("```")
    if code_start != -1 and code_end != -1 and code_end > code_start:
        code = ai_response[code_start + 3:code_end].split(maxsplit=1)[1]
        try:
            exec(code)
        except Exception as e:
            print("Error executing generated code:", e)
    else:
        exec(ai_response)

def chat(user_input):
        client = Client()
       
        chat_completion = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}], stream=True)
       
        for completion in chat_completion:
            print(completion.choices[0].delta.content or "", end="", flush=True)
        
        print("/n")
        # type_print(ai_response)

        
input_method = input("(speak/type): ").lower()
chatorauto = input("Want to chat or give AI tasks (chat/auto): ").lower()

while input_method not in ["speak", "type"]:
    print("Invalid input method. Please choose 'speak' or 'type'.")
    input_method = input("Would you like to speak or type your input? (speak/type): ").lower()

while chatorauto in ["chat", "auto"]:
    if chatorauto == "auto":
        while True:
            if input_method == "speak":
                user_input = get_audio()
            elif input_method == "type":
                user_input = input("Ask AI: ")

            if user_input.lower() == "exit":
                print("Exiting...")
                sys.exit()

            handle_other_actions(user_input)
    elif chatorauto == "chat":
        while True:
            if input_method == "speak":
                user_input = get_audio()
            elif input_method == "type":
                user_input = input("Ask AI: ")

            if user_input.lower() == "exit":
                print("Exiting...")
                sys.exit()

            chat(user_input)
    else:
        print("Invalid choice: ", chatorauto)
        chatorauto = input("Would you like to chat or give AI tasks (chat/auto): ").lower()
