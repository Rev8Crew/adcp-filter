from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from PyQt5 import uic

from PyQt5.QtCore import QSettings

from app.Template import Template
from app.Validator import Validator

from app.Model import Model

class Ui (QMainWindow):

    parent = False
    def __init__(self, app:QApplication):
        super(Ui, self).__init__()

        self.parent = app

        self.model = Model(n=50)
        self.ui = uic.loadUi('MainWindow.ui', self)

        self.ui.openFile.clicked.connect(self.onOpenFile)
        self.ui.exec.clicked.connect(self.Exec)

        self.ui.center()
        self.ui.setWindowIcon(QIcon('web.jpg'))

        self.init_menu()
        self.statusBar().showMessage('Готов к работе...')

        self.show()

    menuActions = {}
    menuSubActions = {}

    def onOpenFile(self):
        self.statusBar().showMessage('Выберите файл...')
        settings = QSettings()

        ref = settings.value( 'settings/ref', '', type=str)
        data = settings.value( 'settings/data', '', type=str)

        if Validator.fileExist(ref) and Validator.fileExist(data):
            question = QMessageBox.question( self, 'Кэш', 'Использовать прошлые файлы, чтобы не выбирать новые? \n{}\n{}'.format(ref,data), QMessageBox.Yes| QMessageBox.No)

            if question == QMessageBox.Yes:
                self.model.set_two_files(data, ref)
                return QMessageBox.information(self, "Успешно", "Теперь можно настраивать ограничения")

        QMessageBox.information(self, "Файл", "Выберите сначала ref файл, а затем data")

        fileRef = QFileDialog.getOpenFileName(self, "Выберите ref файл")[0]
        fileData = QFileDialog.getOpenFileName(self, "Выберите data файл")[0]

        if Validator.fileExist(fileRef) is False or Validator.fileExist(fileData) is False:
            return QMessageBox.warning(self, 'Ошибка', 'Вы не выбрали файл или его не существует')

        settings.setValue('settings/ref', fileRef)
        settings.setValue('settings/data', fileData)

        self.model.set_two_files(fileData, fileRef)
        return QMessageBox.information(self, "Успешно", "Теперь можно настраивать ограничения")


    def Exec(self):
        self.model.set_delete_num(self.ui.deleteLine.text())
        self.model.set_speed_limit(self.ui.speedLine.text())
        self.model.set_average_num(self.ui.averageLine.text())

        ret = False
        try:
            ret = self.model.from_two_files()
        except BaseException as e:
            print(str(e))

        if (ret):
            QMessageBox.information(self, "Успешно", "Операция успешно завершилась")
            self.statusBar().showMessage('Операция успешно завершена')
        else:
            self.statusBar().showMessage('Произошла ошибка')


    def init_menu(self):
        self.ui.addMenuMain("Файл")
        self.ui.AddMenuSub("Файл", "Выход", "exit.png", "close")

        self.setWindowTitle("ADCP. Главное окно")

    def AddMenuSep(self, name):
        self.menuActions[name].addSeparator()

    def addMenuMain(self, name : str):
        self.menuActions[name] = self.menuBar().addMenu(name)

    def AddMenuSub(self, mainPoint : str, name : str, icon : str, connect):
        self.menuSubActions[name] = QAction(QIcon(icon), name, self)

        if ( type(connect) == type("str") and connect == 'close'):
            self.menuSubActions[name].triggered.connect(self.close)
        else:
            self.menuSubActions[name].triggered.connect(connect)

        self.menuActions[mainPoint].addAction(self.menuSubActions[name])

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())