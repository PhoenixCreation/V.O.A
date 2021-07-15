import os
import time

if not os.path.isfile("Todos_list.txt"):
    fs = open("Todos_list.txt", "w")
    fs.close()

fs = open("Todos_list.txt", "r")
todos = fs.readlines()
fs.close()
todos = [todo.split(", ") for todo in todos]
# print(todos)
for todo in todos:
    end_time_tuple = time.strptime(todo[3], "%d %B %Y %H:%M")
    end_time = time.mktime(end_time_tuple)
    print(f'{end_time} => {todo[2]}')


def add_todo(title, end_time):
    last_id = int(todos[len(todos) - 1][0])
    new_id = last_id + 1
    crnt_timestamp_string = time.strftime("%d %B %Y %H:%M", time.localtime())
    end_timestamp_string = end_time
    done_string = "False"
    fs = open("Todos_list.txt", "a")
    fs.writelines([
        f'\n{new_id}, {crnt_timestamp_string}, {title}, {end_timestamp_string}, {done_string}'])
