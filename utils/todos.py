import os
import time

if not os.path.isfile("Todos_list.txt"):
    fs = open("Todos_list.txt", "w")
    fs.close()


def add_todo(title, end_time):
    todos = retrive_all_todos()
    last_id = int(todos[len(todos) - 1][0])
    new_id = last_id + 1
    crnt_timestamp_string = time.strftime("%d %B %Y %H:%M", time.localtime())
    end_timestamp_string = end_time
    done_string = "False"
    fs = open("Todos_list.txt", "a")
    fs.writelines([
        f'\n{new_id}, {crnt_timestamp_string}, {title}, {end_timestamp_string}, {done_string}'])
    fs.close()


def sorting_function(e):
    return time.mktime(time.strptime(e[3], "%d %B %Y %H:%M"))


def retrive_all_todos():
    fs = open("Todos_list.txt", "r")
    todos = fs.readlines()
    fs.close()
    todos = [todo.split(", ") for todo in todos]
    return todos


def retrive_undone_todos():
    todos = retrive_all_todos()
    remaining_todos = []
    for todo in todos:
        if todo[4][:1].lower() == "f":
            remaining_todos.append(todo)
    remaining_todos.sort(key=sorting_function)
    # print(remaining_todos)
    return remaining_todos


def retrive_next_todos(count, all=False):
    remaining_todos = retrive_undone_todos()
    next_todos = []
    for todo in remaining_todos:
        if time.mktime(time.strptime(todo[3], "%d %B %Y %H:%M")) > time.time():
            next_todos.append(todo)
    if count > len(next_todos) or all:
        return next_todos
    return next_todos[:count]


def retrive_due_todos():
    remaining_todos = retrive_undone_todos()
    due_todos = []
    for todo in remaining_todos:
        if time.mktime(time.strptime(todo[3], "%d %B %Y %H:%M")) < time.time():
            due_todos.append(todo)
    due_todos.reverse()
    return due_todos


# print(retrive_all_todos())
# print("-----------------------------")
# print([todo[0] for todo in retrive_undone_todos()])
# print("-----------------------------")
# print([todo[0] for todo in retrive_next_todos(1, all=True)])
# print("-----------------------------")
# print([todo[0] for todo in retrive_due_todos()])


def mark_done_todo(id, done_timing=time.strftime("%d %B %Y %H:%M")):
    todos = retrive_all_todos()
    for todo in todos:
        if todo[0] == str(id):
            index = todos.index(todo)
            todos[index][4] = "True"
            todos[index].append(done_timing if index == len(
                todos) - 1 else done_timing + "\n")
            break
    todos = [", ".join(todo) for todo in todos]
    fs = open("Todos_list.txt", "w")
    fs.writelines(todos)
    fs.close()
