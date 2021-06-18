from tkinter import *
from tkinter.ttk import *


def save_changes():
    print("save changes")


gui = Tk()
gui.geometry("750x575")
f_name = StringVar()
m_name = StringVar()
l_name = StringVar()
a_name = StringVar()
age = StringVar()
dob_d = StringVar()
dob_m = StringVar()
dob_y = StringVar()
gender = StringVar()
f_name_label = Label(gui, text="First name: ")
f_name_label.grid(column=0, row=0)
f_name_field = Entry(gui, textvariable=f_name)
f_name_field.grid(column=1, row=0)
m_name_label = Label(gui, text="Middle name: ")
m_name_label.grid(column=0, row=1)
m_name_field = Entry(gui, textvariable=m_name)
m_name_field.grid(column=1, row=1)
l_name_label = Label(gui, text="Last name: ")
l_name_label.grid(column=0, row=2)
l_name_field = Entry(gui, textvariable=l_name)
l_name_field.grid(column=1, row=2)
a_name_label = Label(gui, text="Address name: ")
a_name_label.grid(column=0, row=3)
a_name_field = Entry(gui, textvariable=a_name)
a_name_field.grid(column=1, row=3)
age_label = Label(gui, text="Age: ")
age_label.grid(column=0, row=4)
age_field = Spinbox(gui, from_=10, to=150, textvariable=age)
age_field.grid(column=1, row=4)
gender_label = Label(gui, text="Gender: ")
gender_label.grid(column=0, row=5)
gender.set("male")
gender_field = Combobox(gui, textvariable=gender, values=[
                        "male", "female"], width=8)
gender_field.grid(column=1, row=5)
dob_d_label = Label(gui, text="Date of Birth: ")
dob_d_label.grid(column=0, row=6)
dob_field = Frame(gui)
dob_field.grid(column=1, row=6)
dob_d_field = Combobox(dob_field, textvariable=dob_d,
                       values=[i for i in range(1, 32)], width=3)
dob_d_field.grid(column=0, row=0)
dob_m_field = Combobox(dob_field, textvariable=dob_m,
                       values=[i for i in range(1, 13)], width=3)
dob_m_field.grid(column=1, row=0)
dob_y_field = Combobox(dob_field, textvariable=dob_y,
                       values=[i for i in range(1950, 2050)], width=5)
dob_y_field.grid(column=2, row=0)
submit_button = Button(
    gui, text="Save", command=lambda: save_changes())
submit_button.grid(column=0, row=7, columnspan=2)
gui.mainloop()
