from math import sqrt
import numpy as np
import json

from gui import MainWindow

from scanner import Scanner
from coil import Coil
from lines import Straight, Curved
from segment import Segment
from encoder import CustomEncoder
import sim_utils

import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Polygon
from mpl_toolkits.axes_grid1 import make_axes_locatable
from PyQt5.QtCore import QThread
from PyQt5 import QtGui

class exportVolThread(QThread):
    def __init__(self, export_file, scanner, controller):
        QThread.__init__(self)
        self.controller = controller # FIXME
        self.controller.scanner
        self.scanner = scanner
        self.export_file = export_file

    def get_seg_B(self):
        tmp = []
        for i in range(0, len(self.scanner.coils)):
            for segment in self.scanner.coils[i].segments:
                segment.seg_B = segment.calc_seg_B(self.scanner.get_bbox())
            self.scanner.coils[i].update_mag_vol()
            B_field = self.scanner.coils[i].B_vol
            B_complex = B_field[0, :, :, :] - 1j * B_field[1, :, :, :]  
            print(B_complex)
            tmp.append(B_complex)
        print(tmp)
        export_array = np.array(tmp)
        print(export_array)
        np.save(self.export_file, export_array) 

    def run(self):
        self.get_seg_B()
        self.controller.enable_export_btn()

    

class Controller:

    def __init__(self, view : MainWindow):
        self.view = view
        self.scanner = None
        self.coil_focus_index = None
        self.segment_focus_index = None
        self.editing = False
        self.user_inputs = []
        self.file = None
        self.slice = self.view.tr_w.slice_combo_btn.currentText()
        self.num_slices = None
        self.slice_loc = 1
        self.slice_B_vol = None

        self.view.save_clicked.triggered.connect(self.save_menu_clicked)

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

        self.view.tr_w.slice_combo_btn.currentTextChanged.connect(self.slice_button_changed)
        self.view.tr_w.slice_loc_modified_signal.connect(self.handle_slice_loc_changed)
        self.view.tr_w.export_btn_clicked.connect(self.handle_export_btn_clicked)
        #===================

    def slice_button_changed(self):
        '''
        Handles the modification of the slice selected
        '''

        self.slice = self.view.tr_w.slice_combo_btn.currentText()
        self.update_num_slices()
        if self.slice_loc > self.num_slices:
            self.update_selected_slice(1)

        if self.view.tl_w.stack.currentIndex() == 2:
            self.show_scanner_plot()
        elif self.view.tl_w.stack.currentIndex() == 3:
            self.show_coil_plot()

        if len(self.scanner.coils) != 0:
            self.update_B_vol_slice()

        if self.coil_focus_index != None and len(self.scanner.get_coils(self.coil_focus_index).segments) != 0:
            self.show_bottom_plots()

    def update_num_slices(self):
        '''
        Updates self.num_slices (a 'Controller' property) to reflect the current number of slices

        1. Checks that self.scanner is not None, and print to console if it is (without proceeding further)
        2. Match self.slice to cases 'x', 'y', or 'z'
        3. Update the number of slices in accordance with the scanner bounding box and self.slice
        '''

        if self.scanner != None:
            match self.slice:
                case 'x':
                    self.num_slices = np.arange(self.scanner.get_bbox()[0], self.scanner.get_bbox()[1], self.scanner.get_vol_res()[0]).size
                case 'y':
                    self.num_slices = np.arange(self.scanner.get_bbox()[2], self.scanner.get_bbox()[3], self.scanner.get_vol_res()[1]).size
                case 'z':
                    self.num_slices = np.arange(self.scanner.get_bbox()[4], self.scanner.get_bbox()[5], self.scanner.get_vol_res()[2]).size
            self.update_slice_lbl()
        else:
            print('Controller does not have a instantiated self.scanner property')

    def update_slice_lbl(self):
        '''
        Updates the slice range available for display
        '''

        self.view.tr_w.set_slice_loc_label(1, self.num_slices)

    def handle_slice_loc_changed(self, slice_req):
        '''
        Handles the modification of slice location by the user
        '''
        if slice_req >= 1 and slice_req <= self.num_slices:
            self.update_selected_slice(slice_req)
        else:
            self.update_selected_slice(self.slice_loc)
            self.view.error_poput('Slice Number Error', 'Invalid slice entered (' + str(slice_req) + '). Enter slice within range listed')

    def update_B_vol_slice(self):
        '''
        Update self.B_vol_slice to reflect current slice

        1. Logic: Matches self.slice to 'x', 'y', or 'z' and creates LV slice_volume according to slice, scanner bounding box,
        and scanner volume resolution
        2. Logic: Creates LV B_fields_slice; iteratively calls Segment.calc_seg_B using the defined slice volume and sums all
        arrays returned during this iterative calling to update self.slice_B_vol to reflect current selection and slice
        '''

        match self.slice:
                case 'x':
                    slice_range = np.arange(self.scanner.get_bbox()[0], self.scanner.get_bbox()[1], self.scanner.get_vol_res()[0])
                    x = slice_range[self.slice_loc - 1]
                    y_min = self.scanner.get_bbox()[2]
                    y_max = self.scanner.get_bbox()[3]
                    z_min = self.scanner.get_bbox()[4]
                    z_max = self.scanner.get_bbox()[5]
                    slice_volume = [x, x, y_min, y_max, z_min, z_max]
                case 'y':
                    slice_range = np.arange(self.scanner.get_bbox()[2], self.scanner.get_bbox()[3], self.scanner.get_vol_res()[1])
                    y = slice_range[self.slice_loc - 1]
                    x_min = self.scanner.get_bbox()[0]
                    x_max = self.scanner.get_bbox()[1]
                    z_min = self.scanner.get_bbox()[4]
                    z_max = self.scanner.get_bbox()[5]
                    slice_volume = [x_min, x_max, y, y, z_min, z_max]
                case 'z':
                    slice_range = np.arange(self.scanner.get_bbox()[4], self.scanner.get_bbox()[5], self.scanner.get_vol_res()[2])
                    z = slice_range[self.slice_loc - 1]
                    x_min = self.scanner.get_bbox()[0]
                    x_max = self.scanner.get_bbox()[1]
                    y_min = self.scanner.get_bbox()[2]
                    y_max = self.scanner.get_bbox()[3]
                    slice_volume = [x_min, x_max, y_min, y_max, z, z]

        B_fields_slice = []

        for segment in self.scanner.get_coils(self.coil_focus_index).segments:
            B_fields_slice.append(segment.calc_seg_B(slice_volume))

        self.slice_B_vol = sum(B_fields_slice)

    def update_selected_slice(self, slice_req):
        '''
        General update for the selected slice
        '''
        self.slice_loc = slice_req
        self.view.tr_w.slice_loc_btn.setText(str(self.slice_loc))
        if self.view.tl_w.stack.currentIndex() == 2:
            self.show_scanner_plot()
        elif self.view.tl_w.stack.currentIndex() == 3:
            self.show_coil_plot()

        if len(self.scanner.coils) != 0:
            self.update_B_vol_slice()

        if self.coil_focus_index != None:
            self.show_bottom_plots()

    def done(self):
        """
        Show the message that fetching posts is done.
        Disable Stop button, enable the Start one and reset progress bar to 0
        """
        QtGui.QMessageBox.information(self, "Done!", "Done calculating sensitivity maps!")

    def enable_export_btn(self):
        self.view.tr_w.export_btn.setEnabled(True)

    def handle_export_btn_clicked(self):
        '''
        Handles the exporting of the final sensitivity profiles
        '''
        try:
            export_file = self.view.save_file_dialog()
            self.view.thread = exportVolThread(export_file, self.scanner, self)
            #self.view.connect(self.get_thread.quit, self.done)
            self.view.tr_w.export_btn.setEnabled(False)
            self.view.thread.start()
            #tmp = []
            #for i in range(0, len(self.scanner.coils)):
            #    # B_field = self.scanner.coils[i].B_vol
            #    for segment in self.scanner.coils[i].segments:
            #        segment.seg_B = segment.calc_seg_B(self.scanner.get_bbox())
            #    self.scanner.coils[i].update_mag_vol()
            #    B_field = self.scanner.coils[i].B_vol
            #    B_complex = B_field[0, :, :, :] - 1j * B_field[1, :, :, :]  
            #    print(B_complex)
            #    tmp.append(B_complex)
            #print(tmp)
            #export_array = np.array(tmp)
            #print(export_array)
            #np.save(export_file, export_array) 
        except Exception as e:
            print('Error exporting sensitivity maps')
            print(e)
            self.view.error_poput('Error', 'Error exporting sensitivity maps')

    def save_menu_clicked(self):
        '''
        Handles the user clicking 'Save'
        '''
        self.save_workspace()

    def handle_mouse_clicked_outside(self):
        '''
        Handles the user clicking outside of the focus area (the scroll pane)

        Used to reset coil/segment focus
        '''
        if self.view.tl_w.stack.currentIndex() == 2:
            self.view.tl_w.coil_control.remove_highlight(self.coil_focus_index)
            self.update_coil_focus(None)
        elif self.view.tl_w.stack.currentIndex() == 3:
            self.view.tl_w.coil_design.remove_highlight(self.segment_focus_index)
            self.update_segment_focus(None)

    def handle_init_scanner_btn_clicked(self):
        self.view.tl_w.stack.setCurrentIndex(1)

    def handle_mod_scanner_btn_clicked(self):
        if self.load_workspace():
            self.update_coil_control()

            self.show_scanner_plot()

            self.disable_coil_ed()

            self.view.tl_w.stack.setCurrentIndex(2)

    def handle_init_scanner_clicked(self, bbox : list, vol_res : list):
        '''
        Handles the (valid) pressing of 'Initialize Scanner'

        1. Initializes the Controller's 'Scanner' object using the passed parameters
        2. Updates the number of slices according to the given bbox
        3. Updates the coil_control widget accordingly
        4. Disables the edit/delete options (i.e., buttons) in the coil overview pans
        5. Sets the GUI to view the coil overview pane in the top left widget

        Parameters
        ----------
        bbox : list
            The parsed bbox values from the GUI
        vol_res : list
            The parsed vol_res values from the GUI
        '''
        self.scanner = Scanner(bbox, vol_res)
        self.update_num_slices()
        self.update_coil_control()
        self.show_scanner_plot()
        self.disable_coil_ed()
        self.view.tl_w.stack.setCurrentIndex(2)

    def handle_mod_scanner_clicked(self):
        self.view.tl_w.stack.setCurrentIndex(1)

    def handle_del_coil_clicked(self):
        '''
        Handles the user's choice to delete a coil

        1. Deletes the corresponding index's coil
        2. Updates the focus index to None
        3. Updates the coil control pane
        '''

        del self.scanner.coils[self.coil_focus_index]
        self.update_coil_focus(None)
        self.update_coil_control()

    def handle_edit_coil_clicked(self):
        '''
        Handles the user selecting to 'Edit' an already created coil

        1. Logic: Updates 
        2. GUI: Pane preparation - disables segment editing and segment editing panel
        '''

        # self.update_coil_focus(self.coil_focus_index) # Sets the focus index
        # self.update_num_slices()

        self.disable_segment_ed()
        self.disable_seg_edit()
        # self.view.tl_w.coil_design.del_seg_btn.setDisabled(True)
        # self.view.tl_w.coil_design.edit_seg_btn.setDisabled(True)
        # self.view.tl_w.coil_design.seg_edit_gb.setDisabled(True)
        self.update_coil_design()
        self.view.tl_w.stack.setCurrentIndex(3)

    def handle_add_coil_clicked(self):
        '''
        Handles a user pressing the 'Add Coil' button in the coil control pane

        1. Logic: Adds a new coil to the scanner object without any segments; updates the coil
        focus (index) to the newly created coil; appropriately updates the segment focus to None
        2. GUI: Prepares 'Coil Design' pane by disabling the 'Edit' and 'Delete' segment buttons;
        disabling the segment editing widget; updates the the design pane; and sets the in-view
        '''

        self.scanner.add_coils(Coil(scanner = self.scanner)) # Adds a coil without any segments
        self.update_coil_focus(len(self.scanner.coils) - 1) # Sets the focus index to be the last
        self.update_segment_focus(None)

        # self.view.tl_w.coil_design.del_seg_btn.setDisabled(True)
        # self.view.tl_w.coil_design.edit_seg_btn.setDisabled(True)
        self.disable_coil_ed()
        self.view.tl_w.coil_design.seg_edit_gb.setDisabled(True)
        # self.update_num_slices()
        self.update_coil_design()
        self.view.tl_w.stack.setCurrentIndex(3)

    def disable_seg_edit(self):
        '''
        Clears and disables the segment editor pane in the coil design panel
        '''

        self.view.tl_w.coil_design.clear_all_text()
        self.view.tl_w.coil_design.seg_edit_gb.setDisabled(True)

    def handle_back_clicked(self):
        self.update_coil_focus(None)
        self.update_coil_control()
        self.view.tl_w.stack.setCurrentIndex(2)

    def handle_delete_segment_clicked(self):
        del self.user_inputs[self.coil_focus_index][self.segment_focus_index]
        self.user_inputs[self.coil_focus_index].append(None)
        del self.scanner.coils[self.coil_focus_index].segments[self.segment_focus_index]
        self.update_segment_focus(None)
        self.update_coil_design()
        # Also need to update coil plots

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
        '''
        Handles the user's selection of 'Confirm' (either upon segment creation or segment editing)

        1. Checks self.editing to determine if a new segment is being created or if an old one is being edited 
        2. Stores the user's inputs (replacing if necessary)
        3. (Re)creates segment
        4. Updates B_vol_slice accordingly
        5. Updates the coil design pane
        '''


        if self.editing == False:
            # Storing input values
            if len(self.user_inputs) <= self.coil_focus_index:
                self.user_inputs.append([seg])
            else:
                self.user_inputs[self.coil_focus_index].append(seg)

            if len(seg) == 6: # Straight Segment
                line = Straight(seg[0], seg[1], seg[2], seg[3] - seg[0], seg[4] - seg[1], seg[5] - seg[2])

                self.scanner.coils[self.coil_focus_index].add_segment(Segment(line, 0, 1, self.scanner.get_coils(self.coil_focus_index))) # Add segment

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
            
                self.scanner.coils[self.coil_focus_index].add_segment(Segment(line, p_min * np.pi, p_max * np.pi, self.scanner.get_coils(self.coil_focus_index))) # Add segment

            else: # Should never happen if controller works (i.e., passed list is not of length 6 or 13)
                raise ValueError('Incompatible list size passed for segment creation')
            
        else: # Modifying a previously creating segment (i.e., editing a segment)
            # Storing input values
            self.user_inputs[self.coil_focus_index][self.segment_focus_index] = seg

            if len(seg) == 6: # Straight Segment
                line = Straight(seg[0], seg[1], seg[2], seg[3] - seg[0], seg[4] - seg[1], seg[5] - seg[2])

                self.scanner.coils[self.coil_focus_index].segments[self.segment_focus_index] = (Segment(line, 0, 1, self.scanner.get_coils(self.coil_focus_index))) # Add segment

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
            
                self.scanner.coils[self.coil_focus_index].segments[self.segment_focus_index] = (Segment(line, p_min * np.pi, p_max * np.pi, self.scanner.get_coils(self.coil_focus_index))) # Add segment

            else: # Should never happen if controller works (i.e., passed list is not of length 6 or 13)
                raise ValueError('Incompatible list size passed for segment creation')  
            
            # self.scanner.coils[self.coil_focus_index].B_vol = self.scanner.coils[self.coil_focus_index].B_volume()
            self.update_B_vol_slice()

            self.editing = False         

        self.view.tl_w.coil_design.seg_edit_gb.setDisabled(True)
        self.view.tl_w.coil_design.add_seg_btn.setChecked(False)

        self.update_coil_design()

    def show_fields_plot(self):
        '''
        Displays the magnetic field plots in the bottom left pane
        '''

        
        # if type(self.scanner.coils[self.coil_focus_index].B_vol_slice) != np.ndarray:
        #     print('can\'t show field plots; type not array')
        #     return

        if len(self.view.bl_w.figure.get_axes()) == 4:
            self.view.bl_w.figure.get_axes()[3].remove()

        # B_field = self.scanner.coils[self.coil_focus_index].B_vol_slice
        B_field = self.slice_B_vol


        Bx = B_field[0, :, :, :]
        print(Bx.shape)

        By = B_field[1, :, :, :]
        Bz = B_field[2, :, :, :]

        x_dim = np.arange(self.scanner.bbox[0], self.scanner.bbox[1] + 1e-10, self.scanner.vol_res[0])
        y_dim = np.arange(self.scanner.bbox[2], self.scanner.bbox[3] + 1e-10, self.scanner.vol_res[1])
        z_dim = np.arange(self.scanner.bbox[4], self.scanner.bbox[5] + 1e-10, self.scanner.vol_res[2])
        xv, yv, zv = np.meshgrid(x_dim, y_dim, z_dim, indexing='ij')

        Bx_slice = sim_utils.get_slice(Bx, self.slice, self.slice_loc, self.scanner.vol_res, self.scanner.bbox)
        By_slice = sim_utils.get_slice(By, self.slice, self.slice_loc, self.scanner.vol_res, self.scanner.bbox)
        Bz_slice = sim_utils.get_slice(Bz, self.slice, self.slice_loc, self.scanner.vol_res, self.scanner.bbox)

        if self.slice == 'x':
            ax1_label, ax2_label = 'y', 'z'
            ax2 = sim_utils.get_slice(yv, self.slice, self.slice_loc, self.scanner.vol_res, self.scanner.bbox)
            ax1 = sim_utils.get_slice(zv, self.slice, self.slice_loc, self.scanner.vol_res, self.scanner.bbox)
        elif self.slice == 'y':
            ax1_label, ax2_label = 'x', 'z'
            ax2 = sim_utils.get_slice(xv, self.slice, self.slice_loc, self.scanner.vol_res, self.scanner.bbox)
            ax1 = sim_utils.get_slice(zv, self.slice, self.slice_loc, self.scanner.vol_res, self.scanner.bbox)
        elif self.slice == 'z':
            ax1_label, ax2_label = 'x', 'y'
            ax2 = sim_utils.get_slice(xv, self.slice, self.slice_loc, self.scanner.vol_res, self.scanner.bbox)
            ax1 = sim_utils.get_slice(yv, self.slice, self.slice_loc, self.scanner.vol_res, self.scanner.bbox)

        vmin = min(np.min(Bx_slice), np.min(By_slice), np.min(Bz_slice))
        vmax = max(np.max(Bx_slice), np.max(By_slice), np.max(Bz_slice))
        print(vmin)
        print(vmax)
        if vmin == 0:
            norm = mpl.colors.Normalize(vmin = vmin, vmax = vmax)
        else:
            norm = mpl.colors.TwoSlopeNorm(vmin=vmin, vcenter=0., vmax=vmax)


        self.view.bl_w.axes[0].contourf(ax2, ax1, Bx_slice, levels=20, norm=norm, cmap='RdBu_r')
        self.view.bl_w.axes[0].set_title(r'$B_x$')
        self.view.bl_w.axes[0].set_xlabel(ax1_label + " (cm)")
        self.view.bl_w.axes[0].set_ylabel(ax2_label + " (cm)")
        self.view.bl_w.axes[0].set_aspect('equal')

        self.view.bl_w.axes[1].contourf(ax2, ax1, By_slice, levels=20, norm=norm, cmap='RdBu_r')
        self.view.bl_w.axes[1].set_title(r'$B_y$')
        self.view.bl_w.axes[1].set_xlabel(ax2_label+ " (cm)")
        self.view.bl_w.axes[1].set_ylabel(ax1_label + " (cm)")
        self.view.bl_w.axes[1].set_aspect('equal')

        self.view.bl_w.axes[2].contourf(ax2, ax1, Bz_slice, levels=20, norm=norm, cmap='RdBu_r')
        self.view.bl_w.axes[2].set_title(r'$B_z$')
        self.view.bl_w.axes[2].set_xlabel(ax1_label + " (cm)")
        self.view.bl_w.axes[2].set_ylabel(ax2_label + " (cm)")
        self.view.bl_w.axes[2].set_aspect('equal')

        cax = self.view.bl_w.figure.add_axes([self.view.bl_w.axes[2].get_position().x1 + 0.1, 
                                              self.view.bl_w.axes[2].get_position().y0, 0.02, 
                                              self.view.bl_w.axes[2].get_position().y1 - self.view.bl_w.axes[2].get_position().y0])
        plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap='RdBu_r'), cax=cax)
        
        self.view.bl_w.canvas.draw()

    def show_mag_phase_plot(self):
        '''
        Shows the magnitude and phase of the sensitivity maps in the bottom right pane
        '''

        # if type(self.scanner.coils[self.coil_focus_index].B_vol_slice) != np.ndarray:
        #     print('can\'t show mag phase plots; type not array')
        #     return

        for axes in self.view.br_w.axes:
            axes.clear()

        if len(self.view.br_w.figure.get_axes()) == 4:
            self.view.br_w.figure.get_axes()[2].remove()
            self.view.br_w.figure.get_axes()[2].remove()

        # B_field = self.scanner.coils[self.coil_focus_index].B_vol_slice
        B_field = self.slice_B_vol
        B_complex = B_field[0, :, :, :] - 1j * B_field[1, :, :, :]    

        x_dim = np.arange(self.scanner.bbox[0], self.scanner.bbox[1] + 1e-10, self.scanner.vol_res[0])
        y_dim = np.arange(self.scanner.bbox[2], self.scanner.bbox[3] + 1e-10, self.scanner.vol_res[1])
        z_dim = np.arange(self.scanner.bbox[4], self.scanner.bbox[5] + 1e-10, self.scanner.vol_res[2])
        xv, yv, zv = np.meshgrid(x_dim, y_dim, z_dim, indexing='ij')

        B_slice = sim_utils.get_slice(B_complex, self.slice, self.slice_loc, self.scanner.vol_res, self.scanner.bbox)
        B_mag = np.abs(B_slice)
        B_phase = np.angle(B_slice)

        if self.slice == 'x':
            ax1_label, ax2_label = 'y', 'z'
            ax2 = sim_utils.get_slice(yv, self.slice, self.slice_loc, self.scanner.vol_res, self.scanner.bbox)
            ax1 = sim_utils.get_slice(zv, self.slice, self.slice_loc, self.scanner.vol_res, self.scanner.bbox)
        elif self.slice == 'y':
            ax1_label, ax2_label = 'x', 'z'
            ax2 = sim_utils.get_slice(xv, self.slice, self.slice_loc, self.scanner.vol_res, self.scanner.bbox)
            ax1 = sim_utils.get_slice(zv, self.slice, self.slice_loc, self.scanner.vol_res, self.scanner.bbox)
        elif self.slice == 'z':
            ax1_label, ax2_label = 'x', 'y'
            ax2 = sim_utils.get_slice(xv, self.slice, self.slice_loc, self.scanner.vol_res, self.scanner.bbox)
            ax1 = sim_utils.get_slice(yv, self.slice, self.slice_loc, self.scanner.vol_res, self.scanner.bbox)

        divider1 = make_axes_locatable(self.view.br_w.figure.axes[0])
        cax1 = divider1.append_axes('right', size='5%', pad=0.05)
        divider2 = make_axes_locatable(self.view.br_w.figure.axes[1])
        cax2 = divider2.append_axes('right', size='5%', pad=0.05)

        im1 = self.view.br_w.figure.axes[0].contourf(ax2, ax1, B_mag, levels=20)
        self.view.br_w.figure.axes[0].set_title('Magnitude')
        self.view.br_w.figure.axes[0].set_xlabel(ax1_label + " (cm)")
        self.view.br_w.figure.axes[0].set_ylabel(ax2_label + " (cm)")
        self.view.br_w.figure.axes[0].set_aspect('equal')

        im2 = self.view.br_w.figure.axes[1].contourf(ax2, ax1, B_phase, levels=20)
        self.view.br_w.figure.axes[1].set_title('Phase')
        self.view.br_w.figure.axes[1].set_xlabel(ax1_label  + " (cm)")
        self.view.br_w.figure.axes[1].set_ylabel(ax2_label + " (cm)")
        self.view.br_w.figure.axes[1].set_aspect('equal')

        self.view.br_w.figure.colorbar(im1, cax=cax1, orientation='vertical')
        self.view.br_w.figure.colorbar(im2, cax=cax2, orientation='vertical') 

        self.view.br_w.canvas.draw()  

    def clear_bottom_plots(self):
        '''
        Clears the bottom plots on the GUI
        '''

        for ax in self.view.bl_w.figure.axes:
            ax.cla()
        self.view.bl_w.canvas.draw()
        for ax in self.view.br_w.axes:
            ax.cla()
        if len(self.view.br_w.figure.get_axes()) > 2:
            self.view.br_w.figure.get_axes()[2].clear()
            self.view.br_w.figure.get_axes()[3].clear()
        self.view.br_w.canvas.draw()

    def show_bottom_plots(self):
        self.clear_bottom_plots()
        self.show_fields_plot()
        self.show_mag_phase_plot()

    def update_coil_control(self):
        '''
        Updates the coil control widget in the GUI

        1. Updates the coil scroll bar according to the current scanner properties
        2. Displays the current scanner plot according to the current scanner properties
        '''
        self.update_coil_scroll()
        self.show_scanner_plot()

    def update_coil_scroll(self):
        '''
        Updates the coil scroll bar in the coil control widget as part of the GUI

        1. Instantiates a LV seg_n_list (a list)
        2. Appends to seg_n_list the number of segments in each of the scanner's coils iteratively 
        3. Calls the GUI coil control's method 'update_coils', with seg_n_list passed as a parameter:
            Replaces the 'current' (i.e., old) coil scroll panel with a newly built one reflecting 
            the current scanner parameters
        '''

        seg_n_list = []
        for coil in self.scanner.coils:
            seg_n_list.append(len(coil.segments))

        self.view.tl_w.coil_control.update_coils(seg_n_list)

    def show_scanner_plot(self):
        '''
        Displays (i.e., plots) the current 'Scanner' with all coils in the coil control pane of the GUI

        1. Clears the previously displayed plot (to prevent ghosting residue)
        2. Sets labels and view, and plots the bounding box within the frmae
        3. Plots the currently 'in-focus' slice within the bounding box plot
        4. Iteratively plots every coil within the scanner frame
        '''

        self.view.tr_w.ax.cla()
        self.view.tr_w.ax.set_xlabel("$x$")
        self.view.tr_w.ax.set_ylabel("$y$")
        self.view.tr_w.ax.set_zlabel("$z$")
        x_dif = self.scanner.get_bbox()[1] - self.scanner.get_bbox()[0]
        y_dif = self.scanner.get_bbox()[3] - self.scanner.get_bbox()[2]
        z_dif = self.scanner.get_bbox()[5] - self.scanner.get_bbox()[4]
        self.view.tr_w.ax.set_xlim(self.scanner.get_bbox()[0] - 0.25 * x_dif, self.scanner.get_bbox()[1] + 0.25 * x_dif)
        self.view.tr_w.ax.set_ylim(self.scanner.get_bbox()[2] - 0.25 * y_dif, self.scanner.get_bbox()[3] + 0.25 * y_dif)
        self.view.tr_w.ax.set_zlim(self.scanner.get_bbox()[4] - 0.25 * z_dif, self.scanner.get_bbox()[5] + 0.25 * z_dif)

        bbox_vertices = [
            (self.scanner.get_bbox()[0], self.scanner.get_bbox()[2], self.scanner.get_bbox()[4]),
            (self.scanner.get_bbox()[1], self.scanner.get_bbox()[2], self.scanner.get_bbox()[4]),
            (self.scanner.get_bbox()[0], self.scanner.get_bbox()[3], self.scanner.get_bbox()[4]),
            (self.scanner.get_bbox()[1], self.scanner.get_bbox()[3], self.scanner.get_bbox()[4]),
            (self.scanner.get_bbox()[0], self.scanner.get_bbox()[2], self.scanner.get_bbox()[5]),
            (self.scanner.get_bbox()[1], self.scanner.get_bbox()[2], self.scanner.get_bbox()[5]),
            (self.scanner.get_bbox()[0], self.scanner.get_bbox()[3], self.scanner.get_bbox()[5]),
            (self.scanner.get_bbox()[1], self.scanner.get_bbox()[3], self.scanner.get_bbox()[5])
        ]

        bbox_faces = [
            (bbox_vertices[0], bbox_vertices[1], bbox_vertices[3], bbox_vertices[2]),
            (bbox_vertices[4], bbox_vertices[5], bbox_vertices[7], bbox_vertices[6]),
            (bbox_vertices[1], bbox_vertices[3], bbox_vertices[7], bbox_vertices[5]),
            (bbox_vertices[0], bbox_vertices[2], bbox_vertices[6], bbox_vertices[4]),
            (bbox_vertices[2], bbox_vertices[3], bbox_vertices[7], bbox_vertices[6]),
            (bbox_vertices[0], bbox_vertices[1], bbox_vertices[5], bbox_vertices[4]),
        ]

        bbox_prism = Poly3DCollection(bbox_faces, linewidths=1, edgecolors='b', alpha=0.2)
        self.view.tr_w.ax.add_collection3d(bbox_prism)

        match self.slice:
            case 'x':
                slice_range = np.arange(self.scanner.get_bbox()[0], self.scanner.get_bbox()[1], self.scanner.get_vol_res()[0])
                x = slice_range[self.slice_loc - 1]
                y_min = self.scanner.get_bbox()[2]
                y_max = self.scanner.get_bbox()[3]
                z_min = self.scanner.get_bbox()[4]
                z_max = self.scanner.get_bbox()[5]
                slice = Poly3DCollection([[(x, y_min, z_min), (x, y_max, z_min), (x, y_max, z_max), (x, y_min, z_max)]],
                                          linewidths = 1, edgecolors = 'r', facecolors = 'r', alpha = 0.2)
                self.view.tr_w.ax.add_collection3d(slice)
            case 'y':
                slice_range = np.arange(self.scanner.get_bbox()[2], self.scanner.get_bbox()[3], self.scanner.get_vol_res()[1])
                y = slice_range[self.slice_loc - 1]
                x_min = self.scanner.get_bbox()[0]
                x_max = self.scanner.get_bbox()[1]
                z_min = self.scanner.get_bbox()[4]
                z_max = self.scanner.get_bbox()[5]
                slice = Poly3DCollection([[(x_min, y, z_min), (x_max, y, z_min), (x_max, y, z_max), (x_min, y, z_max)]],
                                          linewidths = 1, edgecolors = 'r', facecolors = 'r', alpha = 0.2)
                self.view.tr_w.ax.add_collection3d(slice)
            case 'z':
                slice_range = np.arange(self.scanner.get_bbox()[4], self.scanner.get_bbox()[5], self.scanner.get_vol_res()[2])
                z = slice_range[self.slice_loc - 1]
                x_min = self.scanner.get_bbox()[0]
                x_max = self.scanner.get_bbox()[1]
                y_min = self.scanner.get_bbox()[2]
                y_max = self.scanner.get_bbox()[3]
                slice = Poly3DCollection([[(x_min, y_min, z), (x_max, y_min, z), (x_max, y_max, z), (x_min, y_max, z)]],
                                          linewidths = 1, edgecolors = 'r', facecolors = 'r', alpha = 0.2)
                self.view.tr_w.ax.add_collection3d(slice)

        for coil in self.scanner.coils:
            if (self.coil_focus_index != None) and (self.scanner.coils[self.coil_focus_index] == coil):
                coil.plot_coil(self.view.tr_w.ax, True, self.segment_focus_index)
            else:
                coil.plot_coil(self.view.tr_w.ax, False, self.segment_focus_index)

        self.view.tr_w.canvas.draw()

    def update_segment_scroll(self):
        '''
        Updates the segment scroll pane in the 'Coil Design' widget

        1. GUI: Iterates through each segment in the focus coil and collects information to 
        display on the segment scroll pane
        '''

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
        '''
        Displays the coil plot

        1. Clears the previous plot to prevent labeling and defines the frame
        2. Plots bounding box with current slice
        3. Plots in-focus coil
        '''

        self.view.tr_w.ax.cla()
        self.view.tr_w.ax.set_xlabel("$x$")
        self.view.tr_w.ax.set_ylabel("$y$")
        self.view.tr_w.ax.set_zlabel("$z$")

        x_dif = self.scanner.get_bbox()[1] - self.scanner.get_bbox()[0]
        y_dif = self.scanner.get_bbox()[3] - self.scanner.get_bbox()[2]
        z_dif = self.scanner.get_bbox()[5] - self.scanner.get_bbox()[4]
        self.view.tr_w.ax.set_xlim(self.scanner.get_bbox()[0] - 0.25 * x_dif, self.scanner.get_bbox()[1] + 0.25 * x_dif)
        self.view.tr_w.ax.set_ylim(self.scanner.get_bbox()[2] - 0.25 * y_dif, self.scanner.get_bbox()[3] + 0.25 * y_dif)
        self.view.tr_w.ax.set_zlim(self.scanner.get_bbox()[4] - 0.25 * z_dif, self.scanner.get_bbox()[5] + 0.25 * z_dif)

        bbox_vertices = [
            (self.scanner.get_bbox()[0], self.scanner.get_bbox()[2], self.scanner.get_bbox()[4]),
            (self.scanner.get_bbox()[1], self.scanner.get_bbox()[2], self.scanner.get_bbox()[4]),
            (self.scanner.get_bbox()[0], self.scanner.get_bbox()[3], self.scanner.get_bbox()[4]),
            (self.scanner.get_bbox()[1], self.scanner.get_bbox()[3], self.scanner.get_bbox()[4]),
            (self.scanner.get_bbox()[0], self.scanner.get_bbox()[2], self.scanner.get_bbox()[5]),
            (self.scanner.get_bbox()[1], self.scanner.get_bbox()[2], self.scanner.get_bbox()[5]),
            (self.scanner.get_bbox()[0], self.scanner.get_bbox()[3], self.scanner.get_bbox()[5]),
            (self.scanner.get_bbox()[1], self.scanner.get_bbox()[3], self.scanner.get_bbox()[5])
        ]

        bbox_faces = [
            (bbox_vertices[0], bbox_vertices[1], bbox_vertices[3], bbox_vertices[2]),
            (bbox_vertices[4], bbox_vertices[5], bbox_vertices[7], bbox_vertices[6]),
            (bbox_vertices[1], bbox_vertices[3], bbox_vertices[7], bbox_vertices[5]),
            (bbox_vertices[0], bbox_vertices[2], bbox_vertices[6], bbox_vertices[4]),
            (bbox_vertices[2], bbox_vertices[3], bbox_vertices[7], bbox_vertices[6]),
            (bbox_vertices[0], bbox_vertices[1], bbox_vertices[5], bbox_vertices[4]),
        ]

        bbox_prism = Poly3DCollection(bbox_faces, linewidths=1, edgecolors='b', alpha=0.2)
        self.view.tr_w.ax.add_collection3d(bbox_prism)

        match self.slice:
            case 'x':
                slice_range = np.arange(self.scanner.get_bbox()[0], self.scanner.get_bbox()[1], self.scanner.get_vol_res()[0])
                x = slice_range[self.slice_loc - 1]
                y_min = self.scanner.get_bbox()[2]
                y_max = self.scanner.get_bbox()[3]
                z_min = self.scanner.get_bbox()[4]
                z_max = self.scanner.get_bbox()[5]
                slice = Poly3DCollection([[(x, y_min, z_min), (x, y_max, z_min), (x, y_max, z_max), (x, y_min, z_max)]],
                                          linewidths = 1, edgecolors = 'r', facecolors = 'r', alpha = 0.2)
                self.view.tr_w.ax.add_collection3d(slice)
            case 'y':
                slice_range = np.arange(self.scanner.get_bbox()[2], self.scanner.get_bbox()[3], self.scanner.get_vol_res()[1])
                y = slice_range[self.slice_loc - 1]
                x_min = self.scanner.get_bbox()[0]
                x_max = self.scanner.get_bbox()[1]
                z_min = self.scanner.get_bbox()[4]
                z_max = self.scanner.get_bbox()[5]
                slice = Poly3DCollection([[(x_min, y, z_min), (x_max, y, z_min), (x_max, y, z_max), (x_min, y, z_max)]],
                                          linewidths = 1, edgecolors = 'r', facecolors = 'r', alpha = 0.2)
                self.view.tr_w.ax.add_collection3d(slice)
            case 'z':
                slice_range = np.arange(self.scanner.get_bbox()[4], self.scanner.get_bbox()[5], self.scanner.get_vol_res()[2])
                z = slice_range[self.slice_loc - 1]
                x_min = self.scanner.get_bbox()[0]
                x_max = self.scanner.get_bbox()[1]
                y_min = self.scanner.get_bbox()[2]
                y_max = self.scanner.get_bbox()[3]
                slice = Poly3DCollection([[(x_min, y_min, z), (x_max, y_min, z), (x_max, y_max, z), (x_min, y_max, z)]],
                                          linewidths = 1, edgecolors = 'r', facecolors = 'r', alpha = 0.2)
                self.view.tr_w.ax.add_collection3d(slice)
        
        self.scanner.coils[self.coil_focus_index].plot_coil(self.view.tr_w.ax, False, self.coil_focus_index)
        self.view.tr_w.canvas.draw()  

    def update_coil_design(self):
        '''
        Updates the 'Coil Design' pane to reflect the current coil being created/modified/etc.

        1. Logic: Update self.slice_B_vol
        2. GUI: Update the segment scroll bar
        3. GUI: Show the coil plot in the top right pane
        4. GUI: Clears all text values (unless a segment is being added)
        5. GUI: Shows the bottom plots if there is information to show, and clears and updates coil 
        and segment focus otherwise.
        '''

        self.update_B_vol_slice()

        self.update_segment_scroll()
        self.show_coil_plot()

        if not self.view.tl_w.coil_design.add_seg_btn.isChecked():
            self.view.tl_w.coil_design.clear_all_text() 
        
        if len(self.scanner.coils) >= 1 and len(self.scanner.coils[-1].segments) >= 1:
            self.show_bottom_plots()
        else:
            # if len(self.scanner.coils) == 0:
            #     self.update_coil_focus(None)
            #     self.update_segment_focus(None)
            # elif len(self.scanner.coils[-1].segments) == 0:
            #     self.update_segment_focus(None)
            self.clear_bottom_plots()      

    def update_coil_focus(self, index : int | None):
        '''
        Updates the in-focus coil using its index

        1. GUI: Removes the highlight of the currently in-focus coil in the 'Coil Control' pane
        2. Logic: Sets self.coil_focus_index to the passed parameter index and update the number of slices
        3. GUI: If new self.coil_focus_index is None, disables coil edit + delete
        in the coil control panel and clear the bottom plots
        4. GUI: If new self.coil_focus_index is not None, update self.slice_B_vol, enable coil editing and deleting,
        highlight the in-focus coil on the coil scroll pane, and update bottom plots if there are segments to plot

        Parameters
        ----------
        index : int | None
            The index of the desired coil to set in focus
        '''

        self.view.tl_w.coil_control.remove_highlight(self.coil_focus_index)

        self.coil_focus_index = index
        self.update_num_slices()

        if self.coil_focus_index == None:
            self.disable_coil_ed()
            self.clear_bottom_plots()
        else:
            self.update_B_vol_slice()
            self.enable_coil_ed()
            self.view.tl_w.coil_control.highlight_selected(self.coil_focus_index)
            if len(self.scanner.coils[self.coil_focus_index].segments) >= 1:
                self.show_bottom_plots()

    def enable_coil_ed(self):
        '''
        Set 'Coil Control' pane to permit editing and deleting of coils

        1. GUI: Enables both the 'Delete Coil' and 'Edit Coil' buttons
        '''

        self.view.tl_w.coil_control.del_coil_btn.setDisabled(False)
        self.view.tl_w.coil_control.edit_coil_btn.setDisabled(False)

    def disable_coil_ed(self):
        '''
        Disables the coil edit + delete buttons in the coil control panel
        '''

        self.view.tl_w.coil_control.del_coil_btn.setDisabled(True)
        self.view.tl_w.coil_control.edit_coil_btn.setDisabled(True)

    def update_segment_focus(self, index : int | None):
        '''
        Updates the segment focus 

        1. Removes the currently highlighted segment in the coil design scroll wheel
        2. Updates segment_focus_index to passed index
        3. Call self.update_coil_design() to update the coil design pane
        4. If segment focus is None, disable segment editing and deleting;
        else enable segment editing and deleting and highlight focus segment

        Parameters
        ----------
        index : int | None
            The index to which the segment focus is being set
        '''

        self.view.tl_w.coil_design.remove_highlight(self.segment_focus_index)

        self.segment_focus_index = index

        self.update_coil_design()

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

    def save_workspace(self):
        '''
        Saves the current workspace
        '''
        try:
            if self.file is None:
                self.file = self.view.save_file_dialog()

            with open(self.file, "w") as json_file:
                json.dump(self, json_file, cls = CustomEncoder, indent=4)
        except Exception as e:
            print('Error saving workspace')
            print(e)
            self.view.error_poput('Error', 'Error saving workspace')

    def load_workspace(self):
        '''
        Loads a stored workspace, throwing an error if it is not completed
        Uses the stored user values 
        '''
        try:
            self.file = self.view.open_file_dialog()    

            with open(self.file, "r") as json_file:
                data = json.load(json_file)
                self.scanner = Scanner(data['scanner_bbox'], data['scanner_vol_res'])
                for i in range(len(data['user_inputs'])):
                    segs = []
                    # for seg in data['user_inputs'][i]:
                    for j in range(0, len(data['user_inputs'][i])): # inserted instead of 713
                        seg = data['user_inputs'][i][j]
                        if len(data['user_inputs'][i][j]) == 6: # Straight Segment
                            line = Straight(seg[0], seg[1], seg[2], seg[3] - seg[0], seg[4] - seg[1], seg[5] - seg[2])

                            # segs.append(Segment(line, 0, 1, seg_B = np.array(data['coils'][i][j]))) # Add segment
                            segs.append(Segment(line, 0, 1)) # Add segment


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
                        
                            # segs.append(Segment(line, p_min * np.pi, p_max * np.pi, seg_B = np.array(data['coils'][i][j]))) # Add segment
                            segs.append(Segment(line, p_min * np.pi, p_max * np.pi)) # Add segment

                        else: # Should never happen if controller works (i.e., passed list is not of length 6 or 13)
                            raise ValueError('Incompatible list size passed for segment creation')
                    
                    coil_to_add = Coil(scanner = self.scanner)
                    for seg in segs:
                        coil_to_add.add_segment(seg)
                    self.scanner.add_coils(coil_to_add)

                self.user_inputs = data['user_inputs']
            
            return True
        
        except Exception as e:
            print('Error loading workspace')
            print(e)
            self.view.error_poput('Error', 'Error loading workspace')

            return False