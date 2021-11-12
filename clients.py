'''
gestion clientes
'''
import clients
import conexion
import var,event
from window import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtSql
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
            pass

        except Exception as error: print("Error en modulo selGen")









    def cargaProv(prov):
        try:
            var.ui.cmbProv.clear()

            for i in prov:
                var.ui.cmbProv.addItem(i)

        except Exception as error: print("Error en modulo cargaProv")

    def cargaMun(mun):
        try:
            var.ui.cmbMun.clear()
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
                newcli=[var.ui.txtDNI.text(),var.ui.txtFecha.text(),var.ui.txtApel.text(),var.ui.txtNombre.text(),var.ui.txtDir.text()] #Para la base de datos
                newcli.append(var.ui.cmbProv.currentText())
                newcli.append(var.ui.cmbMun.currentText())
                if var.ui.rbtHom.isChecked():
                    newcli.append('Hombre')
                elif var.ui.rbtFem.isChecked():
                    newcli.append('Mujer')
                elif var.ui.rbtOtro.isChecked():
                    newcli.append('Otro')
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

                newcli.append("; ".join(pagos))


                conexion.Conexion.altaCli(newcli)
                conexion.Conexion.cargarTablaCli(self)
            else:
                msg=QtWidgets.QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("DNI INCORRECTO")
                msg.exec()


        except Exception as error: print("Error en modulo GuardaClie")

    def CargaCli(self):

        try:
            var.ui.PagoCuenta.setChecked(False)
            var.ui.PagoTransfer.setChecked(False)
            var.ui.PagoTarjeta.setChecked(False)
            var.ui.PagoEfectivo.setChecked(False)
            fila=var.ui.tabClientes.selectedItems()


            if fila:
                row=[dato.text() for dato in fila]
                dni1=row[0]
                query = QtSql.QSqlQuery()
                query.prepare('SELECT dni,apellidos,nombre,alta,pagos,direccion,provincia, municipio,sexo FROM CLIENTES WHERE dni="'+dni1+'"')
                if query.exec_():
                    while query.next():
                        dni = query.value(0)
                        alta = query.value(3)
                        apellidos = query.value(1)
                        nombre = query.value(2)
                        pago = query.value(4)
                        direccion=query.value(5)
                        provincia=query.value(6)
                        municipio=query.value(7)
                        genero=query.value(8)
                var.ui.txtDNI.setText(dni)
                var.ui.txtApel.setText(apellidos)
                var.ui.txtNombre.setText(nombre)
                var.ui.txtFecha.setText(alta)
                var.ui.txtDir.setText(direccion)


                var.ui.cmbProv.setCurrentText(provincia)
                var.ui.cmbMun.setCurrentText(municipio)
                if "Hombre" in genero: var.ui.rbtHom.setChecked(True)
                if "Mujer" in genero: var.ui.rbtFem.setChecked(True)
                if "Otro" in genero: var.ui.rbtOtro.setChecked(True)
                if "Cargo cuenta" in pago: var.ui.PagoCuenta.setChecked(True)
                if "Pago Efectivo" in pago: var.ui.PagoEfectivo.setChecked(True)
                if "Pago Tarjeta" in pago: var.ui.PagoTarjeta.setChecked(True)
                if "Pago por transferencia" in pago: var.ui.PagoTransfer.setChecked(True)


        except Exception as error: print("Error en modulo CargaCli")

    def modifCli(self):

        try:
            Clientes.validarDNI()
            if control == 1:
                # Preparamos el registro
                newcli = [var.ui.txtDNI.text(), var.ui.txtFecha.text(), var.ui.txtApel.text(),
                          var.ui.txtNombre.text(), var.ui.txtDir.text()]  # Para la base de datos
                tabcli = []  # Para tableview
                client = [var.ui.txtDNI, var.ui.txtApel, var.ui.txtNombre, var.ui.txtFecha]
                for i in client:
                    tabcli.append(i.text())

                newcli.append(var.ui.cmbProv.currentText())
                newcli.append(var.ui.cmbMun.currentText())
                if var.ui.rbtHom.isChecked():
                    newcli.append('Hombre')
                elif var.ui.rbtFem.isChecked():
                    newcli.append('Mujer')
                elif var.ui.rbtOtro.isChecked():
                    newcli.append('Otro')
                pagos = []
                if var.ui.PagoCuenta.isChecked():
                    pagos.append("Cargo cuenta")
                if var.ui.PagoEfectivo.isChecked():
                    pagos.append("Pago Efectivo")
                if var.ui.PagoTarjeta.isChecked():
                    pagos.append("Pago Tarjeta")
                if var.ui.PagoTransfer.isChecked():
                    pagos.append("Pago por transferencia")

                pagos = set(pagos)
                tabcli.append("; ".join(pagos))
                newcli.append("; ".join(pagos))

                conexion.Conexion.modCli(newcli)
                conexion.Conexion.cargarTablaCli(self)
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("DNI INCORRECTO")
                msg.exec()

        except Exception as error: print("Error en modulo modifCli")