'''
gestion clientes
'''
import clients
import var,event
from window import *
from PyQt5.QtWidgets import QMessageBox

class Clientes():
    def validarDNI():
        try:
            global control
            control=0
            dni= var.ui.txtDNI.text()
            tabla="TRWAGMYFPDXBNJZSQVHLCKE" #Letra DNI
            dig_ext= "XYZ"  #DIGITO EXTRANJEROS
            reemp_dig_ext= {"X":0,"Y":1,"Z":2}
            numeros= "1234567890"
            dni= dni.upper()
            if len(dni)==9:
                dig_control= dni[8]
                dni=dni[:8]
                if dni[0] in dig_ext:
                    dni= dni.replace(dni[0],reemp_dig_ext(dni[0]))
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni)%23] == dig_control:
                    control=1
                    var.ui.ValidarDNI.setStyleSheet ("QLabel{color:green;}")
                    var.ui.ValidarDNI.setText("Menudo cumbiote ")
                    var.ui.txtDNI.setStyleSheet("background-color: green;")
                else:

                    var.ui.ValidarDNI.setStyleSheet("QLabel{color:red;}")
                    var.ui.ValidarDNI.setText("La erraste pendejo")
                    var.ui.txtDNI.setStyleSheet("background-color: rgb(255, 155, 90);")
            else:

                var.ui.ValidarDNI.setStyleSheet("QLabel{color:red;}")
                var.ui.ValidarDNI.setText("Aprende a escribir amigo")
                var.ui.txtDNI.setStyleSheet("background-color: rgb(255, 155, 90);")


        except Exception as error: print("Error en modulo validarDNI")

    def selGen(self):
        try:
            if var.ui.rbtFem.isChecked():
                print("marcaste muhe")
            if var.ui.rbtHom.isChecked():
                print("marcaste simio")
            if var.ui.rbtOtro.isChecked():
                print("marcaste other")


        except Exception as error: print("Error en modulo selGen")









    def cargaProv(self):
        try:
            var.ui.cmbProv.clear()
            prov=[" ","A Coruña","Lugo","Ourense","Pontevedra","Vigo"]
            for i in prov:
                var.ui.cmbProv.addItem(i)

        except Exception as error: print("Error en modulo cargaProv")

    def selProv(prov):
        try:
            clients.Clientes.cargaMun(prov)
        except Exception as error: print("Error en modulo selProv")

    def cargaMun(prov):
        try:
            var.ui.cmbMun.clear()
            if prov == "Vigo":
                mun=[" ","Vigo","Redondela","Ponteareas","Cangas"]
            if prov == "A Coruña":
                mun=[" ","A Coruña","Ferrol","Betanzos","Santiago"]
            if prov == "Pontevedra":
                mun=[" ","Pontevedra","Moaña","Lalín","A Cañiza"]
            if prov == "Ourense":
                mun=[" ","Ourense","O Barco","Monforte","Verin"]
            if prov== "Lugo":
                mun=[" ","Lugo","Sarria","Villalba","Ribadeo"]
            for i in mun:
                var.ui.cmbMun.addItem(i)
        except Exception as error: print("Error en modulo cargaMun")




    def cargarFecha(qDate):
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(),qDate.month(),qDate.year()))
            var.ui.txtFecha.setText(str(data))
            var.dlgcalendar.hide()

        except Exception as error: print("Error en modulo cargarFecha")

    def capitalizar():
        try:
            nombre=var.ui.txtNombre.text()
            var.ui.txtNombre.setText(nombre.title())
            apel = var.ui.txtApel.text()
            var.ui.txtApel.setText(apel.title())
            dir = var.ui.txtDir.text()
            var.ui.txtDir.setText(dir.title())


        except Exception as error: print("Error en modulo capitalizar")
    def avisoDNI(self):
        QMessageBox.about(self, "ERROR", "DNI incorrecto")

    def GuardaClie(self):

        try:
            Clientes.validarDNI()
            if control == 1:
                #Preparamos el registro
                newcli=[] #Para la base de datos
                tabcli=[] #Para tableview
                client= [var.ui.txtDNI,var.ui.txtApel,var.ui.txtNombre,var.ui.txtFecha]
                for i in client:
                    tabcli.append(i.text())
                pagos=[]
                if var.ui.PagoCuenta.isChecked():
                    pagos.append("Cargo cuenta")
                if var.ui.PagoEfectivo.isChecked():
                    pagos.append("Pago Efectivo")
                if var.ui.PagoTarjeta.isChecked():
                    pagos.append("Pago Tarjeta")
                if var.ui.PagoTransfer.isChecked():
                    pagos.append("Pago por transferencia")

                pagos=set(pagos)
                tabcli.append("; ".join(pagos))
                #Cargamos en la tabla
                row=0
                column=0
                var.ui.tabClientes.insertRow(row)
                for campo in tabcli:
                    cell = QtWidgets.QTableWidgetItem(str(campo))
                    var.ui.tabClientes.setItem(row,column,cell)
                    column +=1
            else:
                msg=QtWidgets.QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("DNI INCORRECTO")
                msg.exec()


        except Exception as error: print("Error en modulo GuardaClie")

    def CargaCli(self):
        try:
            fila=var.ui.tabClientes.selectedItems()
            datos=[var.ui.txtDNI,var.ui.txtApel,var.ui.txtNombre,var.ui.txtFecha]
            if fila:
                row=[dato.text() for dato in fila]
            for i, dato in enumerate(datos):
                dato.setText(row[i])
                if i==5:
                    pass

        except Exception as error: print("Error en modulo CargaCli")
