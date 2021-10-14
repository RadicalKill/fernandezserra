# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import clients
from window import *
from windowaviso import *
from windowcal import *
from datetime import *
import sys,var,event





class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogCalendar,self).__init__()
        var.dlgcalendar=Ui_windowcal()
        var.dlgcalendar.setupUi(self)
        diaactual= datetime.now().day
        mesactual= datetime.now().month
        anoactual=datetime.now().year
        var.dlgcalendar.calendario.setSelectedDate(QtCore.QDate(anoactual,mesactual,diaactual))
        var.dlgcalendar.calendario.clicked.connect(clients.Clientes.cargarFecha)

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
        var.ui.rbtGroupPago.buttonClicked.connect(clients.Clientes.selPago)
        var.ui.rbtGroupGen.buttonClicked.connect(clients.Clientes.selGen)
        var.ui.btFecha.clicked.connect(event.Eventos.abrirCal)
        '''
        Barra de menu
        '''
        var.ui.actionSalir.triggered.connect(event.Eventos.Salir)

        '''
        comprobar el dni
        '''

        var.ui.txtDNI.editingFinished.connect(clients.Clientes.validarDNI)




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
    var.dlgcalendar=DialogCalendar()
    window.show()
    sys.exit(app.exec())
