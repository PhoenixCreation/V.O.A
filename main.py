import speech_recognition as sr
import pyttsx3
import time
import webbrowser
import pywhatkit as kit
from bs4 import BeautifulSoup as bs
import requests
from tkinter import *
import os
import datetime
from config import RADIO_URL
from utils.whatsapp import send_message
from utils.weather import get_weather
engine = pyttsx3.init()
engine.setProperty('rate', 170)
r = sr.Recognizer()

gui = Tk()
gui.geometry("750x575")
frame = Frame(gui, bg="black")
frame.place(relwidth=1, relheight=0.9, rely=0.1)

last_command = []
if not os.path.isfile("VOA_log.txt"):
    fs = open("VOA_log.txt", "w")
    fs.close()
fs = open("VOA_log.txt", "r")
logs = fs.readlines()
fs.close()
for log in logs:
    log = log.replace("\n", "")
    log = log.split(", ")
    last_command.append(
        {"timestamp": log[0], "command": log[1], "output": " ".join(log[2:])})


def initiate():
    talk_back("How can I help you?")


def talk_back(speech):
    label = Label(frame, text=speech)
    label.pack()
    engine.say(speech)
    engine.runAndWait()


def handle_command(command):
    command = command.lower()
    last_command.append(
        {"timestamp": datetime.datetime.now(), "command": command})
    log_file = open("VOA_log.txt", "a")
    log_file.write(f'{datetime.datetime.now()}, {command}\n')
    log_file.close()
    commands = command.split()
    if len(commands) > 0 and "ver" in commands[0]:
        commands = commands[1:]
        if not len(commands) > 0:
            print("no command found")
        else:
            if commands[0] == "time":
                now = datetime.datetime.now()
                talk_back(now.strftime("it's %I : %M : %p"))
            elif commands[0] == "date":
                now = datetime.datetime.now()
                talk_back(now.strftime("%d %B %Y"))
            elif commands[0] == "timestamp":
                now = datetime.datetime.now()
                talk_back(now.strftime(
                    "It's %A,  %B %d today and it is %I : %M : %p now"))
            elif commands[0] == "who":
                if commands[1] == "am" or commands[1] == "i":
                    fs = open("profile.txt", "r")
                    profile = fs.readlines()
                    info = {}
                    for data in profile:
                        data = data.replace("\n", "")
                        data = data.split(", ")
                        info[data[0]] = data[1]
                    response = f'You are {"Mr." if info["gender"][0] == "m" else "Mrs."} {info["first_name"]} {info["middle_name"][0]}. {info["last_name"]} also known as {info["address_name"]}'
                    talk_back(response)
                elif commands[1] == "is":
                    name = " ".join(commands[2:])
                    info = kit.info(name, lines=1)
                    talk_back(info)
            elif commands[0] == "play":
                commands = commands[1:]
                if "radio" in commands:
                    webbrowser.open(RADIO_URL)
                elif "song" in commands:
                    commands.pop(commands.index('song'))
                    kit.playonyt(" ".join(commands))
                else:
                    kit.playonyt(" ".join(commands))
            elif commands[0] == "what":
                if commands[1] == "is":
                    commands = commands[2:]
                    res = kit.info(" ".join(commands), lines=1)
                    talk_back(res)
            elif commands[0] == "weather":
                date = "today"
                if "on" in commands:
                    date = " ".join(commands[commands.index("on")+1:])
                    commands = commands[:commands.index("on")]
                if "at" in commands:
                    date = " ".join(commands[commands.index("at")+1:])
                    commands = commands[:commands.index("at")]
                city = "surat"
                if "of" in commands:
                    city = " ".join(commands[commands.index("of")+1:])
                if "in" in commands:
                    city = " ".join(commands[commands.index("in")+1:])
                talk_back(get_weather(city, date))
            elif commands[0] == "send" and commands[1] == "whatsapp":
                commands = commands[2:]
                to_index = commands.index("to")
                message_index = -1
                if "message" in commands:
                    message_index = commands.index("message")
                that_index = -1
                if "that" in commands:
                    that_index = commands.index("that")
                if that_index != -1:
                    if message_index + 1 == that_index:
                        name = " ".join(commands[to_index+1:])
                        message = " ".join(commands[that_index+1:to_index])
                    else:
                        name = " ".join(commands[to_index+1:that_index])
                        message = " ".join(commands[that_index+1:])
                else:
                    name = " ".join(commands[to_index+1:])
                    message = " ".join(commands[message_index+1:to_index])
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
                    handle_command("veronika what is "+" ".join(commands))
                elif commands[0] == "joke":
                    joke = requests.get(
                        "https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
                    print(joke.json()["joke"])
                    talk_back(
                        "90% you won't get this joke but anyway here it is,     ")
                    talk_back(joke.json()["joke"])
            elif commands[0] == "test":
                talk_back("test successfully completed")
            else:
                talk_back("I didn't get that. Try again please.")


def take_command():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    print("recognizing audio...")

    try:
        command = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + command)
        info.set(command)
        handle_command(command)
    except sr.UnknownValueError:
        command = "Could not understand audio, Please try again"
        talk_back(command)
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        command = "something went wrong"
        talk_back(command)
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(e))


def handle_submit(event):
    handle_command(info.get())


def handle_up(event):
    if len(last_command) > 0:
        info.set(last_command.pop()["command"])


btn = Button(gui, text='Speak', fg='black', bg='red',
             command=lambda: take_command(), height=1, width=7)
btn.pack()
info = StringVar()
info_cont = Entry(gui, textvariable=info, width=700,
                  justify="center")
info_cont.bind("<Key-Return>", handle_submit)
info_cont.bind("<Key-Up>", handle_up)
info_cont.pack()
# initiate()
info_cont.focus()
gui.mainloop()
