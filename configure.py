import os


def screen_clear():
    # for mac and linux(here, os.name is 'posix')
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # for windows platfrom
        _ = os.system('cls')


def configure_profile():
    profile = {}
    if not os.path.isfile("profile.txt"):
        fs = open("profile.txt", "w")
        towrite = "first_name, \nmiddle_name, \nlast_name, \naddress_name, \nage, \ndob, \ngender, \n"
        fs.write(towrite)
        fs.close()
    fs = open("profile.txt", "r")
    datas = fs.readlines()
    for data in datas:
        data = data.replace("\n", "")
        data = data.split(", ")
        profile[data[0]] = data[1]
    for field in profile:
        display = field.replace("_", " ")
        value = input(f'What is your {display}: ({profile[field]}) >> ')
        if value != "":
            profile[field] = value.lower()
        else:
            print(f'Applied default value: {display} => {profile[field]}')
    fs.close()
    fs = open("profile.txt", "w")
    for field in profile:
        line = f'{field}, {profile[field]}\n'
        fs.write(line)
    fs.close()
    screen_clear()
    print('------------------------')
    print("Your personal details updated as per below:")
    for field in profile:
        display = field.replace("_", " ")
        print(f'{display} => {profile[field]}')
    print('------------------------')


def configure_whatsapp_groups():
    f = open("groups.txt", "a")
    while True:
        print("----------------------")
        print("whatsapp groups configuration")
        print("----------------------")
        print("Choose what do you want to do?")
        print("1: Add groups info")
        print("2: Change group info")
        print("3: Exit")
        choice = input("Enter you choice for whatsapp groups >> ")
        screen_clear()
        if choice == "1":
            while True:
                name = input("Enter Group Name(Real name recomended) >> ")
                number = input("Enter Group ID >> ")
                f.write(f'\n{name}, {number}')
                innerCnt = input("Do you want to add another one? [Y/N] ")
                if innerCnt.lower() == "y":
                    screen_clear()
                    continue
                else:
                    break
        elif choice == "2":
            print("You can manually edit the groups.txt for this")
        elif choice == "3":
            break
        else:
            print("Invalid option")
        cnt = input("Do you want to continue for whatsapp groups menu? [Y/N] ")
        if cnt.lower() == "y":
            screen_clear()
            continue
        else:
            break


screen_clear()

while True:
    print('------------------------')
    print("Welcome to V.O.A.")
    print('------------------------')
    print("Select Your Choice:")
    print("1: Configure your profile")
    print("2: Configure whatsapp groups")
    print("3: Exit Menu")
    print("------------------------")
    choice = input("Enter you choice >> ")
    screen_clear()
    if choice == "1":
        configure_profile()
    elif choice == "2":
        configure_whatsapp_groups()
    elif choice == "3":
        break
    else:
        print("Invalid option")
    cnt = input("Do you want to continue for main menu? [Y/N] ")
    if cnt.lower() == "y":
        screen_clear()
        continue
    else:
        break
