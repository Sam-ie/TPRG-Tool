import tkinter as tk
from tkinter import ttk
import os

# 尝试导入 PIL 处理图片
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class SupportWindow:
    def __init__(self, parent, language_manager):
        self.window = tk.Toplevel(parent)
        self.language_manager = language_manager
        self.images = []  # 保持图片引用
        self.setup_ui()

    def setup_ui(self):
        self.window.title(self.language_manager.get_text("support_window_title"))
        self.window.geometry("500x600")  # 增大窗口以容纳图片

        # 主框架
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 标题
        title_label = ttk.Label(main_frame, text=self.language_manager.get_text("thank_you_support"),
                                font=("Microsoft YaHei", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # 图片区域
        image_frame = ttk.LabelFrame(main_frame, text=self.language_manager.get_text("support_author_title"))
        image_frame.pack(fill=tk.X, pady=(0, 20))

        # 水平排列图片
        inner_frame = ttk.Frame(image_frame)
        inner_frame.pack(fill=tk.X, padx=10, pady=10)

        # 创建两个二维码图片（国内：微信支付，国外：Patreon）
        self.create_qr_frame(inner_frame, "wechat", "微信支付")
        self.create_qr_frame(inner_frame, "patreon", "Patreon")

        # 支持信息文本
        support_text = f"""
感谢您使用文本处理工具！

如果您觉得这个软件对您有帮助，请考虑支持我的开发工作。

{self.language_manager.get_text('support_methods')}：
• 分享给更多用户
• 提供宝贵建议
• 反馈使用问题

联系邮箱：1163429473@qq.com
项目地址：https://github.com/Sam-ie/TPRG-Tool
"""
        text_label = ttk.Label(main_frame, text=support_text, font=("Microsoft YaHei", 10),
                               justify=tk.LEFT, wraplength=450)
        text_label.pack(fill=tk.X, pady=(0, 20))

        # 关闭按钮
        ttk.Button(main_frame, text=self.language_manager.get_text("close"),
                   command=self.window.destroy).pack()

    def create_qr_frame(self, parent, name, display_name):
        """创建一个包含二维码图片和标签的框架"""
        frame = ttk.Frame(parent)
        frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)

        # 图片显示区域
        canvas = tk.Canvas(frame, width=150, height=150, bg="white", relief=tk.SUNKEN, borderwidth=1)
        canvas.pack(pady=(0, 5))

        # 尝试加载图片（路径：项目根目录/images/xxx_qr.png）
        img_path = os.path.join(os.path.dirname(__file__), "..", "images", f"{name}_qr.png")
        if os.path.exists(img_path) and PIL_AVAILABLE:
            try:
                img = Image.open(img_path)
                img = img.resize((140, 140), Image.LANCZOS)
                tk_img = ImageTk.PhotoImage(img)
                canvas.create_image(75, 75, image=tk_img, anchor=tk.CENTER)
                self.images.append(tk_img)  # 保持引用
            except Exception as e:
                canvas.create_text(75, 75, text="图片加载失败", font=("Microsoft YaHei", 10), fill="gray")
        else:
            # 图片不存在或PIL不可用
            if not PIL_AVAILABLE:
                placeholder = "需安装PIL"
            else:
                placeholder = "请放置图片"
            canvas.create_text(75, 75, text=placeholder, font=("Microsoft YaHei", 10), fill="gray")

        # 标签
        ttk.Label(frame, text=display_name, font=("Microsoft YaHei", 9)).pack()