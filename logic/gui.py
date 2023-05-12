from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel

import matplotlib.pyplot as plt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MR Coil Sensitivity Map Simulator") # Set main window title
        self.init_UI() # Call initUI() to initialize the user interface
        self.showMaximized() # Open GUI to maximized screen size
    
    def init_UI(self):
        window = QWidget() # Initialize main widget for self
        self.setCentralWidget(window) # Make window central widget of self
        main_layout = QHBoxLayout() # HBox for the "biggest" bin
        window.setLayout(main_layout) # Set main_bin as window's layout

        self.init_left_bin_UI(main_layout)

    def init_left_bin_UI(self, layout : QHBoxLayout):
        left_bin = QWidget() # Left QWidget bin 
        layout.addWidget(left_bin) # Add left_bin to main_bin
        self.init_params_UI(left_bin) # Initialize parameter insertion UI

        right_bin = QWidget() # Right QWidget bin
        layout.addWidget(right_bin) # Add right_bin to main_bin

        

        # right_bin.setLayout(self.init_coil_plot_UI()) # Initialize coil plot UI

    def init_params_UI(self, widget : QWidget):
        params_layout = QVBoxLayout() # Set params_layout as vertical box
        init_scanner_btn = QPushButton('Initialize MR Scanner') # Button to create a scanner object
        params_layout.addWidget(init_scanner_btn) # Add button to params layout

        init_scanner_btn.clicked.connect(self.init_scanner)

        params_layout.addWidget(QLabel('Placeholder')) # Placeholder
        
        widget.setLayout(params_layout)
  
    def init_scanner(self):
        btn_layout = self.sender().parent().layout()
        

    def init_coil_plot_UI(self):
        coil_plot_bin = QWidget()

    

        


if __name__ == '__main__':
    app = QApplication([])
    gui = MainWindow()
    app.exec()


