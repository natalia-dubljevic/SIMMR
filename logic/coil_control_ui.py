from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDoubleValidator

class CoilOverviewUI(QWidget):

    mod_scanner_clicked = pyqtSignal()
    del_coil_clicked = pyqtSignal()
    edit_coil_clicked = pyqtSignal()
    add_coil_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.lo = QVBoxLayout()
        self.setLayout(self.lo)
        
        # Scroll area for coils
        scr = QScrollArea()
        self.scr_w = QWidget()
        scr_lo = QVBoxLayout()
        self.scr_w.setLayout(scr_lo)

        for i in range(0, 51):
            scr_lo.addWidget(QLabel('Testing: ' + str(i) + '!'))

        scr.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scr.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scr.setWidget(self.scr_w)

        self.lo.addWidget(scr)
        #------------------------

        # Buttons for 'edit' and 'add' coils
        btn_lo = QHBoxLayout()
        self.lo.addLayout(btn_lo)

        self.edit_scanner_btn = QPushButton('Modify Scanner Parameters')
        btn_lo.addWidget(self.edit_scanner_btn)
        self.del_coil_btn = QPushButton('Delete Coil')
        btn_lo.addWidget(self.del_coil_btn)
        self.edit_coil_btn = QPushButton('Edit Coil')
        btn_lo.addWidget(self.edit_coil_btn)
        self.add_coil_btn = QPushButton('Add Coil')
        btn_lo.addWidget(self.add_coil_btn)
        
        self.edit_scanner_btn.clicked.connect(self.mod_scanner_clicked)
        self.del_coil_btn.clicked.connect(self.del_coil_clicked)
        self.edit_coil_btn.clicked.connect(self.edit_coil_clicked)
        self.add_coil_btn.clicked.connect(self.add_coil_clicked)
        #-------------------------
