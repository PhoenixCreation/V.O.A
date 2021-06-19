# pure-python module for adb interaction
from ppadb.client import Client
# for time.sleep(sec)
import time
# Classic os module for interaction with os, here for file check
import os


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
# type: {"type": "personal" | "group", "name": str, "number": int}[]
contact_list = []


# Function that retrives the contacts and groups from the user's phone through adb
def retrive_contacts():
    # If group.txt file does not exists, create one
    if not os.path.isfile("groups.txt"):
        fs = open("groups.txt", "w")
        fs.close()

    # Read the all file lines from groups.txt
    with open("groups.txt", "r") as f:
        groups = f.readlines()

    # Append the data from the file, data on each line will be like this
    # name of group, group id
    for group in groups:
        group = group.split(", ")
        # append to contact list with type as group
        contact_list.append(
            {"type": "group", "name": group[0], "number": group[1]})

    # Now retrive contacts from the contacts on phone
    contacts = device.shell('content query --uri content://contacts/phones/')
    # Above command returns the data in very uninteractivable form, so we need some processing
    # You can see this data in sample.txt file
    with open("sample.txt", "w") as f:
        f.write(contacts)
    # read the data from sample.txt file
    with open("sample.txt", "r") as f:
        contacts = f.readlines()

    # final data will be written to contacts.txt file in close to CSV formate
    final = open("contacts.txt", "w")
    # For each data line
    for i in range(len(contacts)):
        # First we need to remove word ROW: and number follwed by it
        count = 5
        if i < 10:
            count = 7
        elif i < 100:
            count = 8
        else:
            count = 9
        # Cut the first Row: <number> part
        contacts[i] = contacts[i][count:]
    # Now we have out data in near csv formate
    final.writelines(contacts)
    # close the file
    final.close()

    # Now read the data from file
    f = open("contacts.txt", "r")
    contacts = f.readlines()
    # Everything is saprated by ", " (colon and space)
    contacts = [contacts[i].split(", ") for i in range(len(contacts))]
    # we only need name and number which are found on specific column and also have to remove prefix of them
    # Set type as personal
    for i in range(len(contacts)):
        contact_list.append({"type": "personal", "name": contacts[i][14][5:].lower(), "number": contacts[i][11][7:].replace(
            " ", "")})


# Call the function to actually make it work
retrive_contacts()


# Function that sends the message as per requested
# Params:
#   - name(str): name of the person or group to be send message to
#   - message(str): actual message to be send
def send_message(name, message):
    # Get the phone number of the person or group to be called from name
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
        print("Mulitiple numbers found. try specific name")
        print(numbers)
        # return from the function
        return "Mulitiple numbers found. try specific name"

    # Everything is fine, good to go
    number = numbers[0]

    # If we are sending to person and number does not start from country code
    if not number[0] == "+" and current["type"] == "personal":
        # Currently we will assume it is Indian(+91) number but later can be raised warning
        # TODO: transfer default country code to config
        number = "+91" + str(number)

    # This is to check is device is curently locked or not, display is off or not
    already_on = device.shell(
        "dumpsys power | grep 'mHoldingDisplaySuspendBlocker'")[32:]
    # Above command return the string with true or false
    if "false" in already_on:
        already_on = False
    else:
        already_on = True

    # If device is locked or screen is off
    if not already_on:
        # Click the power button, 26 is power key code
        device.shell('input keyevent 26')
        # wait for a sec
        time.sleep(1)
        # swipe up to unlock
        device.shell('input touchscreen swipe 560 880 560 380')
        # TODO: If user has a password then do something
        # Send the password through input command and then click ok if neccessary

    # press the home button, 3 is home key code
    # Because whatsapp intent does not top priority so it might open in background
    device.shell('input keyevent 3')
    # wait a sec
    time.sleep(1)

    # If we have to send to personal contact
    if current["type"] == "personal":
        # for personal contacts opeing the url opens the chat with that individual
        # It does not matter if it is existing or new one
        device.shell(
            f'am start -a android.intent.action.VIEW -d "https://api.whatsapp.com/send?phone={number}&text="')
        # It will take time to open based on your phone processsing capabilities
        time.sleep(4)
    # If we have to send to group
    else:
        # We can use joining group url to open the chat
        # Because it opens existing group chat if you are already in the group
        device.shell(
            f'am start -a android.intent.action.VIEW -d https://chat.whatsapp.com/{number}')
        # It will take alot time specifically if you have potato device like me
        time.sleep(6)

    # replace the spaces in message with %s
    message = message.replace(" ", "%s")
    # Type the message in input box
    device.shell('input text ' + message)
    # Tap on the send button at the right bottom of the screen
    # TODO: transfer the touch coordinates to config file,
    # It will be width - 50 height - 50
    device.shell("input touchscreen tap 650 1250")

    # Press the back button 5 times to go back from app
    # we are using backs instead of home so that whatsapp gets cleared from memory of phone
    for _ in range(5):
        # press the back button, 4 is back key code
        device.shell('input keyevent 4')

    # If device was locked then lock it again to get it to initially position
    if not already_on:
        # Click the power button, 26 is power key code
        device.shell('input keyevent 26')

    # return the response
    return f'message sent successfully to {current["name"]}'
