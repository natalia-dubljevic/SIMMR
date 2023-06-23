from PyQt5.QtWidgets import QApplication
from controller import Controller
from gui import MainWindow

def main():
    app = QApplication([])
    gui = MainWindow()
    controller = Controller(gui)

    # with open("style.qss", "r") as f:
    #     _style = f.read()
    #     app.setStyleSheet(_style)

    app.exec()

if __name__ == '__main__':
    main()