from tkinter import StringVar
from typing import List
from models.task import Task
from models.database import DataBase

class TasksViewModel:
    def __init__(self, database: DataBase):
        self.database = database
        self.description = StringVar()
        self.tasks: List[Task] = []
        self.get_tasks()

    def add_task(self):
        task = Task(description=self.description.get())
        self.database.add_task(task)
        self.get_tasks()

    def get_tasks(self):
        self.tasks = self.database.get_tasks()

    def edit_task(self, task: Task, new_description: str):
        task.description = new_description
        self.database.update_task(task)
        self.get_tasks()

    def delete_task(self, task: Task):
        self.database.delete_task(task)
        self.get_tasks()

    def toggle_task_completion(self, task: Task):
        task.is_done = not task.is_done
        self.database.update_task(task)
        self.get_tasks()