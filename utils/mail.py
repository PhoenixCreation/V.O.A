# pure-python module for adb interaction
from ppadb.client import Client
# for time.sleep(sec)
import time
# Import the coordinates of the send button
from config import MAIL_SEND_BUTTON

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


def send_mail(to, body, title="Mail sent through AI assistant"):
    device.shell(
        f'am start -a android.intent.action.VIEW -d "mailto:{to}?body={body}&subject={title}"')
    time.sleep(3)
    # touch on the send button
    device.shell(
        f'input touchscreen tap {MAIL_SEND_BUTTON["x"]} {MAIL_SEND_BUTTON["y"]}')
    return "mail sent successfully"
