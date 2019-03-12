from app.Model import Model
from app.ui import Ui

from PyQt5 import QtWidgets

qApp = QtWidgets.QApplication([])

ui = Ui()
qApp.exec()


#model = Model()
#model.fromTwoFiles('data.TXT', 'ref.TXT')