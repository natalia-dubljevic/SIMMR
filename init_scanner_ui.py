from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QStackedWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDoubleValidator

class InitScannerUI(QWidget):

    init_scanner_btn_clicked = pyqtSignal()
    load_scanner_btn_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        lo = QHBoxLayout()
        self.setLayout(lo)
        
        self.init_scanner_btn = QPushButton('Initialize MR Scanner')
        lo.addWidget(self.init_scanner_btn)
        self.init_scanner_btn.clicked.connect(self.init_scanner_btn_clicked)

        # TO DEVELOP:
        self.load_scanner_btn = QPushButton('Load Previous Workspace')
        lo.addWidget(self.load_scanner_btn)
        self.load_scanner_btn.clicked.connect(self.load_scanner_btn_clicked)