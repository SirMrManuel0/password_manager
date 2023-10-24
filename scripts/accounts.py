# Import necessary PyQt5 modules and other required libraries
from PyQt5.QtWidgets import *
import re
from scripts import en_decrypt
from GUI import home
from GUI import index
import os
import shutil
import sys

# List of characters used for email encryption and decryption
email_key = ['1', '714', '193', '126', '182', '512', '237', '112', '379', '466', '746', '669', '835', '934', '864', '273', '195', '252', '436',
                 '949', '899', '696', '054', '189', '440', '670', '190', '110', '108', '853', '285', '961', '492', '264', '694', '144', '506', '650',
                 '265', '761', '596', '780', '975', '146', '392', '433', '686', '414', '491', '944', '862', '609', '361', '798', '133', '555', '464',
                 '639', '395', '481', '767', '741', '994', '337', '958', '801', '134', '002', '563', '578', '465', '954', '778', '438','761', '539']


# Function to check if an email is valid
def is_valid_email(email):
    """
    Check if the given email is valid.

    Args:
        email (str): The email to be checked for validity.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.fullmatch(email_pattern, email) and email[email.find("@"):].find("..") < 0:
        return True
    else:
        return False

# Function for user login
def login(app, window, email, password):
    """
    Log in the user with the provided email and password.

    Args:
        app: The PyQt5 application object.
        window: The current application window.
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        None
    """

    # Check for empty email or password fields
    if email == "" or password == "":
        QMessageBox.warning(window, "incorrect input", "email and password can not be empty!")
        return

    # Check if the entered email is valid
    if not is_valid_email(email):
        QMessageBox.warning(window, "not a valid email", "Please make sure to enter a valid email!")
        return
    
    # Encrypt and hash the password
    password_check = en_decrypt.numbers_in_text(en_decrypt.oneHash(password))
    email = en_decrypt.encrypt(email, email_key)
    
    
    # Check if the user exists in the data directory
    if not os.path.isdir(f"data/{email}") and not os.path.isfile(f"data/{email}/{email}"):
        QMessageBox.warning(window, "user not found", "Please make sure to enter the email of an existing account!")
        return

    # Read the saved password and compare it with the entered password
    file = open(f"data/{email}/{email}", "r", encoding="utf-8")
    saved_password = file.read()
    
    if password_check == saved_password:
        password_check = ""
        saved_password = ""
        # Call the home.start function for successful login
        home.start(app, window, email, en_decrypt.numbers_in_text(en_decrypt.twoOneKey(en_decrypt.decrypt(email, email_key), password)))
        return


    QMessageBox.warning(window, "wrong password or email", "Please make sure to enter the right email and password!")
    return

# Function for user sign-up
def sign_up(window, email, password, confirm_password):
    """
    Create a new user account with the provided email and password.

    Args:
        window: The current application window.
        email (str): The user's email.
        password (str): The user's password.
        confirm_password (str): The confirmation of the user's password.

    Returns:
        None
    """

    # Check for empty email, password, or confirm_password fields
    if email == "" or password == "" or confirm_password == "":
        QMessageBox.warning(window, "incorrect input", "Fields can not be empty!")
        return

    # Check if password and confirm_password match
    if not password == confirm_password:
        QMessageBox.warning(window, "passwords do not match up", "Please make sure that the password is the same as the confirm!")
        return

    # Check if the entered email is valid
    if not is_valid_email(email):
        QMessageBox.warning(window, "not a valid email", "Please make sure to enter a valid email!")
        return
    

    confirm_password = ""

    # Hash the password
    password = en_decrypt.numbers_in_text(en_decrypt.oneHash(password))
    
    already_exists = False
    email = en_decrypt.encrypt(email, email_key)

    # Check if the user already exists
    if os.path.isdir(f"data/{email}") or os.path.isfile(f"data/{email}/{email}"):
        already_exists = True
    

    if already_exists:
        QMessageBox.information(window, "email exists", "This email exists already!")
        return
    
    # Create a new user directory and store the hashed password
    os.mkdir(f"data/{email}")
    with open(f"data/{email}/{email}", "w", encoding="utf-8") as f:
        f.write(password)
    
    

    QMessageBox.information(window, "Success!", "The account has been created!")

# Function to change user account details
def change(app, window, email, key, new_email, new_password):
    """
    Change user account information, including email and password.

    Args:
        app: The PyQt5 application object.
        window: The current application window.
        email (str): The user's current email.
        key (str): The encryption key for the user.
        new_email (str): The new email to set (optional).
        new_password (str): The new password to set (optional).

    Returns:
        None
    """
    
    user_input, has_verified = QInputDialog.getText(window, "verify", "Enter your current password:", QLineEdit.Password)
    if not has_verified:
        return
    if user_input == "":
        QMessageBox.warning(window, "invalid input", "Please enter your current password!")
        return
    
    file = open(f"data/{email}/{email}", "r", encoding="utf-8")
    saved_password = file.read()
    file.close()
    
    # Check if the entered current password matches the saved password
    if not en_decrypt.numbers_in_text(en_decrypt.oneHash(user_input)) == saved_password:
        QMessageBox.warning(window, "invalid input", "Please enter your current password!")
        return
    old_password = user_input
    user_input = ""
    
    # Check if the new email is valid
    if not is_valid_email(new_email):
        QMessageBox.warning(window, "invalid input", "PLease make sure your new email is a valid email!")
        return
    
    data_dir = os.listdir("data")
    # Check if the new email already has an account
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
    
# Function to update data for a sub-account
def circel(old_email, new_key, key, file_name, new_email: str = None):
    """
    Update encryption for a specific file when changing user information.

    Args:
        old_email (str): The old email.
        new_key (str): The new encryption key.
        key (str): The encryption key.
        file_name (str): The name of the file to update.
        new_email (str): The new email to set (optional).

    Returns:
        None
    """
    
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
        
        


# Function to delete the user's account
def delete(email, window):
    """
    Delete a user account.

    Args:
        email (str): The email of the user to delete.
        window: The current application window.

    Returns:
        None
    """
    
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
    
    # Check if the entered password matches the saved password
    if user_input != password:
        QMessageBox.warning(window, "invalid input", "Please enter your password!")
        return
    password = ""
    user_input = ""
    # Delete the user's account directory
    shutil.rmtree(f"data/{email}")
    QMessageBox.information(window, "Success", "Your account was successfully deleted!")
    sys.exit()

# Function to delete a sub-account
def delete_sub_acc(app, window, email, key, sub_name):
    """
    Delete a sub-account associated with a user.

    Args:
        app: The PyQt5 application object.
        window: The current application window.
        email (str): The user's email.
        key (str): The encryption key for the user.
        sub_name (str): The name of the sub-account to delete.

    Returns:
        None
    """
    
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
    
    # Check if the entered password matches the saved password
    if user_input != password:
        QMessageBox.warning(window, "invalid input", "Please enter your password!")
        return
    password = ""
    user_input = ""
    # Remove the sub-account file
    os.remove(f"data/{email}/{sub_name}")
    QMessageBox.information(window, "Success!", f"{sub_name} was deleted!")
    home.start(app, window, email, key)

# Function to add or update data for a sub-account
def actions_sub_acc(app, window, email, key, sub_name, sub_username, sub_email, sub_password, acc: str = None):
    """
    Perform actions on sub-accounts, such as creating or updating them.

    Args:
        app: The PyQt5 application object.
        window: The current application window.
        email (str): The user's email.
        key (str): The encryption key for the user.
        sub_name (str): The name of the sub-account.
        sub_username (str): The username for the sub-account.
        sub_email (str): The email for the sub-account.
        sub_password (str): The password for the sub-account.
        acc (str): The name of the sub-account to update (optional).

    Returns:
        None
    """
    
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
        