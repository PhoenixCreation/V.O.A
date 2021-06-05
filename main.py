import speech_recognition as sr
import pyttsx3
import time
import webbrowser
import pywhatkit as kit
from bs4 import BeautifulSoup as bs
import requests
from tkinter import *
from config import RADIO_URL
from whatsapp_send import send_message

engine = pyttsx3.init()
engine.setProperty('rate', 170)
r = sr.Recognizer()

# gui = Tk()
# gui.geometry("270x150")
# button1 = Button(gui, text=' 1 ', fg='black', bg='red', height=1, width=7)
# button1.pack()
# w = Label(gui, text='GeeksForGeeks.org!')
# w.pack()
# gui.mainloop()


def initiate():
    talk_back("How can I help you?")


def talk_back(speech="No speech provided"):
    engine.say(speech)
    engine.runAndWait()


def take_command():
    pass
    # with sr.Microphone() as source:
    #     print("Say something!")
    #     audio = r.listen(source)

    # print("recognizing audio...")

    # try:
    #     command = r.recognize_google(audio)
    #     error = ""
    #     print("Google Speech Recognition thinks you said " + command)
    # except sr.UnknownValueError:
    #     command = ""
    #     error = "Could not understand audio 0"
    #     print("Google Speech Recognition could not understand audio")
    # except sr.RequestError as e:
    #     command = ''
    #     error = "something went wrong -1"
    #     print(
    #         "Could not request results from Google Speech Recognition service; {0}".format(e))
    # return command,error


def handle_command(command):
    commands = command.split()
    if len(commands) > 0 and "ver" in commands[0]:
        commands = commands[1:]
        if not len(commands) > 0:
            print("no command found")
        else:
            if commands[0] == "play":
                commands = commands[1:]
                if "radio" in commands:
                    webbrowser.open(RADIO_URL)
                elif "song" in commands:
                    commands.pop(commands.index('song'))
                    kit.playonyt(" ".join(commands))
                else:
                    kit.playonyt(" ".join(commands))
            elif commands[0] == "what" and commands[1] == "is":
                commands = commands[2:]
                res = kit.info(" ".join(commands), lines=1)
                talk_back(res)
            elif commands[0] == "weather":
                city = "surat"
                if "of" in commands:
                    city = " ".join(commands[commands.index("of"):])

                # creating url and requests instance
                url = "https://www.google.com/search?q="+"weather"+city
                html = requests.get(url).content

                # getting raw data
                soup = bs(html, 'html.parser')
                temp = soup.find(
                    'div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
                # this conatains time and sky description
                data = soup.find(
                    'div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

                # format the data
                data = data.split('\n')
                sky = data[1]
                print(temp)
                print(sky)
                talk_back(
                    f'Temperature of {city} is {temp[:2]} degree celcius and sky is {sky}')
            elif commands[0] == "send" and commands[1] == "whatsapp":
                commands = commands[2:]
                to_index = commands.index("to")
                name = commands[to_index+1:]
                name = " ".join(name)
                message = " ".join(
                    commands[commands.index("message")+1:commands.index("to")])
                talk_back(send_message(name, message))
            elif commands[0] == "tell":
                commands = commands[1:]
                if 'me' in commands:
                    commands.pop(commands.index('me'))
                if 'a' in commands:
                    commands.pop(commands.index('a'))
                if commands[0] == "what" and commands[1] == "is":
                    commands.pop(0)
                    commands.pop(0)
                    print(" ".join(commands))
                    handle_command("veronika what is "+" ".join(commands))
                elif commands[0] == "joke":
                    joke = requests.get(
                        "https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
                    print(joke.json()["joke"])
                    talk_back(
                        "90% you won't get this joke but anyway here it is,     ")
                    talk_back(joke.json()["joke"])
