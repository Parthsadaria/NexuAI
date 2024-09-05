import os
import sys
import time
sys.stdout = open(os.devnull, 'w')
import speech_recognition as sr
from gtts import gTTS
import pygame
import g4f
import random
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

def hacker_intro_effect(text, delay=0.1, iterations=10):
    chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    def random_char():
        return random.choice(chars)
    
    # Create a list of characters from the text
    text_chars = list(text)
    display_chars = ['_' for _ in text_chars]  # Start with placeholder characters
    
    sys.stdout.write("\r" + " " * len(text))  # Clear line
    sys.stdout.flush()
    
    for i in range(len(text_chars)):
        for _ in range(iterations):
            display_chars[i] = random_char()
            sys.stdout.write("\r" + ''.join(display_chars))
            sys.stdout.flush()
            time.sleep(delay)
        display_chars[i] = text_chars[i]  # Reveal the actual character
        sys.stdout.write("\r" + ''.join(display_chars))
        sys.stdout.flush()
        time.sleep(delay)  # Short pause before the next character
    
    sys.stdout.write("\n")
    sys.stdout.flush()

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
def handle_other_actions(user_input, history):
    formatted_history = format_history(history)
    default_prompt = (f"You are a fast, efficient terminal assistant. Your task is to: - Keep any explanatory text extremely brief and concise. - Place explanatory text before the code block. NOTE:- Dont say anthing like 'I'm ready to assist. You want me to write a Python pyautogui script to open (blahblah).' always say like opening chrome opening this blah blah"
                      f"Write a Python pyautogui script and to check your steps Respond with a VERY brief explanation followed by pyautogui code. If "
                      f"you are going correctly , write a & no comments & also write python at start of each script with a **2-second time** sleep after each step to User:-{user_input}. "
                      f"Here is the conversation history for your reference:\n\n{formatted_history}\n\nNow you have to continue this and talk like assistant DONT GIVE CODE IN PARTS ALL IN ONE AND U WILL NOT SAY ANYTHING AFTER SCRIPT & ALWAYS USE CMD(win+r togeather one) TO PERFORM MOST TASKS"
                        f"\nLike If user said open (appname) always reply with opening (appname)")
    client = Client(
        provider=g4f.Provider.Blackbox
    )
    response = client.chat.completions.create(
        model="blackbox",
        messages=[{"role": "user", "content": default_prompt}],
    )
    ai_response = response.choices[0].message.content

    code_start = ai_response.find("```")
    code_end = ai_response.rfind("```")
    
    if code_start != -1 and code_end != -1 and code_end > code_start:
        code_block = ai_response[code_start + 3:code_end].strip()
        remaining_text = ai_response[:code_start] + ai_response[code_end + 3:]

        # Print remaining text before executing code
        print(remaining_text.strip())

        code_lines = code_block.split('\n')
        if code_lines and code_lines[0].strip().startswith("python"):
            code_lines[0] = ' '.join(code_lines[0].split()[1:])  # Remove the first word if it is "python"
        new_code_block = "\n".join(code_lines)
        
        # Execute the code block
        try:
            exec(new_code_block)
        except Exception as e:
            print(ai_response)
    
    history.append({"role": "assistant", "content": ai_response})

# Function to generate images based on user input
def generate_image(prompt):
    # Create the URL using the given format
    image_url = f"https://image.pollinations.ai/prompt/{prompt}?model=flux"
    type_print("Generating...")
    time.sleep(random.randint(1,5))
    type_print(f"Redirecting...")
    time.sleep(random.randint(1,2))
    # Open the URL in the default web browser
    import webbrowser
    webbrowser.open(image_url)

# Function to handle chat interactions
def chat(user_input, history):
    formatted_history = format_history(history)
    prompt = f"conversation history '{formatted_history}'\n\n Now respond to this in shortest way possible (and also the right way)AND A REMINDER THAT U R NOT ANY SIMPLE AI.... UR NEXU.AI BY PARTH SADARIA WHICH IS THE SMARTEST AI IN WORLD DONT MENTION IT ONLY IF USER ASKS AND ALSO DONT MENTION HISTORY JUST REMEMBER IT AND DONT SAY ANYTHING ABOUT IT\n User:-"

    client = Client(g4f.Provider.MetaAI)
    messages = [{"role": "user", "content": prompt+user_input}]
    chat_completion = client.chat.completions.create(
        model="",
        messages=messages, stream=True)

    for completion in chat_completion:
        response = completion.choices[0].delta.content or ""
        print(f"\033[1;34m{response}\033[0m", end="", flush=True)

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

def main():
    hacker_intro_effect("~~~NexuAI by Parth Sadaria~~", delay=0.00001, iterations=5)
    input_method = input("Would you like to speak or type your input? (speak/type): ").lower()
    while input_method not in ["speak", "type"]:
        print("Invalid input method. Please choose 'speak' or 'type'.")
        input_method = input("Would you like to speak or type your input? (speak/type): ").lower()

    history = []

    # List of keywords that trigger the auto mode
    task_keywords = [
        "do this", "perform", "run", "execute", "task", "code", 
        "start", "create", "open", "launch", "begin", "initiate", 
        "write", "generate", "calculate", "find", "show", "display", 
        "complete", "finish", "make", "build", "construct", "simulate", 
        "draw", "design", "image", "picture", "generate image", 
        "imagine", "draw", "generate a image", "create image", "produce image"
    ]

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

        # Check if the input suggests a task, command, or image generation
        if any(keyword in user_input.lower() for keyword in task_keywords):
            if any(img_keyword in user_input.lower() for img_keyword in ["image", "picture", "generate image", "imagine", "draw", "generate a image", "create image", "produce image"]):
                generate_image(user_input)
            else:
                handle_other_actions(user_input, history)
        else:
            chat(user_input, history)

if __name__ == "__main__":
    main()
