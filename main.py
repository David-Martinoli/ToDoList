from tkinter import Tk
from models.database import DataBase
from viewmodels.tasks_viewmodel import TasksViewModel
from views.tasks_view import TasksView

if __name__ == "__main__":
    root = Tk()
    root.title("Tasks App")
    db = DataBase()
    view_model = TasksViewModel(db)
    view = TasksView(root, view_model)
    view.pack(expand=True, fill='both')
    root.mainloop()