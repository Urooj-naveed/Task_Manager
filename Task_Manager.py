
import keyboard
import json
import hashlib
import os

users=[]
#list used for authentication

tasks=[]
#list used to save tasks
dir = os.path.dirname(os.path.abspath(__file__))


def load_data():
    global users
    global tasks

    with open(f'{dir}\\users.txt', 'r') as file:      #open file with user data
        users_data=json.load(file)                    #extract user info
    #print(users_data)
    if users_data!='':
        users=users_data                              #save user data as a list
    with open(f'{dir}\\task.txt', 'r') as file:       #open task file
        tasks_list=json.load(file)                    #ectract all tasks from json file
    #print(tasks_list)
    if tasks_list!='':
        tasks= tasks_list                             #

def print_menu():
    role_options = {
        1: 'General Manager',
        2: 'Dept manager',
        3: 'Worker'
    }
    for key in role_options.keys():
        print (key, '--', role_options[key] )

def print_dept_menu():
    dept_options = {
        1: 'Computer Science',
        2: 'Engineering'
    }
    for key in dept_options.keys():
        print (key, '--', dept_options[key] )

class Authentication:
    def __init__(self, user_registered, user_info):
        self.user_registered = user_registered
        self.user_info = user_info

    def sign_up(self):
        while True:
            user_email = str(input('Email: '))
            if user_email != '':
                break
            else:
                print('Invalid email')
                # return False
        while True:
            password = str(input('Password: '))
            if password != '':
                break
            else:
                print('Invalid password')
                # return False
        user_exist = False
        for user in users:
            if user["user_email"] == user_email:
                user_exist = True
                print('User already registered!')
                break

        if not user_exist:
            user_role = 0
            while (True):
                print_menu()
                option = int(input('Enter your role: '))
                if option == 1:
                    user_role = 1
                    break
                elif option == 2:
                    user_role = 2
                    break
                elif option == 3:
                    user_role = 3
                    break
                else:
                    print('Invalid option selected. Please enter a number between 1 and 3.')
            if len(users) > 0:
                user_id = users[-1]["user_id"] + 1
            else:
                user_id = 1
            pass_text = hashlib.sha256(password.encode('utf-8')).hexdigest()
            department = 0  #int(input('Enter department number: \n 0 or 1: '))
            while (True):
                print_dept_menu()
                option = int(input('Enter your department: '))
                if option == 1:
                    department = 1
                    break
                elif option == 2:
                    department = 2
                    break
                else:
                    print('Invalid option selected. Please enter a number between 1 and 2.')

            new_user = {
                "user_id": user_id,
                "user_email": user_email,
                "password": pass_text,
                "user_role": user_role,
                "department": department
            }
            users.append(new_user)
            with open(f'{dir}\\users.txt', 'w') as file:
                json.dump(users, file)
            print('User registered')
            self.user_registered = True
            self.user_info = new_user
            return True

    def login(self):
        while True:
            user_email = str(input('Email: '))
            if user_email != '':
                break
            else:
                print('Invalid email')
                # return False
        while True:
            password = str(input('Password: '))
            if password != '':
                break
            else:
                print('Invalid password')
                # return False
        user_exist = False
        user = None
        for user_ in users:
            if user_["user_email"] == user_email:
                user_exist = True
                user = user_

        if user_exist:
            if user['password'] == hashlib.sha256(password.encode('utf-8')).hexdigest():
                print('Login successful!')

                self.user_registered = True

                self.user_info = user

            else:
                print('Incorrect password')
                return False
        else:
            print('User donot exist, signup to register a new user.')
            return False


class Task:

    def __init__(self, user_info, user_role, user_email, department):
        self.user_info = user_info
        self.user_role = user_role
        self.user_email = user_email
        self.department = department

    def display_tasks(self):
        print ("{:<4} {:<10} {:<50} {:<12} {:<20} {:<4}".format('#','Task Id', 'Task', 'Status', 'Assigned to', 'delete request'))
        if self.user_role == 0:
                i = 1
                for task in tasks:
                    print("{:<10} {:<6} {:<50} {:<12} {:<20} {:<4}".format(i, task["task_id"], task["name"], task["status"], task["assigned_to"], task["delete_request"]))
                    i += 1
        elif self.user_role == 2:
                i = 1
                for task in tasks:
                    if task["department"] == self.department:
                        print("{:<4} {:<10} {:<50} {:<12} {:<20} {:<4}".format(i, task["task_id"], task["name"], task["status"], task["assigned_to"], task["delete_request"]))
                        i += 1

        elif self.user_role == 3:
                i = 1
                for task in tasks:
                    if task["assigned_to"] == self.user_email or task["status"] == 1:
                        print("{:<4} {:<10} {:<50} {:<12} {:<20}".format(i, task["task_id"], task["name"], task["status"], task["assigned_to"]))
                        i += 1

    def user_activity(self):
            re_run = False
            if self.user_role == 0:
                print('Press a to add a task, d to delete a task, e to edit task or q  to exit!')
                while True:
                    if keyboard.is_pressed("a"):
                        self.add_task()
                        re_run = True
                        break
                    elif keyboard.is_pressed("d"):
                        self.delete_task()
                        re_run = True
                        break
                    elif keyboard.is_pressed("q"):
                        break
                    elif keyboard.is_pressed("e"):
                        self.edit_task()
                        re_run = True
                        break
                if re_run:
                    self.display_tasks()
                    self.user_activity()

            if self.user_role == 2:
                    print('Press a to assign task, d to delete task, e to edit task and q to exit')
                    while True:
                        if keyboard.is_pressed("a"):
                            self.add_task()
                            re_run = True
                            break
                        elif keyboard.is_pressed("d"):
                            self.delete_task()
                            re_run = True
                            break
                        elif keyboard.is_pressed("e"):
                            self.edit_task()
                            re_run = True
                            break
                        elif keyboard.is_pressed("q"):
                            break
                    if re_run:
                        self.display_tasks()
                        self.user_activity()

            if self.user_role == 3:
                    print('Press a to assign task, press q to exit')
                    while True:
                        if keyboard.is_pressed("a"):
                                self.add_task()
                                re_run = True
                                break
                        elif keyboard.is_pressed("q"):
                                break
                    if re_run:
                        self.display_tasks()
                        self.user_activity()
                        
    def write_json(self):
        with open(f'{dir}\\task.txt', 'w') as file:
            json.dump(tasks, file)  # storing new addition in json
        with open(f'{dir}\\users.txt', 'w') as file:
            json.dump(users, file)  # storing new addition in json
        load_data()

    def add_task(self):
            if self.user_role == 0:
                task_name = str(input('Enter task name:'))
                while True:
                    asign_to = str(input('Enter user id to assign task to: '))
                    if not any(user['user_email'] ==asign_to for user in users):
                        print('This user does not exist!')
                    else:
                        for user in users:
                            if user["user_email"] == asign_to:
                                taskcount = len(list(filter(lambda task: task['assigned_to'] == asign_to and task['status'] == 0, tasks)))
                                print(taskcount)
                                if taskcount > 2 and user["user_role"] == 3:
                                    print("The assignee has reached maximum pending task count limit")
                                    break
                                else:
                                    if len(tasks) > 0:
                                        task_id = tasks[-1]["task_id"] + 1
                                    else:
                                        task_id = 1001
                                    status = int(input('Enter 0 for assigned task, 1 for unassigned task, 2 for pending and 3 for completed task.: '))
                                    delete_request = 0
                                    while (True):
                                        print_dept_menu()
                                        option = int(input('Enter your department: '))
                                        if option == 1:
                                            department = 1
                                            break
                                        elif option == 2:
                                            department = 2
                                            break
                                        else:
                                            print('Invalid option selected. Please enter a number between 1 and 2.')

                                    new_task = {
                                        "task_id": task_id,
                                        "name": task_name,
                                        "assigned_to": asign_to,
                                        "status": status,
                                        "delete_request": delete_request,
                                        "department": department
                                    }
                                    tasks.append(new_task)  # update the new task in the text file
                                    user["taskcount"] = user["taskcount"] + 1
                                    # print(new_task)
                                    # print(tasks)

                        self.write_json()
                        break
                    break

            if self.user_role== 2:
                task_name = str(input('Enter task name:'))

                while True:
                    asign_to = str(input('Enter user id to assign task to: '))
                    if not any(user['user_email'] == asign_to for user in users):
                        print('This user does not exist!')
                    elif not any(user['user_email'] ==asign_to and user['department'] == self.department for user in users):
                        print('User is not a member of your department.')
                    else:
                        for user in users:
                            if asign_to == user["user_email"]:
                                #taskcount = user["taskcount"]
                                taskcount = len(list(filter(lambda task: task['assigned_to'] == asign_to and task['status'] == 0, tasks)))
                                print(taskcount)
                                if taskcount >3:
                                    print("The assignee has reached maximum pending task count limit")
                                    break
                                else:
                                    if len(tasks) > 0:
                                        task_id = tasks[-1]["task_id"] + 1
                                    else:
                                        task_id = 1001
                                    status = int(input('Enter 0 for assigned task, 1 for unassigned task, 2 for pending and 3 for completed task.: '))
                                    delete_request = 0
                                    department = self.user_info["department"]

                                    new_task = {
                                        "task_id": task_id,
                                        "name": task_name,
                                        "assigned_to": asign_to,
                                        "status": status,
                                        "delete_request": delete_request,
                                        "department": department
                                    }
                                    tasks.append(new_task)
                                    user["taskcount"] = user["taskcount"] + 1
                                    self.write_json()
                                    break
                    break

            elif self.user_info["user_role"] == 3:
                task_count = len(list(filter(lambda task: task['assigned_to'] == self.user_email and task['status'] == 0, tasks)))
                if task_count < 3:
                    task_id = int(input('Enter task id you would like to assign yourself:'))
                    user_email = self.user_info["user_email"]
                    for i in range(len(tasks)):
                        if tasks[i]['task_id'] == task_id:
                            tasks[i]['assigned_to'] = user_email
                    
                    self.write_json()
                else:
                    print('You have reached maximum pending task count limit')

    def delete_task(self):

        task_id = int(input('Enter id of the task to delete: '))
        if self.user_role == 0:
            if not any(task['task_id'] == task_id for task in tasks):
                print('There is no task with this ID')
            else:
                for i in range(len(tasks)):
                    if tasks[i]['task_id'] == task_id:
                        task_assignee = tasks[i]['assigned_to']
                        del tasks[i]
                        print('Task deleted!')
                        for user in users:
                            if user['user_email'] == task_assignee and user['taskcount'] > 0:
                                user['taskcount'] = user['taskcount'] - 1
                        break

            self.write_json()

        if self.user_role == 2:
            if not any(task['task_id'] == task_id for task in tasks):
                print('There is no task with this ID')
            else:
                for i in range(len(tasks)):
                    if tasks[i]['task_id'] == task_id:
                        if tasks[i]['delete_request'] == 0:
                            tasks[i]['delete_request'] = 1
                            print('Delete request sent')
                            break
                        else:
                            print('Delete request is pending')
                            break
            self.write_json()

    def edit_task(self):
        task_id = int(input('Enter id of the task to edit: '))
        if not any(task['task_id'] == task_id for task in tasks):
                print('There is no task with this ID')
        else:
            if self.user_role == 0:
                for i in range(len(tasks)):
                    if tasks[i]['task_id'] == task_id:
                        asigned_before = tasks[i]['assigned_to']
                        tasks[i]['name'] = str(input('Enter the new task name: '))
                        
                        asign_to = str(input('Enter the new assignee: '))
                        task_count = len(list(filter(lambda task: task['assigned_to'] == asign_to and task['status'] == 0, tasks)))
                        if task_count > 2:
                            print('User has reached maximum pending task count limit')
                            break
                        else:
                            tasks[i]['assigned_to'] = asign_to
                            tasks[i]['status'] = int(input('Enter the new status:'))
                            asigned_after = tasks[i]['assigned_to']
                            print('task updated')
                            if asigned_before != asigned_after:
                                for user in users:
                                    if user['user_email'] == asigned_before and user['taskcount'] > 0:
                                        user['taskcount'] = user['taskcount'] -1
                                    elif user['user_email'] == asigned_after:
                                        user['taskcount'] = user['taskcount'] + 1
                            break
                    # else:
                    #     print('Error while editing task')
                    #     break
                
                self.write_json()

            if self.user_role == 2:
                for i in range(len(tasks)):
                    #print(tasks[i]['department'], self.department)
                    if tasks[i]['task_id'] == task_id and tasks[i]['department'] == self.department:
                        asigned_before = tasks[i]['assigned_to']
                        tasks[i]['name'] = str(input('Enter the new task name: '))
                        asign_to = str(input('Enter the new assignee: '))
                        task_count = len(list(filter(lambda task: task['assigned_to'] == asign_to and task['status'] == 0, tasks)))
                        if task_count > 2:
                            print('User has reached maximum pending task count limit')
                            break
                        else:
                            tasks[i]['assigned_to'] = asign_to
                            tasks[i]['status'] = int(input('Enter the new status:'))
                            asigned_after = tasks[i]['assigned_to']
                            print('task updated')
                            if asigned_before != asigned_after:
                                for user in users:
                                    if user['user_email'] == asigned_before and user['taskcount'] > 0:
                                        user['taskcount'] = user['taskcount'] -1
                                    elif user['user_email'] == asigned_after:
                                        user['taskcount'] = user['taskcount'] + 1
                    elif tasks[i]['task_id'] == task_id and tasks[i]['department'] != self.department:
                        print('User is not a member of your department.')
                    # else:
                    #     print('You are not authorized to assign this task')
                self.write_json()

def main():
    load_data()
    x = Authentication(False, None)
    if not x.user_registered:
        print('Press 1 to login, 2 to signup or q to exit')

        while True:
            if keyboard.is_pressed("1"):
                res=x.login()
                if res:
                    break
                else:
                    break
            elif keyboard.is_pressed("2"):
                x.sign_up()
                break
            elif keyboard.is_pressed("q"):
                break

    if x.user_registered and x.user_info!=None:
        U = Task(x.user_info, x.user_info["user_role"], x.user_info["user_email"], x.user_info["department"])
        U.display_tasks()
        U.user_activity()
main()