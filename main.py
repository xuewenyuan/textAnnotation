import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)    #创建QApplication类的实例
    mainWindow = MainWindow()              #创建DumbDialog类的实例
    mainWindow.show()                      #显示程序主窗口
    sys.exit(app.exec_())                   #开启事件主循环
