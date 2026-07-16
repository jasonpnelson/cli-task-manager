"""
Task Manager program

Allows login, task assignment,viewing,editing, and report generation for a simple task management system.
Maintains tasks.txt and user.txt for storage of tasks and user credentials.
"""

import os
from datetime import datetime, date

# Date format for storing and displaying dates
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Ensure tasks file exists
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w", encoding="utf-8") as default_file:
        pass

# Load tasks
with open("tasks.txt", "r", encoding="utf-8") as task_file:
    task_data = [line for line in task_file.read().split("\n") if line.strip()]

# store all tasks as dictionaries in a list
task_list = []
for task in task_data:
    task_components = task.split(";")
    if len(task_components) < 6:
        continue
    current_task = {
        "username": task_components[0],
        "title": task_components[1],
        "description": task_components[2],
    }
    try:
        current_task["due_date"] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    except ValueError:
        current_task["due_date"] = datetime.now()
    try:
        current_task["assigned_date"] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    except ValueError:
        current_task["assigned_date"] = datetime.now()
    current_task["completed"] = task_components[5].strip().lower() == "yes"
    task_list.append(current_task)

# Ensure user file exists and load users into a dictionary
if not os.path.exists("user.txt"):
    with open("user.txt", "w", encoding="utf-8") as default_file:
        default_file.write("admin;password")

with open("user.txt", "r", encoding="utf-8") as user_file:
    user_data = [line for line in user_file.read().split("\n") if line.strip()]

username_password = {}
for user in user_data:
    if ";" not in user:
        continue
    username, password = user.split(";", 1)
    username_password[username] = password

# login system
while True:
    print("LOGIN")
    current_user = input("Username: ")
    current_pass = input("Password: ")
    if current_user not in username_password:
        print("User does not exist")
        continue
    if username_password[current_user] != current_pass:
        print("Wrong password")
        continue
    print("Login Successful!")
    break

def reg_user():
    """
    Register a new user.

    Only the admin can register a user.
    Prompts for username and password and saves it to user.txt.
    """
    while True:
        new_username = input("New username: ")
        if not new_username:
            print("Username cannot be empty.")
            continue
        if new_username in username_password:
            print("Username already exists, please choose another username.")
            continue

        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")

        if new_password != confirm_password:
            print("Passwords do not match, please try again.")
            continue

        username_password[new_username] = new_password

        with open("user.txt", "w", encoding="utf-8") as out_file:
            user_lines = [f"{u};{p}" for u, p in username_password.items()]
            out_file.write("\n".join(user_lines))

        print("User registered successfully!")
        break

def add_task():
    """
    Add a new task and save it to tasks.txt.
    """
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password:
            print("User does not exist, please enter a valid username.")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")

        while True:
            task_due_input = input("Due date of task (YYYY-MM-DD): ")
            try:
                task_due_date = datetime.strptime(task_due_input, DATETIME_STRING_FORMAT)
                break
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

        current_date = datetime.now()
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": task_due_date,
            "assigned_date": current_date,
            "completed": False
        }

        task_list.append(new_task)
        _write_tasks()
        print("Task added successfully!")
        break

def _write_tasks():
    """Write the current task list to tasks.txt in the specified format.
        Each task is written as a line with attributes separated by semicolons:"""
    with open("tasks.txt", "w", encoding="utf-8") as out_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        out_file.write("\n".join(task_list_to_write))

def view_all():
    """
    Display all tasks in a readable format.
    """
    if not task_list:
        print("No tasks to display.")
        return

    for task in task_list:
        display = (
            f"Task: \t\t{task['title']}\n"
            f"Assigned to: \t{task['username']}\n"
            f"Date Assigned: \t{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            f"Due Date: \t{task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            f"Task Description:\n{task['description']}\n"
            f"Completed: \t{'Yes' if task['completed'] else 'No'}\n"
        )
        print(display)

def view_mine():
    """
    Display tasks assigned to the current user.

    Allows the user to mark a task as complete or edit its details.
    """
    user_tasks = [task for task in task_list if task['username'] == current_user]

    if not user_tasks:
        print("You have no tasks assigned.")
        return

    for i, task in enumerate(user_tasks, 1):
        display = (
            f"Task {i}:\n"
            f"Title: \t\t{task['title']}\n"
            f"Date Assigned: \t{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            f"Due Date: \t{task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            f"Task Description:\n{task['description']}\n"
            f"Completed: \t{'Yes' if task['completed'] else 'No'}\n"
        )
        print(display)

    while True:
        task_choice = input("Enter the number of the task you want to edit (or -1 to return to main menu): ")
        if task_choice == "-1":
            return
        if not task_choice.isdigit() or int(task_choice) < 1 or int(task_choice) > len(user_tasks):
            print("Invalid choice, please try again.")
            continue

        task_index = int(task_choice) - 1
        selected_task = user_tasks[task_index]

        if selected_task['completed']:
            print("This task is already completed and cannot be edited.")
            return

        action = input("Enter 'c' to mark as complete or 'e' to edit the task: ").lower()
        if action == 'c':
            selected_task['completed'] = True
            _write_tasks()
            print("Task marked as complete.")
            return
        elif action == 'e':
            new_username = input("Enter new username to assign task to (or press Enter to keep current): ")
            if new_username:
                if new_username in username_password:
                    selected_task['username'] = new_username
                else:
                    print("User does not exist, keeping current assignment.")

            new_due_date = input("Enter new due date (YYYY-MM-DD) (or press Enter to keep current): ")
            if new_due_date:
                try:
                    selected_task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                except ValueError:
                    print("Invalid date format, keeping current due date.")

            _write_tasks()
            print("Task updated successfully.")
            return
        else:
            print("Unknown action, returning to menu.")
            return

def generate_reports():
    """
    Generate a task overview report.

    Calculates total tasks, completed, incomplete, and overdue tasks,
    and writes them to task_overview.txt.
    """
    total_tasks = len(task_list)
    completed_tasks = sum(1 for task in task_list if task['completed'])
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(
        1 for task in task_list
        if not task['completed'] and task['due_date'] < datetime.now()
    )
    percent_overdue = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    percent_incomplete = (incomplete_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    with open("task_overview.txt", "w", encoding="utf-8") as task_report:
        task_report.write(f"Total tasks: {total_tasks}\n")
        task_report.write(f"Completed tasks: {completed_tasks}\n")
        task_report.write(f"Incomplete tasks: {incomplete_tasks}\n")
        task_report.write(f"Overdue tasks: {overdue_tasks}\n")
        task_report.write(f"Percent incomplete: {percent_incomplete:.2f}%\n")
        task_report.write(f"Percent overdue: {percent_overdue:.2f}%\n")

def generate_user_overview():
    """
    Generate a user overview report.

    For each user, calculates number of tasks, completed tasks,
    and writes the report to user_overview.txt.
    """
    total_tasks = len(task_list)
    total_users = len(username_password)

    with open("user_overview.txt", "w", encoding="utf-8") as f:
        f.write(f"Total users: {total_users}\n")
        f.write(f"Total tasks: {total_tasks}\n\n")

        for user in username_password:
            user_tasks = [task for task in task_list if task['username'] == user]
            total_user_tasks = len(user_tasks)
            completed = sum(1 for task in user_tasks if task['completed'])
            uncompleted = total_user_tasks - completed
            overdue = sum(1 for task in user_tasks if not task['completed'] and task['due_date'].date() < date.today())

            percent_total = (total_user_tasks / total_tasks * 100) if total_tasks else 0
            percent_completed = (completed / total_user_tasks * 100) if total_user_tasks else 0
            percent_uncompleted = (uncompleted / total_user_tasks * 100) if total_user_tasks else 0
            percent_overdue = (overdue / total_user_tasks * 100) if total_user_tasks else 0

            f.write(f"User: {user}\n")
            f.write(f"  Total tasks: {total_user_tasks}\n")
            f.write(f"  % of total tasks: {percent_total:.2f}%\n")
            f.write(f"  % completed: {percent_completed:.2f}%\n")
            f.write(f"  % uncompleted: {percent_uncompleted:.2f}%\n")
            f.write(f"  % overdue: {percent_overdue:.2f}%\n\n")

def display_statistics():
    """
    Display task and user statistics.

    Generates reports if missing, then prints task_overview.txt and
    user_overview.txt contents.
    """
    if (not os.path.exists("task_overview.txt") or
            not os.path.exists("user_overview.txt")):
        print("Reports not found. Generating reports now...")
        generate_reports()
        generate_user_overview()

    print("\n===== TASK OVERVIEW =====")
    with open("task_overview.txt", "r", encoding="utf-8") as f:
        print(f.read())

    print("===== USER OVERVIEW =====")
    with open("user_overview.txt", "r", encoding="utf-8") as f:
        print(f.read())

# Main program loop
while True:
    print()
    menu = input("Select one of the following Options below:\n"
                 "r - Register a user\n"
                 "a - Add a task\n"
                 "va - View all tasks\n"
                 "vm - View my tasks\n"
                 "gr - Generate reports (admin only)\n"
                 "ds - Display statistics (admin only)\n"
                 "e - Exit\n"
                 ": ").lower()

    if menu == "r" and current_user == "admin":
        reg_user()
    elif menu == "r":
        print("Admin only.")

    elif menu == "a":
        add_task()

    elif menu == "va":
        view_all()

    elif menu == "vm":
        view_mine()

    elif menu == "gr" and current_user == "admin":
        generate_reports()
        generate_user_overview()
        print("Reports generated.")

    elif menu == "ds" and current_user == "admin":
        display_statistics()

    elif menu == "e":
        print("Goodbye!")
        break

    else:
        print("Invalid option.")
