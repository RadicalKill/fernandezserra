# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from time import strftime, gmtime



import clients
import informes
from window import *
from windowaviso import *
from windowcal import *
from datetime import *
import sys,var,event,conexion,locale,invoice
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
        var.ui.btnBuscar.clicked.connect(conexion.Conexion.buscaCliente)
        var.ui.btnBuscar_Art.clicked.connect(conexion.Conexion.buscaArt)


        var.ui.rbtGroupGen.buttonClicked.connect(clients.Clientes.selGen)
        var.ui.btFecha.clicked.connect(event.Eventos.abrirCal)
        var.ui.btnGuardaClie.clicked.connect(clients.Clientes.GuardaClie)
        var.ui.btnGuardaClie.clicked.connect(event.Eventos.ClearForm)

        var.ui.btnGuardaArt.clicked.connect(clients.Clientes.GuardaProd)
        var.ui.btnGuardaArt.clicked.connect(event.Eventos.ClearFormProd)



        var.ui.btnModifCli.clicked.connect(clients.Clientes.modifCli)
        var.ui.btnModifCli.clicked.connect(event.Eventos.ClearForm)

        var.ui.btnEliminarCli.clicked.connect(conexion.Conexion.DelCli)


        var.ui.btnModifArt.clicked.connect(clients.Clientes.modifProd)
        var.ui.btnModifArt.clicked.connect(event.Eventos.ClearFormProd)

        var.ui.btnEliminarArt.clicked.connect(conexion.Conexion.DelProd)
        var.ui.btnEliminarArt.clicked.connect(event.Eventos.ClearFormProd)


        var.ui.btnLimpiar.clicked.connect(event.Eventos.ClearForm)

        var.ui.btnBuscaClifac.clicked.connect(invoice.Facturas.buscaCli)
        var.ui.btnFechaFac.clicked.connect(event.Eventos.abrirCal)
        var.ui.btnFact.clicked.connect(invoice.Facturas.Facturar)
        var.ui.btnPDFCli.clicked.connect(informes.Informes.listadoClientes)
        var.ui.btnPDFProd.clicked.connect(informes.Informes.listadoProductos)
        '''
        Barra de menús y herramientas
        '''
        var.ui.actionSalir.triggered.connect(event.Eventos.Salir)
        var.ui.actionAbrir.triggered.connect(event.Eventos.Abrir)
        var.ui.actionCrearBackup.triggered.connect(event.Eventos.crearBackup)
        var.ui.actionRestaurarBD.triggered.connect(event.Eventos.RestaurarDB)
        var.ui.actionImprimir.triggered.connect(event.Eventos.Imprimir)
        var.ui.actionImportar_Datos.triggered.connect(event.Eventos.ImportarExcel)
        var.ui.actionExportar_Datos.triggered.connect(event.Eventos.ExportarDatos)

        '''
        comprobar el dni
        '''
        var.ui.txtNomArt.editingFinished.connect(clients.Clientes.capitalizar)
        var.ui.txtDNI.editingFinished.connect(clients.Clientes.validarDNI)
        var.ui.txtNombre.editingFinished.connect(clients.Clientes.capitalizar)
        var.ui.txtApel.editingFinished.connect(clients.Clientes.capitalizar)
        var.ui.txtDir.editingFinished.connect(clients.Clientes.capitalizar)
        var.ui.txtDNIFact.editingFinished.connect(clients.Clientes.validarDNIFac)
        var.txtCantidad = QtWidgets.QLineEdit()
        var.txtCantidad.editingFinished.connect(invoice.Facturas.totalLineaVenta)


        '''
        Eventos combobox
        '''

        var.ui.cmbProv.activated[str].connect(conexion.Conexion.CargaMun)
        var.cmbProducto = QtWidgets.QComboBox()
        var.cmbProducto.currentIndexChanged.connect(invoice.Facturas.procesoVenta)

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
        var.ui.tabClientes.clicked.connect(clients.Clientes.Cargar)
        var.ui.tabClientes.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tabPrograma.currentChanged.connect(event.Eventos.Tab)
        var.ui.tabFact.clicked.connect(clients.Clientes.Cargar)
        var.ui.tabFact.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)


        '''
        Base de datos
        '''
        conexion.Conexion.db_connect(var.filedb)
        conexion.Conexion.cargarTablaCli()
        conexion.Conexion.CargaProv(self)


        '''
        Eventos spin
        '''
        var.ui.spinEnvio.valueChanged.connect(event.Eventos.ControlEnvio)



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
