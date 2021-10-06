# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from window import *

import sys,var,event



class Main (QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui= Ui_MainWindow()
        var.ui.setupUi(self)
        '''
        Eventos de botón
        '''
        var.ui.btnSalir.clicked.connect(event.Eventos.Salir)
        '''
        Barra de menu
        '''
        var.ui.actionSalir.triggered.connect(event.Eventos.Salir)
if __name__ =="__main__":
    app=QtWidgets.QApplication([])
    window=Main()
    window.show()
    sys.exit(app.exec())
