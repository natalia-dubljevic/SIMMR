from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDoubleValidator

class CoilOverviewUI(QWidget):

    mod_scanner_clicked = pyqtSignal()
    del_coil_clicked = pyqtSignal()
    edit_coil_clicked = pyqtSignal()
    add_coil_clicked = pyqtSignal()

    coil_clicked = pyqtSignal(int)

    class SelectableCoilWidget(QWidget):
        def __init__(self, outer, index : int, num_segs : int):
            super().__init__()

            self.outer = outer

            self.ref_index = index

            self.lo = QHBoxLayout()
            self.setLayout(self.lo)

            coil_label = 'Coil: ' + str(index + 1)
            self.lo.addWidget(QLabel(coil_label))

            num_segments_label = 'Segments: ' + str(num_segs)
            self.lo.addWidget(QLabel(num_segments_label))

            self.setStyleSheet('border : 5px solid black')
            self.setStyleSheet('background : yellow')

        def mousePressEvent(self, event):
            self.outer.coil_clicked.emit(self.ref_index)


    def __init__(self):
        super().__init__()

        self.lo = QVBoxLayout()
        self.setLayout(self.lo)
        
        # Scroll area for coils
        self.scr = QScrollArea()
        self.scr_w = QWidget()
        self.scr_lo = QVBoxLayout()
        self.scr_w.setLayout(self.scr_lo)

        self.scr.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scr.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.lo.addWidget(self.scr)
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

    def update_coils(self, num_segs : list):

        replacement_widget = QWidget()
        replacement_lo = QVBoxLayout()
        replacement_widget.setLayout(replacement_lo)

        for i in range(0, len(num_segs)):
            replacement_lo.addWidget(self.SelectableCoilWidget(self, i, num_segs[i]))

        self.scr_w = replacement_widget
        self.scr.setWidget(self.scr_w)

    def highlight_selected(self, index : int):
        if index != None and self.scr_w.layout().itemAt(index) != None:
            self.scr_w.layout().itemAt(index).widget().setStyleSheet('background : cyan')

    def remove_highlight(self, index : int):
        if index != None and self.scr_w.layout().itemAt(index) != None:
            self.scr_w.layout().itemAt(index).widget().setStyleSheet('background : yellow')
