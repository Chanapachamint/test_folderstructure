import sys
import maya.cmds as cmds
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from shiboken2 import wrapInstance
from PySide2 import QtUiTools
import maya.OpenMayaUI as omui
import os
import re
import subprocess

pathDir = os.path.dirname(sys.modules[__name__].__file__)
fileUi = '%s/folderui_widget_new.ui' % pathDir

class MainUi(QMainWindow):

    root_path = "D:/Work_Year3/Work_3/Code/folder_structure"

    def __init__(self, *args, **kwargs):
        super(MainUi, self).__init__(*args, **kwargs)

        fileUi = '%s/folderui_widget_new.ui' % pathDir

        self.mainwidget = setup_ui_maya(fileUi, self)
        self.setCentralWidget(self.mainwidget)

        self.setMinimumSize(500, 600)
        self.setWindowTitle("My Projects")
        self.mainwidget.proj_comboBox.addItems(["(None)", "Duckingdonut"])

        self.mainwidget.close_Button.clicked.connect(self.close)
        self.mainwidget.search_Button.clicked.connect(self.search_name)
        self.mainwidget.create_Button_2.clicked.connect(self.create_newfolder)
        self.mainwidget.proj_comboBox.currentIndexChanged.connect(self.open_project_folder)
        self.mainwidget.proj_comboBox.currentIndexChanged.connect(self.on_project_selected)
        self.mainwidget.save_Button.clicked.connect(self.save_selected_item)  
        self.mainwidget.open_Button.clicked.connect(self.open_selected_item)  
        
        # Connect itemClicked signals to their respective slot methods
        self.mainwidget.assetshot_listWidget.itemClicked.connect(self.on_assetshot_selected)
        self.mainwidget.char_listWidget.itemClicked.connect(self.on_char_selected)
        self.mainwidget.astsht_listWidget.itemClicked.connect(self.on_astsht_selected)
        self.mainwidget.department_listWidget.itemClicked.connect(self.on_department_selected)
        self.mainwidget.verpub_listWidget.itemClicked.connect(self.on_verpub_selected)  

    def on_project_selected(self):
        selected_project = self.mainwidget.proj_comboBox.currentText()
        if selected_project != "(None)":
            self.create_asset_listWidget(selected_project)
            self.update_path_lineedit(os.path.join(self.root_path, selected_project))

    def open_project_folder(self):
        selected_project = self.mainwidget.proj_comboBox.currentText()
        project_folder_path = os.path.join(self.root_path, selected_project)

        if os.path.exists(project_folder_path):
            asset_folders = [folder for folder in os.listdir(project_folder_path) if os.path.isdir(os.path.join(project_folder_path, folder))]
            self.mainwidget.assetshot_listWidget.clear()
            self.mainwidget.assetshot_listWidget.addItems(asset_folders)
        else:
            QMessageBox.warning(self, "Folder Not Found", "The folder for project '{}' does not exist.".format(selected_project))

    def search_name(self):
        search_name = self.mainwidget.path_lineEdit_2.text()

        search_path = os.path.join(self.root_path, search_name)
        if os.path.exists(search_path):
            os.startfile(search_path)  # This opens the folder in Windows Explorer
        else:
            QMessageBox.warning(self, "Folder Not Found", "The folder for project '{}' does not exist.".format(search_name))
        self.mainwidget.path_lineEdit_2.clear()

    def create_asset_listWidget(self, project_name):
        project_path = os.path.join(self.root_path, project_name)
        assetshot_folders = [folder for folder in os.listdir(project_path) if os.path.isdir(os.path.join(project_path, folder))]
        self.mainwidget.assetshot_listWidget.clear()
        self.mainwidget.assetshot_listWidget.addItems(assetshot_folders)

    def on_assetshot_selected(self, item):
        selected_project = self.mainwidget.proj_comboBox.currentText()
        assetshot_folder = item.text()
        self.populate_char_list(selected_project, assetshot_folder)
        self.update_path_lineedit(os.path.join(self.root_path, selected_project, assetshot_folder))

    def populate_char_list(self, project_name, assetshot_folder):
        assetshot_path = os.path.join(self.root_path, project_name, assetshot_folder)
        if os.path.exists(assetshot_path):
            char_folders = [folder for folder in os.listdir(assetshot_path) if os.path.isdir(os.path.join(assetshot_path, folder))]
            self.mainwidget.char_listWidget.clear()
            self.mainwidget.char_listWidget.addItems(char_folders)
        else:
            QMessageBox.warning(self, "Folder Not Found", "The folder for asset/shot '{}' does not exist.".format(assetshot_folder))

    def on_char_selected(self, item):
        selected_project = self.mainwidget.proj_comboBox.currentText()
        assetshot_folder = self.mainwidget.assetshot_listWidget.currentItem().text()
        char_folder = item.text()
        self.populate_astsht_list(selected_project, assetshot_folder, char_folder)
        self.update_path_lineedit(os.path.join(self.root_path, selected_project, assetshot_folder, char_folder))

    def populate_astsht_list(self, project_name, assetshot_folder, char_folder):
        char_path = os.path.join(self.root_path, project_name, assetshot_folder, char_folder)
        if os.path.exists(char_path):
            astsht_folders = [folder for folder in os.listdir(char_path) if os.path.isdir(os.path.join(char_path, folder))]
            self.mainwidget.astsht_listWidget.clear()
            self.mainwidget.astsht_listWidget.addItems(astsht_folders)
        else:
            QMessageBox.warning(self, "Folder Not Found", "The folder for char '{}' does not exist.".format(char_folder))

    def on_astsht_selected(self, item):
        selected_project = self.mainwidget.proj_comboBox.currentText()
        assetshot_folder = self.mainwidget.assetshot_listWidget.currentItem().text()
        char_folder = self.mainwidget.char_listWidget.currentItem().text()
        astsht_folder = item.text()
        self.populate_department_list(selected_project, assetshot_folder, char_folder, astsht_folder)
        self.update_path_lineedit(os.path.join(self.root_path, selected_project, assetshot_folder, char_folder, astsht_folder))

    def populate_department_list(self, project_name, assetshot_folder, char_folder, astsht_folder):
        astsht_path = os.path.join(self.root_path, project_name, assetshot_folder, char_folder, astsht_folder)
        if os.path.exists(astsht_path):
            department_folders = [folder for folder in os.listdir(astsht_path) if os.path.isdir(os.path.join(astsht_path, folder))]
            self.mainwidget.department_listWidget.clear()
            self.mainwidget.department_listWidget.addItems(department_folders)
        else:
            QMessageBox.warning(self, "Folder Not Found", "The folder for asset/shot '{}' does not exist.".format(astsht_folder))

    def on_department_selected(self, item):
        selected_project = self.mainwidget.proj_comboBox.currentText()
        assetshot_folder = self.mainwidget.assetshot_listWidget.currentItem().text()
        char_folder = self.mainwidget.char_listWidget.currentItem().text()
        astsht_folder = self.mainwidget.astsht_listWidget.currentItem().text()
        department_folder = item.text()
        self.populate_verpub_list(selected_project, assetshot_folder, char_folder, astsht_folder, department_folder)
        self.update_path_lineedit(os.path.join(self.root_path, selected_project, assetshot_folder, char_folder, astsht_folder, department_folder))

    def populate_verpub_list(self, project_name, assetshot_folder, char_folder, astsht_folder, department_folder):
        department_path = os.path.join(self.root_path, project_name, assetshot_folder, char_folder, astsht_folder, department_folder)
        if os.path.exists(department_path):
            verpub_folders = [folder for folder in os.listdir(department_path) if os.path.isdir(os.path.join(department_path, folder))]
            self.mainwidget.verpub_listWidget.clear()
            self.mainwidget.verpub_listWidget.addItems(verpub_folders)
        else:
            QMessageBox.warning(self, "Folder Not Found", "The folder for department '{}' does not exist.".format(department_folder))

    def on_verpub_selected(self, item):
        selected_project = self.mainwidget.proj_comboBox.currentText()
        assetshot_folder = self.mainwidget.assetshot_listWidget.currentItem().text()
        char_folder = self.mainwidget.char_listWidget.currentItem().text()
        astsht_folder = self.mainwidget.astsht_listWidget.currentItem().text()
        department_folder = self.mainwidget.department_listWidget.currentItem().text()
        verpub_folder = item.text()
        self.populate_result_list(selected_project, assetshot_folder, char_folder, astsht_folder, department_folder, verpub_folder)
        self.update_path_lineedit(os.path.join(self.root_path, selected_project, assetshot_folder, char_folder, astsht_folder, department_folder, verpub_folder))

    def populate_result_list(self, project_name, assetshot_folder, char_folder, astsht_folder, department_folder, verpub_folder):
        verpub_path = os.path.join(self.root_path, project_name, assetshot_folder, char_folder, astsht_folder, department_folder, verpub_folder)
        if os.path.exists(verpub_path):
            files = [f for f in os.listdir(verpub_path) if os.path.isfile(os.path.join(verpub_path, f))]
            self.mainwidget.result_listWidget.clear()
            self.mainwidget.result_listWidget.addItems(files)
        else:
            QMessageBox.warning(self, "Folder Not Found", "The folder for verpub '{}' does not exist.".format(verpub_folder))

    def create_newfolder(self):
        folder_name = self.mainwidget.create_lineEdit.text()

        if folder_name:
            new_folder_path = os.path.join(self.root_path, folder_name)
            try:
                os.makedirs(new_folder_path)
                QMessageBox.information(self, "Success", "Folder '{}' created successfully.".format(folder_name))
            except OSError as e:
                QMessageBox.critical(self, "Error", "Failed to create folder '{}': {}".format(folder_name, e))

    def save_selected_item(self):
        selected_item = self.mainwidget.result_listWidget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "No File Selected", "Please select a file to save.")
            return

        current_file_name = selected_item.text()
        current_path = self.mainwidget.path_lineEdit.text()
        current_file_path = os.path.join(current_path, current_file_name)
        
        # Extract file name and extension
        base_name, extension = os.path.splitext(current_file_name)
        
        # Regular expression to match the version number
        version_pattern = re.compile(r"^(.*?)(\d{3})$")
        match = version_pattern.match(base_name)
        
        if match:
            base_name, version = match.groups()
            new_version = int(version) + 1
        else:
            base_name = base_name
            new_version = 1
        
        # Create new file name with incremented version number
        new_file_name = f"{base_name}{new_version:03}{extension}"
        new_file_path = os.path.join(current_path, new_file_name)
        
        # Save the file (using Maya or regular file copy as appropriate)
        try:
            if 'maya' in sys.modules:
                cmds.file(rename=new_file_path)
                cmds.file(save=True, type='mayaAscii')
            else:
                import shutil
                shutil.copy(current_file_path, new_file_path)
            
            # Update the result_listWidget with the new file name
            self.populate_result_list(*self.get_current_list_context())
            QMessageBox.information(self, "Success", f"File saved as {new_file_name}.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file '{current_file_name}': {e}")

    def open_selected_item(self):
        selected_item = self.mainwidget.result_listWidget.currentItem()
        if selected_item:
            file_name = selected_item.text()
            current_path = self.mainwidget.path_lineEdit.text()
            file_path = os.path.join(current_path, file_name)
            try:
                if 'maya' in sys.modules:
                    import maya.cmds as cmds
                    # Check for unsaved changes
                    if cmds.file(q=True, modified=True):
                        # If there are unsaved changes, prompt the user to save or discard them
                        result = QMessageBox.question(self, "Unsaved Changes",
                                                    "There are unsaved changes. Do you want to save them?",
                                                    QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
                        if result == QMessageBox.Save:
                            cmds.file(save=True)
                        elif result == QMessageBox.Discard:
                            cmds.file(force=True, new=True)
                        else:  # User clicked Cancel
                            return
                    cmds.file(file_path, o=True)
                else:
                    # Use subprocess to open the file with the default application
                    subprocess.Popen(['xdg-open', file_path])
            except Exception as e:
                QMessageBox.critical(self, "Error", "Failed to open file '{}': {}".format(file_name, e))

    def update_path_lineedit(self, path):
        self.mainwidget.path_lineEdit.setText(path)

    def get_current_list_context(self):
        return (
            self.mainwidget.proj_comboBox.currentText(),
            self.mainwidget.assetshot_listWidget.currentItem().text(),
            self.mainwidget.char_listWidget.currentItem().text(),
            self.mainwidget.astsht_listWidget.currentItem().text(),
            self.mainwidget.department_listWidget.currentItem().text(),
            self.mainwidget.verpub_listWidget.currentItem().text()
        )

def setup_ui_maya(folderui_widget, parent):
    fileUi = os.path.dirname(folderui_widget)
    qt_loader = QtUiTools.QUiLoader()
    qt_loader.setWorkingDirectory(fileUi)

    f = QFile(folderui_widget)
    f.open(QFile.ReadOnly)

    myWidget = qt_loader.load(f, parent)
    f.close()

    return myWidget

def run():
    global ui
    try:
        ui.close()
    except:
        pass

    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QWidget)
    ui = MainUi(parent=ptr)
    ui.show()

run()
