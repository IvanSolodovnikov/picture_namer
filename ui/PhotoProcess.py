import os
from concurrent.futures import ThreadPoolExecutor

from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QPushButton, QTextEdit, QFileDialog, QLabel, QLineEdit)
from PyQt6.QtCore import Qt

from parser import create_driver, URL, get_text
from saver import ExcelResultsSaver

class PhotoProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.images = [[] for _ in range(5)]
        self.setWindowTitle("Обработчик фотографий")
        self.setGeometry(100, 100, 500, 400)

        self.folder_label = QLabel("Папка не выбрана")
        self.folder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Введите название файла для сохранения")

        self.select_button = QPushButton("Выбрать папку")
        self.select_button.clicked.connect(self.select_folder)

        self.process_button = QPushButton("Обработать фотографии")
        self.process_button.clicked.connect(self.get_images)
        self.process_button.setEnabled(False)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.folder_label)
        layout.addWidget(self.filename_input)
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
            self.log("Папка выбрана успешно", 'green')


    def get_images(self):
        if not self.selected_folder:
            self.log("Ошибка: папка не выбрана", 'red')
            return

        filename = self.filename_input.text().strip()
        if not filename:
            self.log("Ошибка: не указано название файла", 'red')
            return
        saver = ExcelResultsSaver(filename)

        self.log(f"Начинаем обработку фотографий в папке: {self.selected_folder}")

        for i, filename in enumerate(os.listdir(self.selected_folder)):
            path = self.selected_folder
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path) and filename.endswith(('.jpg', '.png', '.jpeg', '.bmp', '.gif', '.webp')):
                self.images[i%5].append(file_path)
            else:
                self.log(f'Пропуск{filename.split('\\')[-1]:<30} - не фото', 'red')



        def start(images):
            try:
                wd = create_driver()
                wd.get(URL)
                if images:
                    for image in images:
                        text = get_text(wd, image)
                        if text:
                            saver.add_result(image, text)
                wd.quit()
            except Exception as e:
                print(e)

        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(start, self.images)
        saver.save_all()
        self.log(f'Всё успешно сохранено в {saver.output_file}', 'green')


    def log(self, message, color = 'black'):
        colored_message = f'<span style="color:{color}">{message}</span>'
        self.log_output.append(colored_message)
        self.log_output.ensureCursorVisible()
        QApplication.processEvents()