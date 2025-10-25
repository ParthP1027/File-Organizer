import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QTreeView, QFileSystemModel, QRadioButton, QPushButton, QLabel, QFileDialog, QMessageBox,
    QButtonGroup, QCheckBox
)
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import Qt
from file_organizer import *


class FileOrganizerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer - CS50")
        self.setGeometry(300, 200, 900, 600)
        self.status = self.statusBar()
        self.folder = ""
        self.status.setStyleSheet("""
            QStatusBar {
                background-color: #2d2f30;
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
            QStatusBar::item {
                border: 1px solid;

            }
        """)

        # Main Window
        container = QWidget()
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("📁 File Organizer")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setFixedHeight(30)
        main_layout.addWidget(title)

        # Divider
        splitter = QSplitter(Qt.Horizontal, self)

        # Status Text
        self.status_text = QLabel()
        self.set_status("Idle", "🔃")
        self.status_text.setStyleSheet(
            "margin-top:10px;font-size:18px;font-weight:bold;width:fit")
        self.status_text.setWordWrap(True)

        main_layout.addWidget(splitter)

        # Left Panel
        left_widget = QWidget()
        left_layout = QVBoxLayout()

        folder_label = QLabel("📂 Select Folder:")
        folder_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        left_layout.addWidget(folder_label)

        self.select_folder_button = QPushButton("Select folder")
        self.open_folder_button = QPushButton("Open folder")
        self.select_folder_button.clicked.connect(self.open_folder_dialog)
        self.open_folder_button.clicked.connect(self.open_folder)
        left_layout.addWidget(self.select_folder_button)
        left_layout.addWidget(self.open_folder_button)

        left_layout.addSpacing(20)
        mode_label = QLabel("⚒️ Select Mode:")
        mode_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        left_layout.addWidget(mode_label)

        self.radio_organize = QRadioButton("Organize by Type")
        self.radio_date = QRadioButton("Organize by Date")
        self.radio_duplicate = QRadioButton("Separate Unique Copies")
        self.radio_flatten = QRadioButton("Flatten Folder")

        self.group = QButtonGroup()
        self.group.addButton(self.radio_organize, 1)
        self.group.addButton(self.radio_date, 2)
        self.group.addButton(self.radio_duplicate, 3)
        self.group.addButton(self.radio_flatten, 4)

        left_layout.addWidget(self.radio_organize)
        left_layout.addWidget(self.radio_date)
        left_layout.addWidget(self.radio_duplicate)
        left_layout.addWidget(self.radio_flatten)

        self.remove_folder_button = QCheckBox()
        self.remove_folder_button.setText("🗑️ Remove all the folders")
        self.remove_folder_button.setHidden(True)
        self.remove_folder_button.setStyleSheet("padding-left: 10px")
        self.group.buttonClicked.connect(
            lambda: (self.remove_folder_button.setHidden(self.group.checkedId() != 4), self.set_status("Idle", "🔃")))
        left_layout.addWidget(self.remove_folder_button)

        self.run_button = QPushButton("▶️ Run")
        self.run_button.clicked.connect(self.organize)
        left_layout.addWidget(self.run_button)

        self.run_button.setMinimumHeight(40)
        self.select_folder_button.setMinimumHeight(40)
        self.open_folder_button.setMinimumHeight(40)

        left_layout.addSpacing(20)
        summary_label = QLabel("📋 Summary:")
        summary_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        left_layout.addWidget(summary_label)

        self.summary = QLabel("")
        self.summary.setStyleSheet("font-size: 14px")
        left_layout.addWidget(self.summary)
        left_layout.addStretch()
        left_widget.setLayout(left_layout)

        # Right Panel
        right_widget = QWidget()
        right_layout = QVBoxLayout()

        self.tree_view = QTreeView()
        self.model = QFileSystemModel()
        self.tree_view.setModel(self.model)
        self.tree_view.setColumnWidth(0, 300)

        self.folder_name_text = QLabel("Folder: ")
        right_layout.addWidget(self.folder_name_text)
        right_layout.addWidget(self.tree_view)

        self.folder_details = QLabel("")
        self.folder_details.setStyleSheet("font-size:14px;font-weight:bold")
        right_layout.addWidget(self.folder_details)

        right_widget.setLayout(right_layout)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([300, 600])

        container = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(splitter)

        container.setLayout(main_layout)
        self.setCentralWidget(container)

    # Used to set the text of status bar

    def set_status(self, status, icon="🔍"):
        self.status.showMessage(f"{icon} Status: {status}")

    # Used to show summary after the operation is completed
    def show_summary(self, summaries):
        text = ""
        for key, value in summaries.items():
            subtext = ""

            if type(value) == dict:
                for subkey, subvalue in value.items():
                    subtext += f"\n\t{subkey}: {subvalue}"
                text += f"{key}: {subtext}\n"
            else:
                text += f"{key}: {value}\n"

        self.summary.setText(text)

    # Open folder dialog to select folder
    def open_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select Folder", os.path.expanduser(""))
        if folder:
            self.folder = folder
            self.model.setRootPath(folder)
            self.tree_view.setRootIndex(self.model.index(folder))
            self.folder_name_text.setText(f"Folder: {folder}")
            self.update_directory_details()

    # Open folder in file explorer
    def open_folder(self):
        try:
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.folder))
        except AttributeError:
            QMessageBox.information(
                self, "No folder selected", "Please select a folder to open it in file explorer")
        except Exception as e:
            QMessageBox.warning(self, "Unable to open folder",
                                "Unable to open the selected folder. Please try again")

    # Used to get and update files and folder count
    def update_directory_details(self):
        files = os.listdir(self.folder)
        file_count = 0
        folder_count = 0

        for i in files:
            path = os.path.join(self.folder, i)

            if os.path.isdir(path):
                folder_count += 1
            else:
                file_count += 1

        self.folder_details.setText(
            f"{file_count} Files {folder_count} Subfolder found in folder")

    # Run operation

    def organize(self):
        # Check if folder is selected
        try:
            folder = self.folder
        except AttributeError:
            QMessageBox.information(
                self, "No folder selected", "Please select a folder on which operation is to be performed")
            return

        # Check if operation is selected
        checked_id = self.group.checkedId()
        if checked_id != -1:
            self.group.setExclusive(False)
            self.set_status("Processing", "🔍")
            self.show_summary({})
            QApplication.processEvents()
            result = {}

            match checked_id:
                case 1:
                    result = organize_files(self.folder)
                    self.set_status("Files organized based on type", "✅")
                case 2:
                    result = organize_by_creation(self.folder)
                    self.set_status(
                        "Files organized based on creation time", "✅")
                case 3:
                    result = separate_unique(self.folder)
                    self.set_status("Unique files separated", "✅")
                case 4:
                    result = flatten_folder(
                        self.folder, self.remove_folder_button.isChecked())
                    self.set_status("Folders successfully flatten", "✅")
                    self.remove_folder_button.setHidden(True)

            # Showing summary and deselecting operation
            self.show_summary(result)
            self.group.checkedButton().setChecked(False)
            self.group.setExclusive(True)
            self.update_directory_details()
        else:
            QMessageBox.information(
                self, "Valid operation required", "Please select a operation to be perform")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizerUI()
    window.show()
    sys.exit(app.exec())
