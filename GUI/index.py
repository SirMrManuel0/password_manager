from GUI import standards
from scripts import accounts
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import os


def start(app):
    index_window = standards.manager_window(app)
    index_window.show()
    
    index_window.setLayout(index_layout(index_window))
    
    
    app.exec_()



def index_layout(window):
    layout = QHBoxLayout()

    left_side = QWidget()
    layout.addWidget(left_side, 170)
    
    

    middle_side = QWidget()
    middle_layout = QVBoxLayout()

    

    middle_widget(middle_layout, window)
    
    

    middle_side.setLayout(middle_layout)
    layout.addWidget(middle_side, 100)
    
    right_side = QWidget()
    layout.addWidget(right_side, 30)
    
    
    return layout


def middle_widget(middle_layout, window):
    while middle_layout.count() > 0:
        item = middle_layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
        elif item.layout():
            sub_layout = item.layout()
            while sub_layout.count() > 0:
                sub_item = sub_layout.takeAt(0)
                if sub_item.widget():
                    sub_item.widget().deleteLater()
    
    middle_layout.addStretch(1)
    
    # create widgets
    label = QLabel("LOGIN")
    email_field = QLineEdit()
    password_field = QLineEdit()
    password_field.setEchoMode(QLineEdit.PasswordEchoOnEdit)
    login_button = QPushButton("login")
    signup_button = QPushButton("sign up")
    
    # set placeholder text
    email_field.setPlaceholderText("Enter your email")
    password_field.setPlaceholderText("Enter your password")
    
    # change font
    font = QFont("BIZ UDPMincho Medium", 36)
    label.setFont(font)
    email_field.setFont(font)
    password_field.setFont(font)
    login_button.setFont(font)
    signup_button.setFont(font)

    email_field.setFocus()
    
    
    # Add widgets to the right-side layout
    middle_layout.addWidget(label)
    middle_layout.addWidget(email_field)
    middle_layout.addWidget(password_field)
    middle_layout.addWidget(login_button)
    middle_layout.addWidget(signup_button)

    middle_layout.addStretch(1)
    
    # button click
    login_button.clicked.connect(lambda: accounts.login(window, email_field.text(), password_field.text()))
    signup_button.clicked.connect(lambda: signup_window(middle_layout, window))





def signup_window(middle_layout, window):
    while middle_layout.count() > 0:
        item = middle_layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
        elif item.layout():
            sub_layout = item.layout()
            while sub_layout.count() > 0:
                sub_item = sub_layout.takeAt(0)
                if sub_item.widget():
                    sub_item.widget().deleteLater()

    # Create new widgets for signup
    label = QLabel("SIGNUP")
    email_field = QLineEdit()
    password_field = QLineEdit()
    confirm_password_field = QLineEdit()
    signup_button = QPushButton("sign up")
    cancel_button = QPushButton("cancel")
    
    
    password_field.setEchoMode(QLineEdit.PasswordEchoOnEdit)
    confirm_password_field.setEchoMode(QLineEdit.PasswordEchoOnEdit)

    
    
    # set placeholder text
    email_field.setPlaceholderText("Enter your email")
    password_field.setPlaceholderText("Enter your password")
    confirm_password_field.setPlaceholderText("Confirm your password")

    # change font
    font = QFont("BIZ UDPMincho Medium", 36)
    label.setFont(font)
    email_field.setFont(font)
    password_field.setFont(font)
    confirm_password_field.setFont(font)
    signup_button.setFont(font)
    cancel_button.setFont(font)
    
    middle_layout.addStretch(1)
    
    # Add widgets to the layout
    middle_layout.addWidget(label)
    middle_layout.addWidget(email_field)
    middle_layout.addWidget(password_field)
    middle_layout.addWidget(confirm_password_field)
    middle_layout.addWidget(signup_button)
    middle_layout.addWidget(cancel_button)

    middle_layout.addStretch(1)
    
    # button click
    cancel_button.clicked.connect(lambda: middle_widget(middle_layout, window))
    signup_button.clicked.connect(lambda: accounts.sign_up(window, email_field.text(), password_field.text(), confirm_password_field.text()))
