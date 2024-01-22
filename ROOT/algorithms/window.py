import os
import sys
from PyQt5.QtWidgets import *
import glob
import time
from datetime import datetime
now = time

#SettingDialog
class SettingDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(200,200,300,300)
        self.show()
        self.setWindowModality(False)

class BitNoteWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #set current directory for initiating.
        os.chdir("/Users/johyeonho/BitNote/ROOT")
        #set path to folder txtFiles
        self.dirTxtFiles_path = "./txtFiles/"
        #save list of files
        self.file_list = os.listdir(self.dirTxtFiles_path)
        #save number of files
        self.fileNumber = len(self.file_list)
        #set path to "fileNumbers"
        self.fileNumbersLocation = './config/FileNumbers.txt'
        self.updateFileNumbers()
        self.setFileManageValues()
        self.currentFileLocation = None
        self.txtFilesPath = "./txtFiles/*"
        self.fileList = glob.glob(self.txtFilesPath)
        self.namingNum = 0
        self.importantFileList = []
        self.initUI()
        
        self.updateNamingSystem()
        self.getCurrentFileLocation()
        self.bringFile(self.fileList[0])
        #automatic remove
        self.automaticFileRemoveSystem()
        self.updateTxtInfo()
        self.readImportantFileList()

        
    def updateTxtInfo(self):
        #update Txt Info
        self.currentFileTouchedTime = os.path.getmtime(self.currentFileLocation)
        self.fileTitleLabel.setText(self.currentFileLocation)
        self.fileTimeLabel.setText(str(datetime.utcfromtimestamp(self.currentFileTouchedTime)))

    def getCurrentFileLocation(self):
        path = "./txtFiles/*"
        self.fileList = glob.glob(path)        
        if len(self.fileList) == 0:
            self.createNewFile()
        self.fileList = glob.glob(path)  
        self.currentFileLocation = self.fileList[0]
        
    def setFileManageValues(self):
        #values for automatic file manage                   
        self.startTime = now.time()
        self.expireTime = 1000000
        self.expireSize = 1000
    
    def initUI(self):
        #MenuBar setting
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

        # file menu action
        file_menu = self.menubar.addMenu("File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)
        
        #setting menu action
        setting_menu = self.menubar.addMenu("Setting")
        self.setting_action = QAction("setting")
        self.setting_action.triggered.connect(self.setExpireStandard)
        setting_menu.addAction(self.setting_action)

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
        #help menu actions
        help_menu.addAction(self.doc_action)
        help_menu.addAction(self.release_action)
        help_menu.addAction(self.license_action)
        
        #important checkbox
        self.important_checkbox = QCheckBox('Important', self)
        self.important_checkbox.stateChanged.connect(self.importantCheckBoxControl)
        central_widget = QWidget()
        vbox = QVBoxLayout(central_widget)
        self.te = QTextEdit()
        self.te.setAcceptRichText(True)
        
        #File title
        self.fileTitleLabel = QLabel("Title")
        self.fileTimeLabel = QLabel("Time")
        vbox.addStretch(3)
        vbox.addWidget(self.fileTitleLabel)
        vbox.addWidget(self.fileTimeLabel)
        vbox.addWidget(self.important_checkbox)
        vbox.addWidget(self.te)
        vbox.addStretch(1)

        self.setCentralWidget(central_widget)
        
        self.setWindowTitle("BitNote")
        self.setGeometry(20, 20, 500, 300)     
            
    def Quit(self):
        self.removeCurrentEmptyFile()
        self.writeImportantFileList()
        self.close()
        
    
    def updateNamingSystem(self):
        fileNames = os.listdir('./txtFiles/')
        print(fileNames) 
        maxNum = 0
        for i in range(len(fileNames)):
            a = int(fileNames[i][9])
            if a > maxNum:
                maxNum = a
        self.namingNum = maxNum+1
        
    def createNewFile(self):
        #if current file is empty, ignore.
        if self.currentFileLocation != None and self.isCurrentFileEmpty():
            return
        
        #update fileNumber
        self.fileNumber += 1
        self.updateFileNumbers()
        #create File Name.
        fileName = './txtFiles/Bit Note %d.txt'%self.namingNum
        newTxtFile = open(fileName, 'w')
        self.currentFileLocation = fileName
        
        self.bringFile(self.currentFileLocation)
        self.updateNamingSystem()
        self.updateTxtInfo()
    
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
        self.fileTitleLabel.setText(self.currentFileLocation)
        
        self.updateTxtInfo()

    def singleStepSave(self, fileLocation):        
        Text = self.te.toPlainText()
        with open(fileLocation, 'w') as file:
            file.write(Text)    
            
    
    def saveFile(self):
        self.singleStepSave(self.currentFileLocation)     
    
    def isCurrentFileEmpty(self):
        isEmpty = False
        if len (self.currentFileLocation) != 0:
            with open(self.currentFileLocation, 'r') as file:
                lines = file.readlines()
                if len(lines) == 0:
                    isEmpty = True
        return isEmpty
    
    def removeCurrentEmptyFile(self):
        #read current file
        if self.fileNumber > 1 and self.isCurrentFileEmpty():
            os.remove(self.currentFileLocation)
            self.currentFileLocation = self.fileList[0]
            self.updateFileNumbers()
        self.updateNamingSystem()
    
    def updateFileNumbers(self):
        dirTxtFiles_path = "./txtFiles/"
        file_list = os.listdir(dirTxtFiles_path)
        
        with open(self.fileNumbersLocation, 'w') as FileNumbers:
            FileNumbers.write(str(len(file_list)))
    
        self.fileNumber = len(file_list)
        print("file number updated")
        
    def automaticFileRemoveSystem(self):
        #1. get File List
        path = "./txtFiles/*"
        self.fileList = glob.glob(path)
        self.fileTimeList = []
        self.fileSizeList = []
        
        #2. get managed time of files. also list. and also 
        for i in range(len(self.fileList)):
            self.fileTimeList.append(os.path.getmtime(self.fileList[i]))
            self.fileSizeList.append(os.path.getsize(self.fileList[i]))
        
        print("self.expireTime:", datetime.utcfromtimestamp(self.expireTime))
        #3. inspection
        for i in range(len(self.fileList)-1, 0, -1):
            print("fileName:", self.fileList[i], "fileTime:", self.fileTimeList[i], "fileSize:", self.fileSizeList[i])
            if self.startTime - self.fileTimeList[i] >= self.expireTime and self.fileSizeList[i] < self.expireSize:
                print("remove code initiated!!!!!!!!!!!!!!!!!!!!!!", self.fileList[i])
                os.remove(self.fileList[i])
        print("automatically cleared ----------------------")
    
    def setExpireStandard(self):
        #if setting dialog has not opened
        settingDialog = SettingDialog()
        settingDialog.exec()
    
    def readImportantFileList(self):
        with open("./config/ImportantFileList.txt", 'r') as f:
            tmp = f.readlines()
        tmp = str(tmp)
        tmp = tmp[1:-1:1]
        tmp = tmp[1:-1:1]
        tmp = tmp[1:-1:1]
        tmp = tmp[1:-1:1]
        self.importantFileList.append(tmp)
        print("read important file list", self.importantFileList)

        
    def addImportantFileList(self): #not updating file
        self.importantFileList.append(self.currentFileLocation)
        print("added current file", self.importantFileL햣 ist)
    
    def removeImportantFileList(self):
        self.importantFileList.remove(self.currentFileLocation)
        print("removed current file", self.importantFileList)
        
    def writeImportantFileList(self):
        with open("./config/ImportantFileList.txt", 'w') as f:
            f.write(str(self.importantFileList))
   
    def importantCheckBoxControl(self):
        if self.important_checkbox.isChecked():
            self.addImportantFileList()
        else:
            self.removeImportantFileList()
   
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BitNoteWindow()
    window.show()
    app.exec_()