# The purpose of this app is to display the file and folder structure of a directory and its subdirectories. Thanks to DuckDuckGo and Grok for help with bug squashing. 

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class FolderViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Folder Tree Viewer")
        self.resize(900, 700)
        self.setAcceptDrops(True)
        self.current_path = ""

        main_layout = QVBoxLayout(self)

        #Top labels
        self.label = QLabel("Drag & drop a folder or click 'Open Folder'")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; color: #444; padding: 10px;")

        #Text area
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont("Consolas", 11))

        #Buttons
        btn_layout = QHBoxLayout()

        self.open_btn = QPushButton("Open Folder…")
        self.open_btn.clicked.connect(self.open_folder)

        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_view)

        btn_layout.addWidget(self.open_btn)
        btn_layout.addWidget(self.copy_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()

        # Assemble everything
        main_layout.addWidget(self.label)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.text_edit)

    #Drag n' Drop
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        path = event.mimeData().urls()[0].toLocalFile()
        if os.path.isdir(path):
            self.load_folder(path)
        else:
            self.label.setText("Please drop a folder")

    #Functions
    def open_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if path:
            self.load_folder(path)

    def load_folder(self, path):
        self.current_path = path
        self.label.setText(f"Folder: {path}")
        tree_text = self.build_tree(path)
        self.text_edit.setPlainText(tree_text)

    def copy_to_clipboard(self):
        text = self.text_edit.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.label.setText("Copied to clipboard!")

    def clear_view(self):
        self.current_path = ""
        self.text_edit.clear()
        self.label.setText("Drag & drop a folder or click 'Open Folder'")

    #How the tree looks
    def build_tree(self, root_path, indent=""):
        lines = [os.path.basename(root_path) + "/\n"]
        try:
            items = sorted(os.listdir(root_path))
        except PermissionError:
            lines.append(indent + "    [Permission Denied]\n")
            return "".join(lines)

        for i, item in enumerate(items):
            item_path = os.path.join(root_path, item)
            connector = "└── " if i == len(items) - 1 else "├── "
            display_name = item + ("/" if os.path.isdir(item_path) else "")
            lines.append(f"{indent}{connector}{display_name}\n")

            if os.path.isdir(item_path):
                extension = "    " if i == len(items) - 1 else "│   "
                lines.append(self.build_tree(item_path, indent + extension))

        return "".join(lines)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FolderViewer()
    window.show()
    sys.exit(app.exec())
