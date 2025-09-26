import tkinter as tk
from tkinter import ttk


class SupportWindow:
    def __init__(self, parent, language_manager):
        self.window = tk.Toplevel(parent)
        self.language_manager = language_manager
        self.setup_ui()

    def setup_ui(self):
        self.window.title(self.language_manager.get_text("support_window_title"))
        self.window.geometry("400x500")

        # 主框架
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 标题
        title_label = ttk.Label(main_frame, text=self.language_manager.get_text("thank_you_support"),
                                font=("Microsoft YaHei", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # 图片占位区域
        image_frame = ttk.LabelFrame(main_frame, text=self.language_manager.get_text("support_author_title"),
                                     height=200)
        image_frame.pack(fill=tk.X, pady=(0, 20))
        image_frame.pack_propagate(False)  # 防止框架收缩

        # 图片占位符
        canvas = tk.Canvas(image_frame, bg="lightgray", relief=tk.SUNKEN, borderwidth=1)
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        canvas.create_text(150, 100, text="图片区域\n(功能待实现)",
                           font=("Microsoft YaHei", 12), fill="gray")

        # 支持信息文本
        support_text = f"""
感谢您使用文本处理工具！

如果您觉得这个软件对您有帮助，请考虑支持我们的开发工作。

{self.language_manager.get_text('support_methods')}：
• 分享给更多用户
• 提供宝贵建议
• 反馈使用问题

您的支持是我们持续改进的动力！

联系邮箱：TODO
项目地址：TODO
"""
        text_label = ttk.Label(main_frame, text=support_text, font=("Microsoft YaHei", 10),
                               justify=tk.LEFT, wraplength=350)
        text_label.pack(fill=tk.X, pady=(0, 20))

        # 关闭按钮
        ttk.Button(main_frame, text=self.language_manager.get_text("close"),
                   command=self.window.destroy).pack()