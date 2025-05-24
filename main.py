import sys
from PyQt6.QtWidgets import QApplication
from ui.PhotoProcess import PhotoProcessor


def main():
    app = QApplication(sys.argv)
    window = PhotoProcessor()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()