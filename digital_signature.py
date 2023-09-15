import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout,  QTextEdit, QHBoxLayout, QWidget, QCheckBox, QMessageBox
import hashlib 
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QFont



E = 4485537749594267867829640416044157591559771081212083301395047132726030661928940340469239951081860131555558608956103637924473598004279005306785083642003891434725386150319968406654317242339529166190113725288855438317099069981348142848982255618713007248036139471676847230133085321003750956326244934281516850485001235508183754467108146386240146216858659932704542928149213480946965580819104206434194088562601821862601317230349008110997253332102131287625198035655624982729526230863193966273537600840976393348866727423955321720498598711409409632544903237883601183788294943850984039698831673115235199397896371414376978561173
D = 17911653087018085719813350085960076553003727177758856315656261723534487212019110042431852715401245359450769750973823114714949962146003073681790942708726054000824000626307367743864069945709727571249922342654127671500962045655295799389895510609834908569526496164683514120084261796972545313946402048763591688738357920987652029506045224949907402288569141813740481484743043350795552460970855440235879034321433259993026086384525013640236426273699577325321284399589483244561053380187427164179255387299721910714621349135629240740061825714392248037001368043777884363514472003536207609695803002009703024217121462750942506826717
N = 13369944450773052110590942710640512582746853508461993464572453378783852730253267430220609754018715950847369086589584993279172033012972872304926966665888168580554687325455990884734815672250953251446092391929062280852853863110980615390020598691287466815760472346126611108246893208923893820511380680630393938504167946775632628631182607153068695229504268963468892115404557733345850347786372017076615317610632056204607826884754420871296857478553190910799399971115396323415893280721046245502073101386679174606020096483651199917016646574069260285562460454183952338321241063984180935960437324406889962795010877275030599642389
was_unvalid = False

def sign_function(private_key: tuple, hash_value: str):
    if not isinstance(private_key, tuple) or len(private_key) != 2:
        raise ValueError("Invalid private key")
    key, n = private_key
    signature = ""
    for c in hash_value:
        print('c = ', c)
        m = ord(c)
        print('m = ', m)
        print('cypher = ', str(pow(m, key, n)))
        signature += str(pow(m, key, n)) + '*'
    return signature


def verify_function(public_key: tuple, signed_message: str, self):
    global was_unvalid
    was_unvalid = False
    if not isinstance(public_key, tuple) or len(public_key) != 2:
        raise ValueError("Invalid private key")
    try:
        key, n = public_key
        msg = ""
        parts = signed_message.split('*')
        for part in parts:
            print('part = ', part)
            if part:
                c = int(part)
                print('c = ', c)
                msg += chr(pow(c, key, n))
                print('msg = ', msg)
    except Exception as e:
        was_unvalid = True
        QMessageBox.information(self, "լավ","Ցավում ենք, նամակը վավեր չէ")
        return
    return msg

    # if not isinstance(public_key, tuple) or len(public_key) != 2:
    #     raise ValueError("Invalid private key")
    # key, n = public_key
    # msg = ""
    # parts = signed_message.split('*')
    # for part in parts:
    #     print('part = ', part)
    #     if part:
    #         c = int(part)
    #         print('c = ', c)
    #         msg += chr(pow(c, key, n))
    #         print('msg = ', msg)
    # # QMessageBox.information(self, "լավ","Ցավում ենք, նամակը վավեր չէ")
    # return msg

class DigitalSignatureApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Թվային ստորագրություն")
        # self.setStyleSheet( "background-image : 'encryption-encoding-hashing.jpeg'")


        # background_image = QPixmap("encryption-encoding-hashing.jpeg")
        # background_label = QLabel(self)
        # background_label.setPixmap(background_image)
        # background_label.setFixedSize( self.width(), self.height())



        self.sign_checkbox = QCheckBox("Ստորագրել")
        self.verify_checkbox = QCheckBox("Վավերացնել")
        self.sign_checkbox.setChecked(True)
        self.sign_checkbox.clicked.connect(self.handle_sign_checkbox)
        self.verify_checkbox.clicked.connect(self.handle_verify_checkbox)

        self.private_key_label = QLabel("Մասնավոր բանալի:")
        self.private_key_label.setStyleSheet("color: white")
        self.private_key_label.setFont(QFont("Arial", 20))
        self.private_key_label.setMinimumSize(400, 30)
        self.private_key_input = QLineEdit()
        self.private_key_input.setFixedSize(1000, 50)
        self.private_key_input.setStyleSheet("background-color: #283349; border-radius: 5px; padding: 5px")


        self.public_key_label = QLabel("Հանրային բանալի:")
        self.public_key_label.setStyleSheet("color: white")
        self.public_key_label.setFont(QFont("Arial", 20))
        self.public_key_label.setMinimumSize(400, 30)
        self.public_key_input = QLineEdit()
        self.public_key_input.setFixedSize(1000, 50)
        self.public_key_input.setStyleSheet("background-color: #283349; border-radius: 5px; padding: 5px")

        self.message_label_sign = QLabel("Հաղորդագրություն:")
        self.message_label_sign.setStyleSheet("color: white")
        self.message_label_sign.setFont(QFont("Arial", 20))
        self.message_input_sign = QLineEdit()
        self.message_input_sign.setFixedSize(1000, 50)
        self.message_input_sign.setStyleSheet("background-color: #283349; border-radius: 5px; padding: 5px")
        # self.message_input_sign.setMinimumSize(400, 30)


        self.message_label_verify = QLabel("Հաղորդագրություն:")
        self.message_label_verify.setStyleSheet("color: white; ")
        self.message_label_verify.setFont(QFont("Arial", 20))
        self.message_input_verify = QLineEdit()
        self.message_input_verify.setFixedSize(1000, 50)
        # self.message_input_verify.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.message_input_verify.setStyleSheet("background-color: #283349; border-radius: 5px; padding: 0px")

        self.compute_hash_button_sign = QPushButton("Հեշավորել")
        self.compute_hash_button_sign.setStyleSheet("background-color: #5D1EAC;border: 1px solid black; border-radius: 10px; padding: 0px ")
        self.compute_hash_button_sign.setFixedSize(200,40)
        self.compute_hash_button_sign.setFont(QFont("Arial", 20))
        self.compute_hash_button_sign.clicked.connect(self.compute_hash_sign)


        self.compute_hash_button_verify = QPushButton("Հեշավորել")
        self.compute_hash_button_verify.setStyleSheet(" background-color: #5D1EAC;border: 1px solid black; border-radius: 10px; padding: 0px ")
        self.compute_hash_button_verify.setFixedSize(200,40)
        self.compute_hash_button_verify.setFont(QFont("Arial", 20))
        self.compute_hash_button_verify.clicked.connect(self.compute_hash_verify)
   
        self.hash_result_sign = QLabel("Հեշավորված տեքստը կհայտնվի այստեղ")
        self.hash_result_sign.setStyleSheet("background-color : #283349; border: 1px solid black; border-radius: 5px; padding: 0px; color: #a19c9c")
        self.hash_result_sign.setFixedSize(1000, 100)


        self.hash_result_verify = QLabel("Հեշավորված տեքստը կհայտնվի այստեղ")
        self.hash_result_verify.setStyleSheet("background-color: #283349; border: 1px solid black; border-radius: 5px; padding: 0px; color: #a19c9c")
        self.hash_result_verify.setFixedSize(1000, 100)

 

        self.sign_button = QPushButton("Ստորագրել")
        self.sign_button.setStyleSheet("color: white; background-color: #5D1EAC;border: 1px solid black; border-radius: 10px; padding: 0px ")
        self.sign_button.setFixedSize(200,40)
        self.sign_button.setFont(QFont("Arial", 20))
        self.sign_button.clicked.connect(self.sign)

        

        # self.result_label = QLineEdit("")
        self.signature_result = QLineEdit('Ստորագրված տեքստը ներմուծիր այստեղ')
        self.signature_result.setStyleSheet("background-color: #283349; border: 1px solid black; border-radius: 5px; padding: 0px; color: #a19c9c")
        self.signature_result.setFixedSize(1000, 400)

        # self.signature_result.setPlaceholderText("Ստորագրված տեքստը կհայտնվի այստեղ")



        self.verify_button = QPushButton("Վավերացնել")
        self.verify_button.setStyleSheet("color: 044906; background-color: #5D1EAC;border: 1px solid black; border-radius: 10px; padding: 0px ")
        self.verify_button.setFixedSize(200,40)
        self.verify_button.setFont(QFont("Arial", 20))
        self.verify_button.clicked.connect(self.verify)


        self.signed_message = QLineEdit('')
        self.signed_message.setStyleSheet("background-color: #283349; border: 1px solid black; border-radius: 5px; padding: 0px; color: #a19c9c")
        self.signed_message.setFixedSize(1000, 400)
        self.signed_message.setPlaceholderText("Ներմուծիր ստորագրված նամակը")

        sign_signature_layout = QHBoxLayout()
        sign_signature_layout.addWidget(self.sign_button)
        sign_signature_layout.addWidget(self.signature_result)

        checkbox_layout = QHBoxLayout()
        checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        checkbox_layout.addWidget(self.sign_checkbox)
        checkbox_layout.addWidget(self.verify_checkbox)

        hash_copy_layout_sign = QHBoxLayout()
        hash_copy_layout_sign.addWidget(self.compute_hash_button_sign)
        hash_copy_layout_sign.addWidget(self.hash_result_sign)

        hash_copy_layout_verify = QHBoxLayout()
        hash_copy_layout_verify.addWidget(self.compute_hash_button_verify)
        hash_copy_layout_verify.addWidget(self.hash_result_verify)

        verify_layout = QHBoxLayout()
        verify_layout.addWidget(self.verify_button)
        verify_layout.addWidget(self.signed_message)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(checkbox_layout)
        layout.addWidget(self.private_key_label)
        layout.addWidget(self.private_key_input)
        layout.addWidget(self.public_key_label)
        layout.addWidget(self.public_key_input)
        layout.addWidget(self.message_label_sign)
        layout.addWidget(self.message_input_sign)
        layout.addWidget(self.message_label_verify)
        layout.addWidget(self.message_input_verify)
        layout.addLayout(hash_copy_layout_sign)
        layout.addLayout(hash_copy_layout_verify)

        layout.addLayout(verify_layout)

        layout.addLayout(sign_signature_layout)
        layout.addWidget(self.sign_button)
        layout.addWidget(self.signature_result)


        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.update_interface()

        self.resize_to_screen()

    def resize_to_screen(self):
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        self.setGeometry(screen_rect)

    def handle_sign_checkbox(self):
        if self.sign_checkbox.isChecked():
            self.verify_checkbox.setChecked(False)
            self.update_interface()

    def handle_verify_checkbox(self):
        if self.verify_checkbox.isChecked():
            self.sign_checkbox.setChecked(False)
            self.update_interface()

    def update_interface(self):
        sign_checked = self.sign_checkbox.isChecked()
        verify_checked = self.verify_checkbox.isChecked()

        self.private_key_label.setVisible(sign_checked)
        self.private_key_input.setVisible(sign_checked)
        self.public_key_label.setVisible(verify_checked)
        self.public_key_input.setVisible(verify_checked)
        self.message_label_sign.setVisible(sign_checked )
        self.message_input_sign.setVisible(sign_checked )
        self.message_label_verify.setVisible(verify_checked)
        self.message_input_verify.setVisible(verify_checked)
        self.compute_hash_button_sign.setVisible(sign_checked)
        self.compute_hash_button_verify.setVisible(verify_checked)

        # self.hash_label.setVisible(sign_checked or verify_checked)
        self.hash_result_sign.setVisible(sign_checked)
        self.hash_result_verify.setVisible(verify_checked)

        # self.copy_button.setVisible(sign_checked or verify_checked)
        self.sign_button.setVisible(sign_checked)
        # self.result_label.setVisible(sign_checked)
        self.signature_result.setVisible(sign_checked)
        self.verify_button.setVisible(verify_checked)
        self.signed_message.setVisible(verify_checked)

    def compute_hash_sign(self):
        if self.message_input_sign.text() is None or self.message_input_sign.text() ==  ' ' or self.message_input_sign.text() == '':
            QMessageBox.information(self, "լավ","Հաղորդագրության դաշտը դատարկ է")
            return
        hash_value = hashlib.sha256(self.message_input_sign.text().encode()).hexdigest()
        hash_value = hash_value[:32]
        self.hash_result_sign.setText(hash_value)

    def compute_hash_verify(self):
        if self.message_input_verify.text() is None or self.message_input_verify.text() ==  ' ' or self.message_input_verify.text() == '':
            QMessageBox.information(self, "լավ","Հաղորդագրության դաշտը դատարկ է")
            return
        hash_value = hashlib.sha256(self.message_input_verify.text().encode()).hexdigest()
        hash_value = hash_value[:32]

        self.hash_result_verify.setText(hash_value)

    # def copy_hash(self):
    #     clipboard = QApplication.clipboard()
    #     clipboard.setText(self.hash_result_sign.text()) 

    #     QMessageBox.information(self, "Copy Successful", "Hashed message has been copied to the clipboard.")

    def sign(self):
        global signature
        if self.hash_result_sign.text() is None or self.hash_result_sign.text() ==  ' ' or self.hash_result_sign.text() == '':
            QMessageBox.information(self, "լավ","Հեշի դաշտը դատարկ է")
            return
        elif self.private_key_input.text() is None or self.private_key_input.text() ==  ' ' or self.private_key_input.text() == '':
            QMessageBox.information(self, "լավ","Խնդրում ենք ներմուծել մասնավոր բանալին")
            return
        signature = sign_function((D, N), self.hash_result_sign.text())
        self.signature_result.setText(signature) 
        #self.signed_message.setText(signature)
        # verify = verify_function((E, N),signature)
        clipboard = QApplication.clipboard()
        clipboard.setText(signature)
        # if self.hash_result_sign.text() == verify:
        print('len(self.hash_result_sign.text()) = ', len(self.signature_result.text()))
        print('len(self.signed_message.text()) = ', len(self.signed_message.text()))
        print('len(signature) = ', len(signature))

            # print('verify = ', verify)


    def verify(self):
        if self.hash_result_verify.text() is None or self.hash_result_verify.text() ==  ' ' or self.hash_result_verify.text() == '':
            QMessageBox.information(self, "լավ","Հեշի դաշտը դատարկ է")

            return
        elif self.public_key_input.text() is None or self.public_key_input.text() ==  ' ' or self.public_key_input.text() == '':
            self.message = QMessageBox.information(self, "լավ","Խնդրում ենք ներմուծել հանրային բանալին")
    

            return
        elif self.signed_message.text() is None or self.signed_message.text() ==  ' ' or self.signed_message.text() == '':
            QMessageBox.information(self, "լավ","Խնդրում ենք ներմուծել ստորագրված տեքստը")
            return
        # hashed_value = verify_function((E, N), self.signed_message.text())
        # if self.signed_message.text() == self.signature_result.text():
            # print('yeeeeees\n\n\n\n')
            # #print('type self.signed_message.text() = ', self.signed_message.text())
            # print('type self.signature_result.text() = ', self.signature_result.text())
            # print('type signature = ', signature)
        # else :
        #     print('NOOOOOOOOOOO\n\n\n\n\n')
        hashed_value = verify_function((E, N), self.signed_message.text(), self)


        if hashed_value == self.hash_result_verify.text(): 
            QMessageBox.information(self,  "լավ", "Շնորհավորում ենք, նամակը վավեր է")
            return
        else:
            if was_unvalid != True:
                QMessageBox.information(self, "լավ","Ցավում ենք, նամակը վավեր չէ")
                return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DigitalSignatureApp()
    window.setStyleSheet("background-color: #081633")
    # window.setStyleSheet("background-image: url(4.jpeg)")

    window.show()
    sys.exit(app.exec())


