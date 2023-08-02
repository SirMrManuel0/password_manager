from GUI import index
from GUI import home
import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout


app = QApplication(sys.argv)
index.start(app)
#home.start()
app.exec_()
