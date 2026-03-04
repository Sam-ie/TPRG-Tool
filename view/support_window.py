import tkinter as tk
from tkinter import ttk
import os

try:
    from PIL import Image, ImageTk

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class SupportWindow:
    def __init__(self, parent, language_manager):
        self.window = tk.Toplevel(parent)
        self.language_manager = language_manager
        self.setup_ui()

    def setup_ui(self):
        self.window.title(self.language_manager.get_text("support_window_title"))
        self.window.geometry("500x600")

        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title_label = ttk.Label(main_frame, text=self.language_manager.get_text("thank_you_support"),
                                font=("Microsoft YaHei", 16, "bold"))
        title_label.pack(pady=(0, 20))

        image_frame = ttk.LabelFrame(main_frame, text=self.language_manager.get_text("support_author_title"))
        image_frame.pack(fill=tk.X, pady=(0, 20))

        inner_frame = ttk.Frame(image_frame)
        inner_frame.pack(fill=tk.X, padx=10, pady=10)

        self.create_qr_frame(inner_frame, "wechat", self.language_manager.get_text("wechat_pay"))
        self.create_qr_frame(inner_frame, "BMAC", "Buy Me A Coffee")  # 专有名词保留

        support_text = self.language_manager.get_text("support_text_content")
        text_label = ttk.Label(main_frame, text=support_text, font=("Microsoft YaHei", 10),
                               justify=tk.LEFT, wraplength=450)
        text_label.pack(fill=tk.X, pady=(0, 20))

    def create_qr_frame(self, parent, name, display_name):
        frame = ttk.Frame(parent)
        frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)

        canvas = tk.Canvas(frame, width=150, height=150, bg="white", relief=tk.SUNKEN, borderwidth=1)
        canvas.pack(pady=(0, 5))

        img_path = os.path.join(os.path.dirname(__file__), "..", "images", f"{name}_qr.png")
        if os.path.exists(img_path) and PIL_AVAILABLE:
            try:
                img = Image.open(img_path)
                img = img.resize((140, 140), Image.LANCZOS)
                tk_img = ImageTk.PhotoImage(img)
                canvas.create_image(75, 75, image=tk_img, anchor=tk.CENTER)
                canvas.image = tk_img  # 防止自动回收
            except Exception as e:
                canvas.create_text(75, 75, text=self.language_manager.get_text("image_load_failed"),
                                   font=("Microsoft YaHei", 10), fill="gray")
        else:
            if not PIL_AVAILABLE:
                placeholder = self.language_manager.get_text("need_pil")
            else:
                placeholder = self.language_manager.get_text("please_place_image")
            canvas.create_text(75, 75, text=placeholder, font=("Microsoft YaHei", 10), fill="gray")

        ttk.Label(frame, text=display_name, font=("Microsoft YaHei", 9)).pack()
