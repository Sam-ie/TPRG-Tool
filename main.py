# main.py
import tkinter as tk
from model import ApplicationModel
from view import GUIView
from controller import Controller


def main():
    # 创建主窗口
    root = tk.Tk()
    root.title("文本处理与分析工具")
    root.geometry("800x600")

    # 初始化模型
    model = ApplicationModel()

    # 初始化视图
    view = GUIView(root)

    # 初始化控制器
    controller = Controller(model, view)

    # 将视图注册为模型的观察者
    model.attach(view)

    # 初始更新视图
    view.update(model)

    # 显示主窗口
    root.mainloop()


if __name__ == '__main__':
    main()
