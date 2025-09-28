import tkinter as tk
from tkinter import ttk
from typing import Optional


class ProgressWindow:
    def __init__(self, parent, language_manager, title: str, total_steps: int = 100):
        self.window = tk.Toplevel(parent)
        self.language_manager = language_manager
        self.total_steps = total_steps
        self.current_step = 0

        self.setup_ui(title)
        self.center_on_parent(parent)

    def setup_ui(self, title: str):
        """设置进度条窗口UI"""
        self.window.title(title)
        self.window.geometry("400x120")
        self.window.resizable(False, False)

        # 设置窗口居中
        self.window.transient(self.window.master)
        self.window.grab_set()

        # 主框架
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 进度标签
        self.status_label = ttk.Label(main_frame, text=self.language_manager.get_text("reading_file"),
                                      font=("Microsoft YaHei", 10))
        self.status_label.pack(pady=(0, 10))

        # 进度条
        self.progress_bar = ttk.Progressbar(
            main_frame,
            orient=tk.HORIZONTAL,
            length=360,
            mode='determinate',
            maximum=self.total_steps
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))

        # 进度百分比标签
        self.percentage_label = ttk.Label(main_frame, text="0%", font=("Microsoft YaHei", 9))
        self.percentage_label.pack()

        # 强制更新界面
        self.window.update()

    def center_on_parent(self, parent):
        """将窗口居中显示在父窗口中心"""
        self.window.update_idletasks()  # 确保窗口尺寸已计算

        # 获取父窗口位置和尺寸
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # 获取进度窗口尺寸
        width = self.window.winfo_width()
        height = self.window.winfo_height()

        # 计算居中位置
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2

        # 设置窗口位置
        self.window.geometry(f"+{x}+{y}")

    def update_progress(self, current: int, total: int, status: str = ""):
        """更新进度"""
        if total > 0:
            percentage = min(int((current / total) * 100), 100)
        else:
            percentage = 0

        self.progress_bar['value'] = percentage
        self.percentage_label.config(text=f"{percentage}%")

        if status:
            self.status_label.config(text=status)
        else:
            processing_text = self.language_manager.get_text("processing")
            self.status_label.config(text=f"{processing_text}: {current}/{total}")

        # 强制更新界面
        self.window.update()

    def complete(self, message: str = ""):
        """完成进度"""
        self.progress_bar['value'] = 100
        self.percentage_label.config(text="100%")

        if message:
            self.status_label.config(text=message)
        else:
            self.status_label.config(text=self.language_manager.get_text("completed"))

        self.window.update()

        # 0.6秒后自动关闭
        self.window.after(600, self.close)

    def close(self):
        """关闭窗口"""
        if self.window.winfo_exists():  # 确保窗口还存在
            self.window.grab_release()
            self.window.destroy()