class Controller:

    def __init__(self, view):
        self.view = view

        self.view.tl_w.init_scanner.init_scanner_btn_clicked.connect(self.handle_init_scanner_btn_clicked)
        self.view.tl_w.init_scanner.load_scanner_btn_clicked.connect(self.handle_mod_scanner_btn_clicked)

        self.view.tl_w.set_scanner.button_clicked.connect(self.handle_init_scanner_clicked)

        self.view.tl_w.coil_control.mod_scanner_clicked.connect(self.handle_mod_scanner_clicked)
        self.view.tl_w.coil_control.del_coil_clicked.connect(self.handle_del_coil_clicked)
        self.view.tl_w.coil_control.edit_coil_clicked.connect(self.handle_edit_coil_clicked)
        self.view.tl_w.coil_control.add_coil_clicked.connect(self.handle_add_coil_clicked)

        self.view.tl_w.coil_design.straight_seg_clicked.connect(self.handle_straight_seg_clicked)
        self.view.tl_w.coil_design.curved_seg_clicked.connect(self.handle_curved_seg_clicked)

    def handle_init_scanner_btn_clicked(self):
        self.view.tl_w.stack.setCurrentIndex(1)

    def handle_mod_scanner_btn_clicked(self):
        print('Connected to load scanner button')
        # Needs implementation

    def handle_init_scanner_clicked(self):
        self.view.tl_w.stack.setCurrentIndex(2)

    def handle_mod_scanner_clicked(self):
        self.view.tl_w.stack.setCurrentIndex(1)

    def handle_del_coil_clicked(self):
        print('Connected to handle_del_coil_clicked')
        # Needs implementation

    def handle_edit_coil_clicked(self):
        print('Connected to handle_edit_coil_clicked')
        # Needs implementation

    def handle_add_coil_clicked(self):
        self.view.tl_w.stack.setCurrentIndex(3)

    def handle_straight_seg_clicked(self):
        self.view.tl_w.coil_design.seg_edit_curved.setChecked(False)
        self.view.tl_w.coil_design.seg_edit_stack.setCurrentIndex(0)  
        self.view.tl_w.coil_design.seg_edit_stack.show()

    def handle_curved_seg_clicked(self):
        self.view.tl_w.coil_design.seg_edit_straight.setChecked(False) 
        self.view.tl_w.coil_design.seg_edit_stack.setCurrentIndex(1) 
        self.view.tl_w.coil_design.seg_edit_stack.show()