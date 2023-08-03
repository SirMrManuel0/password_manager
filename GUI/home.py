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
    home_window.setLayout(home_layout(home_window, email))



def home_layout(window, email):
    layout = QHBoxLayout()
    
    middle_side = QWidget()
    middle_layout = QVBoxLayout()

    left_layout = QVBoxLayout()
    left_side = QWidget()
    
    left_widget(left_layout, window, email, middle_layout)
    
    left_side.setLayout(left_layout)
    layout.addWidget(left_side, 80)
    
    

    

    

    middle_widget(middle_layout, window)
    
    

    middle_side.setLayout(middle_layout)
    layout.addWidget(middle_side, 180)
    
    right_layout = QVBoxLayout()
    right_side = QWidget()
    
    right_widget(right_layout, window)
    
    right_side.setLayout(right_layout)
    layout.addWidget(right_side, 80)
    
    return layout



def left_widget(left_layout, window, email, middle_layout):
    # create widgets
    label = QLabel("ACCOUNTS")
    
    
    # change font
    font = QFont("BIZ UDPMincho Medium", 36)
    label.setFont(font)
 
    # Add widgets to the left-side layout
    left_layout.addWidget(label)
    
    # to have all accounts appear on the left side
    files = os.listdir(f"data/{email}")
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)
    
    for i in files:
        if i == email:
            continue
        new_button = QPushButton(i)
        new_button.setFont(font)
        new_button.clicked.connect(lambda ch, acc=new_button.text(): middle_widget(middle_layout, window, True, acc, email))
        layout.addWidget(new_button)
    
    # scrolling
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    container = QWidget()
    container.setLayout(layout)
    scroll_area.setWidget(container)
    left_layout.addWidget(scroll_area)
    
def right_widget(right_layout, window):
    # create widgets
    add_acc_button = QPushButton("add an account")
    change_button = QPushButton("change email or password")
    delete_button = QPushButton("delete your account")
    logout_button = QPushButton("logout & close")
    
    
    
    # change font
    font = QFont("BIZ UDPMincho Medium", 36)
    add_acc_button.setFont(font)
    change_button.setFont(font)
    delete_button.setFont(font)
    logout_button.setFont(font)
    
    
    # Add widgets to the right-side layout
    right_layout.addWidget(add_acc_button)
    
    right_layout.addStretch(1)
    
    right_layout.addWidget(delete_button)
    right_layout.addWidget(change_button)
    right_layout.addWidget(logout_button)
    
    # button click
    logout_button.clicked.connect(lambda: sys.exit())
    change_button.clicked.connect(lambda: accounts.change())
    delete_button.clicked.connect(lambda: accounts.delete())
    
    



def middle_widget(middle_layout, window, called: bool = False, acc: str = None, email: str = None, 
                  see_email: bool = False, see_password: bool = False):
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
    delete_button = QPushButton("delete")
    change_button = QPushButton("change email or password")
    
    # change font
    font = QFont("BIZ UDPMincho Medium", 36)
    label.setFont(font)
    delete_button.setFont(font)
    change_button.setFont(font)
    
    
    # Add widgets to the middle-side layout
    middle_layout.setAlignment(Qt.AlignTop)
    middle_layout.addWidget(label)
    middle_layout.addWidget(delete_button)
    middle_layout.addWidget(change_button)
    
    if called:
        # create widgets
        name_label = QLabel("name: ")
        name_field = QLineEdit(acc)
        name_field.setReadOnly(True)
        
        file = open(f"data/{email}/{acc}", "r", encoding="utf-8")
        lines = file.readlines()
        
        sub_email = lines[1][:int(lines[0][:-1])]
        
        email_label = QLabel("email: ")
        if see_email:
            email_field = QLineEdit(sub_email)
        else:
            email_field = QLineEdit("*" * 10)
        email_field.setReadOnly(True)
        if see_email:
            see_email_button = QPushButton("hide email")
        else:
            see_email_button = QPushButton("see email")
        
        sub_password = lines[1][int(lines[0][:-1]):]
        
        password_label = QLabel("password: ")
        if see_password:
            password_field = QLineEdit(sub_password)
        else:
            password_field = QLineEdit("*" * 10)
        password_field.setReadOnly(True)
        if see_password:
            see_password_button = QPushButton("hide password")
        else: 
            see_password_button = QPushButton("see password")
        
        
        # change font
        name_label.setFont(font)
        name_field.setFont(font)
        email_label.setFont(font)
        email_field.setFont(font)
        see_email_button.setFont(font)
        password_field.setFont(font)
        password_label.setFont(font)
        see_password_button.setFont(font)
        
        
        # Add widgets to the middle-side layout
        middle_layout.addWidget(name_label)
        middle_layout.addWidget(name_field)
        middle_layout.addWidget(email_label)
        middle_layout.addWidget(email_field)
        middle_layout.addWidget(see_email_button)
        middle_layout.addWidget(password_label)
        middle_layout.addWidget(password_field)
        middle_layout.addWidget(see_password_button)
        
        
        # button click
        delete_button.clicked.connect(lambda: accounts.delete_sub_acc())
        change_button.clicked.connect(lambda: accounts.change_sub_acc())
        if see_email:
            see_email_button.clicked.connect(lambda: middle_widget(middle_layout, window, True, acc, email))
        else:
            see_email_button.clicked.connect(lambda: middle_widget(middle_layout, window, True, acc, email, True))
        if see_password:
            see_password_button.clicked.connect(lambda: middle_widget(middle_layout, window, True, acc, email))
        else:
            see_password_button.clicked.connect(lambda: middle_widget(middle_layout, window, True, acc, email, see_password=True))
        
        