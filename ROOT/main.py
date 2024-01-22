
from algorithms import window
import sys
from PyQt5.QtWidgets import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = window.BitNoteWindow()
    window.show()
    app.exec_()