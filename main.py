# Import necessary modules from the GUI package
from GUI import index
from GUI import home

# Import essential operating system and system modules
import os
import sys

# Import required classes and functions from PyQt5
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

# Check if the 'data' directory exists, and create it if not
if not os.path.isdir("data"):
    os.mkdir("data")

# Create a PyQt5 application instance
app = QApplication(sys.argv)

# Start the 'index' module from the GUI package
index.start(app)

# Execute the PyQt5 application
app.exec_()
