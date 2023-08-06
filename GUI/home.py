from GUI import standards
from scripts import accounts, en_decrypt
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import os
import random


def start(app, window, email, key):
    window.hide()
    home_window = standards.manager_window(app)
    home_window.show()
    home_window.setLayout(home_layout(home_window, email, app, key))



def home_layout(window, email, app, key):
    layout = QHBoxLayout()
    
    middle_side = QWidget()
    middle_layout = QVBoxLayout()

    left_layout = QVBoxLayout()
    left_side = QWidget()
    
    left_widget(left_layout, window, email, middle_layout, key, app=app)
    
    left_side.setLayout(left_layout)
    layout.addWidget(left_side, 80)
    
    

    

    

    middle_widget(middle_layout, window)
    
    

    middle_side.setLayout(middle_layout)
    layout.addWidget(middle_side, 180)
    
    right_layout = QVBoxLayout()
    right_side = QWidget()
    
    right_widget(right_layout, window, email, middle_layout, key, app)
    
    right_side.setLayout(right_layout)
    layout.addWidget(right_side, 80)
    
    return layout



def left_widget(left_layout, window, email, middle_layout, key, app):
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
        new_button.clicked.connect(lambda ch, acc=new_button.text(): middle_widget(middle_layout, window,
                                                                                   True, acc, email, key=key, app=app))
        layout.addWidget(new_button)
    
    # scrolling
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    container = QWidget()
    container.setLayout(layout)
    scroll_area.setWidget(container)
    left_layout.addWidget(scroll_area)
    
def right_widget(right_layout, window, email, middle_layout, key, app):
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
    change_button.clicked.connect(lambda: middle_widget(middle_layout, window, called_right=True, email=email, key=key,
                                                         app=app, is_change=True))
    delete_button.clicked.connect(lambda: accounts.delete(email, window))
    add_acc_button.clicked.connect(lambda: middle_widget(middle_layout, window, called_right=True, email=email, key=key,
                                                         app=app, is_sub_add=True))
    
    



def middle_widget(middle_layout, window, called_left: bool = False, acc: str = None, email: str = None, see_email: bool = False,
                  see_password: bool = False, key: str = None, called_right: bool = False, app = None, is_sub_add: bool = False,
                  is_sub_change: bool = False, is_change: bool = False):
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
    
    font = QFont("BIZ UDPMincho Medium", 36)
    
    if called_left:
        # create widgets
        label = QLabel("ACCOUNT")
        delete_button = QPushButton("delete")
        change_button = QPushButton("change")
        
        # change font
        label.setFont(font)
        delete_button.setFont(font)
        change_button.setFont(font)
        
        
        # Add widgets to the middle-side layout
        middle_layout.setAlignment(Qt.AlignTop)
        middle_layout.addWidget(label)
        middle_layout.addWidget(delete_button)
        middle_layout.addWidget(change_button)

        # create widgets
        name_label = QLabel("name: ")
        name_field = QLineEdit(acc)
        name_field.setReadOnly(True)
        
        # change font
        name_label.setFont(font)
        name_field.setFont(font)
        
        # Add widgets to the middle-side layout
        middle_layout.addWidget(name_label)
        middle_layout.addWidget(name_field)
        
        file = open(f"data/{email}/{acc}", "r", encoding="utf-8")
        lines = file.readlines()
        file.close()
        email_there = False
        username_there = False
        if lines[0] != "0\n" and lines[1] != "0\n":
            email_there = True
            username_there = True
        elif lines[0] == "0\n" and lines[1] != "0\n":
            username_there = True
        elif lines[0] != "0\n" and lines[1] == "0\n":
            email_there = True
        
        
        if username_there and int(lines[1][:-1]) > 0:
            username_label = QLabel("username: ")
            sub_username = lines[2][:int(lines[1][:-1])]
            sub_username = en_decrypt.decrypt(sub_username, en_decrypt.twoOneKey(acc, key))
            username_field = QLineEdit(sub_username)
            username_field.setReadOnly(True)
            
            # change font
            username_label.setFont(font)
            username_field.setFont(font)
            
            # Add widgets to the middle-side layout
            middle_layout.addWidget(username_label)
            middle_layout.addWidget(username_field)
        
            
        if email_there and int(lines[0][:-1]) > 0:
            email_label = QLabel("email: ")
            if see_email:
                sub_email = lines[2][int(lines[1][:-1]):int(lines[1][:-1]) + int(lines[0][:-1])]
                sub_email = en_decrypt.decrypt(sub_email, en_decrypt.twoOneKey(acc, key))
                email_field = QLineEdit(sub_email)
                see_email_button = QPushButton("hide email")
            else:
                email_field = QLineEdit("*" * 10)
                see_email_button = QPushButton("see email")
            
            email_field.setReadOnly(True)
            
            # change font
            email_label.setFont(font)
            email_field.setFont(font)
            see_email_button.setFont(font)
            
            # Add widgets to the middle-side layout
            middle_layout.addWidget(email_label)
            middle_layout.addWidget(email_field)
            middle_layout.addWidget(see_email_button)
            
            # button click
            if see_email:
                see_email_button.clicked.connect(lambda: middle_widget(middle_layout, window, True, acc, email,
                                                                       see_password=see_password, key=key, app=app))
            else:
                see_email_button.clicked.connect(lambda: middle_widget(middle_layout, window, True, acc, email, True,
                                                                       see_password, key=key, app=app))
            
        
        password_label = QLabel("password: ")
        
        if see_password:
            sub_password = lines[2][int(lines[1][:-1]) + int(lines[0][:-1]):]
            sub_password = en_decrypt.decrypt(sub_password, en_decrypt.twoOneKey(acc, key))
            password_field = QLineEdit(sub_password)
            see_password_button = QPushButton("hide password")
        else:
            password_field = QLineEdit("*" * 10)
            see_password_button = QPushButton("see password")
        
        password_field.setReadOnly(True)
        
        
        # change font
        password_field.setFont(font)
        password_label.setFont(font)
        see_password_button.setFont(font)
        
        
        # Add widgets to the middle-side layout
        middle_layout.addWidget(password_label)
        middle_layout.addWidget(password_field)
        middle_layout.addWidget(see_password_button)
        
        
        # button click
        delete_button.clicked.connect(lambda: accounts.delete_sub_acc(app, window, email, key, acc))
        change_button.clicked.connect(lambda: middle_widget(middle_layout, window, called_right=True, email=email, key=key, 
                                                            app=app, is_sub_change=True, acc=acc))
        if see_password:
            see_password_button.clicked.connect(lambda: middle_widget(middle_layout, window, True, acc, email, see_email,
                                                                      key=key, app=app))
        else:
            see_password_button.clicked.connect(lambda: middle_widget(middle_layout, window, True, acc, email, see_email,
                                                                      True, key=key, app=app))
    
    if called_right:
        # create widgets
        if is_sub_add:
            label = QLabel("add an account")
        elif is_sub_change:
            label = QLabel("change an account")
        elif is_change:
            label = QLabel("change email or password")
        back_button = QPushButton("back")
        if is_change:
            exp_label = QLabel("\n* must be filled\nIf password is **********, it will not be changed.\n")
            email_label = QLabel("email *:")
        else:
            exp_label = QLabel("\n* must be filled\nname must be unique and can not be the same as one of your other accounts\n")
            name_label = QLabel("name *: ")
            username_label = QLabel("username: ")
            email_label = QLabel("email :")
        password_label = QLabel("password *: ")
        if is_sub_change:
            file = open(f"data/{email}/{acc}", "r", encoding="utf-8")
            lines = file.readlines()
            file.close()
            sub_email = lines[2][int(lines[1][:-1]):int(lines[1][:-1]) + int(lines[0][:-1])]
            sub_email = en_decrypt.decrypt(sub_email, en_decrypt.twoOneKey(acc, key))
            sub_username = lines[2][:int(lines[1][:-1])]
            sub_username = en_decrypt.decrypt(sub_username, en_decrypt.twoOneKey(acc, key))
            sub_password = lines[2][int(lines[1][:-1]) + int(lines[0][:-1]):]
            sub_password = en_decrypt.decrypt(sub_password, en_decrypt.twoOneKey(acc, key))
            name_field = QLineEdit(acc)
            username_field = QLineEdit(sub_username)
            email_field = QLineEdit(sub_email)
            password_field = QLineEdit(sub_password)
        elif is_sub_add:
            name_field = QLineEdit()
            username_field = QLineEdit()
            email_field = QLineEdit()
            password_field = QLineEdit()
        elif is_change:
            file = open(f"data/{email}/{email}", "r", encoding="utf-8")
            lines = file.read()
            file.close()
            email_field = QLineEdit(en_decrypt.decrypt(email, accounts.email_key))
            password_field = QLineEdit("*" * 10)
        password_gen_label = QLabel("\nsecure password generator: ")
        password_length_label = QLabel("password length: ")
        password_length_field = QLineEdit("10") # default length 10
        checkbox_lower = QCheckBox("include lowercase letters (a-z)")
        checkbox_upper = QCheckBox("include uppercase letters (A-Z)")
        checkbox_numbers = QCheckBox("include numbers (0-9)")
        checkbox_special = QCheckBox("include special characters")
        password_specialcharacter_field = QLineEdit("[!@#$%^&*()]")
        password_gen_button = QPushButton("generate a new password")
        if is_sub_add:
            sub_acc_button = QPushButton("create account")
        elif is_sub_change:
            sub_acc_button = QPushButton("change account")
        elif is_change:
            change_acc_button = QPushButton("change email and password")
        
        # change font
        label.setFont(font)
        back_button.setFont(font)
        exp_label.setFont(font)
        if not is_change:
            name_label.setFont(font)
            name_field.setFont(font)
            username_label.setFont(font)
            username_field.setFont(font)
        email_label.setFont(font)
        email_field.setFont(font)
        password_label.setFont(font)
        password_field.setFont(font)
        password_gen_label.setFont(font)
        password_length_label.setFont(font)
        password_length_field.setFont(font)
        password_gen_button.setFont(font)
        checkbox_lower.setFont(font)
        checkbox_upper.setFont(font)
        checkbox_numbers.setFont(font)
        checkbox_special.setFont(font)
        password_specialcharacter_field.setFont(font)
        if not is_change:
            sub_acc_button.setFont(font)
        else:
            change_acc_button.setFont(font)
        
        # Add widgets to the middle-side layout
        middle_layout.setAlignment(Qt.AlignTop)
        middle_layout.addWidget(label)
        middle_layout.addWidget(back_button)
        middle_layout.addWidget(exp_label)
        if not is_change:
            middle_layout.addWidget(name_label)
            middle_layout.addWidget(name_field)
            middle_layout.addWidget(username_label)
            middle_layout.addWidget(username_field)
        middle_layout.addWidget(email_label)
        middle_layout.addWidget(email_field)
        middle_layout.addWidget(password_label)
        middle_layout.addWidget(password_field)
        middle_layout.addWidget(password_gen_label)
        middle_layout.addWidget(password_length_label)
        middle_layout.addWidget(password_length_field)
        middle_layout.addWidget(checkbox_lower)
        middle_layout.addWidget(checkbox_upper)
        middle_layout.addWidget(checkbox_numbers)
        middle_layout.addWidget(checkbox_special)
        middle_layout.addWidget(password_specialcharacter_field)
        middle_layout.addWidget(password_gen_button)
        middle_layout.addStretch(1)
        if not is_change:
            middle_layout.addWidget(sub_acc_button)
        else:
            middle_layout.addWidget(change_acc_button)
        middle_layout.addStretch(2)
        
        # button click
        back_button.clicked.connect(lambda: middle_widget(middle_layout, window))
        password_gen_button.clicked.connect( lambda: password_gen(window, checkbox_lower, checkbox_upper, checkbox_numbers, checkbox_special,
                                                                password_length_field, password_field, password_specialcharacter_field))
        if is_sub_add:
            sub_acc_button.clicked.connect(lambda: accounts.actions_sub_acc(app, window, email, key, name_field.text(), username_field.text(),
                                                                            email_field.text(), password_field.text()))
        elif is_sub_change:
            sub_acc_button.clicked.connect(lambda: accounts.actions_sub_acc(app, window, email, key, name_field.text(), username_field.text(),
                                                                                email_field.text(), password_field.text(), acc))
        elif is_change:
            change_acc_button.clicked.connect(lambda: accounts.change(app, window, email, key, email_field.text(), password_field.text()))
            
      

def password_gen(window, checkbox_lower, checkbox_upper, checkbox_numbers, checkbox_special,
                 password_length_field, password_field, password_specialcharacter_field):
    characters = ""

    if checkbox_lower.isChecked():
        characters += "abcdefghijklmnopqrstuvwxyz"
    if checkbox_upper.isChecked():
        characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if checkbox_numbers.isChecked():
        characters += "0123456789"
    if checkbox_special.isChecked():
        characters += password_specialcharacter_field.text()
    try:
        password_length = int(password_length_field.text())
    except:
        password_length = 10
    
    try:
        generated_password = ''.join(random.choice(characters) for i in range(password_length))
        password_field.setText(generated_password)
    except IndexError:
        QMessageBox.warning(window, "no characters", "Please check at least one checkbox, so that there can be characters in your password!")