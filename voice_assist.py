import speech_recognition as sr
from langdetect import detect
import pyttsx3
import datetime
import webbrowser
import os

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio).lower()
            print("User:", user_input)
            return user_input
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
            return ""

def detect_language(text):
    try:
        language = detect(text)
        return language
    except:
        return "unknown"

def learn_new_command():
    speak("Please provide the new command.")
    new_command = listen()
    
    if new_command:
        speak("What action or response should be associated with this command?")
        description = listen()
        if description:
            # Store the new command and its description in the data storage
            with open("commands.txt", "a") as f:
                f.write(f"{new_command}\t{description}\n")
            speak("New command learned and saved.")

def main():
    speak("Hello! I am Jarvis. How can I assist you today?")
    
    while True:
        user_input = listen()
        language = detect_language(user_input)
        
        if "hello" in user_input:
            speak("Hello! How can I help you?")
        elif "time" in user_input:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {current_time}.")
        elif "open website" in user_input:
            speak("Sure, please specify the website URL.")
            website = listen()
            webbrowser.open_new_tab(website)
        elif "open notepad" in user_input:
            os.system("notepad")
        elif "tell me a joke" in user_input:
            speak("Sure, here's a joke for you: Why don't scientists trust atoms? Because they make up everything!")
        elif "search" in user_input:
            speak("What would you like me to search for?")
            search_query = listen()
            webbrowser.open_new_tab(f"https://www.google.com/search?q={search_query}")
        elif "learn new command" in user_input:
            learn_new_command()
        elif language == "unknown":
            speak("I'm sorry, I couldn't detect the language.")
        elif language != "en":
            speak("I'm sorry, I currently support only English.")
        elif "exit" in user_input:
            speak("Goodbye!")
            break
        else:
            # Check if the user input matches a known command in the data storage
            with open("commands.txt", "r") as f:
                for line in f:
                    command, description = line.strip().split("\t")
                    if command in user_input:
                        speak(description)
                        break
                else:
                    speak("I'm sorry, I don't understand that command.")

if __name__ == "__main__":
    main()
