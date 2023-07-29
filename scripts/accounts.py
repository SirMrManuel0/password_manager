from PyQt5.QtWidgets import *


def password_check(window, username, password):
    
    if username == "" or password == "":
        QMessageBox.warning(window, "incorrect input", "Username and password can not be empty!")
        return
    
    file = open("data/accs", "r", encoding="utf-8")
    lines = file.readlines()
    file.close()
    
    pass_allowed = False
    
    print(f"{username}: {lines[0][:-1]}\n{password}: {lines[1][:-1]}")
    
    for i in range(0, len(lines) - 1):
        if lines[i][:-1] == username and i % 2 == 0 and lines[i + 1][:-1] == password:
            pass_allowed = True
            break
    
    if not pass_allowed:
        QMessageBox.warning(window, "wrong password or username", "Please make sure to enter the right username and password!")
        return
                
    