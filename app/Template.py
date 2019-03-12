from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import *
class Template:

    set_base = "settings/basic"

    templates = {}
    mainWindow = None
    def __init__(self, mW ):
        self.mainWindow = mW
        self.settings = QSettings()
        # Load Basic Templates
        basic = self.settings.value(self.set_base, "", type=str)

        if ( len(basic) < 3 ):
            self.add( self.set_base, "N,shirota, dolgota,distance,speed,depth,...(n)")

        self.addToBar()

    def add(self, name : str, template : str):
        self.settings.setValue(name, template)
        self.settings.sync()

    def ShowBasic(self):
        self.mainWindow.getTextEdit().setText("BasicTemplate:: N,shirota, dolgota,distance,speed,depth,...(n)")

    def addToBar(self):
        self.mainWindow.AddMenuSep("Шаблон")
        self.mainWindow.AddMenuSub("Шаблон", "BasicRef", "...", self.ShowBasic)




