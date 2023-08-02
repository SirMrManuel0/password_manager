from GUI import standards
from scripts import accounts
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import os


def start(app, window, email, hash):
    window.hide()
    home_window = standards.manager_window(app)
    home_window.show()
    home_window.setLayout(home_layout(home_window))



def home_layout(window):
    layout = QHBoxLayout()

    left_layout = QVBoxLayout()
    left_side = QWidget()
    
    left_widget(left_layout, window)
    
    left_side.setLayout(left_layout)
    layout.addWidget(left_side, 80)
    
    

    middle_side = QWidget()
    middle_layout = QVBoxLayout()

    

    middle_widget(middle_layout, window)
    
    

    middle_side.setLayout(middle_layout)
    layout.addWidget(middle_side, 180)
    
    right_layout = QVBoxLayout()
    right_side = QWidget()
    
    right_widget(right_layout, window)
    
    right_side.setLayout(right_layout)
    layout.addWidget(right_side, 80)
    
    return layout



def left_widget(left_layout, window):
    # create widgets
    label = QLabel("ACCOUNTS")
    
    
    # change font
    font = QFont("BIZ UDPMincho Medium", 36)
    label.setFont(font)

    
    
    # Add widgets to the left-side layout
    left_layout.addWidget(label)

    left_layout.addStretch(1)
    
def right_widget(right_layout, window):
    # create widgets
    add_acc_button = QPushButton("add an account")
    change_button = QPushButton("change email or password")
    logout_button = QPushButton("logout & close")
    
    
    # change font
    font = QFont("BIZ UDPMincho Medium", 36)
    add_acc_button.setFont(font)
    change_button.setFont(font)
    logout_button.setFont(font)
    
    
    # Add widgets to the right-side layout
    right_layout.addWidget(add_acc_button)
    
    right_layout.addStretch(1)
    
    right_layout.addWidget(change_button)
    right_layout.addWidget(logout_button)
    
    # button click
    logout_button.clicked.connect(lambda: sys.exit())
    change_button.clicked.connect(lambda: accounts.change())
    
    



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
    
    # create widgets
    label = QLabel("ACCOUNT")
    boop = QPushButton("login")
    
    # change font
    font = QFont("BIZ UDPMincho Medium", 36)
    label.setFont(font)
    boop.setFont(font)
    
    
    # Add widgets to the middle-side layout
    middle_layout.addWidget(label)
    middle_layout.addWidget(boop)

    middle_layout.addStretch(1)
    
    # button click
    boop.clicked.connect(lambda: accounts.login(window, email_field.text(), password_field.text()))