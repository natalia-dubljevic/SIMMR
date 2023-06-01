from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QStackedWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDoubleValidator

class CoilDesignUI(QWidget):

    straight_seg_clicked = pyqtSignal()
    curved_seg_clicked = pyqtSignal()


    def __init__(self):
        super().__init__()

        self.lo = QVBoxLayout()
        self.setLayout(self.lo)

        # GroupBox containing coil segment overview
        self.coil_seg_gb = QGroupBox('Coil Segments')
        self.lo.addWidget(self.coil_seg_gb)
        coil_seg_lo = QVBoxLayout()
        self.coil_seg_gb.setLayout(coil_seg_lo)

        # Scroll area for segment overview area (inisde coil_seg_gb)
        coil_seg_sa = QScrollArea()
        coil_seg_lo.addWidget(coil_seg_sa)
        coil_seg_sa_w = QWidget()
        coil_seg_sa_w_lo = QVBoxLayout()
        coil_seg_sa_w.setLayout(coil_seg_sa_w_lo)

        # Buttons areas
        coil_seg_btns_lo = QHBoxLayout()
        coil_seg_lo.addLayout(coil_seg_btns_lo)
        self.del_seg_btn = QPushButton('Delete Segment')
        self.edit_seg_btn = QPushButton('Edit Segment')
        self.add_seg_btn = QPushButton('Add Segment')
        coil_seg_btns_lo.addWidget(self.del_seg_btn)
        coil_seg_btns_lo.addWidget(self.edit_seg_btn)
        coil_seg_btns_lo.addWidget(self.add_seg_btn)

        # GroupBox containing segment editor 
        self.seg_edit_gb = QGroupBox('Segment Editor')
        seg_edit_lo = QVBoxLayout()
        self.seg_edit_gb.setLayout(seg_edit_lo)
        self.lo.addWidget(self.seg_edit_gb)

        seg_edit_gb_lo = QHBoxLayout()
        seg_edit_lo.addLayout(seg_edit_gb_lo)
        self.seg_edit_straight = QPushButton('Straight Segment')
        self.seg_edit_straight.clicked.connect(self.straight_seg_clicked)
        self.seg_edit_straight.setCheckable(True)
        self.seg_edit_curved = QPushButton('Curved Segment')
        self.seg_edit_curved.clicked.connect(self.curved_seg_clicked)
        self.seg_edit_curved.setCheckable(True)
        seg_edit_gb_lo.addWidget(self.seg_edit_straight)
        seg_edit_gb_lo.addWidget(self.seg_edit_curved)

        self.seg_edit_stack = QStackedWidget()
        seg_edit_lo.addWidget(self.seg_edit_stack)

        self.seg_edit_stack.addWidget(StraightSegmentEditor())
        self.seg_edit_stack.addWidget(CurvedSegmentEditor())

        self.seg_edit_stack.hide()


class StraightSegmentEditor(QWidget):

    def __init__(self):
        super().__init__()

        self.lo = QVBoxLayout()
        self.setLayout(self.lo)

        s_gb1 = QGroupBox('Initial Point')
        self.layout().addWidget(s_gb1)
        s_gb1_lo = QHBoxLayout()
        s_gb1.setLayout(s_gb1_lo)
        s_gb1_lo.addLayout(QVBoxLayout())
        s_gb1_lo.itemAt(0).addWidget(QLabel('X-Coordinate'))
        self.init_point_x_le = QLineEdit()
        s_gb1_lo.itemAt(0).addWidget(self.init_point_x_le)
        s_gb1_lo.addLayout(QVBoxLayout())
        s_gb1_lo.itemAt(1).addWidget(QLabel('Y-Coordinate'))
        self.init_point_y_le = QLineEdit()
        s_gb1_lo.itemAt(1).addWidget(self.init_point_y_le)
        s_gb1_lo.addLayout(QVBoxLayout())
        s_gb1_lo.itemAt(2).addWidget(QLabel('Z-Coordinate'))
        self.init_point_z_le = QLineEdit()
        s_gb1_lo.itemAt(2).addWidget(self.init_point_z_le)

        s_gb2 = QGroupBox('Direction Vector')
        self.layout().addWidget(s_gb2)
        s_gb2.setLayout(QHBoxLayout())
        s_gb2.layout().addLayout(QVBoxLayout())
        s_gb2.layout().itemAt(0).addWidget(QLabel('X-Component'))
        self.dir_x_le = QLineEdit()
        s_gb2.layout().itemAt(0).addWidget(self.dir_x_le)
        s_gb2.layout().addLayout(QVBoxLayout())
        s_gb2.layout().itemAt(1).addWidget(QLabel('Y-Component'))
        self.dir_y_le = QLineEdit()
        s_gb2.layout().itemAt(1).addWidget(self.dir_y_le)
        s_gb2.layout().addLayout(QVBoxLayout())
        s_gb2.layout().itemAt(2).addWidget(QLabel('Z-Component'))
        self.dir_z_le = QLineEdit()
        s_gb2.layout().itemAt(2).addWidget(self.dir_z_le)

        s_gb3 = QGroupBox('Direction Vector Multiplication Factor')
        self.layout().addWidget(s_gb3)
        s_gb3.setLayout(QHBoxLayout())
        s_gb3.layout().addLayout(QVBoxLayout())
        s_gb3.layout().itemAt(0).addWidget(QLabel('Multiplication Factor'))
        self.str_mul_fac = QLineEdit()
        s_gb3.layout().itemAt(0).addWidget(self.str_mul_fac)
        s_gb3.layout().addLayout(QVBoxLayout())
        s_gb3.layout().itemAt(1).addWidget(QLabel('Segment Length'))
        s_gb3.layout().itemAt(1).addWidget(QLabel('Test'))

class CurvedSegmentEditor(QWidget):

    def __init__(self):
        super().__init__()

        self.lo = QVBoxLayout()
        self.setLayout(self.lo)

        c_gb1 = QGroupBox('Centre Coordinate')
        self.lo.addWidget(c_gb1)
        c_gb1_lo = QHBoxLayout()
        c_gb1.setLayout(c_gb1_lo)
        c_gb1_lo.addLayout(QVBoxLayout())
        c_gb1_lo.itemAt(0).addWidget(QLabel('X-Coordinate'))
        self.ctr_x_le = QLineEdit() 
        c_gb1_lo.itemAt(0).addWidget(self.ctr_x_le)
        c_gb1_lo.addLayout(QVBoxLayout())
        c_gb1_lo.itemAt(1).addWidget(QLabel('Y-Coordinate'))
        self.ctr_y_le = QLineEdit() 
        c_gb1_lo.itemAt(1).addWidget(self.ctr_y_le)
        c_gb1_lo.addLayout(QVBoxLayout())
        c_gb1_lo.itemAt(2).addWidget(QLabel('Z-Coordinate'))
        self.ctr_z_le = QLineEdit() 
        c_gb1_lo.itemAt(2).addWidget(self.ctr_z_le)

        c_gb2 = QGroupBox('First Radius Vector')
        self.lo.addWidget(c_gb2)
        c_gb2_lo = QHBoxLayout()
        c_gb2.setLayout(c_gb2_lo)
        c_gb2_lo.addLayout(QVBoxLayout())
        c_gb2_lo.itemAt(0).addWidget(QLabel('X-Component'))
        self.r1_x_comp_le = QLineEdit()
        c_gb2_lo.itemAt(0).addWidget(self.r1_x_comp_le)
        c_gb2_lo.addLayout(QVBoxLayout())
        c_gb2_lo.itemAt(1).addWidget(QLabel('Y-Component'))
        self.r1_y_comp_le = QLineEdit()
        c_gb2_lo.itemAt(1).addWidget(self.r1_y_comp_le)
        c_gb2_lo.addLayout(QVBoxLayout())
        c_gb2_lo.itemAt(2).addWidget(QLabel('Z-Component'))
        self.r1_z_comp_le = QLineEdit()
        c_gb2_lo.itemAt(2).addWidget(self.r1_z_comp_le)


        c_gb3 = QGroupBox('Second Radius Vector')
        self.lo.addWidget(c_gb3)
        c_gb3_lo = QHBoxLayout()
        c_gb3.setLayout(c_gb3_lo)
        c_gb3_lo.addLayout(QVBoxLayout())
        c_gb3_lo.itemAt(0).addWidget(QLabel('X-Component'))
        self.r2_x_comp_le = QLineEdit()
        c_gb3_lo.itemAt(0).addWidget(self.r2_x_comp_le)
        c_gb3_lo.addLayout(QVBoxLayout())
        c_gb3_lo.itemAt(1).addWidget(QLabel('Y-Component'))
        self.r2_y_comp_le = QLineEdit()
        c_gb3_lo.itemAt(1).addWidget(self.r2_y_comp_le)
        c_gb3_lo.addLayout(QVBoxLayout())
        c_gb3_lo.itemAt(2).addWidget(QLabel('Z-Component'))
        self.r2_z_comp_le = QLineEdit()
        c_gb3_lo.itemAt(2).addWidget(self.r2_z_comp_le)

        c_gb4 = QGroupBox('Parameter Range (Factor of Pi)')
        self.lo.addWidget(c_gb4)
        c_gb4_lo = QHBoxLayout()
        c_gb4.setLayout(c_gb4_lo)
        c_gb4_lo.addLayout(QVBoxLayout())
        c_gb4_lo.itemAt(0).addWidget(QLabel('Minimum'))
        self.par_min_le = QLineEdit()
        c_gb4_lo.itemAt(0).addWidget(self.par_min_le)
        c_gb4_lo.addLayout(QVBoxLayout())
        c_gb4_lo.itemAt(1).addWidget(QLabel('Maximum'))
        self.par_max_le = QLineEdit()
        c_gb4_lo.itemAt(1).addWidget(self.par_max_le)