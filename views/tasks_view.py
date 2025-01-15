import tkinter as tk
from tkinter import NORMAL, ttk, PhotoImage
from tkinter import font
from viewmodels.tasks_viewmodel import TasksViewModel
from models.task import Task


class TasksView(ttk.Frame):
    PLACEHOLDER_TEXT = "Task description"
    PLACEHOLDER_COLOR = "gray"
    DEFAULT_ENTRY_TEXT_COLOR = "black"

    def __init__(self, root, view_model: TasksViewModel):
        super().__init__(root)
        self.view_model = view_model

        self.delete_icon = PhotoImage(file="resources/delete_icon.png")
        self.delete_icon = self.delete_icon.subsample(3, 3)

        self.configure(padding=10)

        self.create_widgets()
        self.update_list()

    def create_widgets(self):

        # Entry Style
        self.style = ttk.Style()
        self.style.configure("Placeholder.TEntry", foreground=self.PLACEHOLDER_COLOR)
        self.style.configure("Normal.TEntry", foreground=self.DEFAULT_ENTRY_TEXT_COLOR)
        # Entry with placeholder
        self.entry = ttk.Entry(
            self,
            textvariable=self.view_model.description,
            width=50,
            style="Placeholder.TEntry",
            justify="center",
        )
        self.entry.insert(0, self.PLACEHOLDER_TEXT)
        self.entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.entry.bind("<FocusOut>", self._on_entry_focus_out)
        self.entry.bind("<Return>", lambda e: self.add_task())
        self.entry.grid(row=0, column=1, padx=5, pady=5, columnspan=3, sticky="ew")

        # Frame for tasks list with scrollbar
        self.tasks_frame = ttk.Frame(self)
        self.tasks_frame.grid(
            row=2, column=0, columnspan=4, padx=5, pady=5, sticky="nsew"
        )

        self.canvas = tk.Canvas(self.tasks_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(
            self.tasks_frame, orient="vertical", command=self.canvas.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.task_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.task_frame, anchor="nw")

        self.task_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # Bind double-click event to checkbuttons
        self.task_frame.bind("<Double-1>", self._on_task_double_click)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def _on_entry_focus_in(self, event):
        if self.entry.get() == self.PLACEHOLDER_TEXT:
            self.entry.delete(0, "end")
            self.entry.configure(style="Normal.TEntry")

    def _on_entry_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.PLACEHOLDER_TEXT)
            self.entry.configure(style="Placeholder.TEntry")

    def _on_task_double_click(self, event):
        widget = event.widget
        if isinstance(widget, tk.Checkbutton):
            widget.invoke()

    def add_task(self):
        description = self.view_model.description.get()
        if description != self.PLACEHOLDER_TEXT:
            self.view_model.add_task()
            self.entry.delete(0, "end")
            self.entry.insert(0, self.PLACEHOLDER_TEXT)
            self.entry.configure(style="Placeholder.TEntry")
            self.focus_set()
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
            selected_index = index

        if selected_index is not None:
            task = self.view_model.tasks[selected_index]
            self.view_model.delete_task(task)
            self.update_list()


    def update_list(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        for index, task in enumerate(self.view_model.tasks):
            # checkbutton = ttk.Checkbutton(
            #     self.tasks_frame,
            #     command=lambda i=index: self.view_model.toggle_task_completion(
            #         self.view_model.tasks[i]
            #     ),
            # )
            checkbutton = ttk.Checkbutton(self.tasks_frame)
            
            task_label = ttk.Label(
                self.tasks_frame, 
                text=task.description, 
                anchor="center"
            )

            checkbutton.config( command=lambda i=index, cb=checkbutton, lbl=task_label: self.update_task_status(i, cb, lbl))


            checkbutton.state(
                ["!alternate"] + (["selected"] if task.is_done else ["!selected"])
            )

            task_entry = ttk.Entry(self.tasks_frame, width=40, justify="center")
            task_entry.insert(0, task.description)
            task_entry.grid(row=index, column=1, padx=5, pady=2, sticky="nsew")
            task_entry.grid_remove()
            task_entry.bind(
                "<Return>",
                lambda e, t=task, ent=task_entry, lbl=None: self.on_entry_return(
                    t, ent, lbl
                ),
            )


            self.set_label_style(task_label, task.is_done)

            task_label.grid(row=index, column=1, padx=5, pady=2, sticky="nsew")
            task_label.bind(
                "<Double-1>",
                lambda e, entry=task_entry, label=task_label, t=task: self.on_label_double_click(
                    entry, label, t
                ),
            )

            # Grid widgets
            checkbutton.grid(row=index, column=0, sticky="w")
            task_label.grid(row=index, column=1, sticky="ew")
            task_entry.grid(row=index, column=1, sticky="ew")
            task_entry.grid_remove()
            delete_button = ttk.Button(
                self.tasks_frame,
                image=self.delete_icon,
                command=lambda i=index: self.delete_task(i),
            )
            delete_button.grid(row=index, column=2, padx=5, sticky="e")

            # Configure column weights to make task_label and task_entry expand
            self.tasks_frame.grid_columnconfigure(1, weight=1)
            self.tasks_frame.grid_columnconfigure(2, weight=0)

    def update_task_status(self, index, checkbutton:ttk.Checkbutton, label:ttk.Label):
        task = self.view_model.tasks[index]

        is_selected = "selected" in checkbutton.state()
        
        if is_selected:
            self.set_label_style(label, True)
        else:
            self.set_label_style(label, False)

        self.view_model.toggle_task_completion(task)


    def set_label_style(self, label: ttk.Label, is_done:bool):
        if is_done:
            label.config(font=("Console", 10, "overstrike"))
        else:
            label.config(font=("Console", 10, "normal"))


    def on_label_double_click(self, entry: ttk.Entry, label: ttk.Label, task: Task):
        row = label.grid_info()["row"]
        label.grid_remove()
        entry.grid(row=row, column=1, sticky="w")

    def on_entry_return(self, task: Task, entry: ttk.Entry, label: ttk.Label):
        new_text = entry.get()
        self.view_model.edit_task(task, new_text)
        entry.grid_remove()
        self.update_list()

    def get_selected_task_index(self):
        for index, widget in enumerate(self.tasks_frame.winfo_children()):
            if widget.winfo_class() == "TCheckbutton" and widget.instate(["selected"]):
                return index
        return None
