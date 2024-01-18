#this is change
from algorithms import window
import sys
from PyQt5.QtWidgets import *

# class MyWindow(window.MyWindow):
#     def __init__(self):
#         super().__init__()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = window.MyWindow()
    window.show()
    app.exec_()