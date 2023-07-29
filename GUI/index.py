from GUI import standards
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import os


def start(app):
    index_window = standards.manager_window(app)
    index_window.show()

    index_window.setLayout(index_layout())
    
    app.exec_()



def index_layout():
    layout = QHBoxLayout()

    left_side = QWidget()
    layout.addWidget(left_side, 170)
    
    

    middle_side = QWidget()
    middle_layout = QVBoxLayout()

    middle_layout.addStretch(1)

    # create widgets
    label = QLabel("LOGIN")
    textfield = QLineEdit()
    passwordfield = QLineEdit()
    passwordfield.setEchoMode(QLineEdit.Password)
    login_button = QPushButton("login")
    signup_button = QPushButton("sign up")
    
    #change font
    font = QFont("BIZ UDPMincho Medium", 36)
    label.setFont(font)
    textfield.setFont(font)
    passwordfield.setFont(font)
    login_button.setFont(font)
    signup_button.setFont(font)

    textfield.setFocus()
    
    # Add widgets to the right-side layout
    middle_layout.addWidget(label)
    middle_layout.addWidget(textfield)
    middle_layout.addWidget(passwordfield)
    middle_layout.addWidget(login_button)
    middle_layout.addWidget(signup_button)

    middle_layout.addStretch(1)

    middle_side.setLayout(middle_layout)
    layout.addWidget(middle_side, 100)
    
    right_side = QWidget()
    layout.addWidget(right_side, 30)
    
    return layout