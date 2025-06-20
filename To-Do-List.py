# Copyright © 2025 Raj Code Hub. All rights reserved.

import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("350x500")

        self.tasks = []
        self.load_tasks()

        # GUI Elements
        tk.Label(root, text="Task:").pack(pady=5)
        self.entry_desc = tk.Entry(root)
        self.entry_desc.pack(pady=5, padx=20, fill="x")

        tk.Label(root, text="Priority:").pack(pady=5)
        self.priority_var = tk.StringVar(value="Low")
        ttk.Combobox(root, textvariable=self.priority_var, values=["Low", "Medium", "High"], state="readonly").pack(pady=5, padx=20, fill="x")

        tk.Label(root, text="Due Date (YYYY-MM-DD):").pack(pady=5)
        self.entry_due_date = tk.Entry(root)
        self.entry_due_date.pack(pady=5, padx=20, fill="x")
        self.entry_due_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        self.task_listbox = tk.Listbox(root, height=10)
        self.task_listbox.pack(pady=10, padx=20, fill="x")
        self.update_task_listbox()

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="Add", command=self.add_task, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Edit", command=self.edit_task, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Complete", command=self.mark_complete, bg="#FF9800", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Delete", command=self.delete_task, bg="#F44336", fg="white").grid(row=0, column=3, padx=5)

        # Add copyright notice at the bottom
        copyright_label = tk.Label(root, text="© 2025 Raj Code Hub. All rights reserved.", 
                                  font=("Arial", 8), fg="#666666")
        copyright_label.pack(pady=10)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)

    def add_task(self):
        desc, due_date = self.entry_desc.get().strip(), self.entry_due_date.get().strip()
        if not desc:
            messagebox.showerror("Error", "Task description is required.")
            return
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid due date (YYYY-MM-DD).")
            return
        self.tasks.append({"description": desc, "completed": False, "priority": self.priority_var.get(), "due_date": due_date})
        self.save_tasks()
        self.update_task_listbox()
        self.clear_entries()

    def edit_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select a task to edit.")
            return
        index = selected[0]
        desc, due_date = self.entry_desc.get().strip(), self.entry_due_date.get().strip()
        if not desc:
            messagebox.showerror("Error", "Task description is required.")
            return
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid due date (YYYY-MM-DD).")
            return
        self.tasks[index] = {"description": desc, "completed": self.tasks[index]["completed"], "priority": self.priority_var.get(), "due_date": due_date}
        self.save_tasks()
        self.update_task_listbox()
        self.clear_entries()

    def mark_complete(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select a task to mark as completed.")
            return
        self.tasks[selected[0]]["completed"] = True
        self.save_tasks()
        self.update_task_listbox()

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select a task to delete.")
            return
        self.tasks.pop(selected[0])
        self.save_tasks()
        self.update_task_listbox()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "Completed" if task["completed"] else "Pending"
            self.task_listbox.insert(tk.END, f"{task['description']} [P: {task['priority']}, Due: {task['due_date']}, {status}]")

    def clear_entries(self):
        self.entry_desc.delete(0, tk.END)
        self.priority_var.set("Low")
        self.entry_due_date.delete(0, tk.END)
        self.entry_due_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
