import tkinter as tk
from tkinter import ttk


class SupportWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.setup_ui()

    def setup_ui(self):
        self.window.title("支持作者")
        self.window.geometry("400x300")

        # TODO: 实现支持作者界面（放置图片等）
        label = ttk.Label(self.window, text="感谢支持！")
        label.pack(expand=True)