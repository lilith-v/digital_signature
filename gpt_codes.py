class DigitalSignatureApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Թվային ստորագրություն")

        # Create layouts
        self.main_layout = QVBoxLayout()
        self.sign_layout = QVBoxLayout()
        self.verify_layout = QVBoxLayout()
        
        # Create Widgets
        self.create_widgets()
        
        # Set Main Layout
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        self.update_interface()
        self.resize_to_screen()
    
    def create_widgets(self):
        # Your widget initialization code
        
        # Add Widgets to Layouts
        self.sign_layout.addWidget(self.private_key_label)
        self.sign_layout.addWidget(self.private_key_input)
        self.sign_layout.addWidget(self.message_label_sign)
        self.sign_layout.addWidget(self.message_input_sign)
        self.sign_layout.addLayout(hash_copy_layout_sign)
        self.sign_layout.addWidget(self.sign_button)
        self.sign_layout.addWidget(self.signature_result)
        
        self.verify_layout.addWidget(self.public_key_label)
        self.verify_layout.addWidget(self.public_key_input)
        self.verify_layout.addWidget(self.message_label_verify)
        self.verify_layout.addWidget(self.message_input_verify)
        self.verify_layout.addLayout(hash_copy_layout_verify)
        self.verify_layout.addWidget(self.verify_button)
        self.verify_layout.addWidget(self.signed_message)

        # Add checkbox to main layout first
        self.main_layout.addLayout(checkbox_layout)
        
        # Add other layouts to main layout
        self.main_layout.addLayout(self.sign_layout)
        self.main_layout.addLayout(self.verify_layout)

    def update_interface(self):
        sign_checked = self.sign_checkbox.isChecked()
        verify_checked = self.verify_checkbox.isChecked()

        # Simply show or hide the layouts
        self.sign_layout.setVisible(sign_checked)
        self.verify_layout.setVisible(verify_checked)

    # Your other methods...
