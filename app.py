import sys
from PySide6.QtWidgets import QApplication

from model.model import TransactionModel
from view.view import MainWindow as MainView # 重命名以避免与主模块名冲突
from controller.controller import Controller

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 1. 创建 Model
    # init_db() 在 TransactionModel 的 __init__ 中被调用，所以这里不需要显式调用
    model = TransactionModel()

    # 2. 创建 View
    view = MainView()

    # 3. 创建 Controller 并连接 Model 和 View
    controller = Controller(model=model, view=view)
    
    # 4. 显示主窗口 (由 View 控制)
    view.show()
    
    sys.exit(app.exec())
