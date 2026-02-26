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
