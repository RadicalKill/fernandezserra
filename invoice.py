'''
Gestion facturacion
'''
from PyQt5 import QtSql

import conexion
import var
import window
class Facturas():
    def buscaCli(self):
        try:
            dni=var.ui.txtDNIFact.text().upper()
            var.ui.txtDNIFact.setText(dni)
            registro=conexion.Conexion.buscaCliFac(dni)
            nombre=registro[0]+", "+registro[1]
            var.ui.lblCliFac.setText(nombre)

        except Exception as error: print("Error buscar cliente en facturas",error)

    def Facturar(self):
        try:
            registro=[]
            dni=var.ui.txtDNIFact.text().upper()
            registro.append(str(dni))
            var.ui.txtDNIFact.setText(dni)
            fechafac=var.ui.txtFechaFac.text()
            registro.append(str(fechafac))
            conexion.Conexion.altaFact(registro)
        except Exception as error: print("Error al facturar",error)

    def CargaCli(self):

        try:
            fila = var.ui.tabClientes.selectedItems()

            if fila:
                row = [dato.text() for dato in fila]
                dni1 = row[0]
                query = QtSql.QSqlQuery()
                query.prepare(
                    'SELECT dni,apellidos,nombre FROM CLIENTES WHERE dni="' + dni1 + '"')
                if query.exec_():
                    while query.next():
                        dni = query.value(0)
                        apellidos = query.value(1)
                        nombre = query.value(2)

                var.ui.txtDNIFact.setText(dni)
                cliente = apellidos + ", " + nombre
                var.ui.lblCliFac.setText(cliente)


        except Exception as error:
            print("Error en modulo CargaCli", error)