# SpeechRecognition module for speech to text transformation
import speech_recognition as sr
# pyttsx3 module for offline text to speech transformation
import pyttsx3
# gTTS module for online text to speech transformation for better quality video
from gtts import gTTS
# playsound module for playing audio files coming from gTTS
from playsound import playsound
# Classic time module, mostly used for time.sleep(sec)
import time
# webbrowser module for opening specific link in default browser
import webbrowser
# pywhatkit module for helping hands in some things, might get removed in future
import pywhatkit as kit
# Classic request module for calling APIs
import requests
# Classic tkinter module for GUI, might get change in future if found better alternative, currently not looking forward to change it but not sure about this
from tkinter import *
# Classic os module for interaction with os
import os
# Classic datetime module for date and time manupulation
import datetime
# Get the Radio url from config.py
from config import RADIO_URL
# Get the function which sends whatsapp message as per request
from utils.whatsapp import send_message
# IMPORTANT: always import call function after whatsapp function
# Get the function which can make calls
from utils.call import make_call
# Get the function which returns the weather conditions as per requested
from utils.weather import get_weather
# Get the function which returns the set of news strings
from utils.news import get_news

# This is for offline text to speech
engine = pyttsx3.init()
# Default speed is very fast so slow down it a bit, 200 --> 170
engine.setProperty('rate', 170)

# Initiate speech recognizing module
r = sr.Recognizer()


# GUI configuration, subject to heavy change
gui = Tk()
gui.geometry("750x575")
# This frame will hold the output logs
frame = Frame(gui, bg="black")
frame.place(relwidth=1, relheight=0.9, rely=0.1)


# Keep track of commands
last_command = []
# If the log file does not exists then create one
if not os.path.isfile("VOA_log.txt"):
    fs = open("VOA_log.txt", "w")
    fs.close()
# Open log file to read
fs = open("VOA_log.txt", "r")
logs = fs.readlines()
fs.close()
# Each line of file contains the data like following example on each line
# Date, Command, Additional details like error or output if I think about it in future
for log in logs:
    log = log.replace("\n", "")
    log = log.split(", ")
    last_command.append(
        {"timestamp": log[0], "command": log[1], "output": " ".join(log[2:])})


# Function to be callled upon first startup
# Currently does nothing but can be used to check things like todos and birthdays
def initiate():
    talk_back("How can I help you?")


# Function that talks back to you
def talk_back(speech):
    # Add to the frame whatever is spoken back to read if you didn't understand
    label = Label(frame, text=speech)
    label.pack()
    # Using try/catch to so if anything goes wrong we can have fallback
    try:
        # Initiate the google text to speach module
        myobj = gTTS(text=speech, lang='en', slow=False, tld="co.in")
        # Save in res.mp3 file, because we can't play it directly
        myobj.save("res.mp3")
        # play the audio with playsound module
        playsound("res.mp3")
    except:
        # 99% problem will be of internet down, so here we can use the offline text to speech
        engine.say("Check your internet")
        engine.runAndWait()


# Function that handles the command, BRAIN of everything
# Params:
#   -command(str): command to be dealt with
def handle_command(command):
    # I don't know how I feel about lowering everything but it is necessary for
    command = command.lower()
    # Append the command to last command list
    last_command.append(
        {"timestamp": datetime.datetime.now(), "command": command})

    # Append the current time and command to lofg file.
    log_file = open("VOA_log.txt", "a")
    log_file.write(f'{datetime.datetime.now()}, {command}\n')
    # Don't forget to close the file
    log_file.close()

    # Split the commands into words
    commands = command.split()
    # if the length of command is greater then one and it starts with `ver`(can be subject to chnage in future)
    if len(commands) > 0 and "ver" in commands[0]:
        # remove the first word (starting with `ver`) from list
        commands = commands[1:]
        # Now if you don't have anything then say nothing found
        if not len(commands) > 0:
            print("no command found")
            talk_back("Please tell me to do something too")
        # This is the else statement that does the MAGIC
        else:
            # First word is the most important word so we checks for it always first
            # All the logic is not explained because it will take too much time and is
            # very confusing too so check README.md for statements and how they works

            # Tells the current time only
            if commands[0] == "time":
                now = datetime.datetime.now()
                talk_back(now.strftime("it's %I : %M : %p"))
            # Tells the today's date only
            elif commands[0] == "date":
                now = datetime.datetime.now()
                talk_back(now.strftime("%d %B %Y"))
            # Tells the detailed info like current time and today's date
            elif commands[0] == "timestamp":
                now = datetime.datetime.now()
                talk_back(now.strftime(
                    "It's %A,  %B %d today and it is %I : %M : %p now"))
            # questions starting with who
            # either know your details
            # Or find about someone famous
            elif commands[0] == "who":
                if commands[1] == "am" or commands[1] == "i":
                    fs = open("profile.txt", "r")
                    profile = fs.readlines()
                    info = {}
                    for data in profile:
                        data = data.replace("\n", "")
                        data = data.split(", ")
                        info[data[0]] = data[1]
                    response = f'You are {"Mr." if info["gender"][0] == "m" else "Mrs."} {info["first_name"]} {info["middle_name"][0]} {info["last_name"]} also known as {info["address_name"]}'
                    talk_back(response)
                elif commands[1] == "is":
                    name = " ".join(commands[2:])
                    info = kit.info(name, lines=1)
                    talk_back(info)
            # play Something
            # Either play a radio from url provided in config.py
            # Or play a song on youtube
            # Or play anything on youtube
            elif commands[0] == "play":
                commands = commands[1:]
                if "radio" in commands:
                    webbrowser.open(RADIO_URL)
                elif "song" in commands:
                    commands.pop(commands.index('song'))
                    kit.playonyt(" ".join(commands))
                else:
                    kit.playonyt(" ".join(commands))
            # Find about anything like what is mango
            elif commands[0] == "what":
                if commands[1] == "is":
                    commands = commands[2:]
                    res = kit.info(" ".join(commands), lines=1)
                    talk_back(res)
            # Find the weather of your location or any city either current or on specific date
            elif commands[0] == "weather":
                date = ""
                if "on" in commands:
                    date = " ".join(commands[commands.index("on")+1:])
                    commands = commands[:commands.index("on")]
                if "at" in commands:
                    date = " ".join(commands[commands.index("at")+1:])
                    commands = commands[:commands.index("at")]
                if "today" in commands:
                    date = "today"
                    commands = commands.pop(commands.index("today"))
                city = "surat"
                if "of" in commands:
                    city = " ".join(commands[commands.index("of")+1:])
                if "in" in commands:
                    city = " ".join(commands[commands.index("in")+1:])
                talk_back(get_weather(city, date))
            # Send whatsapp message to someone
            elif commands[0] == "send":
                if commands[1] == "whatsapp":
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
            # Tell a joke or find out about something like tell me what is something
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
            # Test command for development purposes
            elif commands[0] == "test":
                talk_back("test successfully completed")
            # Tells you the top news of your local country
            elif commands[0] == "news":
                newses = get_news()
                for news in newses:
                    talk_back(news)
            # Calls someone on your mobile
            elif commands[0] == "call":
                if "speaker" in commands:
                    if "on" in commands:
                        commands.pop(commands.index("on"))
                    talk_back(make_call(
                        " ".join(commands[1:commands.index("speaker")]), speaker=True))
                elif "speakerphone" in commands:
                    if "on" in commands:
                        commands.pop(commands.index("on"))
                    talk_back(make_call(
                        " ".join(commands[1:commands.index("speakerphone")]), speaker=True))
                else:
                    talk_back(make_call(" ".join(commands[1:])))
            # If none of the first word is picked up
            else:
                talk_back("I didn't get that. Try again please.")


# Function to take command with voice command
def take_command():
    # Use microphone to listen to the audio
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    print("recognizing audio...")

    # Using try/catch because there can be so many things that can go wrong
    try:
        # Get the text from speech
        command = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + command)
        # GUI change, won't be in effect unless it completes the execution
        info.set(command)
        # Handle the command if everything is fine
        handle_command(command)
    except sr.UnknownValueError:
        # Runs when the audio is not recognizable
        command = "Could not understand audio, Please try again"
        talk_back(command)
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        # Runs when we can not reach google speech recognition service
        command = "something went wrong"
        talk_back(command)
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(e))


# When ENTER key is pressed from GUI, this function is called
def handle_submit(event):
    # handle command from input box
    handle_command(info.get())


# When user clicks up arrow on text box, fills with last command like terminal
def handle_up(event):
    # DO something if only you have at least one last command
    if len(last_command) > 0:
        info.set(last_command.pop()["command"])


# Button to start listning for audio input command
btn = Button(gui, text='Speak', fg='black', bg='red',
             command=lambda: take_command(), height=1, width=7)
btn.pack()
# varibale that stores the text input box values
info = StringVar()
# Input text box for writting command
info_cont = Entry(gui, textvariable=info, width=700,
                  justify="center")
# If enter key is pressed then call handle_submit function
info_cont.bind("<Key-Return>", handle_submit)
# If up key is pressed then call handle_up function
info_cont.bind("<Key-Up>", handle_up)
info_cont.pack()
# Call the initial function from above before starting gui
initiate()
# Set the focus to the input box might get change to button
info_cont.focus()
# Start the main GUI loop, can be treated as while True: loop with break condition upon closing request
gui.mainloop()
