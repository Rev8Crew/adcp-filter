import sys
from PyQt5.QtWidgets import QApplication

from app.ui import Ui

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = Ui(app)

    sys.exit(app.exec_())