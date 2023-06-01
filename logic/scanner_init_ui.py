from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDoubleValidator

from controller import Controller

class SetScannerUI(QWidget):

    button_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.lo = QVBoxLayout() 
        self.setLayout(self.lo)

        self.bbox_gb_w = QGroupBox('Set Bounding Box Limits', self)
        self.bbox_gb_lo = QVBoxLayout()
        self.bbox_gb_w.setLayout(self.bbox_gb_lo)

        self.bbox_xlim_lo = self.BBoxCoordLimLO('X-Coordinate')
        self.bbox_gb_lo.addLayout(self.bbox_xlim_lo)

        ylim_layout = self.BBoxCoordLimLO('Y-Coordinate')
        self.bbox_gb_lo.addLayout(ylim_layout)

        zlim_layout = self.BBoxCoordLimLO('Z-Coordinate')
        self.bbox_gb_lo.addLayout(zlim_layout)

        vol_widget = QGroupBox('Set Volume Resolution') # Modify to have buttons for resolution
        vol_layout = QHBoxLayout()
        vol_widget.setLayout(vol_layout)

        xvol_lo = self.VolResLimLO(' X-Plane')
        vol_layout.addLayout(xvol_lo)

        yvol_lo = self.VolResLimLO(' Y-Plane')
        vol_layout.addLayout(yvol_lo)

        zvol_lo = self.VolResLimLO(' Z-Plane')
        vol_layout.addLayout(zvol_lo)

        self.init_scanner_btn = QPushButton('Initialize Scanner')
        self.init_scanner_btn.clicked.connect(self.init_scanner_pressed)

        self.lo.addWidget(self.bbox_gb_w)
        self.lo.addWidget(vol_widget)
        self.lo.addWidget(self.init_scanner_btn)

    def init_scanner_pressed(self):
        self.button_clicked.emit()

    class BBoxCoordLimLO(QHBoxLayout):

        BBOX_MIN_VALUE = 0.001 # Double (minimum double)
        BBOX_MAX_VALUE = 10.000 # Double (maximum double)
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
            self.bbox_min_lim_lo.addWidget(self.bbox_lim_min_le)

            self.bbox_max_lim_lo = QVBoxLayout()
            self.addLayout(self.bbox_max_lim_lo)
            self.bbox_lim_l3 = QLabel(' Maximum')
            self.bbox_lim_l3.setAlignment(Qt.AlignBottom)
            self.bbox_max_lim_lo.addWidget(self.bbox_lim_l3)
            self.bbox_lim_max_le = QLineEdit()
            self.bbox_lim_max_le.setValidator(self.bbox_validator)
            self.bbox_max_lim_lo.addWidget(self.bbox_lim_max_le)

    class VolResLimLO(QVBoxLayout):
        MIN_RESOLUTION = 0.01 # Double (minimum double)
        MAX_RESOLUTION = 1.00 # Double (maximum double)
        MIN_MAX_RES_DEC = 2 # Integer (number of decimal places)

        vol_res_validator = QDoubleValidator(MIN_RESOLUTION, MAX_RESOLUTION, MIN_MAX_RES_DEC)

        def __init__(self, plane : str):
            super().__init__()

            xvol_l1 = QLabel(plane)
            xvol_l1.setAlignment(Qt.AlignBottom)
            self.addWidget(xvol_l1)
            xvol_le = QLineEdit()
            xvol_le.setValidator(self.vol_res_validator)
            self.addWidget(xvol_le)
     