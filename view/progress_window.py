import tkinter as tk
from tkinter import ttk


class ProgressWindow:
    def __init__(self, parent, language_manager, title: str, total_steps: int = 100):
        self.window = tk.Toplevel(parent)
        self.language_manager = language_manager
        self.total_steps = total_steps
        self.current_step = 0
        self._updating = False
        self.running = True
        self.cancel_callback = None

        self.setup_ui(title)
        self.center_on_parent(parent)
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

    def set_cancel_callback(self, callback):
        """设置取消回调函数，当用户关闭窗口时调用"""
        self.cancel_callback = callback

    def _on_close(self):
        """窗口关闭时的处理"""
        if self.cancel_callback:
            self.cancel_callback()
        self.close()

    def setup_ui(self, title: str):
        self.window.title(title)
        self.window.geometry("400x120")
        self.window.resizable(False, False)

        self.window.transient(self.window.master)
        self.window.grab_set()

        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.status_label = ttk.Label(main_frame, text=self.language_manager.get_text("reading_file"),
                                      font=("Microsoft YaHei", 10))
        self.status_label.pack(pady=(0, 10))

        self.progress_bar = ttk.Progressbar(
            main_frame,
            orient=tk.HORIZONTAL,
            length=360,
            mode='determinate',
            maximum=self.total_steps
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))

        self.percentage_label = ttk.Label(main_frame, text="0%", font=("Microsoft YaHei", 9))
        self.percentage_label.pack()

        self.window.update()

    def center_on_parent(self, parent):
        self.window.update_idletasks()

        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        width = self.window.winfo_width()
        height = self.window.winfo_height()

        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2

        self.window.geometry(f"+{x}+{y}")

    def update_progress(self, current: int, total: int, status: str = ""):
        if not self.running or self._updating:
            return
        self._updating = True
        try:
            if total != self.total_steps:
                self.total_steps = total
                self.progress_bar['maximum'] = total

            if total > 0:
                percentage = min(int((current / total) * 100), 100)
            else:
                percentage = 0

            self.progress_bar['value'] = current
            self.percentage_label.config(text=f"{percentage}%")

            if status:
                self.status_label.config(text=status)
            else:
                processing_text = self.language_manager.get_text("processing")
                self.status_label.config(text=f"{processing_text}: {current}/{total}")

            self.window.update()
        finally:
            self._updating = False

    def complete(self, message: str = ""):
        if not self.running:
            return
        max_val = self.progress_bar['maximum']
        self.progress_bar['value'] = max_val
        self.percentage_label.config(text="100%")

        if message:
            self.status_label.config(text=message)
        else:
            self.status_label.config(text=self.language_manager.get_text("completed"))

        self.window.update()
        self.window.after(600, self.close)

    def close(self):
        self.running = False
        if self.window.winfo_exists():
            self.window.grab_release()
            self.window.destroy()
