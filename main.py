from GUI import index
import os
import sys
from PyQt5.QtWidgets import QApplication



if __name__ == "__main__":
    app = QApplication(sys.argv)
    index.start(app)
    sys.exit(0)
