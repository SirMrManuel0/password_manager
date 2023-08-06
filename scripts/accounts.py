from PyQt5.QtWidgets import *
import re
from scripts import en_decrypt
from GUI import home
from GUI import index
import os
import shutil
import sys

email_key = ['1', '714', '193', '126', '182', '512', '237', '112', '379', '466', '746', '669', '835', '934', '864', '273', '195', '252', '436',
                 '949', '899', '696', '054', '189', '440', '670', '190', '110', '108', '853', '285', '961', '492', '264', '694', '144', '506', '650',
                 '265', '761', '596', '780', '975', '146', '392', '433', '686', '414', '491', '944', '862', '609', '361', '798', '133', '555', '464',
                 '639', '395', '481', '767', '741', '994', '337', '958', '801', '134', '002', '563', '578', '465', '954', '778', '438','761', '539']


def is_valid_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.fullmatch(email_pattern, email) and email[email.find("@"):].find("..") < 0:
        return True
    else:
        return False


def login(app, window, email, password):

    if email == "" or password == "":
        QMessageBox.warning(window, "incorrect input", "email and password can not be empty!")
        return

    if not is_valid_email(email):
        QMessageBox.warning(window, "not a valid email", "Please make sure to enter a valid email!")
        return
    

    password_check = en_decrypt.numbers_in_text(en_decrypt.oneHash(password))
    email = en_decrypt.encrypt(email, email_key)
    
    

    if not os.path.isdir(f"data/{email}") and not os.path.isfile(f"data/{email}/{email}"):
        QMessageBox.warning(window, "user not found", "Please make sure to enter the email of an existing account!")
        return


    file = open(f"data/{email}/{email}", "r", encoding="utf-8")
    saved_password = file.read()
    
    if password_check == saved_password:
        password_check = ""
        saved_password = ""
        home.start(app, window, email, en_decrypt.numbers_in_text(en_decrypt.twoOneKey(en_decrypt.decrypt(email, email_key), password)))
        return


    QMessageBox.warning(window, "wrong password or email", "Please make sure to enter the right email and password!")
    return


def sign_up(window, email, password, confirm_password):

    if email == "" or password == "" or confirm_password == "":
        QMessageBox.warning(window, "incorrect input", "Fields can not be empty!")
        return

    if not password == confirm_password:
        QMessageBox.warning(window, "passwords do not match up", "Please make sure that the password is the same as the confirm!")
        return

    if not is_valid_email(email):
        QMessageBox.warning(window, "not a valid email", "Please make sure to enter a valid email!")
        return
    

    confirm_password = ""

    password = en_decrypt.numbers_in_text(en_decrypt.oneHash(password))
    
    already_exists = False
    email = en_decrypt.encrypt(email, email_key)


    if os.path.isdir(f"data/{email}") or os.path.isfile(f"data/{email}/{email}"):
        already_exists = True
    

    if already_exists:
        QMessageBox.information(window, "email exists", "This email exists already!")
        return
    

    os.mkdir(f"data/{email}")
    with open(f"data/{email}/{email}", "w", encoding="utf-8") as f:
        f.write(password)
    
    

    QMessageBox.information(window, "Success!", "The account has been created!")
   
def change(app, window, email, key, new_email, new_password):
    user_input, has_verified = QInputDialog.getText(window, "verify", "Enter your current password:", QLineEdit.Password)
    if not has_verified:
        return
    if user_input == "":
        QMessageBox.warning(window, "invalid input", "Please enter your current password!")
        return
    
    file = open(f"data/{email}/{email}", "r", encoding="utf-8")
    saved_password = file.read()
    file.close()
    if not en_decrypt.numbers_in_text(en_decrypt.oneHash(user_input)) == saved_password:
        QMessageBox.warning(window, "invalid input", "Please enter your current password!")
        return
    old_password = user_input
    user_input = ""
    
    if not is_valid_email(new_email):
        QMessageBox.warning(window, "invalid input", "PLease make sure your new email is a valid email!")
        return
    
    data_dir = os.listdir("data")
    if en_decrypt.encrypt(new_email, email_key) in data_dir and not new_email == en_decrypt.decrypt(email, email_key):
        QMessageBox.warning(window, "invalid input", f"{new_email} already has an account!")
        return
    
    has_new_email = True
    has_new_password = True
    
    if (new_password == "*" * 10 or new_password == "" or new_password == old_password) \
            and (new_email == en_decrypt.decrypt(email, email_key) or new_email == ""):
        QMessageBox.warning(window, "no new values", "There are no new values to save.")
        return
    if new_password == "*" * 10 or new_password == "" or new_password == old_password:
        QMessageBox.information(window, "Info", "Please note that the password will not change.")
        has_new_password = False
    if new_email == en_decrypt.decrypt(email, email_key) or new_email == "":
        QMessageBox.information(window, "Info", "Please note that the email will not change.")
        has_new_email = False
    
    if has_new_password and not has_new_email:
        with open(f"data/{email}/{email}", "w", encoding="utf-8") as file:
            file.write(en_decrypt.numbers_in_text(en_decrypt.oneHash(new_password)))
            
        new_key = en_decrypt.numbers_in_text(en_decrypt.twoOneKey(en_decrypt.decrypt(email, email_key), new_password))
        
        data_dir = os.listdir(f"data/{email}")
        for file_name in data_dir:
            if file_name == email:
                continue
            circel(email, new_key, key, file_name)
            
        QMessageBox.information(window, "Success!", "Your password was updated!")
        window.hide()
        index.start(app)
        return

    if has_new_email:
        en_email = en_decrypt.encrypt(new_email, email_key)
        os.mkdir(f"data/{en_email}")
        
        if not has_new_password:
            new_password = old_password
        
        hash_new_password = en_decrypt.numbers_in_text(en_decrypt.oneHash(new_password))
        
        with open(f"data/{en_email}/{en_email}", "w", encoding="utf-8") as file:
            file.write(hash_new_password)
        
        new_key = en_decrypt.numbers_in_text(en_decrypt.twoOneKey(new_email, new_password))
        
        data_dir = os.listdir(f"data/{email}")
        for file_name in data_dir:
            if file_name == email:
                continue
            circel(email, new_key, key, file_name, new_email=en_email)
        shutil.rmtree(f"data/{email}")
        QMessageBox.information(window, "Success!", "Your account was updated!")
        window.hide()
        index.start(app)
        return
    
    
def circel(old_email, new_key, key, file_name, new_email: str = None):
    file = open(f"data/{old_email}/{file_name}", "r", encoding="utf-8")
    lines = file.readlines()
    file.close()
    
    if new_email is None:
        new_email = old_email
    
    sub_key = en_decrypt.twoOneKey(file_name, key)
    
    if int(lines[1]) > 0:
        old_sub_username = en_decrypt.decrypt(lines[2][:int(lines[1][:-1])], sub_key)
    else:
        old_sub_username, new_sub_username = "", ""
    if int(lines[0][:-1]) > 0:
        old_sub_email = en_decrypt.decrypt(lines[2][int(lines[1][:-1]):int(lines[1][:-1]) + int(lines[0][:-1])], sub_key)
    else:
        old_sub_email, new_sub_email = "", ""
    old_sub_password = en_decrypt.decrypt(lines[2][int(lines[1][:-1]) + int(lines[0][:-1]):], sub_key)
    
    sub_key = en_decrypt.twoOneKey(file_name, new_key)
    
    username_len = len(old_sub_username)
    email_len = len(old_sub_email)
    
    if username_len > 0:
        new_sub_username = en_decrypt.encrypt(old_sub_username, sub_key)
    if email_len > 0:
        new_sub_email = en_decrypt.encrypt(old_sub_email, sub_key)
    new_sub_password = en_decrypt.encrypt(old_sub_password, sub_key)
    
    with open(f"data/{new_email}/{file_name}", "w", encoding="utf-8") as file:
        file.write(f"{email_len}\n{username_len}\n{new_sub_username}{new_sub_email}{new_sub_password}")
        
        


   
def delete(email, window):
    user_input, has_verified = QInputDialog.getText(window, "verify", "Enter your password:", QLineEdit.Password)
    if not has_verified:
        return
    if user_input == "":
        QMessageBox.warning(window, "invalid input", "Please enter your password!")
        return
    file = open(f"data/{email}/{email}", "r", encoding="utf-8")
    password = file.read()
    file.close()
    
    user_input = en_decrypt.numbers_in_text(en_decrypt.oneHash(user_input))
    
    if user_input != password:
        QMessageBox.warning(window, "invalid input", "Please enter your password!")
        return
    password = ""
    user_input = ""
    shutil.rmtree(f"data/{email}")
    QMessageBox.information(window, "Success", "Your account was successfully deleted!")
    sys.exit()
   
def delete_sub_acc(app, window, email, key, sub_name):
    user_input, has_verified = QInputDialog.getText(window, "verify", "Enter your password:", QLineEdit.Password)
    if not has_verified:
        return
    if user_input == "":
        QMessageBox.warning(window, "invalid input", "Please enter your password!")
        return
    file = open(f"data/{email}/{email}", "r", encoding="utf-8")
    password = file.read()
    file.close()
    
    user_input = en_decrypt.numbers_in_text(en_decrypt.oneHash(user_input))
    
    if user_input != password:
        QMessageBox.warning(window, "invalid input", "Please enter your password!")
        return
    password = ""
    user_input = ""
    os.remove(f"data/{email}/{sub_name}")
    QMessageBox.information(window, "Success!", f"{sub_name} was deleted!")
    home.start(app, window, email, key)

def actions_sub_acc(app, window, email, key, sub_name, sub_username, sub_email, sub_password, acc: str = None):
    if sub_name == "" or sub_password == "":
        QMessageBox.warning(window, "invalid input", "Fields marked with * must not be empty!")
        return
    if acc is None:
        if os.path.isfile(f"data/{email}/{sub_name}"):
            QMessageBox.warning(window, "invalid input", "The name must be unique!")
            return
    else:
        if os.path.isfile(f"data/{email}/{sub_name}") and sub_name != acc:
            QMessageBox.warning(window, "invalid input", "The name must be unique!")
            return
    
    email_len = len(sub_email)
    username_len = len(sub_username)
    
    sub_key = en_decrypt.twoOneKey(sub_name, key)
    
    if email_len > 0:
        if not is_valid_email(sub_email):
            QMessageBox.warning(window, "not a valid email", "Please make sure to enter a valid email!")
            return
        sub_email = en_decrypt.encrypt(sub_email, sub_key)
    if username_len > 0:
        sub_username = en_decrypt.encrypt(sub_username, sub_key)
    
    sub_password = en_decrypt.encrypt(sub_password, sub_key)
    
    
    with open(f"data/{email}/{sub_name}", "w", encoding="utf-8") as file:
        file.write(f"{email_len}\n{username_len}\n{sub_username}{sub_email}{sub_password}")
    
    if acc is None:
        QMessageBox.information(window, "Success!", f"{sub_name} was created!")
    else:
        QMessageBox.information(window, "Success!", f"{sub_name} was changed!")
    
    home.start(app, window, email, key)
        