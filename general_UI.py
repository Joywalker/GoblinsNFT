""" Script for auto-naming contents from within a folder to selected name pattern."""
import os
import json
import shutil
from glob import glob

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QLabel,
    QTextEdit, QFileDialog,
    QMessageBox, QVBoxLayout, QScrollArea, QFormLayout, QGroupBox, QHBoxLayout

)
from PyQt5.QtCore import (
    QRect, Qt,
)
from PyQt5 import QtGui

# Define window w/h
w_width = 844
w_height = 509


#######################################
# Define method for re-naming files
#######################################
def rename_files_from_folder(folder, name, extension, st_index):
    files = glob(os.path.join(folder, '*.{}'.format(extension)))
    for i, file in enumerate(files):
        new_filename = name + '_{}.{}'.format(i + int(st_index), extension)
        os.rename(file, os.path.join(folder, new_filename))


# Define & Implement UI
class Ui_MainWindow(object):
    def __init__(self):
        # Define widgets/callbacks
        self.main_widget = QWidget(MainWindow)

        # Auto Rename, identified by [rn] (rename) tag
        self.rn_browse_folder_field = QTextEdit(self.main_widget)
        self.rn_new_name_field = QTextEdit(self.main_widget)
        self.rn_extension_field = QTextEdit(self.main_widget)
        self.rn_browse_label = QLabel(self.main_widget)
        self.rn_name_label = QLabel(self.main_widget)
        self.rn_ext_label = QLabel(self.main_widget)
        self.rn_exec_button = QPushButton(self.main_widget)
        self.rn_topic_label = QLabel(self.main_widget)

        # Auto updating json, identified by [uj] (update json) tag
        self.new_uj_folder_select_window = QMainWindow()
        self.uj_browse_folder_field = QTextEdit(self.main_widget)
        self.uj_browse_label = QLabel(self.main_widget)
        self.uj_topic_label = QLabel(self.main_widget)
        self.uj_exec_button = QPushButton(self.main_widget)
        self.uj_folders = []
        self.uj_id_folder_match = []
        self.json_contents = {"meta": {},
                              "variables_metadata": {}}


        # Auto-Duplicating, identified by [ad] (auto, duplicate) tag
        self.ad_browse_folder_field = QTextEdit(self.main_widget)
        self.ad_browse_folder_label = QLabel(self.main_widget)
        self.ad_topic_label = QLabel(self.main_widget)
        self.ad_qt_label = QLabel(self.main_widget)
        self.ad_qt_field = QTextEdit(self.main_widget)
        self.ad_exec_button = QPushButton(self.main_widget)

        # Define needed variables
        self.rn_folder_path = ''
        self.uj_folder_path = ''
        self.ad_folder_path = ''

    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(w_width, w_height)
        MainWindow.setFixedSize(w_width, w_height)
        self.main_widget.setObjectName("main_widget")

        # Set widgets positions and events
        self.rn_topic_label.setGeometry(QRect(40, 57, 210, 20))
        self.rn_topic_label.setText("Auto File Namer")
        self.rn_topic_label.setFont(QFont('Times', 15))
        self.rn_browse_label.setGeometry(QRect(27, 94, 145, 15))
        self.rn_browse_label.setText("Folder")
        self.rn_browse_folder_field.setGeometry(QRect(153, 93, 325, 32))
        self.rn_browse_folder_field.selectionChanged.connect(self.rn_clicked)
        self.rn_extension_field.setGeometry(QRect(613, 93, 56, 32))
        self.rn_ext_label.setGeometry(QRect(613, 68, 90, 24))
        self.rn_ext_label.setText("(png,jpg)")
        self.rn_name_label.setText("Name")
        self.rn_name_label.setGeometry(QRect(539, 68, 62, 24))
        self.rn_new_name_field.setGeometry(QRect(539, 93, 56, 32))
        self.rn_exec_button.setGeometry(QRect(693, 93, 150, 32))
        self.rn_exec_button.setText("Execute")
        self.rn_exec_button.clicked.connect(self.rn_execute_clicked)
        self.rn_starting_idx = QTextEdit(self.main_widget)
        self.rn_starting_idx.setGeometry(QRect(488, 93, 41, 32))
        self.rn_starting_idx_lb = QLabel(self.main_widget)
        self.rn_starting_idx_lb.setGeometry(QRect(488, 68, 62, 24))
        self.rn_starting_idx_lb.setText("idx")

        self.uj_main_wid = QWidget(self.new_uj_folder_select_window)
        self.uj_topic_label.setGeometry(QRect(40, 179, 271, 52))
        self.uj_topic_label.setText("Auto Json Populator")
        self.uj_browse_label.setGeometry(QRect(27, 254, 105, 25))
        self.uj_browse_label.setText("Assets Path")
        self.uj_topic_label.setFont(QFont('Times', 15))
        self.uj_browse_folder_field.setGeometry(QRect(153, 248, 516, 32))
        self.uj_browse_folder_field.selectionChanged.connect(self.uj_clicked)
        self.uj_exec_button.setGeometry(QRect(693, 248, 150, 32))
        self.uj_exec_button.setText("Execute")
        self.uj_exec_button.clicked.connect(self.uj_execute_clicked)

        self.ad_topic_label.setGeometry(QRect(40, 355, 171, 27))
        self.ad_topic_label.setText("Auto Duplicator")
        self.ad_topic_label.setFont(QFont('Times', 15))
        self.ad_browse_folder_field.setGeometry(QRect(153, 392, 452, 32))
        self.ad_browse_folder_field.selectionChanged.connect(self.ad_clicked)
        self.ad_browse_folder_label.setGeometry(QRect(27, 396, 145, 15))
        self.ad_browse_folder_label.setText("Folder")
        self.ad_qt_field.setGeometry(QRect(620, 392, 50, 32))
        self.ad_qt_label.setText("Qty")
        self.ad_qt_label.setGeometry(QRect(620, 367, 80, 15))
        self.ad_exec_button.setGeometry(QRect(693, 392, 150, 32))
        self.ad_exec_button.setText("Execute")
        self.ad_exec_button.clicked.connect(self.ad_execute_clicked)
        MainWindow.setWindowTitle("Automate Scripts")
        MainWindow.setCentralWidget(self.main_widget)

    def rn_clicked(self):
        self.rn_folder_path = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        self.rn_browse_folder_field.setText(self.rn_folder_path)

    def uj_clicked(self):
        self.uj_folder_path = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\',
                                                               QFileDialog.ShowDirsOnly)
        self.uj_browse_folder_field.setText(self.uj_folder_path)

    def ad_clicked(self):
        self.ad_folder_path = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\',
                                                               QFileDialog.ShowDirsOnly)
        self.ad_browse_folder_field.setText(self.ad_folder_path)

    @staticmethod
    def check_extension(ext):
        if "." in ext:
            ext = ext.split('.')[-1]
        if ext.lower() in ['png', 'jpg', 'json', 'svg']:
            return True, ext
        return False, None

    def rn_execute_clicked(self):
        # Verify if fields are empty, and execute button was clicked
        folder_path = self.rn_folder_path
        extension = self.rn_extension_field.toPlainText()
        starting_idx = self.rn_starting_idx.toPlainText()
        naming_convention = self.rn_new_name_field.toPlainText()

        if len(folder_path) < 2 or len(extension) < 2 or len(naming_convention) < 2:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Make sure all the fields are filled.")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
        else:
            QApplication.processEvents()
            is_extension_valid, ext = self.check_extension(extension)
            if is_extension_valid:
                rename_files_from_folder(folder_path, naming_convention, ext, starting_idx)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Complete. Check {}".format(self.rn_folder_path))
            msg.setWindowTitle("Success")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()

    def uj_folder_select_window(self):
        self.new_uj_folder_select_window.setWindowTitle("Folder Order Select")
        self.new_uj_folder_select_window.setFixedWidth(300)
        self.new_uj_folder_select_window.setFixedHeight(400)
        middle_layout = QFormLayout(self.uj_main_wid)
        v_layout = QVBoxLayout(self.uj_main_wid)
        scroll_area = QScrollArea(self.uj_main_wid)
        for folder in self.uj_folders:
            id_tedit = QTextEdit()
            id_tedit.setObjectName(folder)
            id_tedit.setFixedWidth(50)
            id_tedit.setFixedHeight(50)
            id_lbl = QLabel()
            id_lbl.setText(folder)
            id_lbl.setFixedWidth(100)
            id_lbl.setFixedHeight(20)
            middle_layout.addRow(id_tedit, id_lbl)
        finish_btn = QPushButton(self.uj_main_wid)
        finish_btn.setText("Finish")
        finish_btn.clicked.connect(self.uj_folder_selected_btn)
        finish_btn.setFixedSize(100, 50)
        middle_layout.addWidget(finish_btn)
        group_box = QGroupBox(self.uj_main_wid)
        group_box.setLayout(middle_layout)
        scroll_area.setWidget(group_box)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(300)
        scroll_area.setFixedWidth(300)
        v_layout.addWidget(scroll_area, alignment=Qt.AlignTop)
        self.new_uj_folder_select_window.setCentralWidget(self.uj_main_wid)
        self.new_uj_folder_select_window.show()

    def uj_folder_selected_btn(self):
        # Iterate all folder & text-edits
        for i, edit in enumerate(self.uj_main_wid.findChildren(QTextEdit)):
            id = edit.toPlainText() if len(edit.toPlainText()) > 0 else i + 99
            if edit.objectName() in self.uj_folders:
                self.uj_id_folder_match.append([int(id), edit.objectName()])

        self.uj_id_folder_match.sort(key=lambda x: x[0])
        temp_json = {}
        for k in self.json_contents["meta"]:
            temp_json[k] = self.json_contents["meta"][k]

        temp_json["variables_metadata"] = {}
        for (id, key) in self.uj_id_folder_match:
            temp_json["variables_metadata"][key] = self.json_contents["variables_metadata"][key]

        # Write updated json
        with open(os.path.join(self.uj_folder_path, "assets_selection.json"), 'w') as json_write:
            json.dump(temp_json, json_write, indent=4, sort_keys=True)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Updated Json.")
        msg.setWindowTitle("Success")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()

    def uj_execute_clicked(self):
        if len(self.uj_folder_path) < 2:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Make sure all the fields are filled.")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
        else:
            self.uj_folders = []
            # Look for json file in assets folder
            if self.uj_folder_path and os.path.exists(os.path.join(self.uj_folder_path, "assets_selection.json")):
                # Read file
                with open(os.path.join(self.uj_folder_path, "assets_selection.json"), 'r') as json_reader:
                    temp_json = json.load(json_reader)
                    for k in list(temp_json.keys())[:-1]:
                        self.json_contents["meta"][k] = temp_json[k]
                    self.json_contents["variables_metadata"] = temp_json["variables_metadata"]

                # Iterate assets folders and see if any new files are added
                for subdir, dirs, files in os.walk(self.uj_folder_path):
                    for dir in dirs:
                        # The directory is the asset category
                        if dir in list(self.json_contents["variables_metadata"].keys()):
                            existing_assets = self.json_contents["variables_metadata"][dir]["assets"]
                            self.uj_folders.append(dir)
                            for filename in os.listdir(os.path.join(subdir, dir)):
                                file_names = [val[0] for val in existing_assets]
                                if filename not in file_names and filename.split(".")[-1] in ["png", "jpg"]:
                                    existing_assets.append([filename, filename, 0.1])
                            sorted(existing_assets, key=lambda x: int(x[0].split("_")[-1].split('.')[0]))
                        else:
                            new_assets = []
                            self.uj_folders.append(dir)
                            for filename in os.listdir(os.path.join(subdir, dir)):
                                if filename.split(".")[-1] in ["png", "jpg"]:
                                    new_assets.append([filename, filename, 0.1])
                            sorted(new_assets, key=lambda x: int(x[0].split("_")[-1].split('.')[0]))
                            self.json_contents["variables_metadata"][dir] = {
                                "assets": new_assets,
                                "can_export": 1,
                                "selected": 1
                            }
                        # Popup another UI, where to select folders.
                        # Sort all lists alltogether
                for key in self.json_contents["variables_metadata"]:
                    self.json_contents["variables_metadata"][key]["assets"] = sorted(self.json_contents["variables_metadata"][key]["assets"], key=lambda x: int(x[0].split("_")[-1].split('.')[0]))
            QApplication.processEvents()
            self.uj_folder_select_window()

    def ad_execute_clicked(self):
        folder_path = self.ad_folder_path
        qty = self.ad_qt_field.toPlainText()
        if len(folder_path) < 2 or int(qty) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Make sure all the fields are filled.")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
        else:
            files = glob(os.path.join(folder_path, "*"))
            for file in files:
                for i in range(int(qty)):
                    (f_name, f_ext) = file.split("\\")[-1].split(".")
                    new_file_path = os.path.join(folder_path, f_name + "_{}.{}".format(i, f_ext))
                    shutil.copy(file, new_file_path)
            QApplication.processEvents()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Successfully duplicated {} files.".format(qty))
            msg.setWindowTitle("Success")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()


if __name__ == "__main__":
    while True:
        import sys
        app = QApplication(sys.argv)
        MainWindow = QMainWindow()
        ui = Ui_MainWindow()
        ui.setup_ui(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
