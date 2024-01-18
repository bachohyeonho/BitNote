import sys
from PyQt5.QtWidgets import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        #파일, 편집, 포멧, 보기, 윈도우, 도움
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)

        # file menu action
        self.new_action = QAction("New")
        self.new_action.triggered.connect(self.newFile)
        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.close)

        # help menu action
        self.doc_action = QAction("Documentation")
        self.release_action = QAction("Release Notes")
        self.license_action = QAction("View License")

        # file menu
        file_menu = self.menubar.addMenu("File")
        file_menu.addAction(self.new_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)

        #edit menu
        edit_menu = self.menubar.addMenu("Edit")
        
        #format menu
        format_menu = self.menubar.addMenu("Format")
        
        #view menu
        view_menu = self.menubar.addMenu("View")
        
        #window menu
        window_menu = self.menubar.addMenu("Window")
        
        # help menu
        help_menu = self.menubar.addMenu("Help")
        help_menu.addAction(self.doc_action)
        help_menu.addAction(self.release_action)
        help_menu.addAction(self.license_action)
        
    def initUI(self):
        central_widget = QWidget()
        vbox = QVBoxLayout(central_widget)
        self.te = QTextEdit()
        self.te.setAcceptRichText(True)
        
        vbox.addStretch(0)
        vbox.addWidget(self.te)
        vbox.addStretch(0)


        self.setCentralWidget(central_widget)
        
        self.setWindowTitle("BitNote")
        self.setGeometry(20, 20, 1000, 700)     
    
    def newFile(self):
        print("created New File")
        print(self)
               


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()