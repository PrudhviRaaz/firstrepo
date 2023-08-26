from gtts import gTTS
import os
import speech_recognition as sr
from langdetect import detect
import webbrowser
import datetime

recognizer = sr.Recognizer()

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

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')
    os.system('mpv output.mp3')  # Make sure you have 'mpv' installed in Termux

def main():
    speak("Hello! I am your basic voice assistant. How can I assist you today?")
    
    while True:
        user_input = listen()
        language = detect(user_input)
        
        if "hello" in user_input:
            speak("Hello! How can I help you?")
        elif "time" in user_input:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {current_time}.")
        elif "search" in user_input:
            speak("What would you like me to search for?")
            search_query = listen()
            webbrowser.open_new_tab(f"https://www.google.com/search?q={search_query}")
        elif "exit" in user_input:
            speak("Goodbye!")
            break
        else:
            speak("I'm sorry, I don't understand that command.")

if __name__ == "__main__":
    main()
