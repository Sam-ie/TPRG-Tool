import tkinter as tk
from tkinter import ttk


class HelpWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.setup_ui()

    def setup_ui(self):
        self.window.title("帮助")
        self.window.geometry("600x400")

        # TODO: 实现帮助内容
        text = tk.Text(self.window, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(self.window, command=text.yview)
        text.config(yscrollcommand=scrollbar.set)

        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)