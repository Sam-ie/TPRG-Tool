"""
text_processor/
├── main.py
├── model/
│   ├── __init__.py
│   ├── document_model.py
│   ├── text_processor.py
│   └── language_detector.py
├── view/
│   ├── __init__.py
│   ├── main_window.py
│   ├── analysis_window.py
│   ├── help_window.py
│   └── support_window.py
├── controller/
│   ├── __init__.py
│   └── main_controller.py
├── languages/
│   ├── __init__.py
│   ├── language_factory.py
│   ├── base_language.py
│   ├── chinese_simplified.py
│   ├── chinese_traditional.py
│   ├── english.py
│   └── japanese.py
└── utils/
    ├── __init__.py
    ├── file_manager.py
    └── config.py
"""

import tkinter as tk
from controller.main_controller import MainController


def main():
    root = tk.Tk()

    # 可以从配置中读取相似度阈值
    similarity_threshold = 0.8  # 可配置参数

    app = MainController(root, similarity_threshold)
    root.mainloop()


if __name__ == "__main__":
    main()
