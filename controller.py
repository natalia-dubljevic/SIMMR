from math import sqrt
import numpy as np

from gui import MainWindow

from scanner import Scanner
from coil import Coil
from lines import Straight, Curved
from segment import Segment
import sim_utils

import matplotlib.pyplot as plt

class Controller:

    def __init__(self, view : MainWindow):
        self.view = view
        self.coil_focus_index = None
        self.segment_focus_index = None
        self.editing = False
        self.user_inputs = []

        # Button Connections
        self.view.mouse_clicked_outside.connect(self.handle_mouse_clicked_outside)

        self.view.tl_w.init_scanner.init_scanner_btn_clicked.connect(self.handle_init_scanner_btn_clicked)
        self.view.tl_w.init_scanner.load_scanner_btn_clicked.connect(self.handle_mod_scanner_btn_clicked)

        self.view.tl_w.set_scanner.button_clicked.connect(self.handle_init_scanner_clicked)

        self.view.tl_w.coil_control.mod_scanner_clicked.connect(self.handle_mod_scanner_clicked)
        self.view.tl_w.coil_control.del_coil_clicked.connect(self.handle_del_coil_clicked)
        self.view.tl_w.coil_control.edit_coil_clicked.connect(self.handle_edit_coil_clicked)
        self.view.tl_w.coil_control.add_coil_clicked.connect(self.handle_add_coil_clicked)

        self.view.tl_w.coil_control.coil_clicked.connect(self.update_coil_focus) 

        self.view.tl_w.coil_design.segment_clicked.connect(self.update_segment_focus) 

        self.view.tl_w.coil_design.back_clicked.connect(self.handle_back_clicked)

        self.view.tl_w.coil_design.delete_segment_clicked.connect(self.handle_delete_segment_clicked)
        self.view.tl_w.coil_design.edit_segment_clicked.connect(self.handle_edit_segment_clicked)
        self.view.tl_w.coil_design.add_segment_clicked.connect(self.handle_add_segment_clicked)

        self.view.tl_w.coil_design.straight_seg_clicked.connect(self.handle_straight_seg_clicked)
        self.view.tl_w.coil_design.curved_seg_clicked.connect(self.handle_curved_seg_clicked)

        self.view.tl_w.coil_design.cancel_seg_clicked.connect(self.handle_cancel_seg_clicked)
        self.view.tl_w.coil_design.confirm_seg_clicked.connect(self.handle_confirm_seg_clicked)
        #===================

    def handle_mouse_clicked_outside(self):
        if self.view.tl_w.stack.currentIndex() == 2:
            self.view.tl_w.coil_control.remove_highlight(self.coil_focus_index)
            self.update_coil_focus(None)
        elif self.view.tl_w.stack.currentIndex() == 3:
            self.view.tl_w.coil_design.remove_highlight(self.segment_focus_index)
            self.update_segment_focus(None)

    def handle_init_scanner_btn_clicked(self):
        self.view.tl_w.stack.setCurrentIndex(1)

    def handle_mod_scanner_btn_clicked(self):
        print('Connected to load scanner button')
        # Needs implementation

    def handle_init_scanner_clicked(self, bbox : list, vol_res : list):
        self.scanner = Scanner(bbox, vol_res)

        self.update_coil_control()

        self.show_scanner_plot()

        self.disable_coil_ed()

        self.view.tl_w.stack.setCurrentIndex(2)

    def handle_mod_scanner_clicked(self):
        self.view.tl_w.stack.setCurrentIndex(1)

    def handle_del_coil_clicked(self):
        del self.scanner.coils[self.coil_focus_index]
        self.update_coil_focus(None)
        self.update_coil_control()

    def handle_edit_coil_clicked(self):

        self.view.tl_w.coil_design.del_seg_btn.setDisabled(True)
        self.view.tl_w.coil_design.edit_seg_btn.setDisabled(True)
        self.view.tl_w.coil_design.seg_edit_gb.setDisabled(True)

        self.update_coil_focus(self.coil_focus_index) # Sets the focus index
        self.update_coil_design()
        self.view.tl_w.stack.setCurrentIndex(3)

    def handle_add_coil_clicked(self):
        self.view.tl_w.coil_design.del_seg_btn.setDisabled(True)
        self.view.tl_w.coil_design.edit_seg_btn.setDisabled(True)
        self.view.tl_w.coil_design.seg_edit_gb.setDisabled(True)

        self.scanner.add_coils(Coil()) # Adds a coil without any segments
        self.update_coil_focus(len(self.scanner.coils) - 1) # Sets the focus index to be the last
        self.update_coil_design()
        self.view.tl_w.stack.setCurrentIndex(3)

    def handle_back_clicked(self):
        self.update_coil_control()
        self.update_coil_focus(None)
        self.view.tl_w.stack.setCurrentIndex(2)

    def handle_delete_segment_clicked(self):
        # NEW ADDITION:
        del self.user_inputs[self.coil_focus_index][self.segment_focus_index]
        self.user_inputs[self.coil_focus_index].append(None)
        # END NEW ADDITION:
        del self.scanner.coils[self.coil_focus_index].segments[self.segment_focus_index]
        self.update_segment_focus(None)
        self.update_coil_design()

    def handle_edit_segment_clicked(self):
        self.editing = True

        if len(self.user_inputs[self.coil_focus_index][self.segment_focus_index]) == 6: # Segment being loaded is straight
            self.view.tl_w.coil_design.switch_to_straight()
        elif len(self.user_inputs[self.coil_focus_index][self.segment_focus_index]) == 13: 
            self.view.tl_w.coil_design.switch_to_curved()

        self.view.tl_w.coil_design.show_segment_inputs(self.user_inputs[self.coil_focus_index][self.segment_focus_index])
        self.view.tl_w.coil_design.seg_edit_gb.setDisabled(False)

    def handle_add_segment_clicked(self):
        self.editing = False

        self.view.tl_w.coil_design.clear_all_text()
        self.view.tl_w.coil_design.seg_edit_gb.setDisabled(False)

    def handle_straight_seg_clicked(self):
        self.view.tl_w.coil_design.switch_to_straight()

    def handle_curved_seg_clicked(self):
        self.view.tl_w.coil_design.switch_to_curved()

    def handle_cancel_seg_clicked(self):
        self.view.tl_w.coil_design.clear_all_text()
        self.editing = False

        self.view.tl_w.coil_design.seg_edit_gb.setDisabled(True)
        self.view.tl_w.coil_design.add_seg_btn.setChecked(False)
        self.update_segment_focus(None)

    def handle_confirm_seg_clicked(self, seg : list):

        if self.editing == False:
            # Storing input values
            if len(self.user_inputs) <= self.coil_focus_index:
                self.user_inputs.append([seg])
            else:
                self.user_inputs[self.coil_focus_index].append(seg)

            if len(seg) == 6: # Straight Segment
                line = Straight(seg[0], seg[1], seg[2], seg[3] - seg[0], seg[4] - seg[1], seg[5] - seg[2])

                self.scanner.coils[self.coil_focus_index].add_segment(Segment(line, 0, 1)) # Add segment

            elif len(seg) == 13: # Curved Segment
                c_x, c_y, c_z = seg[0], seg[1], seg[2]
                r1_x, r1_y, r1_z, r1_mag = seg[3], seg[4], seg[5], seg[6]
                r2_x, r2_y, r2_z, r2_mag = seg[7], seg[8], seg[9], seg[10]
                p_min, p_max = seg[11], seg[12]
                r1_norm = sqrt(r1_x ** 2 + r1_y ** 2 + r1_z **2)
                r2_norm = sqrt(r2_x ** 2 + r2_y ** 2 + r2_z **2)
                r1_mult = r1_norm * r1_mag
                r2_mult = r2_norm * r2_mag
                r1_x, r1_y, r1_z = r1_mult * r1_x, r1_mult * r1_y, r1_mult * r1_z
                r2_x, r2_y, r2_z = r2_mult * r2_x, r2_mult * r2_y, r2_mult * r2_z
                line = Curved(c_x, c_y, c_z, r1_x, r1_y, r1_z, r2_x, r2_y, r2_z)
            
                self.scanner.coils[self.coil_focus_index].add_segment(Segment(line, p_min * np.pi, p_max * np.pi)) # Add segment

            else: # Should never happen if controller works (i.e., passed list is not of length 6 or 13)
                raise ValueError('Incompatible list size passed for segment creation')
            
        else: # Modifying a previously creating segment (i.e., editing a segment)
             # Storing input values
            self.user_inputs[self.coil_focus_index][self.segment_focus_index] = seg

            if len(seg) == 6: # Straight Segment
                line = Straight(seg[0], seg[1], seg[2], seg[3] - seg[0], seg[4] - seg[1], seg[5] - seg[2])

                self.scanner.coils[self.coil_focus_index].segments[self.segment_focus_index] = (Segment(line, 0, 1)) # Add segment

            elif len(seg) == 13: # Curved Segment
                c_x, c_y, c_z = seg[0], seg[1], seg[2]
                r1_x, r1_y, r1_z, r1_mag = seg[3], seg[4], seg[5], seg[6]
                r2_x, r2_y, r2_z, r2_mag = seg[7], seg[8], seg[9], seg[10]
                p_min, p_max = seg[11], seg[12]
                r1_norm = sqrt(r1_x ** 2 + r1_y ** 2 + r1_z **2)
                r2_norm = sqrt(r2_x ** 2 + r2_y ** 2 + r2_z **2)
                r1_mult = r1_norm * r1_mag
                r2_mult = r2_norm * r2_mag
                r1_x, r1_y, r1_z = r1_mult * r1_x, r1_mult * r1_y, r1_mult * r1_z
                r2_x, r2_y, r2_z = r2_mult * r2_x, r2_mult * r2_y, r2_mult * r2_z
                line = Curved(c_x, c_y, c_z, r1_x, r1_y, r1_z, r2_x, r2_y, r2_z)
            
                self.scanner.coils[self.coil_focus_index].segments[self.segment_focus_index] = (Segment(line, p_min * np.pi, p_max * np.pi)) # Add segment

            else: # Should never happen if controller works (i.e., passed list is not of length 6 or 13)
                raise ValueError('Incompatible list size passed for segment creation')  

            self.editing = False         

        self.view.tl_w.coil_design.seg_edit_gb.setDisabled(True)
        self.view.tl_w.coil_design.add_seg_btn.setChecked(False)

        self.update_coil_design()

    def show_fields_plot(self):
        pass

    def show_mag_phase_plot(self):
        pass

    def update_coil_control(self):
        self.update_coil_scroll()
        self.show_scanner_plot()

    def update_coil_scroll(self):
        seg_n_list = []
        for coil in self.scanner.coils:
            seg_n_list.append(len(coil.segments))

        self.view.tl_w.coil_control.update_coils(seg_n_list)

    def show_scanner_plot(self):
        self.view.tr_w.figure.clf()

        ax = self.view.tr_w.figure.add_subplot(111, projection='3d')
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        ax.set_zlabel("$z$")

        for coil in self.scanner.coils:
            coil.plot_coil(ax)
        
        self.view.tr_w.canvas.draw()

    def update_coil_design(self):
        self.update_segment_scroll()
        self.show_coil_plot()
        self.view.tl_w.coil_design.clear_all_text()

    def update_segment_scroll(self):
        fns = []
        low_lims = []
        up_lims = []
        for segment in self.scanner.coils[self.coil_focus_index].segments:
            if type(segment.line_fn) == Curved:
                fns.append('Curved')
            else:
                fns.append('Straight')
            low_lims.append(segment.low_lim)
            up_lims.append(segment.up_lim)
        
        self.view.tl_w.coil_design.update_segments(fns, low_lims, up_lims)
            
    def show_coil_plot(self):
        self.view.tr_w.figure.clf()

        ax = self.view.tr_w.figure.add_subplot(111, projection='3d')
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        ax.set_zlabel("$z$")

        self.scanner.coils[self.coil_focus_index].plot_coil(ax)
        
        self.view.tr_w.canvas.draw()        

    def update_coil_focus(self, index : int | None):
        self.view.tl_w.coil_control.remove_highlight(self.coil_focus_index)

        self.coil_focus_index = index

        if self.coil_focus_index == None:
            self.disable_coil_ed()
        else:
            self.enable_coil_ed()
            self.view.tl_w.coil_control.highlight_selected(self.coil_focus_index)
            if len(self.scanner.coils[self.coil_focus_index].segments) >= 1:
                self.show_fields_plot()

    def enable_coil_ed(self):
        self.view.tl_w.coil_control.del_coil_btn.setDisabled(False)
        self.view.tl_w.coil_control.edit_coil_btn.setDisabled(False)

    def disable_coil_ed(self):
        self.view.tl_w.coil_control.del_coil_btn.setDisabled(True)
        self.view.tl_w.coil_control.edit_coil_btn.setDisabled(True)

    def update_segment_focus(self, index : int | None):
        self.view.tl_w.coil_design.remove_highlight(self.segment_focus_index)

        self.segment_focus_index = index

        if self.segment_focus_index == None:
            self.disable_segment_ed()
        else:
            self.enable_segment_ed()
            self.view.tl_w.coil_design.highlight_selected(self.segment_focus_index)

    def enable_segment_ed(self):
        self.view.tl_w.coil_design.del_seg_btn.setDisabled(False)
        self.view.tl_w.coil_design.edit_seg_btn.setDisabled(False)

    def disable_segment_ed(self):
        self.view.tl_w.coil_design.del_seg_btn.setDisabled(True)
        self.view.tl_w.coil_design.edit_seg_btn.setDisabled(True)

