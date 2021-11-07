import sys, os, json, shutil
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from lazydragging_ui import Ui_MainWindow
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'File dialogs'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        if os.path.exists("pathes.json"):
            with open("pathes.json") as json_file:
                data = json.load(json_file)
                self.path_to_file = data["filename"]
                self.path_to_folder = data["foldname"]
                self.path_to_fut_folder = data["futurefoldname"]
                self.fut_folder_name = os.path.basename(self.path_to_fut_folder)

                self.ui.setiings_label.setText(self.path_to_file)
                self.ui.alpha_label.setText(self.path_to_folder)
                self.ui.lineEdit.setText(self.fut_folder_name)
        else:
            self.path_to_file = ""
            self.path_to_folder = ""
            self.path_to_fut_folder = ""
        self.ui.AlphaFolder.clicked.connect(self.saveFileDialog)
        self.ui.Settings.clicked.connect(self.openFileNameDialog)
        self.ui.Merge.clicked.connect(self.text_getter)
        self.ui.SaveButton.clicked.connect(self.save_pathes)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(None,"Find settings.json from steam files ", "","All Files (*);;Json Суета (*.json)",options = options)
        if fileName:
            self.ui.setiings_label.setText(fileName)
            self.path_to_file = fileName
    
    
    def saveFileDialog(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        dir_cur = QtCore.QDir.currentPath() 
        directory = QFileDialog.getExistingDirectory(None, "Find alpha dropbox folder", dir_cur, options)
        if directory:
            self.ui.alpha_label.setText(directory)
            self.path_to_folder = directory
    
    def text_getter(self):
        textboxValue = self.ui.lineEdit.text()
        if len(textboxValue) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Empty folder name")
            msg.setInformativeText("Fill box with letters")
            msg.setWindowTitle("Dude you..")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
        else:
            self.path_to_fut_folder = os.path.join(os.getcwd(),textboxValue)
            self.fut_folder_name = textboxValue
            if self.path_to_file == "":
                file_msg = QMessageBox()
                file_msg.setIcon(QMessageBox.Warning)
                file_msg.setText("Empty file path")
                file_msg.setInformativeText("Press Settings json button")
                file_msg.setWindowTitle("Dude you..")
                file_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                file_msg.exec_()
            elif self.path_to_folder == "":
                folder_msg = QMessageBox()
                folder_msg.setIcon(QMessageBox.Warning)
                folder_msg.setText("Empty folder path")
                folder_msg.setInformativeText("Press Alpha Folder button")
                folder_msg.setWindowTitle("Dude you..")
                folder_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                folder_msg.exec_()
            else:
                try:
                    shutil.copytree(self.path_to_folder, self.path_to_fut_folder)
                    for dirname in os.listdir(self.path_to_folder):
                        path_to_dirname = (os.path.join(self.path_to_folder, dirname))
                        path_to_future_dirname = (os.path.join(self.path_to_fut_folder, dirname)) 
                        if os.path.isdir(path_to_dirname):
                            shutil.copy(self.path_to_file, os.path.join(path_to_future_dirname, "settings.json"))
                except FileExistsError:
                    warn_msg = QMessageBox()
                    warn_msg.setIcon(QMessageBox.Critical)
                    warn_msg.setText("Delete existing " + self.fut_folder_name + " folder")
                    warn_msg.setInformativeText("Delete or change future folder name")
                    warn_msg.setWindowTitle("Dude you..")
                    warn_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    warn_msg.exec_()
                

        

    def save_pathes(self):
        if self.path_to_file == "":
            file_msg = QMessageBox()
            file_msg.setIcon(QMessageBox.Warning)
            file_msg.setText("Empty file path")
            file_msg.setInformativeText("Press Settings json button")
            file_msg.setWindowTitle("Dude you..")
            file_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            file_msg.exec_()
        elif self.path_to_folder == "":
            folder_msg = QMessageBox()
            folder_msg.setIcon(QMessageBox.Warning)
            folder_msg.setText("Empty folder path")
            folder_msg.setInformativeText("Press Alpha Folder button")
            folder_msg.setWindowTitle("Dude you..")
            folder_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            folder_msg.exec_()
        elif self.path_to_fut_folder == "":
            future_folder_msg = QMessageBox()
            future_folder_msg.setIcon(QMessageBox.Warning)
            future_folder_msg.setText("Empty future folder name")
            future_folder_msg.setInformativeText("Press Merge Button button")
            future_folder_msg.setWindowTitle("Dude you..")
            future_folder_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            future_folder_msg.exec_()
        elif self.fut_folder_name !=  self.ui.lineEdit.text():
            future_msg = QMessageBox()
            future_msg.setIcon(QMessageBox.Question)
            future_msg.setText("Changes in future folder name")
            future_msg.setInformativeText("Forget to press Merge Button button?")
            future_msg.setWindowTitle("Dude you..")
            future_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            future_msg.exec_()
        else:
            data = {}
            data["filename"] = self.path_to_file 
            data["foldname"] = self.path_to_folder
            data["futurefoldname"] = self.path_to_fut_folder
            with open('pathes.json', 'w') as outfile:
                json.dump(data, outfile)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())