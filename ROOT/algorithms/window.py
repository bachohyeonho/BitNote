import os
import sys
from PyQt5.QtWidgets import *
import glob


class MyWindow(QMainWindow):
    def __init__(self, fileNumber, fileNumbersLocation):
        super().__init__()
        self.initUI()
        self.fileNumber = fileNumber  #How can I update this?
        self.fileNumbersLocation = fileNumbersLocation
        self.textHasBeenOpened = False
        self.currentFileLocation = None
        self.fileNumbersLocation = './config/FileNumbers.txt'
        path = "./txtFiles/*"
        self.fileList = glob.glob(path)
        self.namingSystem()
        self.namingNum = 0
        self.namingSystem()
        
        if len(self.fileList) != 0:
            self.currentFileLocation = self.fileList[0]

            
        else:
            print('file empty')
            self.createNewFile(self.fileNumbersLocation)
            path = "./txtFiles/*"
            self.fileList = glob.glob(path)
            self.currentFileLocation = self.fileList[0]
        
        self.bringFile(self.fileList[0])
        self.fileTitleLabel.setText(self.currentFileLocation)
        
        #파일, 편집, 포멧, 보기, 윈도우, 도움
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)
        
        
        # file menu action
        
        
        self.new_action = QAction("New")
        self.new_action.triggered.connect(self.createNewFile)
        self.open_action = QAction("Open")
        self.open_action.triggered.connect(self.openFileFromDialog)
        self.save_action = QAction("Save")
        self.save_action.triggered.connect(self.saveFile)
        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.Quit)

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
        #File title
        self.fileTitleLabel = QLabel("Title")

        vbox.addStretch(0)
        vbox.addWidget(self.fileTitleLabel)
        vbox.addWidget(self.te)
        vbox.addStretch(0)

        self.setCentralWidget(central_widget)
        
        self.setWindowTitle("BitNote")
        self.setGeometry(20, 20, 1000, 700)     
    
    def Quit(self):
        self.removeCurrentEmptyFile()
        self.close()
        
    
    def namingSystem(self):
        fileNames = os.listdir('./txtFiles/')
        print(fileNames) #13rd char
        maxNum = 0
        for i in range(len(fileNames)):
            a = int(fileNames[i][13])
            if a > maxNum:
                maxNum = a
        print("maxNum:", maxNum)
        self.namingNum = maxNum+1
    
    def createNewFile(self, fileNumbersLocation):
        
        if self.currentFileLocation != None and self.isCurrentFileEmpty():
            print("Empty. no need to build new one.")
            return
        
        self.fileNumber += 1
        self.updateFileNumbers()
        
        print("created New File %d"%self.namingNum)
        
        fileName = './txtFiles/Unnamed Note %d.txt'%self.namingNum
        newTxtFile = open(fileName, 'w')
        self.currentFileLocation = fileName
        
        self.bringFile(self.currentFileLocation)
        print("current file location: ", self.currentFileLocation)
        self.fileTitleLabel.setText(self.currentFileLocation)
        self.namingSystem()
    
    def bringFile(self, currentFileLocation):
        with open(currentFileLocation, 'r', encoding='utf-8') as file:
                content = file.read()
                self.te.setPlainText(content)
        self.currentFileLocation = currentFileLocation
    
    def openFileFromDialog(self):
        self.removeCurrentEmptyFile()
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly 
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
        self.currentFileLocation = file_path
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.te.setPlainText(content)
        print("current file location: ", self.currentFileLocation)
        self.fileTitleLabel.setText(self.currentFileLocation)
                
    def changeDetect(self):
        #detect whether txt has changed or not.
        print("change detector initating")

    def singleStepSave(self, fileLocation):        
        print("single step save initiated")
        Text = self.te.toPlainText()
        with open(fileLocation, 'w') as file:
            file.write(Text)    
            
    
    def saveFile(self):
        self.singleStepSave(self.currentFileLocation)
        print("current file location: ", self.currentFileLocation)     
    
    def isCurrentFileEmpty(self):
        isEmpty = False
        if len (self.currentFileLocation) != 0:
            with open(self.currentFileLocation, 'r') as file:
                lines = file.readlines()
                if len(lines) == 0:
                    isEmpty = True
            print("current file location: ", self.currentFileLocation)
        print("location: ", self.currentFileLocation, "is empty?", isEmpty)
        return isEmpty
    
    def removeCurrentEmptyFile(self):
        #read current file
        if fileNumber > 1 and self.isCurrentFileEmpty():

            os.remove(self.currentFileLocation)
            self.currentFileLocation = self.fileList[0]
            self.updateFileNumbers()
        print("current file location: ", self.currentFileLocation)
        self.fileTitleLabel.setText(self.currentFileLocation)
        self.namingSystem()

    
    
    def updateFileNumbers(self):
        dirTxtFiles_path = "./txtFiles/"
        file_list = os.listdir(dirTxtFiles_path)
        
        with open(self.fileNumbersLocation, 'w') as FileNumbers:
            FileNumbers.write(str(len(file_list)))
    
        self.fileNumber = len(file_list)
        print("file number updated")
   
   
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
        
    window.show()
    app.exec_()
    