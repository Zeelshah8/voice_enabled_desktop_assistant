import openai
import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import wikipedia
import os
import time
from apikey import api_data

openai.api_key=api_data

# Set  OpenAI API key



def Reply(question):
    messages = [
        {"role": "system", "content": "You are Jarvis, an AI assistant."},
        {"role": "user", "content": question}
    ]
    max_retries = 5
    retry_delay = 1  # Start with a 1-second delay

    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                #stop=['\stop'],
                max_tokens=2000
            )
            answer = response.choices[0].message['content'].strip()
            return answer
        except openai.error.RateLimitError as e:
            print(f"Rate limit exceeded. Retrying in {retry_delay} sec...")
            time.sleep(retry_delay)
            retry_delay *= 1  # Exponential backoff
        except openai.error.OpenAIError as e:
            print(f"An error occurred: {e}")
            return #"Error: Unable to process the request."
    #print("Failed to get a response after multiple retries.")
    return #"Error: Rate limit exceeded."

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning! Hello, how can I assist you today?")

    elif hour>=12 and hour<18:
        speak("Good Afternoon! Hello, how can I assist you today?")   

    else:
        speak("Good Evening! Hello, how can I assist you today?")
      


def takeCommand():#It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query} \n")

    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand().lower()
        # if query == "None":
        #      continue
        # ans = Reply(query)
        # print(ans)

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open wikipedia' in query:
            webbrowser.open("wikipedia.com")

        elif 'learn about django' in query:
            webbrowser.open('https://www.w3schools.com/django/')

        elif 'play music' in query:
            music_dir = 'D:\Music\Songs'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[13]))

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S") 
            print(f"the time is {strTime}")
            speak(f"the time is {strTime}")

        elif 'shutdown pc' in query:
            os.system("shutdown /r /t 1")   

        elif 'restart pc' in query:
           os.system("restart /r /t 1")   

        elif 'goodbye' in query or 'bye' in query:
            print("goood byyee..")
            speak("Goodbye!")
            break
        
