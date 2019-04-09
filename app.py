import sys
from PyQt5.QtWidgets import QApplication

from app.ui import Ui

ORGANIZATION_NAME = 'ADCP App'
ORGANIZATION_DOMAIN = 'empty.com'
APPLICATION_NAME = 'QSettings program'

from PyQt5.QtCore import QCoreApplication

if __name__ == '__main__':
    QCoreApplication.setApplicationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)

    app = QApplication(sys.argv)

    ui = Ui(app)

    sys.exit(app.exec_())