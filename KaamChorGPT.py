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

# Function to open or close an application
def manage_application(app_name, action):
    if action == "open":
        pyautogui.press("win")
        time.sleep(0.5)
        pyautogui.write(app_name)
        pyautogui.press("enter")
        type_print("Opening " + app_name)
        speak("Opening " + app_name)
    elif action == "close":
        app_name = app_name.replace(".exe", "")
        os.system("taskkill /f /im " + app_name)
        type_print("Closing " + app_name)
    else:
        type_print("Invalid action")

# Function to move the mouse left by a small distance
def move_mouse_left():
    current_x, _ = pyautogui.position()
    pyautogui.moveTo(current_x - 50, None, duration=0.25)

# Function to move the mouse right by a small distance
def move_mouse_right():
    current_x, _ = pyautogui.position()
    pyautogui.moveTo(current_x + 50, None, duration=0.25)

# Function to move the mouse up by a small distance
def move_mouse_up():
    _, current_y = pyautogui.position()
    pyautogui.moveTo(None, current_y - 50, duration=0.25)

# Function to move the mouse down by a small distance
def move_mouse_down():
    _, current_y = pyautogui.position()
    pyautogui.moveTo(None, current_y + 50, duration=0.25)
def handle_other_actions(user_input):
    default_prompt = "write a python pyautogui script to" + user_input + "with time sleep(1) after each step so my pc can load all shit properly "
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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role" : "user", "content": user_input}],
        )
        ai_response = response.choices[0].message.content
        speak(ai_response)
        type_print(ai_response)


    # Extracting code between triple backticks and removing the first word


input_method = input("(speak/type): ").lower()
chatorauto = input("Want to chat or give ai tasks(chat/auto): ").lower()

while input_method not in ["speak", "type"]:
    print("Invalid input method. Please choose 'speak' or 'type'.")
    input_method = input("Would you like to speak or type your input? (speak/type): ").lower()

while chatorauto in ["chat", "auto"]:
    if chatorauto == "auto":
        while True:
            if input_method == "speak":
                user_input = get_audio()
            elif input_method == "type":
                user_input = input("Ask Ai: ")

            if user_input.lower() == "exit":
                print("Exiting...")
                break

            if "move left" in user_input.lower():
                move_mouse_left()
            elif "move right" in user_input.lower():
                move_mouse_right()
            elif "move up" in user_input.lower():
                move_mouse_up()
            elif "move down" in user_input.lower():
                move_mouse_down()
            else:
                handle_other_actions(user_input)
    elif chatorauto == "chat":
        while True:
            if input_method == "speak":
                user_input = get_audio()
            elif input_method == "type":
                user_input = input("Ask Ai: ")

            if user_input.lower() == "exit":
                print("Exiting...")
                input_method="exit"
                break

            if "move left" in user_input.lower():
                move_mouse_left()
            elif "move right" in user_input.lower():
                move_mouse_right()
            elif "move up" in user_input.lower():
                move_mouse_up()
            elif "move down" in user_input.lower():
                move_mouse_down()
            else:
                chat(user_input)
    else:
        print("Invalid choice: ", chatorauto)
        chatorauto = input("Would you like to chat or give ai tasks(chat/auto): ").lower()
    if input_method == "exit":
        break
