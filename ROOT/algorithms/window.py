import glob
import os
import sys
import time
from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

now = time

#SettingDialog
class SettingDialog(QDialog):
    def __init__(self, BitNoteWindow):
        super().__init__()
        self.timeSpinBox = QSpinBox(self)
        self.sizeSpinBox = QSpinBox(self)
        timeLabel = QLabel("Expire Time(days): ", self)
        timeLabel.move(10, 20)
        sizeLabel = QLabel("Expire Size(unix characters): ", self)
        sizeLabel.move(10, 100)
        self.t, self.s = 0, 0

        self.timeSpinBox.move(180, 20)
        self.timeSpinBox.resize(80, 22)
        self.sizeSpinBox.move(180, 100)
        self.sizeSpinBox.resize(80, 22)
        self.bringValues()
        
    def bringValues(self):
        with open('./config/ExpireValue.txt', 'r') as f:
            self.t = int(f.readline())//86400
            self.s = int(f.readline())
        #now set these values into spin box.
        self.timeSpinBox.setValue(self.t)
        self.sizeSpinBox.setValue(self.s)
        

    def closeEvent(self, event):
        print('close event!!!!!!!!!')
        os.chdir("/Users/johyeonho/BitNote/ROOT")
        with open('./config/ExpireValue.txt', 'w') as f:
            f.writelines([str(self.timeSpinBox.value()*86400),'\n', str(self.sizeSpinBox.value())])
        

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
        self.currentFileLocation = None
        self.txtFilesPath = "./txtFiles/*"
        self.fileList = glob.glob(self.txtFilesPath)
        self.namingNum = 0
        self.importantFileList = []
        self.initUI()
        
        self.startTime = now.time()
        self.bringValues()
        self.automaticFileRemoveSystem()
        self.updateNamingSystem()
        self.getCurrentFileLocation()
        self.bringFile(self.fileList[0])
        #automatic remove
        self.updateTxtInfo()
        self.isImportant = False
        self.bringFileListOnWidget()

    def bringValues(self):
        with open('./config/ExpireValue.txt', 'r') as f:
            self.expireTime = int(f.readline())
            self.expireSize = int(f.readline())
        print('value brought:', self.expireTime, self.expireSize)
            
        
    def closeEvent(self, event):
        self.Quit()
        
    def updateTxtInfo(self):
        #update Txt Info
        self.currentFileTouchedTime = os.path.getmtime(self.currentFileLocation)
        self.fileTitleLabel.setText(self.currentFileLocation)
        dt_object = datetime.utcfromtimestamp(self.currentFileTouchedTime)
        formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        self.fileTimeLabel.setText(str(formatted_date))

    def getCurrentFileLocation(self):
        path = "./txtFiles/*"
        self.fileList = glob.glob(path)        
        if len(self.fileList) == 0:
            self.createNewFile()
        self.fileList = glob.glob(path)  
        self.currentFileLocation = self.fileList[0]
        
    
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
        
        ####file list
        self.file_list_widget = QListWidget(self)
        
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
        #font =  QtGui.QFont()
        #font.setPointSize(20)
        #self.te.setFont(font)
        self.te.setAcceptRichText(True)
        
        #File title
        self.fileTitleLabel = QLabel("Title")
        self.fileTimeLabel = QLabel("Time")
        vbox.addStretch(3)
        vbox.addWidget(self.file_list_widget)
        vbox.addWidget(self.fileTitleLabel)
        vbox.addWidget(self.fileTimeLabel)
        vbox.addWidget(self.important_checkbox)
        vbox.addWidget(self.te)
        vbox.addStretch(1)

        self.setCentralWidget(central_widget)
        
        self.setWindowTitle("BitNote")
        self.setGeometry(20, 20, 500, 300)     
    
    def bringFileListOnWidget(self):

        self.file_list_widget.clear()
        self.file_list_widget.addItems(self.fileList)
    
    def Quit(self):
        self.removeCurrentEmptyFile()
        self.close()
        
    
    def updateNamingSystem(self):
        fileNames = os.listdir('./txtFiles/')
        #print(fileNames) 
        
        self.namingNum = len(fileNames)+1
        
    def createNewFile(self):
        #if current file is empty, ignore.
        if self.currentFileLocation != None and self.isCurrentFileEmpty():
            return
        
        #update fileNumber
        self.fileNumber += 1
        self.updateFileNumbers()
        #create File Name.
        fileName = './txtFiles/Bit Note %d.txt'%self.fileNumber
        
        with open(fileName, 'w') as newTxtFile:
            newTxtFile.write("NotImportant")    
        self.currentFileLocation = fileName
        
        self.bringFile(self.currentFileLocation)
        self.updateNamingSystem()
        self.updateTxtInfo()
    
    def bringFile(self, currentFileLocation):
        with open(currentFileLocation, 'r') as file:
                importantTmp = file.readline()
                content2 = file.read()
                self.te.setPlainText(content2)
        if importantTmp == 'Important\n':
            if self.important_checkbox.isChecked():
                pass
            else:
                self.important_checkbox.toggle()
        else:
            if self.important_checkbox.isChecked():
                self.important_checkbox.toggle()
            else:
                pass
        self.bringFileListOnWidget()

        self.currentFileLocation = currentFileLocation
    
    def openFileFromDialog(self):
        self.removeCurrentEmptyFile()
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly 
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
        self.currentFileLocation = file_path
        self.bringFile(self.currentFileLocation)
        
        self.updateTxtInfo()

    def singleStepSave(self, fileLocation):        
        Text = self.te.toPlainText()
        tmp = "Important" if self.isImportant else "NotImportant"
        with open(fileLocation, 'w') as file:
            file.writelines([tmp, '\n', Text])
            
    
    def saveFile(self):
        self.singleStepSave(self.currentFileLocation)     
    
    def isCurrentFileEmpty(self):
        isEmpty = False
        if len (self.currentFileLocation) != 0:
            with open(self.currentFileLocation, 'r') as file:
                garbage = file.readline()
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
        #print("file number updated")
        
    def automaticFileRemoveSystem(self):
        #1. get File List
        path = "./txtFiles/*"
        self.fileList = glob.glob(path)
        self.fileTimeList = []
        self.fileSizeList = []
        self.importantFileList = []
        
        #2. get managed time of files. also list. and also 
        for i in range(len(self.fileList)):
            self.fileTimeList.append(os.path.getmtime(self.fileList[i]))
            self.fileSizeList.append(os.path.getsize(self.fileList[i]))
            with open(self.fileList[i], 'r') as f:
                tmp = f.readline()
            if tmp == 'Important\n':
                self.importantFileList.append(True)
            else: 
                self.importantFileList.append(False)
        print("........:", self.importantFileList)
        
        #print("self.expireTime:", datetime.utcfromtimestamp(self.expireTime))
        #3. inspection
        #for i in range(len(self.fileList)-1, 0, -1):
        for i in range(0, len(self.fileList)):
            #print("fileName:", self.fileList[i], "fileTime:", self.fileTimeList[i], "fileSize:", self.fileSizeList[i])
            timeTmp = self.startTime - self.fileTimeList[i]
            sizeTmp = self.fileSizeList[i]
            print("expireValuesLog:", timeTmp, sizeTmp, self.importantFileList[i])
            if timeTmp >= self.expireTime and sizeTmp < self.expireSize and not self.importantFileList[i]:
                #print("remove code initiated!!!!!!!!!!!!!!!!!!!!!!", self.fileList[i])
                print("cleared:", self.fileList[i])
                os.remove(self.fileList[i])
        #만약 다 지웠으면 생성. 그냥 init할때 얘가 생성이 삭제보다 다 먼저 나오게 하면 되afd
        print("automatically cleared ----------------------")
    
    def setExpireStandard(self):
        #if setting dialog has not opened
        settingDialog = SettingDialog(self)
        settingDialog.setWindowModality(Qt.ApplicationModal)
        settingDialog.setGeometry(200,200,300,300)
        settingDialog.exec()
        settingDialog.show()
        print(self.expireTime, self.expireSize)

        
    def addImportantFile(self): #not updating file
        self.isImportant = True
    
    def removeImportantFile(self):
        self.isImportant = False

    def importantCheckBoxControl(self):
        if self.important_checkbox.isChecked():
            self.addImportantFile()
        else:
            self.removeImportantFile()
   
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BitNoteWindow()
    window.show()
    app.exec_()
