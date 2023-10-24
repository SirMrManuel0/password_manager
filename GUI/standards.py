import sys
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import *
import os

# Function to create the main window
def manager_window(app):
    """
    Creates and returns the main window for the password manager application.
    
    Args:
        app (QApplication): The QApplication instance for the application.

    Returns:
        QWidget: The main application window.
    """
    
    window = QWidget()
    window.setWindowTitle("Password Manager")
    
    # Set the window icon
    window_icon = QIcon("img/icon_blue.png")
    window.setWindowIcon(window_icon)
    
    # Apply the theme to the window
    apply_theme(app)
    
    # Get the user's screen dimensions
    desktop = QDesktopWidget().screenGeometry()
    screen_width = desktop.width()
    screen_height = desktop.height()

    # Set the window size relative to the screen dimensions
    window_width = screen_width * 0.687
    window_height = screen_height * 0.679
    window.resize(int(window_width), int(window_height))
    
    return window














# Function to apply the color theme to the application
def apply_theme(app):
    """
    Applies a custom color theme to the application using a style sheet.
    
    Args:
        app (QApplication): The QApplication instance for the application.
    """
    # Define your color theme here
    button_color = "#746426"
    accent_color = "#E15722"
    background_color =  "#15141F"
    text_color = "#FFF"
    accent_color_2 = "#7BA7A4"

    # Set the application's style sheet to customize the color theme
    app.setStyleSheet(
        
        "/* General styles for all widgets */" \
        "* {"\
            "background: " + background_color + ";"\
            "color: " + text_color + ";"\
            "font-size: 14px;"\
        "}"\
        "/* Styles for QPushButton (change QPushButton to other widget types as needed) */"\
        "QPushButton {"\
            "background-color: " + button_color + ";"\
            "border-radius: 5px;"\
            "padding: 5px 10px;"\
        "}"\
        "QPushButton:hover {"\
            "color: white;"\
        "}"\
        "QPushButton:pressed {"\
            "background-color: " + button_color + ";"\
        "}"
        
    )