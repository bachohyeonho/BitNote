import os
import sys
from PyQt5.QtWidgets import *

class MyWindow(QMainWindow):
    def __init__(self, fileNumber, fileNumbersLocation):
        super().__init__()
        self.initUI()
        self.fileNumber = fileNumber
        self.fileNumbersLocation = fileNumbersLocation
        self.textHasBeenOpened = False
        self.currentFileLocation = None
        
        #파일, 편집, 포멧, 보기, 윈도우, 도움
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)

        # file menu action
        self.new_action = QAction("New")
        self.new_action.triggered.connect(self.createNewFile)
        self.open_action = QAction("Open")
        self.open_action.triggered.connect(self.openFile)
        self.save_action = QAction("Save")
        self.save_action.triggered.connect(self.saveFile)
        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.close)

        # help menu action
        self.doc_action = QAction("Documentation")
        self.release_action = QAction("Release Notes")
        self.license_action = QAction("View License")

        # file menu
        file_menu = self.menubar.addMenu("File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.open_action)
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
    
    def createNewFile(self, fileNumbersLocation):
        self.fileNumber += 1
        print("created New File %d"%self.fileNumber)
        print(self)
        fileName = './txtFiles/Unnamed Note %d.txt'%self.fileNumber
        newTxtFile = open(fileName, 'w')
        
        #wirte the FileNumbers
        with open(fileNumbersLocation, 'w') as FileNumbers:
            FileNumbers.write(str(self.fileNumber))
            print('fileNumber.txt updated', self.fileNumber)
    
    def openFile(self):

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly 
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
        self.currentFileLocation = file_path
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.te.setPlainText(content)
    def changeDetect(self):
        #detect whether txt has changed or not.
        print("change detector initating")

    def singleStepSave(self, currentFileLocation):        
        print("single step save initiated")
        # This will let you access the test in your QTextEdit
        Text = self.te.toPlainText()
        # This will prevent you from an error if pressed cancel on file dialog.
        # Finally this will Save your file to the path selected.
        with open(currentFileLocation, 'w') as file:
            file.write(Text)    
            
    
    def saveFile(self):
        if self.currentFileLocation != None: #we have opened the existing file
            self.singleStepSave(self.currentFileLocation)
        
        else:
            S__File = QFileDialog.getSaveFileName(None,'SaveTextFile','/', "Text Files (*.txt)")
            
            # This will let you access the test in your QTextEdit
            Text = self.te.toPlainText()
            
            # This will prevent you from an error if pressed cancel on file dialog.
            if S__File[0]: 
                # Finally this will Save your file to the path selected.
                with open(S__File[0], 'w') as file:
                    file.write(Text)        
        
    
    

    
 


if __name__ == "__main__":
    dirTxtFiles_path = "./txtFiles/"
    file_list = os.listdir(dirTxtFiles_path)
    file_count = len(file_list)
    fileNumbersLocation = './config/FileNumbers.txt'
    
    app = QApplication(sys.argv)
    
    with open(fileNumbersLocation, 'w') as FileNumbers:
        FileNumbers.write(str(file_count))
    
    #read BitNote FileNumbers
    with open(fileNumbersLocation, 'r') as FileNumbers:
        fileNumberTmp = FileNumbers.read()
        fileNumber = int(fileNumberTmp)
                
    window = MyWindow(fileNumber, fileNumbersLocation)
    
    # while True:
    #     window.changeDetect()
        
    window.show()
    app.exec_()
    