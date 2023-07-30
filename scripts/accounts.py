from PyQt5.QtWidgets import *
import re
from scripts import en_decrypt
import secrets
from GUI import home

def is_valid_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.fullmatch(email_pattern, email) and email[email.find("@"):].find("..") < 0:
        return True
    else:
        return False

def login(window, email, password):
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
    
    file = open("data/accs", "r", encoding="utf-8")
    lines = file.readlines()
    file.close()
    
    email_at = ""
    for i in range(0, len(lines) - 1):
        if en_decrypt.decrypt(lines[i][:-1], email_key) == email:
            email_at = i
            break
    if email_at == "":
        QMessageBox.warning(window, "wrong email", "Please make sure to enter the right email!")
        return
    next_email_at = ""
    for i in range(email_at + 1, len(lines)):
        if is_valid_email(en_decrypt.decrypt(lines[i][:-1], email_key)):
            next_email_at = i
            break
    if next_email_at == "":
        next_email_at = len(lines)
    saved_password = ""
    if email_at + 1 == next_email_at - 1:
        saved_password = lines[next_email_at - 1][:-1]
    else:
        for i in range(email_at + 1, next_email_at - 1):
            saved_password += lines[i][:-1]
    
    
    
    if en_decrypt.numbers_in_text(en_decrypt.master_key_maker(password)) == saved_password:
        home.start(email, password)
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
    if not secrets.compare_digest(password, confirm_password):
        QMessageBox.warning(window, "passwords do not match up", "Please make sure that the password is the same as the confirm!")
        return
    if not is_valid_email(email):
        QMessageBox.warning(window, "not a valid email", "Please make sure to enter a valid email!")
        return
    
    password = en_decrypt.numbers_in_text(en_decrypt.master_key_maker(password))
    
    already_exists = False
    
    file = open("data/accs", "r", encoding="utf-8")
    lines = file.readlines()
    file.close()
    for i in range(0, len(lines) - 1):
        if en_decrypt.decrypt(lines[i][:-1], email_key) == email:
            already_exists = True
            break
    
    if already_exists:
        QMessageBox.information(window, "email exists", "This email exists already!")
        return
    email = en_decrypt.encrypt(email, email_key)
    with open("data/accs", "a", encoding="utf-8") as f:
        f.write(f"{email}\n{password}\n")
    
    
    QMessageBox.information(window, "Success!", "The account has been created!")
    
    
        

    
    
    
    