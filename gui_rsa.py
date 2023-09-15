import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtGui import QFont
from api_itegration import conversation_assistant_user, QUESTION, SYSTEM_COMMAND
import os
import openai
import requests
import psycopg2
from datetime import datetime
from rsa_algorithm import encrypt, decrypt, generate_key_pair
#from db_utils import db_connection
import psycopg2


#def db_connection():
conn = psycopg2.connect(
    database = 'rsa_secure_numbers',
    user = 'postgres',
    password = 'password',
    host = 'localhost',
    port = '5434')
    # return conn


#conn = db_connection
cursor = conn.cursor()

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #F0F0F0;")
        self.setWindowTitle("RSA")
        self.setFixedSize(1440, 850)

        # Create label_1
        self.label_1 = QLabel("RSA բանալիներ գեներացնող, գաղտնագրող, գաղտնազերծող գործիք", self)
        self.label_1.setGeometry(200, 10, 1000, 55)
        self.label_1.setFont(QFont("Arial", 27))
        self.label_1.setStyleSheet("background-color: #F0F0F0;  padding: 5px; color: black")

        # Create label_2
        self.label_2 = QLabel(self)
        self.label_2.setText("Հանրային բանալի")
        self.label_2.setGeometry(50, 100, 200, 50)
        self.label_2.setFont(QFont("Arial", 20))
        self.label_2.setStyleSheet("background-color: #F0F0F0;   padding: 0px; color: black")

        # Create label_3
        self.label_3 = QLabel(self)
        self.label_3.setGeometry(50, 150, 600, 80)
        self.label_3.setFont(QFont("Arial", 12))
        self.label_3.setText('')
        self.label_3.setStyleSheet("background-color: lightgray; border: 1px solid black; border-radius: 5px; padding: 5px; color: black ")

        # Create label_4
        self.label_4 = QLabel(self)
        self.label_4.setText("Մասնավոր բանալի")
        self.label_4.setGeometry(890, 100, 210, 50)
        self.label_4.setFont(QFont("Arial", 20))
        self.label_4.setStyleSheet("background-color: #F0F0F0;  padding: 0px; color: black")

        # Create label_5
        self.label_5 = QLabel(self)
        self.label_5.setGeometry(790, 150, 600, 80)
        self.label_5.setFont(QFont("Arial", 12))
        self.label_5.setText('')
        self.label_5.setStyleSheet("background-color: lightgray; border: 1px solid black; border-radius: 5px; padding: 5px; color: black")

        # Create label_7
        self.label_7 = QLabel(self)
        self.label_7.setGeometry(50, 410, 500, 300)
        self.label_7.setFont(QFont("Arial", 12))
        self.label_7.setText('')
        self.label_7.setStyleSheet("background-color: lightgray; padding: 5px; border: 1px solid black; border-radius: 5px; color: black")

        # Create label_8
        self.label_8 = QLabel(self)
        self.label_8.setGeometry(890, 610,  500, 100)
        self.label_8.setFont(QFont("Arial", 12))
        self.label_8.setText('')
        self.label_8.setStyleSheet("background-color: lightgray; border: 1px solid black; border-radius: 5px; padding: 0px; color: black")

        # Create label_9
        self.label_9 = QLabel(self)
        self.label_9.setGeometry(50, 720,  1340, 100)
        self.label_9.setFont(QFont("Arial", 12))
        self.label_9.setText('Հետաքրքիր փաստ RSA ալգորիթմի մասին')
        self.label_9.setStyleSheet("background-color: lightgray; border: 1px solid black; border-radius: 5px; padding: 0px; color: black")

        # Create input_box
        self.input_box = QLineEdit(self)
        self.input_box.setGeometry(50, 250, 500, 100)
        self.input_box.setFont(QFont("Arial", 12))
        self.input_box.setStyleSheet("background-color: lightgray; padding: 5px; border: 1px solid black; border-radius: 5px; color: black")
        self.input_box.setPlaceholderText("Ներմուծիր գաղտնագրվող տեքստը")

        # Create input_box
        self.input_box_1 = QLineEdit(self)
        self.input_box_1.setGeometry(890, 250, 500, 300)
        self.input_box_1.setFont(QFont("Arial", 12))
        self.input_box_1.setStyleSheet("background-color: lightgray; padding: 5px; border: 1px solid black; border-radius: 5px; color: black")
        self.input_box_1.setPlaceholderText("Ներմուծիր գաղտնագրված տեքստը")

        # Create button
        self.button_1 = QPushButton("Գեներացնել բանալիներ", self)
        self.button_1.setGeometry(620, 70, 202, 60)
        self.button_1.setFont(QFont("Arial", 16))
        self.button_1.clicked.connect(self.generateKeys)
        self.button_1.setStyleSheet("background-color: #4CAF50; border-radius: 5px; color: white; padding: 5px;")
        self.button_1.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_1.installEventFilter(self)  

        self.button_2 = QPushButton("գաղտնագրել", self)
        self.button_2.setGeometry(255, 360, 80, 40)
        self.button_2.setFont(QFont("Arial", 10))
        self.button_2.clicked.connect(lambda: self.call_encrypt( str(self.input_box.text())))
        self.button_2.setStyleSheet("background-color: #2480fb; border-radius: 5px; color: white; padding: 5px;")
        self.button_2.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_2.installEventFilter(self)  

        self.button_3 = QPushButton("գաղտնազերծել", self)
        self.button_3.setGeometry(1100, 560, 90, 40)
        self.button_3.setFont(QFont("Arial", 10))
        self.button_3.clicked.connect(lambda: self.call_decrypt( str(self.input_box_1.text())))
        self.button_3.setStyleSheet("background-color: #2480fb; border-radius: 5px; color: white; padding: 5px;")
        self.button_3.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_3.installEventFilter(self)  # Install event filter

        self.button_4 = QPushButton("Սեղմիր, որ տեսնես հետաքրքիր փաստ RSA ալգորիթմի մասին", self)
        self.button_4.setGeometry(50, 720, 400, 30)
        self.button_4.setFont(QFont("Arial", 10))
        self.button_4.clicked.connect(lambda: self.gen_fact())
        self.button_4.setStyleSheet("background-color: gray; border-radius: 0px; color: white; padding: 5px;")
        self.button_4.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_4.installEventFilter(self) 

      # Create copy button
        self.copy_button = QPushButton('Պատճենել գաղտնազերծման բաժնում', self)
        self.copy_button.setGeometry(250, 410, 300, 30)
        self.copy_button.clicked.connect(self.copy_text)
        self.copy_button.setStyleSheet("background-color: gray; color: white")
        self.copy_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_button.installEventFilter(self) 


    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.label_7.text())
        self.input_box_1.setText(self.label_7.text())
            
    # def eventFilter(self, obj, event):
    #         if event.type() == event.Type.MouseButtonPress:
    #             if obj == self.button_1:
    #                 # Button 1 pressed
    #                 obj.setStyleSheet("background-color: green; border-radius: 5px; color: white; padding: 5px;")
    #             elif obj == self.button_2:
    #                 # Button 2 pressed
    #                 obj.setStyleSheet("background-color: blue; border-radius: 5px; color: white; padding: 5px;")
    #         elif event.type() == event.Type.MouseButtonRelease:
    #             if obj == self.button_1:
    #                 # Button 1 released
    #                 obj.setStyleSheet("background-color: #4CAF50; border-radius: 5px; color: white; padding: 5px;")
    #             elif obj == self.button_2:
    #                 # Button 2 released
    #                 obj.setStyleSheet("background-color: #78c0e0; border-radius: 5px; color: black; padding: 5px;")
    #         return super().eventFilter(obj, event)


    def generateKeys(self):
        keysize = 1024 # default keysize
        global public_key, private_key
        global prime_p, prime_q
        cursor.execute("select number_p from rsa_prime_numbers limit 1")
        prime_p= int(((cursor.fetchall()[0][0])))
        cursor.execute("select number_q from rsa_prime_numbers limit 1")
        prime_q= int(((cursor.fetchall()[0][0])))

        self.public_key, self.private_key= generate_key_pair(prime_p, prime_q)
        print('e = ', self.public_key[0])
        print('d = ', self.private_key[0])
        # Display generated keys
        self.label_3.setText(f"{self.public_key[0]}")
        self.label_5.setText(f"{self.private_key[0]}")
        return self.public_key, self.private_key
        
    def call_encrypt( self, msg:str):
        cypher = encrypt(self.public_key,  msg)
        self.label_7.setText(f"{cypher}")

    def call_decrypt( self, cypher:str):
        plain = decrypt(self.private_key,  cypher)
        self.label_8.setText(f"{plain}")        

    def gen_fact(self):
        fact = conversation_assistant_user(QUESTION, SYSTEM_COMMAND)
        self.label_9.setText(fact)
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setGeometry(600, 600, 800, 800)
    window.show()
    sys.exit(app.exec())

