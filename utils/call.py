# pure-python module for adb interaction
from ppadb.client import Client
# for time.sleep(sec)
import time
# Import the speaker button coordinates
from config import CALL_SPEAKER_BUTTON


# Initiate the adb client on default ports: localhost:5037 (as per doc)
adb = Client(host='127.0.0.1', port=5037)
# Get the all devices attached to current adb client
devices = adb.devices()


# If there are no devices attached quit the application, might be changed to just raising warning
if len(devices) == 0:
    print('no device attached')
    quit()


# If we have devices then grab the first device
device = devices[0]


# Intialize the contact list List
# type {"name": str, "number": int}[]
contact_list = []


# Function that retrives the contacts from the contacts.txt file
# CONTEXT: contacts.txt file will be created by whatsapp util
def retrive_contacts():
    # Open the file, read the file, append the data, simple
    f = open("contacts.txt", "r")
    contacts = f.readlines()
    contacts = [contacts[i].split(", ") for i in range(len(contacts))]
    for i in range(len(contacts)):
        contact_list.append({"name": contacts[i][14][5:].lower(), "number": contacts[i][11][7:].replace(
            " ", "")})


# Call the function to actually make it work
retrive_contacts()


# Function that starts the call based on input
# Params:
#   - name(str): name of the person to be called as per contact list, can be short form
#   - speaker(boolean): should be called on speakerphone or not, defaults to false
def make_call(name, speaker=False):
    # Get the phone number of the person to be called from name
    number = ""
    numbers = []
    current = {}
    for contact in contact_list:
        # This is tricky part because sometimes people have duplicates
        # So this is for eleminating the duplicates
        if name.lower() in contact["name"].lower():
            # If we already had a match in list
            if len(numbers) > 0:
                # This might get change in future
                if numbers[len(numbers)-1] != contact["number"]:
                    numbers.append(contact["number"])
                    current = contact
            # If this is first match then just add the number
            else:
                numbers.append(contact["number"])
                current = contact

    # If we didn't got any matches
    if len(numbers) == 0:
        response = "No contact found. Maybe you mean"
        maybe = name.split(" ")
        count = 0
        # Here we try to find the names of closest to requested name, maximum 4
        for word in maybe:
            for contact in contact_list:
                if word.lower() in contact["name"]:
                    response = response + " " + contact["name"] + " or"
                    count = count + 1
                if count > 4:
                    break
            if count > 4:
                break
        print(response)
        # return from the function
        return response

    # If there are multiple matches of name then ask for specific name
    if len(numbers) > 1:
        print("Multiple numbers found. try specific name")
        print(numbers)
        # return from the function
        return "Multiple numbers found. try specific name"

    # Everything is fine, good to go
    number = numbers[0]

    # Command that starts the call by running the intent
    # Since call is top priority intent, no need to minimize other existing intents or apps
    device.shell(f"am start -a android.intent.action.CALL -d tel:{number}")

    # check if speaker should be enabled or not
    if speaker:
        # wait for some time before clicking the speaker button
        # 5 seconds because if it is starting from lock screen then it will take time
        # Also there is not much to listen in first 5 seconds of call except bip bip bip
        time.sleep(5)
        # touch on the speaker button
        device.shell(
            f'input touchscreen tap {CALL_SPEAKER_BUTTON["x"]} {CALL_SPEAKER_BUTTON["y"]}')

    # return the response string
    return f'calling {current["name"]} {"on speaker" if speaker else ""}'
