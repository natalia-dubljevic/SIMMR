from PyQt5.QtWidgets import QApplication
from controller import Controller
from gui import MainWindow


def main():
    app = QApplication([])
    gui = MainWindow()
    controller = Controller(gui)
    app.exec()

if __name__ == '__main__':
    main()