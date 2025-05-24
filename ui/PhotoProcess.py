import os
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QPushButton, QTextEdit, QFileDialog, QLabel)
from PyQt6.QtCore import Qt

from parser import start

class PhotoProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.images = []
        self.setWindowTitle("Обработчик фотографий")
        self.setGeometry(100, 100, 500, 400)

        self.folder_label = QLabel("Папка не выбрана")
        self.folder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.select_button = QPushButton("Выбрать папку")
        self.select_button.clicked.connect(self.select_folder)

        self.process_button = QPushButton("Обработать фотографии")
        self.process_button.clicked.connect(self.get_images)
        self.process_button.setEnabled(False)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.folder_label)
        layout.addWidget(self.select_button)
        layout.addWidget(self.process_button)
        layout.addWidget(self.log_output)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.selected_folder = ""

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с фотографиями")
        if folder:
            self.selected_folder = folder
            self.folder_label.setText(f"Выбрана папка: {folder}")
            self.process_button.setEnabled(True)
            self.log("Папка выбрана успешно")


    def get_images(self):
        if not self.selected_folder:
            self.log("Ошибка: папка не выбрана")
            return

        self.log(f"Начинаем обработку фотографий в папке: {self.selected_folder}")

        for filename in os.listdir(self.selected_folder):
            path = self.selected_folder
            file_path = os.path.join(path, filename)
            print(file_path)
            if os.path.isfile(file_path) and filename.endswith(('.jpg', '.png', '.jpeg', '.bmp', '.gif', '.webr')):
                self.images.append(file_path)
            else:
                print(f'Skipping {filename} - not a image')

        start(self.images)

    def log(self, message):
        self.log_output.append(message)
        self.log_output.ensureCursorVisible()
        QApplication.processEvents()
