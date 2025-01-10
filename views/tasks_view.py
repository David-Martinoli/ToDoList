import tkinter as tk
from tkinter import ttk
from viewmodels.tasks_viewmodel import TasksViewModel
from models.task import Task

class TasksView(ttk.Frame):
    def __init__(self, root, view_model: TasksViewModel):
        super().__init__(root)
        self.view_model = view_model

        self.configure(padding=10)
        
        self.create_widgets()
        self.update_list()

    def create_widgets(self):
        # Entry for task description
        self.entry_label = ttk.Label(self, text="Task Description:")
        self.entry_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.entry = ttk.Entry(self, textvariable=self.view_model.description, width=40)
        self.entry.grid(row=0, column=1, padx=5, pady=5, columnspan=3, sticky="ew")

        # Add task button
        self.add_button = ttk.Button(self, text="Add Task", command=self.add_task)
        self.add_button.grid(row=1, column=0, padx=5, pady=5, columnspan=4, sticky="ew")

        # Frame for tasks list with scrollbar
        self.tasks_frame = ttk.Frame(self)
        self.tasks_frame.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        self.canvas = tk.Canvas(self.tasks_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.tasks_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.task_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.task_frame, anchor="nw")

        self.task_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Bind double-click event to checkbuttons
        self.task_frame.bind("<Double-1>", self.on_double_click)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)


    def on_double_click(self, event):
        widget = event.widget
        if isinstance(widget, tk.Checkbutton):
            widget.invoke()

    def add_task(self):
        self.view_model.add_task()
        self.update_list()

    def edit_task(self, index=None):
        if index is None:
            selected_index = self.get_selected_task_index()
        else:
            selected_index = index

        if selected_index is not None:
            task = self.view_model.tasks[selected_index]
            new_description = self.entry.get()
            self.view_model.edit_task(task, new_description)
            self.update_list()

    def delete_task(self, index=None):
        if index is None:
            selected_index = self.get_selected_task_index()
        else:
            selected_index is index

        if selected_index is not None:
            task = self.view_model.tasks[selected_index]
            self.view_model.delete_task(task)
            self.update_list()

    def complete_task(self):
        selected_index = self.get_selected_task_index()
        if selected_index is not None:
            task = self.view_model.tasks[selected_index]
            self.view_model.toggle_task_completion(task)
            self.update_list()

    def update_list(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        for index, task in enumerate(self.view_model.tasks):
            var = tk.BooleanVar(value=task.is_done)
            checkbutton = ttk.Checkbutton(self.tasks_frame, text="", variable=var, onvalue=True, offvalue=False,  
            command=lambda i=index: self.view_model.toggle_task_completion(self.view_model.tasks[i]))

            if task.is_done:
                checkbutton.state(['selected'])

            
            task_entry = ttk.Entry(self.tasks_frame, width=40)
            task_entry.insert(0, task.description)
            task_entry.grid_remove()
            task_entry.bind('<Return>', lambda e, t=task, ent=task_entry, lbl=None: self.on_entry_return(t, ent, lbl))
            
            task_label = ttk.Label(self.tasks_frame, text=task.description)
            task_label.bind('<Double-1>', lambda e, entry=task_entry, label=task_label, t=task: self.on_label_double_click(entry, label, t))
            task_label.grid(row=index, column=1, sticky="w")
            
            checkbutton.grid(row=index, column=0, sticky="w")

            delete_button = ttk.Button(self.tasks_frame, text="X", 
                command=lambda i=index: self.delete_task(i))
            delete_button.grid(row=index, column=3, padx=5)

    def on_label_double_click(self, entry: ttk.Entry, label: ttk.Label, task: Task):
        row = label.grid_info()['row']
        label.grid_remove()
        entry.grid(row=row, column=1, sticky="w")

    def on_entry_return(self, task: Task, entry: ttk.Entry, label: ttk.Label):
        new_text = entry.get()
        self.view_model.edit_task(task, new_text)
        entry.grid_remove()
        self.update_list()
    
    def get_selected_task_index(self):
        for index, widget in enumerate(self.tasks_frame.winfo_children()):
            if widget.winfo_class() == 'TCheckbutton' and widget.instate(['selected']):
                return index
        return None