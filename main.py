import time
import speech_recognition as sr
import webbrowser
import pyttsx3
import songs
import pyjokes as j
import requests
import client
import variables as v


recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('voice', "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0")

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(text):
    command = text.lower()
    
    if "shutdown" in command:
        speak(f"${v.name} Shutting Down....")
        print(f"${v.name} Shutting Down....")
        exit(0)
    elif "open google" in command:
        print(command)
        webbrowser.open("https://www.google.com")
    elif "open youtube" in command:
        print(command)
        webbrowser.open("https://www.youtube.com")
    elif "open instagram" in command:
        webbrowser.open("https://www.instagram.com")
    elif "open gmail" in command:
        webbrowser.open("https://www.gmail.com")
    elif command.startswith("play"):
        s = command.split(" ")[1]
        link = songs.song.get(s)
        if link:
            print(link)
            webbrowser.open(link)
        else:
            speak("Song not found")
    elif "joke" in command:
        speak("Loading joke...")
        joke = j.get_joke()
        time.sleep(1)
        speak(joke)
    elif "news" in command:
        response = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey='+v.news_api)
        if response.status_code == 200:
            data=response.json()
            headlines = [article["title"] for article in data["articles"]]
            for i in headlines[:3]:
                speak(i)
        else:
            speak(f"Failed to retrieve data. Status code: {response.status_code}")
    else :
        #if you want to use your own local model uncomment the below code and comment the response code
        # stream = ollama.chat(
        #     model='gemma2:2b',
        #     messages=[{'role': 'user', 'content': command}],stream=True,)
        # for chunk in stream:
        #     if 'message' in chunk and 'content' in chunk['message']:
        #         speak(chunk['message']['content'])
        #     else:
        #         # Handle the case where the expected keys are not present
        #         speak("Received unexpected data format.")
        
        
        response=client.getResponse(command)
        for chunk in response:
            if chunk.text=="*" and chunk.text=="**":
                pass
            else:
                print(chunk.text)
                speak(chunk.text)
        


if __name__ == "__main__":
    speak(f"Initializing ${v.name}...")
    
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("Recognizing....")
            word = recognizer.recognize_google(audio)
            print(word)
            if word.lower() == f"${v.name}":
                speak("Yes sir?")
                with sr.Microphone() as source:
                    print(f"${v.name} Activated....")
                    audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                processCommand(text)
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError:
            print("Could not request results; check your network connection.")
        except Exception as e:
            print(f"An error occurred: {e}")
