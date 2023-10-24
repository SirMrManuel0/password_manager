from GUI import standards # Import a module from the GUI package
from scripts import accounts # Import a module from the scripts package
import sys
from PyQt5.QtWidgets import * # Import various classes and functions from PyQt5
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import os

# Define a function named 'start' that takes an 'app' parameter
def start(app):
    """
    Start the application and display the main window.

    Args:
        app: The PyQt5 application instance.

    Returns:
        None
    """
    # Create a manager_window object and show it
    index_window = standards.manager_window(app)
    index_window.show()
    # Set the layout for the index_window
    index_window.setLayout(index_layout(app, index_window))


# Define a function named 'index_layout' that takes 'app' and 'window' parameters
def index_layout(app, window):
    """
    Create the layout for the main window.

    Args:
        app: The PyQt5 application instance.
        window: The main window instance.

    Returns:
        The layout for the main window.
    """
    layout = QHBoxLayout() # Create a horizontal layout

    left_side = QWidget()
    layout.addWidget(left_side, 170) # Add left_side to the layout
    
    

    middle_side = QWidget()
    middle_layout = QVBoxLayout() # Create a vertical layout for the middle side

    

    middle_widget(app, middle_layout, window) # Call the 'middle_widget' function
    
    

    middle_side.setLayout(middle_layout)
    layout.addWidget(middle_side, 100) # Add middle_side to the layout
    
    right_side = QWidget()
    layout.addWidget(right_side, 30) # Add right_side to the layout
    
    
    return layout # Return the created layout


def middle_widget(app, middle_layout, window):
    """
    Create and populate the middle widget with login and signup elements.

    Args:
        app: The PyQt5 application instance.
        middle_layout: The layout of the middle widget.
        window: The main window instance.

    Returns:
        None
    """
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
    
    # Create widgets for the login screen
    label = QLabel("LOGIN")
    email_field = QLineEdit()
    password_field = QLineEdit()
    password_field.setEchoMode(QLineEdit.Password)
    login_button = QPushButton("login")
    signup_button = QPushButton("sign up")
    
    # Set placeholder text for input fields
    email_field.setPlaceholderText("Enter your email")
    password_field.setPlaceholderText("Enter your password")
    
    # Change the font for various widgets
    font = QFont("BIZ UDPMincho Medium", 36)
    label.setFont(font)
    email_field.setFont(font)
    password_field.setFont(font)
    login_button.setFont(font)
    signup_button.setFont(font)

    email_field.setFocus()
    
    
    # Add widgets to the middle-side layout
    middle_layout.addWidget(label)
    middle_layout.addWidget(email_field)
    middle_layout.addWidget(password_field)
    middle_layout.addWidget(login_button)
    middle_layout.addWidget(signup_button)

    middle_layout.addStretch(1)
    
    # Define button click actions
    login_button.clicked.connect(lambda: accounts.login(app, window, email_field.text(), password_field.text()))
    signup_button.clicked.connect(lambda: signup_window(app, middle_layout, window))




# Define a function named 'signup_window' that takes 'app', 'middle_layout', and 'window' parameters
def signup_window(app, middle_layout, window):
    """
    Create and populate the signup window.

    Args:
        app: The PyQt5 application instance.
        middle_layout: The layout of the middle widget.
        window: The main window instance.

    Returns:
        None
    """
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
    
    # Set echo mode for password fields
    password_field.setEchoMode(QLineEdit.PasswordEchoOnEdit)
    confirm_password_field.setEchoMode(QLineEdit.PasswordEchoOnEdit)

    
    
    # Set placeholder text for input fields
    email_field.setPlaceholderText("Enter your email")
    password_field.setPlaceholderText("Enter your password")
    confirm_password_field.setPlaceholderText("Confirm your password")

    # Change the font for various widgets
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
    
    # Define button click actions
    cancel_button.clicked.connect(lambda: middle_widget(app, middle_layout, window))
    signup_button.clicked.connect(lambda: accounts.sign_up(window, email_field.text(), password_field.text(), confirm_password_field.text()))
