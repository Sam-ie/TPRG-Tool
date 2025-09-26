import tkinter as tk
from tkinter import ttk


class AnalysisWindow:
    def __init__(self, parent, controller):
        self.window = tk.Toplevel(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        self.window.title("智能分析")
        self.window.geometry("800x600")

        # TODO: 实现可视化图表展示
        notebook = ttk.Notebook(self.window)

        # 字数统计标签页
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="字数统计")

        # 词云标签页
        wordcloud_frame = ttk.Frame(notebook)
        notebook.add(wordcloud_frame, text="词云")

        # 标点符号标签页
        punctuation_frame = ttk.Frame(notebook)
        notebook.add(punctuation_frame, text="标点符号")

        # TODO: 预留拓展位置
        todo_frame = ttk.Frame(notebook)
        notebook.add(todo_frame, text="待拓展")

        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)