from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLabel,
                             QGridLayout, QStackedWidget, QMenu, QAction,
                             QMessageBox, QFileDialog, QComboBox, QHBoxLayout,
                             QSizePolicy, QLineEdit, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDoubleValidator, QIntValidator

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from init_scanner_ui import InitScannerUI
from scanner_init_ui import SetScannerUI
from coil_control_ui import CoilOverviewUI
from coil_design_ui import CoilDesignUI

class MainWindow(QMainWindow):

    mouse_clicked_outside = pyqtSignal()
    save_clicked = QAction('Save')

    def __init__(self):
        super().__init__()

        self.setWindowTitle("SimMR") # Set main window title

        self.menu = self.menuBar()
        self.save_menu = self.menu.addMenu('File')
        self.setMenuBar(self.menu)
        self.save_menu.addAction(self.save_clicked)

        self.window = QWidget()
        self.setCentralWidget(self.window)
        self.layout = QGridLayout()
        self.window.setLayout(self.layout)

        self.tl_w = Control_Panel_Widget(self.window)
        self.layout.addWidget(self.tl_w, 0, 0)
        self.tr_w = View_Widget(self.window)
        self.layout.addWidget(self.tr_w, 0, 1)
        self.bl_w = Fields_View_Widget(self.window)
        self.layout.addWidget(self.bl_w, 1, 0)
        self.br_w = Mag_Phase_View_Widget(self.window)
        self.layout.addWidget(self.br_w, 1, 1)

        self.layout.setColumnStretch(0, 3)
        self.layout.setColumnStretch(1, 2)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 1)

        self.showMaximized() # Open GUI to maximized screen size

    def mousePressEvent(self, event):
        self.mouse_clicked_outside.emit()

    def error_poput(self, title : str, message : str):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.setStandardButtons(QMessageBox.Ok)

        error_box.exec_()

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle('Open File')
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        # Check if the dialog was accepted (a file was selected)
        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_files = file_dialog.selectedFiles()
            # Process the selected file(s)
            for file_path in selected_files:
                return file_path
            
    def save_file_dialog(self):
        # Open folder dialog for saving a file
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle('Save File')
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setFileMode(QFileDialog.AnyFile)

        # Check if the dialog was accepted (a folder was selected)
        if file_dialog.exec_() == QFileDialog.Accepted:
            return file_dialog.selectedFiles()[0]

class Control_Panel_Widget(QWidget):

    BBOX_MIN_VALUE = 0.001 # Double (minimum double)
    BBOX_MAX_VALUE = 10.000 # Double (maximum double)
    BBOX_MIN_MAX_DEC = 3 # Integer (number of decimal places)

    bbox_validator = QDoubleValidator(BBOX_MIN_VALUE, BBOX_MAX_VALUE, BBOX_MIN_MAX_DEC)

    MIN_RESOLUTION = 0.01 # Double (minimum double)
    MAX_RESOLUTION = 1.00 # Double (maximum double)
    MIN_MAX_RES_DEC = 2 # Integer (number of decimal places)

    vol_res_validator = QDoubleValidator(MIN_RESOLUTION, MAX_RESOLUTION, MIN_MAX_RES_DEC)

    def __init__(self, parent : QWidget):
        super().__init__(parent)

        self.stack = QStackedWidget(self)

        self.init_scanner = InitScannerUI() # Prompt to initialize a scanner
        self.set_scanner = SetScannerUI() # To define scanner parameters
        self.coil_control = CoilOverviewUI() # 'Overview' of coils in a given scanner
        self.coil_design = CoilDesignUI() # Designing / modifying a coil (adding/editing segments etc.)

        self.stack.addWidget(self.init_scanner)
        self.stack.addWidget(self.set_scanner)
        self.stack.addWidget(self.coil_control)
        self.stack.addWidget(self.coil_design)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.stack)

        self.stack.setCurrentIndex(0)

class View_Widget(QWidget):

    export_btn_clicked = pyqtSignal()
    slice_loc_modified_signal = pyqtSignal(int)

    slice_loc_validator = QIntValidator()

    def __init__(self, parent : QWidget):
        super(View_Widget, self).__init__(parent)
        self.figure = plt.figure()

        self.ax = self.figure.add_subplot(111, projection='3d')
        self.ax.set_xlabel("$x$")
        self.ax.set_ylabel("$y$")
        self.ax.set_zlabel("$z$")
        self.ax.view_init(vertical_axis = 'y')

        self.canvas = FigureCanvas(self.figure)

        btn_layout = QHBoxLayout()

        tmp_btn_lo = QVBoxLayout()
        tmp_lbl = QLabel('Slice Axis')
        tmp_lbl.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        tmp_btn_lo.addWidget(tmp_lbl)
        self.slice_combo_btn = QComboBox()
        self.slice_combo_btn.addItem('x')
        self.slice_combo_btn.addItem('y')
        self.slice_combo_btn.addItem('z')
        self.slice_combo_btn.setCurrentIndex(2)
        tmp_btn_lo.addWidget(self.slice_combo_btn)
        btn_layout.addLayout(tmp_btn_lo)

        tmp_btn_lo = QVBoxLayout()
        self.slice_loc_lbl = QLabel('Slice Number')
        self.slice_loc_lbl.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        tmp_btn_lo.addWidget(self.slice_loc_lbl)
        self.slice_loc_btn = QLineEdit('1')
        self.slice_loc_btn.setValidator(self.slice_loc_validator)
        self.slice_loc_btn.editingFinished.connect(self.slice_loc_modified)
        tmp_btn_lo.addWidget(self.slice_loc_btn)
        btn_layout.addLayout(tmp_btn_lo)

        self.export_btn = QPushButton('Export')
        self.export_btn.clicked.connect(self.export_btn_clicked)
        btn_layout.addWidget(self.export_btn)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def set_slice_loc_label(self, low_lim, up_lim):
        self.layout().itemAt(1).layout().itemAt(1).layout().itemAt(0).widget().setText('Slice Number (' + str(low_lim) + ' - ' + str(up_lim) + ')')

    def slice_loc_modified(self):
        self.slice_loc_modified_signal.emit(int(self.slice_loc_btn.text()))

class Fields_View_Widget(QWidget):

    def __init__(self, parent : QWidget):
        super(Fields_View_Widget, self).__init__(parent)
        self.figure, self.axes = plt.subplots(nrows=1, ncols=3)
        plt.subplots_adjust(left = 0.1, right = 0.8, wspace = 0.3)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

class Mag_Phase_View_Widget(QWidget):

    def __init__(self, parent : QWidget):
        super(Mag_Phase_View_Widget, self).__init__(parent)
        self.figure, self.axes = plt.subplots(nrows=1, ncols=2)
        plt.subplots_adjust(wspace = 0.5)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)