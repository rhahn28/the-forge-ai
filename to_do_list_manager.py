# Simple To-Do List Manager

tasks = []

def add_task(task):
    tasks.append(task)
    return f'Task "{task}" added.'

def remove_task(task):
    if task in tasks:
        tasks.remove(task)
        return f'Task "{task}" removed.'
    else:
        return 'Task not found.'

def list_tasks():
    return tasks
