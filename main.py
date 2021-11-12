# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from time import strftime, gmtime

import clients
from window import *
from windowaviso import *
from windowcal import *
from datetime import *
import sys,var,event,conexion,locale
locale.setlocale(locale.LC_ALL,'es-ES')


class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir,self).__init__()








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

        var.ui.rbtGroupGen.buttonClicked.connect(clients.Clientes.selGen)
        var.ui.btFecha.clicked.connect(event.Eventos.abrirCal)

        var.ui.btnGuardaClie.clicked.connect(clients.Clientes.GuardaClie)
        var.ui.btnGuardaClie.clicked.connect(event.Eventos.ClearForm)


        var.ui.btnModifCli.clicked.connect(clients.Clientes.modifCli)
        var.ui.btnModifCli.clicked.connect(event.Eventos.ClearForm)

        var.ui.btnEliminarCli.clicked.connect(conexion.Conexion.DelCli)


        var.ui.btnLimpiar.clicked.connect(event.Eventos.ClearForm)
        '''
        Barra de menús y herramientas
        '''
        var.ui.actionSalir.triggered.connect(event.Eventos.Salir)
        var.ui.actionAbrir.triggered.connect(event.Eventos.Abrir)
        var.ui.actionCrearBackup.triggered.connect(event.Eventos.crearBackup)
        var.ui.actionRestaurarBD.triggered.connect(event.Eventos.RestaurarDB)

        '''
        comprobar el dni
        '''

        var.ui.txtDNI.editingFinished.connect(clients.Clientes.validarDNI)
        var.ui.txtNombre.editingFinished.connect(clients.Clientes.capitalizar)
        var.ui.txtApel.editingFinished.connect(clients.Clientes.capitalizar)
        var.ui.txtDir.editingFinished.connect(clients.Clientes.capitalizar)


        '''
        Eventos combobox
        '''

        var.ui.cmbProv.activated[str].connect(conexion.Conexion.CargaMun)
        '''
        
        Barra de estado
        
        '''
        var.ui.statusbar.addPermanentWidget(var.ui.lblStat,1)
        fecha=date.today().strftime("%A %d de %B de %Y")
        var.ui.lblStat.setText(fecha.capitalize())


        '''
        Eventos barra herramientas
        '''
        var.ui.actionactbarSalir.triggered.connect(event.Eventos.Salir)
        var.ui.actionactbarAbrir.triggered.connect(event.Eventos.Abrir)
        var.ui.actionactbarcrearbackup.triggered.connect(event.Eventos.crearBackup)
        var.ui.actionactbarrestaurarbackup.triggered.connect(event.Eventos.RestaurarDB)
        var.ui.actionactbarimprimir.triggered.connect(event.Eventos.Imprimir)
        '''
        Eventos QTableWidget
        '''
        event.Eventos.resizeTablaCli(self)
        var.ui.tabClientes.clicked.connect(clients.Clientes.CargaCli)
        var.ui.tabClientes.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        '''
        Base de datos
        '''
        conexion.Conexion.db_connect(var.filedb)
        conexion.Conexion.cargarTablaCli(self)
        conexion.Conexion.CargaProv(self)

if __name__ =="__main__":
    app=QtWidgets.QApplication([])
    window=Main()
    desktop=QtWidgets.QApplication.desktop()
    x=(desktop.width()-window.width())//2
    y = (desktop.height() - window.height()) // 2
    window.move(x,y)
    var.dlgaviso=DialogAviso()
    var.dlgcalendar=DialogCalendar()
    var.dlgabrir=FileDialogAbrir()
    window.show()
    sys.exit(app.exec())
