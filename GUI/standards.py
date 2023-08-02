import sys
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import *
import os


def manager_window(app):
    
    window = QWidget()
    window.setWindowTitle("Password Manager")
    
    window_icon = QIcon("img/icon_blue.png")
    window.setWindowIcon(window_icon)
    
    
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















def apply_theme(app):
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