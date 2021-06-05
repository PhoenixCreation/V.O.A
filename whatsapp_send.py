from ppadb.client import Client
import time

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    quit()

device = devices[0]

contact_list = []


def retrive_contacts():
    contacts = device.shell('content query --uri content://contacts/phones/')
    with open("sample.txt", "w") as f:
        f.write(contacts)
    with open("sample.txt", "r") as f:
        contacts = f.readlines()
    final = open("contacts.txt", "w")
    for i in range(len(contacts)):
        count = 5
        if i < 10:
            count = 7
        elif i < 100:
            count = 8
        else:
            count = 9
        contacts[i] = contacts[i][count:]
    final.writelines(contacts)
    f = open("contacts.txt", "r")
    contacts = f.readlines()
    contacts = [contacts[i].split(", ") for i in range(len(contacts))]
    for i in range(len(contacts)):
        contact_list.append({"name": contacts[i][14][5:].lower(), "number": contacts[i][11][7:].replace(
            " ", "")})


retrive_contacts()


def send_message(name, message):
    number = ""
    numbers = []
    for contact in contact_list:
        if name.lower() in contact["name"]:
            if len(numbers) > 0:
                if numbers[len(numbers)-1] != contact["number"]:
                    numbers.append(contact["number"])
            else:
                numbers.append(contact["number"])

    if len(numbers) == 0:
        response = "No contact found. Maybe you mean"
        maybe = name.split(" ")
        count = 0
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
        return response
    if len(numbers) > 1:
        print("Mulitiple numbers found. try specific name")
        print(numbers)
        return "Mulitiple numbers found. try specific name"
    number = numbers[0]

    if not number[0] == "+":
        number = "+91" + str(number)

    already_on = device.shell(
        "dumpsys power | grep 'mHoldingDisplaySuspendBlocker'")[32:]
    if "false" in already_on:
        already_on = False
    else:
        already_on = True
    if not already_on:
        device.shell('input keyevent 26')
        time.sleep(1)
        device.shell('input touchscreen swipe 560 880 560 380')
    device.shell('input keyevent 3')
    time.sleep(1)
    device.shell(
        f'am start -a android.intent.action.VIEW -d "https://api.whatsapp.com/send?phone={number}&text="')
    time.sleep(3)
    device.shell("input touchscreen tap 350 1225")
    message = message.replace(" ", "%s")
    device.shell('input text ' + message)
    device.shell("input touchscreen tap 650 610")
    for _ in range(5):
        device.shell('input keyevent 4')
    if not already_on:
        device.shell('input keyevent 26')
    return "message sent successfully"
