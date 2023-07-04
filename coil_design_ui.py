from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QStackedWidget, QDialog
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDoubleValidator

class CoilDesignUI(QWidget):

    back_clicked = pyqtSignal()

    delete_segment_clicked = pyqtSignal()
    edit_segment_clicked = pyqtSignal()
    add_segment_clicked = pyqtSignal()

    straight_seg_clicked = pyqtSignal()
    curved_seg_clicked = pyqtSignal()

    cancel_seg_clicked = pyqtSignal()
    confirm_seg_clicked = pyqtSignal(list)

    segment_clicked = pyqtSignal(int)

    class SelectableSegmentWidget(QWidget):
        def __init__(self, outer, index : int, type : str, low_lim : float, up_lim : float):
            super().__init__()

            self.outer = outer

            self.ref_index = index

            self.lo = QHBoxLayout()
            self.setLayout(self.lo)

            coil_label = 'Segment ' + str(index + 1)
            self.lo.addWidget(QLabel(coil_label))

            function_label = 'Type: ' + type
            self.lo.addWidget(QLabel(function_label))

            low_lim_label = 'Lower Limit: ' + str(low_lim)
            self.lo.addWidget(QLabel(low_lim_label))

            up_lim_label = 'Upper Limit: ' + str(up_lim)
            self.lo.addWidget(QLabel(up_lim_label))

            self.setStyleSheet('border : 5px solid black')
            self.setStyleSheet('background : yellow')

        def mousePressEvent(self, event):
            self.outer.segment_clicked.emit(self.ref_index)


    def __init__(self):
        super().__init__()

        self.lo = QVBoxLayout()
        self.setLayout(self.lo)

        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.back_clicked)
        self.lo.addWidget(self.back_button)


        # GroupBox containing coil segment overview
        self.coil_seg_gb = QGroupBox('Coil Segments')
        self.lo.addWidget(self.coil_seg_gb)
        self.coil_seg_lo = QVBoxLayout()
        self.coil_seg_gb.setLayout(self.coil_seg_lo)

        # Scroll area for segment overview area (inisde coil_seg_gb)
        self.coil_seg_sa = QScrollArea()
        self.coil_seg_lo.addWidget(self.coil_seg_sa)
        self.coil_seg_sa_w = QWidget()
        self.coil_seg_sa_w_lo = QVBoxLayout()
        self.coil_seg_sa_w.setLayout(self.coil_seg_sa_w_lo)

        # Buttons areas
        coil_seg_btns_lo = QHBoxLayout()
        self.coil_seg_lo.addLayout(coil_seg_btns_lo)
        self.del_seg_btn = QPushButton('Delete Segment')
        self.del_seg_btn.clicked.connect(self.delete_segment_clicked)
        self.edit_seg_btn = QPushButton('Edit Segment')
        self.edit_seg_btn.clicked.connect(self.edit_segment_clicked)
        self.add_seg_btn = QPushButton('Add Segment')
        self.add_seg_btn.setCheckable(True)
        self.add_seg_btn.clicked.connect(self.add_segment_clicked)
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
        self.seg_edit_straight.setChecked(True)
        self.seg_edit_curved = QPushButton('Curved Segment')
        self.seg_edit_curved.clicked.connect(self.curved_seg_clicked)
        self.seg_edit_curved.setCheckable(True)
        seg_edit_gb_lo.addWidget(self.seg_edit_straight)
        seg_edit_gb_lo.addWidget(self.seg_edit_curved)


        self.seg_edit_stack = QStackedWidget()
        seg_edit_lo.addWidget(self.seg_edit_stack)

        self.straight_seg_editor = StraightSegmentEditor()
        self.curved_seg_editor = CurvedSegmentEditor()

        self.seg_edit_stack.addWidget(self.straight_seg_editor)
        self.seg_edit_stack.addWidget(self.curved_seg_editor)

        # self.seg_edit_stack.hide()

        btns_row_lo = QHBoxLayout()
        self.cancel_seg_btn = QPushButton('Cancel')
        self.cancel_seg_btn.clicked.connect(self.cancel_seg_clicked)
        self.confirm_seg_btn = QPushButton('Confirm')
        self.confirm_seg_btn.clicked.connect(self.confirm_segment_pressed)
        btns_row_lo.addWidget(self.cancel_seg_btn)
        btns_row_lo.addWidget(self.confirm_seg_btn)
        seg_edit_lo.addLayout(btns_row_lo)

        # self.seg_edit_gb.setDisabled(True)

    def parse_segment(self):
        if self.seg_edit_straight.isChecked() == True:
            return [
                float(self.straight_seg_editor.init_point_x_le.text()),
                float(self.straight_seg_editor.init_point_y_le.text()),
                float(self.straight_seg_editor.init_point_z_le.text()),
                float(self.straight_seg_editor.end_point_x_le.text()),
                float(self.straight_seg_editor.end_point_y_le.text()),
                float(self.straight_seg_editor.end_point_z_le.text())
            ]
        elif self.seg_edit_curved.isChecked() == True:
            return [
                float(self.curved_seg_editor.ctr_x_le.text()),
                float(self.curved_seg_editor.ctr_y_le.text()),
                float(self.curved_seg_editor.ctr_z_le.text()),
                float(self.curved_seg_editor.r1_x_comp_le.text()),
                float(self.curved_seg_editor.r1_y_comp_le.text()),
                float(self.curved_seg_editor.r1_z_comp_le.text()),
                float(self.curved_seg_editor.r1_mag_le.text()),
                float(self.curved_seg_editor.r2_x_comp_le.text()),
                float(self.curved_seg_editor.r2_y_comp_le.text()),
                float(self.curved_seg_editor.r2_z_comp_le.text()),
                float(self.curved_seg_editor.r2_mag_le.text()),
                float(self.curved_seg_editor.par_min_le.text()),
                float(self.curved_seg_editor.par_max_le.text())
            ]

        return False # If input is not valid
    
    def show_segment_inputs(self, inputs : list):
        if self.seg_edit_straight.isChecked() == True:
            self.straight_seg_editor.fill_text_prompts(inputs)
        elif self.seg_edit_curved.isChecked() == True:
            self.curved_seg_editor.fill_text_prompts(inputs)

        return False # If input is not valid
    
    def clear_all_text(self):
        self.straight_seg_editor.clear_text_prompts()
        self.curved_seg_editor.clear_text_prompts()

    def confirm_segment_pressed(self):
        if (self.seg_edit_straight.isChecked() and self.straight_seg_editor.input_is_valid()
            or self.seg_edit_curved.isChecked() and self.curved_seg_editor.input_is_valid()):
            # Input should be valid
            self.confirm_seg_clicked.emit(self.parse_segment())

            self.clear_all_text()

    def update_segments(self, fns : list, low_lims : list, up_lims : list):

        replacement_widget = QWidget()
        replacement_lo = QVBoxLayout()
        replacement_widget.setLayout(replacement_lo)

        for i in range(0, len(fns)):
            replacement_lo.addWidget(self.SelectableSegmentWidget(self, i, fns[i], low_lims[i], up_lims[i]))

        self.coil_seg_sa_w = replacement_widget
        self.coil_seg_sa.setWidget(self.coil_seg_sa_w)

    def highlight_selected(self, index : int):
        if index != None and self.coil_seg_sa_w.layout().itemAt(index) != None:
            self.coil_seg_sa_w.layout().itemAt(index).widget().setStyleSheet('background : cyan')

    def remove_highlight(self, index : int):
        if index != None and self.coil_seg_sa_w.layout().itemAt(index) != None:
            self.coil_seg_sa_w.layout().itemAt(index).widget().setStyleSheet('background : yellow')

    def switch_to_straight(self):
        if not self.seg_edit_straight.isChecked():
            self.seg_edit_straight.setChecked(True)
        self.seg_edit_curved.setChecked(False)
        self.seg_edit_stack.setCurrentIndex(0)  
        self.seg_edit_stack.show()

    def switch_to_curved(self):
        if not self.seg_edit_curved.isChecked():
            self.seg_edit_curved.setChecked(True)
        self.seg_edit_straight.setChecked(False) 
        self.seg_edit_stack.setCurrentIndex(1) 
        self.seg_edit_stack.show()
            
                
class StraightSegmentEditor(QWidget):

    def __init__(self):
        super().__init__()

        self.lo = QVBoxLayout()
        self.setLayout(self.lo)

        s_gb1 = QGroupBox('Start Point')
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

        s_gb2 = QGroupBox('End Point')
        self.layout().addWidget(s_gb2)
        s_gb2.setLayout(QHBoxLayout())
        s_gb2.layout().addLayout(QVBoxLayout())
        s_gb2.layout().itemAt(0).addWidget(QLabel('X-Coordinate'))
        self.end_point_x_le = QLineEdit()
        s_gb2.layout().itemAt(0).addWidget(self.end_point_x_le)
        s_gb2.layout().addLayout(QVBoxLayout())
        s_gb2.layout().itemAt(1).addWidget(QLabel('Y-Coordinate'))
        self.end_point_y_le = QLineEdit()
        s_gb2.layout().itemAt(1).addWidget(self.end_point_y_le)
        s_gb2.layout().addLayout(QVBoxLayout())
        s_gb2.layout().itemAt(2).addWidget(QLabel('Z-Coordinate'))
        self.end_point_z_le = QLineEdit()
        s_gb2.layout().itemAt(2).addWidget(self.end_point_z_le)

        self.text_prompts = [self.init_point_x_le, self.init_point_y_le, self.init_point_z_le,
                             self.end_point_x_le, self.end_point_y_le, self.end_point_z_le]
        
    def clear_text_prompts(self):
        for text in self.text_prompts:
            text.clear()

    def fill_text_prompts(self, inputs : list):
        if len(self.text_prompts) == len(inputs): # Double check list size correct
            for i in range(len(inputs)):
                self.text_prompts[i].setText(str(inputs[i]))
        else: # Should never happen if controller works
            raise ValueError('Incorrect list size for given text prompts')

    def input_is_valid(self):
        if (self.init_point_x_le.hasAcceptableInput()
            and self.init_point_y_le.hasAcceptableInput()
            and self.init_point_z_le.hasAcceptableInput()
            and self.end_point_x_le.hasAcceptableInput()
            and self.end_point_y_le.hasAcceptableInput()
            and self.end_point_z_le.hasAcceptableInput()):
            return True
        else:
            return False

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


        c_gb2 = QGroupBox('First Radius')
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
        c_gb2_lo.addLayout(QVBoxLayout())
        c_gb2_lo.itemAt(3).addWidget(QLabel('Magnitude'))
        self.r1_mag_le = QLineEdit()
        c_gb2_lo.itemAt(3).addWidget(self.r1_mag_le)


        c_gb3 = QGroupBox('Second Radius')
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
        c_gb3_lo.addLayout(QVBoxLayout())
        c_gb3_lo.itemAt(3).addWidget(QLabel('Magnitude'))
        self.r2_mag_le = QLineEdit()
        c_gb3_lo.itemAt(3).addWidget(self.r2_mag_le)

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

        self.text_prompts = [self.ctr_x_le, self.ctr_y_le, self.ctr_z_le,
                             self.r1_x_comp_le, self.r1_y_comp_le, self.r1_z_comp_le, self.r1_mag_le,
                             self.r2_x_comp_le, self.r2_y_comp_le, self.r2_z_comp_le, self.r2_mag_le,
                             self.par_min_le, self.par_max_le]
        
    def clear_text_prompts(self):
        for text in self.text_prompts:
            text.clear()

    def fill_text_prompts(self, inputs : list):
        if len(self.text_prompts) == len(inputs): # Double check list size correct
            for i in range(len(inputs)):
                self.text_prompts[i].setText(str(inputs[i]))
        else: # Should never happen if controller works
            raise ValueError('Incorrect list size for given text prompts')

    def input_is_valid(self):
        if (self.ctr_x_le.hasAcceptableInput()
            and self.ctr_y_le.hasAcceptableInput()
            and self.ctr_z_le.hasAcceptableInput()
            and self.r1_x_comp_le.hasAcceptableInput()
            and self.r1_y_comp_le.hasAcceptableInput()
            and self.r1_z_comp_le.hasAcceptableInput()
            and self.r1_mag_le.hasAcceptableInput()
            and self.r2_x_comp_le.hasAcceptableInput()
            and self.r2_y_comp_le.hasAcceptableInput()
            and self.r2_z_comp_le.hasAcceptableInput()
            and self.r2_mag_le.hasAcceptableInput()
            and self.par_min_le.hasAcceptableInput()
            and self.par_max_le.hasAcceptableInput()):
            return True
        else:
            return False