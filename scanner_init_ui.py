from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDoubleValidator

class SetScannerUI(QWidget):

    button_clicked = pyqtSignal(list, list)

    def __init__(self):
        super().__init__()

        self.lo = QVBoxLayout() 
        self.setLayout(self.lo)

        self.bbox_gb_w = QGroupBox('Set Bounding Box Limits', self)
        self.bbox_gb_lo = QVBoxLayout()
        self.bbox_gb_w.setLayout(self.bbox_gb_lo)

        self.bbox_xlim_lo = self.BBoxCoordLimLO('X-Coordinate')
        self.bbox_gb_lo.addLayout(self.bbox_xlim_lo)

        self.bbox_ylim_lo = self.BBoxCoordLimLO('Y-Coordinate')
        self.bbox_gb_lo.addLayout(self.bbox_ylim_lo)

        self.bbox_zlim_lo = self.BBoxCoordLimLO('Z-Coordinate')
        self.bbox_gb_lo.addLayout(self.bbox_zlim_lo)

        vol_widget = QGroupBox('Set Volume Resolution') # Modify to have buttons for resolution
        vol_layout = QHBoxLayout()
        vol_widget.setLayout(vol_layout)

        self.xvol_lo = self.VolResLimLO(' X-Plane')
        vol_layout.addLayout(self.xvol_lo)

        self.yvol_lo = self.VolResLimLO(' Y-Plane')
        vol_layout.addLayout(self.yvol_lo)

        self.zvol_lo = self.VolResLimLO(' Z-Plane')
        vol_layout.addLayout(self.zvol_lo)

        self.init_scanner_btn = QPushButton('Initialize Scanner')
        self.init_scanner_btn.clicked.connect(self.init_scanner_pressed)

        self.lo.addWidget(self.bbox_gb_w)
        self.lo.addWidget(vol_widget)
        self.lo.addWidget(self.init_scanner_btn)

    def parse_bbox_coords(self):   
        return [
            float(self.bbox_xlim_lo.bbox_lim_min_le.text()),
            float(self.bbox_xlim_lo.bbox_lim_max_le.text()),
            float(self.bbox_ylim_lo.bbox_lim_min_le.text()),
            float(self.bbox_ylim_lo.bbox_lim_max_le.text()),
            float(self.bbox_zlim_lo.bbox_lim_min_le.text()),
            float(self.bbox_zlim_lo.bbox_lim_max_le.text()),
        ] 
    
    def parse_vol_res(self):
        return [
            float(self.xvol_lo.vol_le.text()),
            float(self.yvol_lo.vol_le.text()),
            float(self.zvol_lo.vol_le.text()),
        ]

    def init_scanner_pressed(self):
        if (self.bbox_xlim_lo.input_is_valid() 
            and self.bbox_ylim_lo.input_is_valid() 
            and self.bbox_zlim_lo.input_is_valid() 
            and self.xvol_lo.input_is_valid() 
            and self.yvol_lo.input_is_valid() 
            and self.zvol_lo.input_is_valid()):
            self.button_clicked.emit(self.parse_bbox_coords(), self.parse_vol_res())

    class BBoxCoordLimLO(QHBoxLayout):

        BBOX_MIN_VALUE = -100.000 # Double (minimum double)
        BBOX_MAX_VALUE = 100.000 # Double (maximum double)
        BBOX_MIN_MAX_DEC = 3 # Integer (number of decimal places)

        bbox_validator = QDoubleValidator(BBOX_MIN_VALUE, BBOX_MAX_VALUE, BBOX_MIN_MAX_DEC) 

        def __init__(self, coord_string : str):
            super().__init__()

            self.bbox_lim_l1 = QLabel(coord_string)
            self.bbox_lim_l1.setAlignment(Qt.AlignBottom | Qt.AlignRight)
            self.bbox_lim_l1.setIndent(5)
            self.addWidget(self.bbox_lim_l1)

            self.bbox_min_lim_lo = QVBoxLayout()
            self.addLayout(self.bbox_min_lim_lo)
            self.bbox_lim_l2 = QLabel(' Minimum')
            self.bbox_lim_l2.setAlignment(Qt.AlignBottom)
            self.bbox_min_lim_lo.addWidget(self.bbox_lim_l2)
            self.bbox_lim_min_le = QLineEdit()
            self.bbox_lim_min_le.setValidator(self.bbox_validator)
            self.bbox_lim_min_le.editingFinished.connect(self.show_validity)
            self.bbox_min_lim_lo.addWidget(self.bbox_lim_min_le)

            self.bbox_max_lim_lo = QVBoxLayout()
            self.addLayout(self.bbox_max_lim_lo)
            self.bbox_lim_l3 = QLabel(' Maximum')
            self.bbox_lim_l3.setAlignment(Qt.AlignBottom)
            self.bbox_max_lim_lo.addWidget(self.bbox_lim_l3)
            self.bbox_lim_max_le = QLineEdit()
            self.bbox_lim_max_le.setValidator(self.bbox_validator)
            self.bbox_lim_max_le.editingFinished.connect(self.show_validity)
            self.bbox_max_lim_lo.addWidget(self.bbox_lim_max_le)

        def show_validity(self):
            sender = self.sender()
            if sender.hasAcceptableInput():
                sender.setStyleSheet('border-color: green')
            else:
                # FIXIT: Currently doesn't trigger this else statement as the editingFinished
                # signal for QLineEdit is only triggered if the input is valid as described
                # by the QLineEdit QValidator - need to find some sort of workaround (text changed, maybe?)
                print('Made it here')
                sender.setStyleSheet('border-color: red')

        def input_is_valid(self):
            if self.bbox_lim_min_le.hasAcceptableInput() and self.bbox_lim_max_le.hasAcceptableInput():
                return True
            
            return False

    class VolResLimLO(QVBoxLayout):
        MIN_RESOLUTION = 0.01 # Double (minimum double)
        MAX_RESOLUTION = 1.00 # Double (maximum double)
        MIN_MAX_RES_DEC = 2 # Integer (number of decimal places)

        vol_res_validator = QDoubleValidator(MIN_RESOLUTION, MAX_RESOLUTION, MIN_MAX_RES_DEC)

        def __init__(self, plane : str):
            super().__init__()

            vol_l1 = QLabel(plane)
            vol_l1.setAlignment(Qt.AlignBottom)
            self.addWidget(vol_l1)
            self.vol_le = QLineEdit()
            self.vol_le.setValidator(self.vol_res_validator)
            self.vol_le.editingFinished.connect(self.show_validity)
            self.addWidget(self.vol_le)

        def show_validity(self):
            sender = self.sender()
            if sender.hasAcceptableInput():
                sender.setStyleSheet('border-color: green')
            else:
                # FIXIT: Currently doesn't trigger this else statement as the editingFinished
                # signal for QLineEdit is only triggered if the input is valid as described
                # by the QLineEdit QValidator - need to find some sort of workaround (text changed, maybe?)
                print('Made it here')
                sender.setStyleSheet('border-color: red')

        def input_is_valid(self):
            if self.vol_le.hasAcceptableInput():
                return True
            
            return False
     