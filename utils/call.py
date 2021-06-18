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
    f = open("contacts.txt", "r")
    contacts = f.readlines()
    contacts = [contacts[i].split(", ") for i in range(len(contacts))]
    for i in range(len(contacts)):
        contact_list.append({"name": contacts[i][14][5:].lower(), "number": contacts[i][11][7:].replace(
            " ", "")})


retrive_contacts()


def make_call(name, speaker=False):
    number = ""
    numbers = []
    current = {}
    for contact in contact_list:
        if name.lower() in contact["name"].lower():
            if len(numbers) > 0:
                if numbers[len(numbers)-1] != contact["number"]:
                    numbers.append(contact["number"])
                    current = contact
            else:
                numbers.append(contact["number"])
                current = contact

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
    device.shell(f"am start -a android.intent.action.CALL -d tel:{number}")
    if speaker:
        time.sleep(3)
        print("now enabling speaker")
        device.shell("input touchscreen tap 155 940")
    return f'calling {current["name"]} {"on speaker" if speaker else ""}'
