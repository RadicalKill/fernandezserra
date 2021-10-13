# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import clients
from window import *
from windowaviso import *
import sys,var,event


class DialogAviso(QtWidgets.QDialog):
    def __init__(self):

        super(DialogAviso,self).__init__()
        var.dlgaviso= Ui_Dialog()
        var.dlgaviso.setupUi(self)


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

        '''
        comprobar el dni
        '''

        var.ui.txtDNI.editingFinished.connect(clients.Clientes.validarDNI)

        '''
        Eventos de género
        '''
        var.ui.rbtGroupGen.buttonClicked.connect(clients.Clientes.selGen)
        '''
        Eventos de forma de pago
        '''

        var.ui.rbtGroupPago.buttonClicked.connect(clients.Clientes.selPago)

        '''
        Eventos combobox
        '''
        clients.Clientes.cargaProv(self)
        var.ui.cmbProv.activated[str].connect(clients.Clientes.selProv)
        var.ui.cmbMun.activated[str].connect(clients.Clientes.selMun)

if __name__ =="__main__":
    app=QtWidgets.QApplication([])
    window=Main()
    var.dlgaviso=DialogAviso()
    window.show()
    sys.exit(app.exec())
