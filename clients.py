'''
gestion clientes
'''
import clients
import conexion
import invoice
import var, event
from window import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtSql


class Clientes():
    def validarDNI():
        try:
            global control
            control = 0
            dni = var.ui.txtDNI.text().upper()
            var.ui.txtDNI.setText(dni)
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"  # Letra DNI
            dig_ext = "XYZ"  # DIGITO EXTRANJEROS
            reemp_dig_ext = {"X": "0", "Y": "1", "Z": "2"}
            numeros = "1234567890"
            dni = dni.upper()
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    control = 1
                    var.ui.ValidarDNI.setStyleSheet("QLabel{color:green;}")
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


        except Exception as error:
            print("Error en modulo validarDNI", error)

    def validarDNIFac():
        try:
            global control
            control = 0
            dni = var.ui.txtDNIFact.text()
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"  # Letra DNI
            dig_ext = "XYZ"  # DIGITO EXTRANJEROS
            reemp_dig_ext = {"X": "0", "Y": "1", "Z": "2"}
            numeros = "1234567890"
            dni = dni.upper()
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    control = 1

                    var.ui.txtDNIFact.setStyleSheet("background-color: green;")
                else:


                    var.ui.txtDNIFact.setStyleSheet("background-color: rgb(255, 155, 90);")

            else:


                var.ui.txtDNIFact.setStyleSheet("background-color: rgb(255, 155, 90);")


        except Exception as error:
            print("Error en modulo validarDNI", error)

    def ValidarPrecio(self):
        try:
            global cont
            cont = 0
            precio = var.ui.txtPrecio.text()
            if (float(precio)): cont = 1




        except Exception as error:
            print("Error en modulo validarPrecio", error)

    def selGen(self):
        try:
            pass

        except Exception as error:
            print("Error en modulo selGen")

    def cargaProv(prov):
        try:
            var.ui.cmbProv.clear()

            for i in prov:
                var.ui.cmbProv.addItem(i)

        except Exception as error:
            print("Error en modulo cargaProv")

    def cargaMun(mun):
        try:
            var.ui.cmbMun.clear()
            for i in mun:
                var.ui.cmbMun.addItem(i)

        except Exception as error:
            print("Error en modulo cargaMun")

    def cargarFecha(qDate):
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            if(var.ui.tabPrograma.currentIndex()==0):
                var.ui.txtFecha.setText(str(data))
            elif(var.ui.tabPrograma.currentIndex()==1):
                var.ui.txtFechaFac.setText(str(data))
            var.dlgcalendar.hide()

        except Exception as error:
            print("Error en modulo cargarFecha")

    def capitalizar():
        try:
            nombre = var.ui.txtNombre.text()
            var.ui.txtNombre.setText(nombre.title())
            apel = var.ui.txtApel.text()
            var.ui.txtApel.setText(apel.title())
            dir = var.ui.txtDir.text()
            var.ui.txtDir.setText(dir.title())
            nomart=var.ui.txtNomArt.text()
            var.ui.txtNomArt.setText(nomart.title())

        except Exception as error:
            print("Error en modulo capitalizar")

    def avisoDNI(self):
        QMessageBox.about(self, "ERROR", "DNI incorrecto")

    def GuardaClie(self):

        try:
            Clientes.validarDNI()
            if control == 1:
                # Preparamos el registro
                newcli = [var.ui.txtDNI.text(), var.ui.txtFecha.text(), var.ui.txtApel.text(), var.ui.txtNombre.text(),
                          var.ui.txtDir.text()]  # Para la base de datos
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

                newcli.append("; ".join(pagos))
                newcli.append(var.ui.spinEnvio.value())

                conexion.Conexion.altaCli(newcli)
                conexion.Conexion.cargarTablaCli()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("DNI INCORRECTO")
                msg.exec()


        except Exception as error:
            print("Error en modulo GuardaClie")

    def CargaCli(self):

        try:
            var.ui.PagoCuenta.setChecked(False)
            var.ui.PagoTransfer.setChecked(False)
            var.ui.PagoTarjeta.setChecked(False)
            var.ui.PagoEfectivo.setChecked(False)
            fila = var.ui.tabClientes.selectedItems()

            if fila:
                row = [dato.text() for dato in fila]
                dni1 = row[0]
                query = QtSql.QSqlQuery()
                query.prepare(
                    'SELECT dni,apellidos,nombre,alta,pagos,direccion,provincia, municipio,sexo, envio FROM CLIENTES WHERE dni="' + dni1 + '"')
                if query.exec_():
                    while query.next():
                        dni = query.value(0)
                        alta = query.value(3)
                        apellidos = query.value(1)
                        nombre = query.value(2)
                        pago = query.value(4)
                        direccion = query.value(5)
                        provincia = query.value(6)
                        municipio = query.value(7)
                        genero = query.value(8)
                        envio = query.value(9)
                var.ui.txtDNI.setText(dni)
                var.ui.txtApel.setText(apellidos)
                var.ui.txtNombre.setText(nombre)
                var.ui.txtFecha.setText(alta)
                var.ui.txtDir.setText(direccion)
                if (envio == 0 or envio == 1 or envio == 2 or envio == 3):
                    var.ui.spinEnvio.setValue(envio)

                var.ui.cmbProv.setCurrentText(provincia)
                var.ui.cmbMun.setCurrentText(municipio)
                if "Hombre" in genero: var.ui.rbtHom.setChecked(True)
                if "Mujer" in genero: var.ui.rbtFem.setChecked(True)
                if "Otro" in genero: var.ui.rbtOtro.setChecked(True)
                if "Cargo cuenta" in pago: var.ui.PagoCuenta.setChecked(True)
                if "Pago Efectivo" in pago: var.ui.PagoEfectivo.setChecked(True)
                if "Pago Tarjeta" in pago: var.ui.PagoTarjeta.setChecked(True)
                if "Pago por transferencia" in pago: var.ui.PagoTransfer.setChecked(True)


        except Exception as error:
            print("Error en modulo CargaCli", error)

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

                newcli.append(var.ui.spinEnvio.value())

                conexion.Conexion.modCli(newcli)
                conexion.Conexion.cargarTablaCli()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("DNI INCORRECTO")
                msg.exec()

        except Exception as error:
            print("Error en modulo modifCli")

    def GuardaProd(self):

        try:
            Clientes.ValidarPrecio(self)
            if cont == 1:
                prec = var.ui.txtPrecio.text()
                precio = round(float(prec), 2)
                # Preparamos el registro
                newProd = [var.ui.txtNomArt.text(), precio]  # Para la base de datos

                conexion.Conexion.altaProd(newProd)
                conexion.Conexion.cargarTablaProd()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("El precio debe ser un numero")
                msg.exec()



        except Exception as error:
            print("Error en modulo GuardaProd", error)

    def CargaProd(self):

        try:
            fila = var.ui.tabClientes.selectedItems()

            if fila:
                row = [dato.text() for dato in fila]
                cod1 = row[0]
                query = QtSql.QSqlQuery()
                query.prepare('SELECT codigo,nombre,precio FROM articulos WHERE codigo="' + cod1 + '"')
                if query.exec_():
                    while query.next():
                        codigo = str(query.value(0))
                        nombre = query.value(1)
                        precio = query.value(2)
                var.ui.lblCod2.setText(codigo)
                var.ui.txtNomArt.setText(nombre)
                var.ui.txtPrecio.setText(precio)



        except Exception as error:
            print("Error en modulo CargaProd", error)

    def Cargar(self):
        try:
            if (var.ui.tabPrograma.currentIndex() == 0):
                clients.Clientes.CargaCli(self)
                invoice.Facturas.CargaCli(self)
            if (var.ui.tabPrograma.currentIndex() == 2):
                clients.Clientes.CargaProd(self)
            if(var.ui.tabPrograma.currentIndex()==1):
                pass
        except Exception as error:
            print("Error en modulo Cargar", error)



    def modifProd(self):

        try:
            Clientes.ValidarPrecio(self)
            if cont == 1:
                prec=var.ui.txtPrecio.text()
                precio=round(float(prec),2)
                # Preparamos el registro
                newProd = [var.ui.lblCod2.text(), var.ui.txtNomArt.text(), precio]  # Para la base de datos

                conexion.Conexion.modProd(newProd)
                conexion.Conexion.cargarTablaProd()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("El precio debe ser un numero")
                msg.exec()


        except Exception as error:
            print("Error en modulo modifProd", error)

#             Cargar datos factura


    def cargaFac(self):
        """

        Método que consulta los datos de una factura seleccionada en tabla con Conexion.buscaDatosFac
        y rellena sus respectivos campos en la interfaz.
        Tambien carga sus lineas de venta con Conexion.cargarLineasVenta.

        """
        try:

            fila = var.ui.tabFact.selectedItems()
            datos = [var.ui.lblnumfac, var.ui.txtFechaFac]
            if fila:
                row = [dato.text() for dato in fila]
            for i, dato in enumerate(datos):
                dato.setText(row[i])
            # Ahora los datos desde la base de datos (de momento solo dni):
            datos=conexion.Conexion.buscaDatosFac(var.ui.lblnumfac.text())
            var.ui.txtDNIFact.setText(datos[0])
            invoice.Facturas.buscaCli(self)
            invoice.Facturas.cargaLineaVenta(self)
            conexion.Conexion.cargarLineasVenta(str(var.ui.lblnumfac.text()))
        except Exception as error:
            print('Error en módulo cargar factura (invoice) ',error)

