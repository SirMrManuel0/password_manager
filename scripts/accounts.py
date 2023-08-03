from PyQt5.QtWidgets import *
import re
from scripts import en_decrypt
from GUI import home
import os


def is_valid_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.fullmatch(email_pattern, email) and email[email.find("@"):].find("..") < 0:
        return True
    else:
        return False


def login(app, window, email, password):

    email_key = ['1', '714', '193', '126', '182', '512', '237', '112', '379', '466', '746', '669', '835', '934', '864', '273', '195', '252', '436',
                 '949', '899', '696', '054', '189', '440', '670', '190', '110', '108', '853', '285', '961', '492', '264', '694', '144', '506', '650',
                 '265', '761', '596', '780', '975', '146', '392', '433', '686', '414', '491', '944', '862', '609', '361', '798', '133', '555', '464',
                 '639', '395', '481', '767', '741', '994', '337', '958', '801', '134', '002', '563', '578', '465', '954', '778', '438','761', '539']
    

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
        home.start(app, window, email, en_decrypt.numbers_in_text(en_decrypt.twoOneHash(en_decrypt.decrypt(email, email_key), password)))
        return


    QMessageBox.warning(window, "wrong password or email", "Please make sure to enter the right email and password!")
    return


def sign_up(window, email, password, confirm_password):

    email_key = ['1', '714', '193', '126', '182', '512', '237', '112', '379', '466', '746', '669', '835', '934', '864', '273', '195', '252', '436',
                 '949', '899', '696', '054', '189', '440', '670', '190', '110', '108', '853', '285', '961', '492', '264', '694', '144', '506', '650',
                 '265', '761', '596', '780', '975', '146', '392', '433', '686', '414', '491', '944', '862', '609', '361', '798', '133', '555', '464',
                 '639', '395', '481', '767', '741', '994', '337', '958', '801', '134', '002', '563', '578', '465', '954', '778', '438','761', '539']
    
    

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
   
def change():
    ...       
   
def delete():
    ...
   
def delete_sub_acc():
    ...

def ange_sub_acc():
    ...