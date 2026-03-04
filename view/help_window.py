import tkinter as tk
from tkinter import ttk

class HelpWindow:
    def __init__(self, parent, language_manager):
        self.window = tk.Toplevel(parent)
        self.language_manager = language_manager
        self.setup_ui()

    def setup_ui(self):
        self.window.title(self.language_manager.get_text("help_window_title"))
        self.window.geometry("600x500")

        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        functions_frame = ttk.Frame(notebook)
        notebook.add(functions_frame, text=self.language_manager.get_text("function_intro"))
        self.setup_functions_tab(functions_frame)

        usage_frame = ttk.Frame(notebook)
        notebook.add(usage_frame, text=self.language_manager.get_text("usage_instructions"))
        self.setup_usage_tab(usage_frame)

        about_frame = ttk.Frame(notebook)
        notebook.add(about_frame, text=self.language_manager.get_text("about"))
        self.setup_about_tab(about_frame)

    def setup_functions_tab(self, parent):
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill=tk.BOTH, expand=True)

        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Microsoft YaHei", 10))
        scrollbar = ttk.Scrollbar(text_frame, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        content = self.language_manager.get_text("function_intro_content")
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_usage_tab(self, parent):
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill=tk.BOTH, expand=True)

        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Microsoft YaHei", 10))
        scrollbar = ttk.Scrollbar(text_frame, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        content = self.language_manager.get_text("usage_instructions_content")
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_about_tab(self, parent):
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill=tk.BOTH, expand=True)

        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Microsoft YaHei", 10))
        scrollbar = ttk.Scrollbar(text_frame, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        content = self.language_manager.get_text("about_content")
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
