import os
import sys
import time
sys.stdout = open(os.devnull, 'w')
import speech_recognition as sr
from gtts import gTTS
import pygame
import g4f
from g4f.client import Client
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
sys.stdout = sys.__stdout__
# Function to print text with a specified delay
def type_print(text, delay=0.01):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

type_print("~~~~~~~~~~~Nexu.ai By Parth Sadaria~~~~~~~~~~~")

# Function to get audio input from the user
def get_audio():
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
        return None
    except sr.RequestError:
        print("Sorry, I couldn't request results. Please check your internet connection.")
        return None

# Function to speak text with a specific voice
def speak(text, lang='en', gender='male'):
    lang_code = 'en'
    if lang == 'en':
        lang_code = 'en-us' if gender == 'male' else 'en-uk'
    elif lang == 'es':
        lang_code = 'es-es' if gender == 'male' else 'es-la'

    tts = gTTS(text=text, lang=lang_code, slow=False)
    tts.save("response.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    os.remove("response.mp3")


# Function to handle other actions based on user input
# Function to handle other actions based on user input
def handle_other_actions(user_input, history):
    formatted_history = format_history(history)
    default_prompt = (f"Write a Python pyautogui script and to check your steps. If "
                      f"you are going correctly , write a & no comments & also write python at start of each script with a 2-second time sleep after each step to User:-{user_input}. "
                      f"Here is the conversation history for your reference:\n\n{formatted_history}\n\nNow you have to continue this convo.")

    client = Client(
    provider = 	g4f.Provider.You
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": default_prompt}],
    )
    ai_response = response.choices[0].message.content
    
    code_start = ai_response.find("```")
    code_end = ai_response.rfind("```")
    
    if code_start != -1 and code_end != -1 and code_end > code_start:
        code_block = ai_response[code_start + 3:code_end].strip()
        code_lines = code_block.split('\n')
        if code_lines and code_lines[0].strip().startswith("python"):
            code_lines[0] = ' '.join(code_lines[0].split()[1:])  # Remove the first word if it is "python"
        new_code_block = "\n".join(code_lines)
        ai_response = ai_response[:code_start + 3] + new_code_block + ai_response[code_end:]
        try:
            exec(new_code_block)
        except Exception as e:
            print("Error executing generated code:", e)
    else:
        print(ai_response)

    history.append({"role": "assistant", "content": ai_response})



# Function to handle chat interactions
def chat(user_input, history):
    formatted_history = format_history(history)
    prompt = f"History '{formatted_history}'\n\n Now respond to this in shortest way possible (and also the right way)AND A REMINDER THAT U R NOT ANY AI.. YOURE NEXU AI BY PARTH SADARIA DONT MENTION IT ONLY IF USER ASKS \n User:-"

    client = Client(	g4f.Provider.MetaAI
    )
    messages = [{"role": "user", "content": prompt+user_input}]
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages, stream=True)

    for completion in chat_completion:
        response = completion.choices[0].delta.content or ""
        print(response, end="", flush=True)
    print("\n")

    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": response})

# Function to format the chat history
def format_history(history):
    formatted = ""
    for entry in history:
        if entry["role"] == "user":
            formatted += f"User:- {entry['content']}\n"
        else:
            formatted += f"Ai:- {entry['content']}\n"
    return formatted

# Main program loop
def main():
    input_method = input("Would you like to speak or type your input? (speak/type): ").lower()
    while input_method not in ["speak", "type"]:
        print("Invalid input method. Please choose 'speak' or 'type'.")
        input_method = input("Would you like to speak or type your input? (speak/type): ").lower()

    chatorauto = input("Would you like to chat or give AI tasks? (chat/auto): ").lower()
    while chatorauto not in ["chat", "auto"]:
        print("Invalid choice. Please choose 'chat' or 'auto'.")
        chatorauto = input("Would you like to chat or give AI tasks? (chat/auto): ").lower()

    history = []

    while True:
        if input_method == "speak":
            user_input = get_audio()
            if not user_input:
                continue
        else:
            user_input = input("Ask AI: ")

        if user_input.lower() == "exit":
            print("Exiting...")
            break

        if chatorauto == "auto":
            handle_other_actions(user_input, history)
        else:
            chat(user_input, history)

if __name__ == "__main__":
    main()
