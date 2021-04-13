import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import pafy
from selenium import webdriver
import pywhatkit as kit
# import time
# import pygame
import file_search
import requests
from pprint import pprint
from bs4 import BeautifulSoup

try:
    from pytube import YouTube
    from pytube import Playlist
except Exception as e:        # just in case the package ain't available at the moment
    print("Some Modules are Missing {}".format(e))

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)  # select voice


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 17:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am here Sir. Please tell me how may I help you")


def playonyt1(title):
    '''Opens YouTube video with following title'''
    url = 'https://www.youtube.com/results?q=' + title
    sc = requests.get(url)
    sctext = sc.text
    soup = BeautifulSoup(sctext, "html.parser")
    songs = soup.findAll("div", {"class": "yt-lockup-video"})
    song = songs[0].contents[0].contents[0].contents[0]
    songurl = song["href"]
    # web.open("https://www.youtube.com"+songurl)
    return "https://www.youtube.com" + songurl


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception:
        # print(e)    
        print("Say that again please...")
        return "None"
    return query


def takeCommand1():
    r1 = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r1.pause_threshold = 1
        audio1 = r1.listen(source)
    try:
        print("Recognizing...")
        query1 = r1.recognize_google(audio1, language='en-in')
        print(f"User said: {query1}\n")

    except Exception:
        # print(e)    
        print("Say that again please...")
        return "None"
    return query1


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('i_am_someone@gmail.com', 'something_it_is')      #your email id and password here
    server.sendmail('i_am_someone@gmail.com', to, content)         #your email id
    server.close()


def print_weather(result, city):
    print("{}'s temperature: {}°C ".format(city, result['main']['temp']))
    print("Wind speed: {} m/s".format(result['wind']['speed']))
    print("Description: {}".format(result['weather'][0]['description']))
    print("Weather: {}".format(result['weather'][0]['main']))
    speak("{}'s temperature: {}°C ".format(city, result['main']['temp']))
    speak("Wind speed: {} meters per seconds".format(result['wind']['speed']))
    speak("Description: {}".format(result['weather'][0]['description']))
    speak("Weather: {}".format(result['weather'][0]['main']))


while True:
    query1 = takeCommand1().lower()
    if 'initialise' in query1:
        if __name__ == "__main__":
            wishMe()
            while True:
                # if 1:
                query = takeCommand().lower()

                # executing tasks based on query
                if 'wikipedia' in query:
                    speak('Searching Wikipedia...')
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=3)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)

                elif 'open youtube' in query:
                    webbrowser.open("youtube.com")

                elif 'open google' in query:
                    webbrowser.open("google.com")

                elif 'open stack overflow' in query:
                    webbrowser.open("stackoverflow.com")


                elif 'play music' in query:
                    music_dir = 'C:\\Users\\Sanjay\\Music'
                    songs = os.listdir(music_dir)  # storing the directory containing all the songs
                    for song in songs:
                        if song.endswith(".mp3") | song.endswith(
                                ".mp4"):  # checking for songs ending with certain extensions
                            print(song)
                            os.startfile(os.path.join(music_dir, song))  # opening using default application set


                elif 'play video' in query:  # same as for songs
                    video_dir = 'C:\\Users\\Sanjay\\Videos'
                    videos = os.listdir(video_dir)
                    for video in videos:
                        if video.endswith(".mp4"):
                            print(video)
                            os.startfile(os.path.join(video_dir, video))


                elif 'time' in query:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")
                    speak(f"Sir, the time is {strTime}")

                elif 'quit' in query or 'bye' in query or 'exit' in query:
                    speak("Quitting sir . Thanks for your time .")
                    break  # breaking out so that it would still wait to take command to initialise

                elif 'open code' in query:
                    speak("Opening visual studio code")
                    codePath = "C:\\Users\\Sanjay\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                    os.startfile(codePath)

                elif 'notepad' in query:
                    speak("Opening notepad")
                    codepath = "C:\\Windows\\system32\\notepad.exe"
                    os.startfile(codepath)



                elif 'send a mail' in query:
                    try:
                        speak("What should I say?")
                        content = takeCommand()
                        to = "whosoever_it_is.com"           #Enter the email id of the person you want to send mail to
                        sendEmail(to, content)  # calling the mail function
                        speak("Email has been sent!")  # confirmation
                    except Exception as e:
                        print(e)
                        speak("Sorry Sir. I am not able to send this email")

                elif 'download video' in query:
                    speak("Would you provide me the link or name sir ")
                    query = takeCommand().lower()
                    if 'link' in query:
                        url = "https://www.youtube.com/watch?v=4H7lvZS5TT8"
                        ytd = YouTube(url).streams.first().download(
                            "C:\\Users\\Sanjay\\Videos")  # downloading with the provided link
                        speak("downloading sir")
                        print(ytd)


                    elif 'name' in query:
                        speak("Which song should i download ")
                        a = takeCommand().lower()
                        # a=kit.playonyt(str(query))
                        if (query != "None"):
                            # ytd=pafy.new(playonyt(str(a)))
                            # ytd=YouTube(playonyt(str(a)).streams.first().download("C:\\Users\\Sanjay\\Videos")      #downloading with the provided link
                            ytd = pafy.new(kit.playonyt(str(a)))
                            speak("downloading sir")
                            bestvideo = ytd.getbestvideo()  # getting the top quality audio
                            bestvideo.download("C:\\Users\\Sanjay\\Videos")
                            print(bestvideo)
                            # print(ytd)
                    speak("The video has been downloaded")

                elif 'download song' in query:
                    speak("Would you provide me the link or name sir ")
                    query = takeCommand().lower()
                    if 'link' in query:
                        url = "https://www.youtube.com/watch?v=yxzD6hitHds"
                        ytd = pafy.new(url)
                        speak("downloading sir")
                        bestaudio = ytd.getbestaudio()  # getting the top quality audio
                        bestaudio.download("C:\\Users\\Sanjay\\Music")
                        print(bestaudio)


                    elif 'name' in query:
                        speak("Which song should i download ")
                        a = takeCommand().lower()
                        # a=kit.playonyt(str(query))
                        if (query != "None"):
                            ytd = pafy.new(kit.playonyt(str(a)))
                            speak("downloading sir")
                            bestaudio = ytd.getbestaudio()  # getting the top quality audio
                            bestaudio.download("C:\\Users\\Sanjay\\Music")
                            print(bestaudio)

                    speak("The song has been downloaded")


                elif 'shutdown pc' in query:

                    try:
                        speak("Are you sure about shutting down the pc")
                        command = takeCommand().lower()
                        if (command == 'yes'):
                            speak("shutting down in 60 seconds")
                            os.system("shutdown /s /t 20")  # setting the command and timer as well
                    except Exception as e:
                        print(e)
                        speak("Sorry Sir. I am not able to shutdown the pc at the moment")

                elif 'cancel shutdown' in query:
                    speak("aborting shut down")
                    os.system("shutdown /a")

                elif 'restart' in query:
                    try:
                        speak("Are you sure about restarting the pc")
                        comand = takeCommand().lower()
                        if (comand == 'yes'):
                            speak("restarting in 15 seconds")
                            os.system("shutdown /r /t 15")


                    except Exception as e:
                        print(e)
                        speak("Sorry Sir. I am not able to restart the pc at the moment")

                elif 'log off' in query:
                    speak("logging off")
                    os.system("shutdown /l ")

                elif 'jarvis' in query:
                    speak("Listening sir .")

                elif 'what can you do' in query:
                    speak("Anything you say sir . I will try my best ")


                elif 'search pc' in query or 'search desktop' in query or 'search laptop' in query:
                    speak("What should i search for")
                    comand = takeCommand().lower()
                    file_search.set_root(
                        "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs")  # root folder containing all the main files
                    files = file_search.searchFile(comand)  # searching the file
                    for file in files:
                        if file.endswith(".lnk"):  # application format
                            print(file)
                            os.startfile(file)


                elif 'search' in query:
                    browser = webdriver.Chrome(
                        "chromedriver")  # searching using the chromewebdriver afterinstalling and placing it in the same folder as this file
                    query = query.replace("search", "")
                    speak("searching " + " " + query)
                    for i in range(1):
                        matched_elements = browser.get("https://www.google.com/search?q=" + query + "&start=" + str(
                            i))  # opening the search result i google's url

                elif 'youtube' in query:
                    query = query.replace("youtube", "")
                    kit.playonyt(str(query))  # plays the first search result that matches with the query
                    while True:
                        break


                elif 'weather' in query:
                    speak("Which city?")
                    city = takeCommand()
                    print()
                    try:
                        city1 = 'q=' + city
                        res = requests.get(
                            'http://api.openweathermap.org/data/2.5/weather?' + city1 + '&APPID=b35975e18dc93725acb092f7272cc6b8&units=metric')
                        w_data = res.json()
                        print_weather(w_data, city)
                        print()
                    except:
                        print('City name not found...')

        continue  # after quiting breaking out of the loop so that the file could get initialise again
