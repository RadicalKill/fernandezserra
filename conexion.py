import csv
import os
import sqlite3
import sys
from datetime import datetime

import xlwt as xlwt
from PyQt5 import QtSql,QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QMessageBox

import clients
import conexion
import event
import invoice
import var
import pandas as pd

class Conexion():
    def create_db(fileName):
        """
               Recibe el nombre de la base de datos
               Módulo que se ejecuta al princio del programa crea las tablas, carga los municipios y provincias y crea los directorios necesarios
               :rtype: object

               """
        try:
            con = sqlite3.connect(database=fileName)
            cur = con.cursor()

            if not os.path.exists('.\\img'):
                os.mkdir('.\\img')

            if not os.path.exists('.\\informes'):
                os.mkdir('.\\informes')
            fd = conexion.Conexion.resource_path("tablas.sql")
            sql_file = open(fd, encoding="utf8")
            sql_as_string = sql_file.read()
            cur.executescript(sql_as_string)

            con.commit()
            con.close()

            '''creacion de directorios'''
            if not os.path.exists('.\\Informes'):
                os.mkdir('.\\Informes')




        except Exception as error:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Aviso")
            msgBox.setIcon((QtWidgets.QMessageBox.Warning))
            msgBox.setText("Error" + str(error))
            msgBox.exec()

    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS2', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def db_connect(filedb):
        try:
            db=QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(filedb)
            if not db.open():
                QtWidgets.QMessageBox.critical(None,"No se puede abrir la BD.\n","Haz click para continuar",
                                               QtWidgets.QMessageBox.Cancel)
                return False
            else:
                print("Conectado")
                return True

        except Exception as error: print("Problemas en conexión a la BD",error)


    '''
    Modulos gestion bd clientes
    '''

    def altaCli(newclie):
        try:

            query = QtSql.QSqlQuery()
            query.prepare('insert into clientes (dni, alta, apellidos, nombre, direccion,'
                          ' provincia, municipio, sexo, pagos,envio )VALUES (:dni, :alta, :apellidos, '
                          ':nombre, :direccion, :provincia, :municipio, :genero, :pago,:envio)')
            query.bindValue(':dni', str(newclie[0]))
            query.bindValue(':alta', str(newclie[1]))
            query.bindValue(':apellidos', str(newclie[2]))
            query.bindValue(':nombre', str(newclie[3]))
            query.bindValue(':direccion', str(newclie[4]))
            query.bindValue(':provincia', str(newclie[5]))
            query.bindValue(':municipio', str(newclie[6]))
            query.bindValue(':genero', str(newclie[7]))
            query.bindValue(':pago', str(newclie[8]))
            query.bindValue(':envio', str(newclie[9]))
            if query.exec_():
                print('Inserción correcta')
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Insercion")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El cliente ha sido guardado en la BD")
                msgBox.exec()
            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El cliente no ha sido guardado en la BD")
                msgBox.exec()
        except Exception as error:
            print('Problemas alta cliente',error)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Aviso")
            msgBox.setIcon((QtWidgets.QMessageBox.Warning))
            msgBox.setText("Error al guardar cliente  en la BD")
            msgBox.exec()

    def cargarTablaCli():
        try:

            index=0
            query=QtSql.QSqlQuery()
            query.prepare('SELECT dni,alta,apellidos,nombre,pagos FROM CLIENTES ORDER BY apellidos')
            if query.exec_():
                while query.next():
                    dni=query.value(0)
                    alta=query.value(1)
                    apellidos=query.value(2)
                    nombre=query.value(3)
                    pago=query.value(4)
                    var.ui.tabClientes.setRowCount(index+1)
                    var.ui.tabClientes.setItem(index,0,QtWidgets.QTableWidgetItem(dni))
                    var.ui.tabClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(apellidos))
                    var.ui.tabClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(nombre))
                    var.ui.tabClientes.setItem(index, 3, QtWidgets.QTableWidgetItem(alta))
                    var.ui.tabClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(pago))
                    index+=1
            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El cliente no ha sido cargado")
                msgBox.exec()
        except Exception as error:
            print("Problemas en cargarTablaCli", error)


    def modCli(newclie):
        try:


            query = QtSql.QSqlQuery()
            query.prepare('UPDATE clientes SET alta=:alta,apellidos=:apellidos,nombre=:nombre,direccion=:direccion,provincia=:provincia,sexo=:genero,pagos=:pago,envio=:envio WHERE dni=:dni')
            query.bindValue(':dni', str(newclie[0]))
            query.bindValue(':alta', str(newclie[1]))
            query.bindValue(':apellidos', str(newclie[2]))
            query.bindValue(':nombre', str(newclie[3]))
            query.bindValue(':direccion', str(newclie[4]))
            query.bindValue(':provincia', str(newclie[5]))
            query.bindValue(':municipio', str(newclie[6]))
            query.bindValue(':genero', str(newclie[7]))
            query.bindValue(':pago', str(newclie[8]))
            query.bindValue(':envio', str(newclie[9]))
            if query.exec_():
                print('Modificación correcta')
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Modificación")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El cliente ha sido modificado en la BD")
                msgBox.exec()


            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El cliente no ha sido modificado en la BD")
                msgBox.exec()

        except Exception as error:
            print('Problemas modificar cliente',error)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Aviso")
            msgBox.setIcon((QtWidgets.QMessageBox.Warning))
            msgBox.setText("Error al modificar cliente  en la BD")
            msgBox.exec()


    def DelCli(self):
        try:
            dni=var.ui.txtDNI.text()
            query = QtSql.QSqlQuery()
            query.prepare(
                'DELETE FROM clientes  WHERE dni=:dni')
            query.bindValue(':dni', dni)

            if query.exec_():
                print('Eliminación correcta')
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Eliminación")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El cliente ha sido eliminado de la BD")
                msgBox.exec()
                conexion.Conexion.cargarTablaCli()
            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El cliente no ha sido eliminado de la BD")
                msgBox.exec()

        except Exception as error:
            print('Problemas eliminar cliente', error)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Aviso")
            msgBox.setIcon((QtWidgets.QMessageBox.Warning))
            msgBox.setText("Error al eliminar cliente  en la BD")
            msgBox.exec()

    def CargaProv(self):
        try:
            prov=[""]
            ids=[]
            query = QtSql.QSqlQuery()
            query.prepare('SELECT id,provincia FROM provincias')
            if query.exec_():
                while query.next():
                    id=query.value(0)
                    ids.append(id)
                    provin=query.value(1)
                    prov.append(provin)
                clients.Clientes.cargaProv(prov)
            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El cliente no ha sido cargado")
                msgBox.exec()

        except Exception as error:
            print('Problemas cargar provincias', error)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Aviso")
            msgBox.setIcon((QtWidgets.QMessageBox.Warning))
            msgBox.setText("Error al cargar provincias de la BD")
            msgBox.exec()




    def CargaMun(prov):

        try:

            query = QtSql.QSqlQuery()
            query.prepare(
                'SELECT id FROM provincias WHERE provincia=:pro')
            query.bindValue(':pro',prov)

            if query.exec_():
                while query.next():
                    idp=query.value(0)


            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("La provincia no ha sido cargada")
                msgBox.exec()
            mun=[""]

            query = QtSql.QSqlQuery()
            query.prepare('SELECT id,municipio FROM municipios WHERE provincia_id=:idp')
            query.bindValue(':idp',idp)
            if query.exec_():
                while query.next():
                    munic=query.value(1)
                    mun.append(munic)
                clients.Clientes.cargaMun(mun)
            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El cliente no ha sido cargado")
                msgBox.exec()

        except Exception as error:
            print('Problemas cargar provincias', error)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Aviso")
            msgBox.setIcon((QtWidgets.QMessageBox.Warning))
            msgBox.setText("Error al cargar provincias de la BD")
            msgBox.exec()

    def comprobarCliente(dni):
        try:

            contador="0"
            query = QtSql.QSqlQuery()
            query.prepare(
                'SELECT * FROM clientes WHERE dni=:dni')
            query.bindValue(':dni', dni)
            if query.exec_():
                while query.next():
                    contador = query.value(0)
            else: contador="0"
            return contador


        except Exception as error:
            print('Problemas al buscar en la bd', error)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Aviso")
            msgBox.setIcon((QtWidgets.QMessageBox.Warning))
            msgBox.setText("Error al cargar provincias de la BD")
            msgBox.exec()

    def altaCliXL(newclie):
        try:


            query = QtSql.QSqlQuery()
            query.prepare('insert into clientes (dni, alta, apellidos, nombre, direccion,'
                          ' provincia, municipio, sexo, pagos,envio )VALUES (:dni, :alta, :apellidos, '
                          ':nombre, :direccion, :provincia, :municipio, :genero, :pago,:envio)')
            query.bindValue(':dni', str(newclie[0]))
            query.bindValue(':alta', str(newclie[1]))
            query.bindValue(':apellidos', str(newclie[2]))
            query.bindValue(':nombre', str(newclie[3]))
            query.bindValue(':direccion', str(newclie[4]))
            query.bindValue(':provincia', str(newclie[5]))
            query.bindValue(':municipio', str(newclie[6]))
            query.bindValue(':genero', str(newclie[7]))
            query.bindValue(':pago', str(newclie[8]))
            query.bindValue(':envio', str(newclie[9]))

            if query.exec_():
                Conexion.cargarTablaCli()
            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El cliente no ha sido guardado en la BD")
                msgBox.exec()


        except Exception as error:
            print('Problemas alta cliente',error)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Aviso")
            msgBox.setIcon((QtWidgets.QMessageBox.Warning))
            msgBox.setText("Error al guardar cliente  en la BD")
            msgBox.exec()

    def modCliXL(newclie):
        try:


            query = QtSql.QSqlQuery()
            query.prepare('UPDATE clientes SET alta=:alta,apellidos=:apellidos,nombre=:nombre,direccion=:direccion,provincia=:provincia,sexo=:genero,pagos=:pago,envio=:envio WHERE dni=:dni')

            query.bindValue(':dni', str(newclie[0]))
            query.bindValue(':alta', str(newclie[1]))
            query.bindValue(':apellidos', str(newclie[2]))
            query.bindValue(':nombre', str(newclie[3]))
            query.bindValue(':direccion', str(newclie[4]))
            query.bindValue(':provincia', str(newclie[5]))
            query.bindValue(':municipio', str(newclie[6]))
            query.bindValue(':genero', str(newclie[7]))
            query.bindValue(':pago', str(newclie[8]))
            query.bindValue(':envio',str(newclie[9]))
            if query.exec_():
                Conexion.cargarTablaCli()


            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El cliente no ha sido modificado en la BD")
                msgBox.exec()
        except Exception as error:
            print('Problemas modificar cliente',error)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Aviso")
            msgBox.setIcon((QtWidgets.QMessageBox.Warning))
            msgBox.setText("Error al modificar cliente  en la BD")
            msgBox.exec()
    # Conexion para exportar con la libreria pandas
    def exportBD(self):
        try:
            list = []
            adiciones=[]
            query = QtSql.QSqlQuery()
            query.prepare('SELECT * FROM clientes')

            if query.exec_():
                while query.next():
                    dni=query.value(0)
                    alta=query.value(1)
                    apellidos=query.value(2)
                    nombre=query.value(3)
                    direccion=query.value(4)
                    provincia=query.value(5)
                    municipio=query.value(6)
                    sexo=query.value(7)
                    pago=query.value(8)
                    envio=query.value(9)
                    list=[dni,alta,apellidos,nombre,direccion,provincia,municipio,sexo,pago,envio]
                    adiciones.append(list)
                event.Eventos.Exportacion(adiciones)
            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("La BD no ha sido exportada")
                msgBox.exec()



        except Exception as error:
            print('Problemas exportar BD',error)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Aviso")
            msgBox.setIcon((QtWidgets.QMessageBox.Warning))
            msgBox.setText("Error al exportar la BD")
            msgBox.exec()
    # Conexion para exportar con la libreria xlwt
    def exportExcel(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
            var.copia = (str(fecha) + '_dataExport.xls')
            option = QtWidgets.QFileDialog.Options()
            directorio, filename = var.dlgabrir.getSaveFileName(None, 'Exportar datos', var.copia, '.xls',
                                                                options=option)
            wb = xlwt.Workbook()
            # add_sheet is used to create sheet.
            sheet1 = wb.add_sheet('Hoja 1')

            # Cabeceras
            sheet1.write(0, 0, 'DNI')
            sheet1.write(0, 1, 'ALTA')
            sheet1.write(0, 2, 'APELIDOS')
            sheet1.write(0, 3, 'NOME')
            sheet1.write(0, 4, 'DIRECCION')
            sheet1.write(0, 5, 'PROVINCIA')
            sheet1.write(0, 6, 'MUNICIPIO')
            sheet1.write(0, 7, 'SEXO')
            sheet1.write(0, 8, 'PAGOS')
            sheet1.write(0, 9, 'ENVIO')
            f = 1
            query = QtSql.QSqlQuery()
            query.prepare('SELECT *  FROM clientes')
            if query.exec_():
                while query.next():
                    sheet1.write(f, 0, query.value(0))
                    sheet1.write(f, 1, query.value(1))
                    sheet1.write(f, 2, query.value(2))
                    sheet1.write(f, 3, query.value(3))
                    sheet1.write(f, 4, query.value(4))
                    sheet1.write(f, 5, query.value(5))
                    sheet1.write(f, 6, query.value(6))
                    sheet1.write(f, 7, query.value(7))
                    sheet1.write(f, 8, query.value(8))
                    sheet1.write(f, 9, query.value(9))
                    f+=1
            wb.save(directorio)

        except Exception as error:
            print('Error en conexion para exportar excel ',error)
            
            
            
    def altaProd(newProd):
        try:


            query = QtSql.QSqlQuery()
            query.prepare('insert into articulos (nombre, precio) VALUES (:nombre, :precio)')
            query.bindValue(':nombre', str(newProd[0]))
            query.bindValue(':precio', str(newProd[1]))

            if query.exec_():
                print('Inserción correcta')
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Insercion")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El articulo ha sido guardado en la BD")
                msgBox.exec()
            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El articulo no ha sido guardado en la BD")
                msgBox.exec()
        except Exception as error:
            print('Problemas alta articulo',error)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Aviso")
            msgBox.setIcon((QtWidgets.QMessageBox.Warning))
            msgBox.setText("Error al guardar articulo  en la BD")
            msgBox.exec()

    def cargarTablaProd():
        try:

            index=0
            query=QtSql.QSqlQuery()
            query.prepare('SELECT codigo, nombre,precio FROM articulos ORDER BY codigo')
            if query.exec_():
                while query.next():
                    codigo=str(query.value(0))
                    nombre=query.value(1)
                    precio=query.value(2)

                    var.ui.tabClientes.setRowCount(index+1)
                    var.ui.tabClientes.setItem(index,0 ,QtWidgets.QTableWidgetItem(codigo))
                    var.ui.tabClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(nombre))
                    var.ui.tabClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(precio))

                    index+=1
            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El producto no ha sido cargado")
                msgBox.exec()
        except Exception as error:
            print("Problemas en cargarTablaProd", error)

    def modProd(newProd):
        try:

            query = QtSql.QSqlQuery()
            query.prepare(
                'UPDATE articulos SET nombre=:nombre,precio=:precio WHERE codigo=:codigo')
            query.bindValue(':codigo', str(newProd[0]))
            query.bindValue(':nombre', str(newProd[1]))
            query.bindValue(':precio', str(newProd[2]))

            if query.exec_():
                print('Modificación correcta')
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Modificación")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El articulo ha sido modificado en la BD")
                msgBox.exec()


            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El articulo no ha sido modificado en la BD")
                msgBox.exec()

        except Exception as error:
            print('Problemas modificar articulo', error)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Aviso")
            msgBox.setIcon((QtWidgets.QMessageBox.Warning))
            msgBox.setText("Error al modificar articulo  en la BD")
            msgBox.exec()

    def DelProd(self):
        try:
            cod=var.ui.lblCod2.text()
            query = QtSql.QSqlQuery()
            query.prepare(
                'DELETE FROM articulos  WHERE codigo=:codigo')
            query.bindValue(':codigo', cod)

            if query.exec_():
                print('Eliminación correcta')
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Eliminación")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El articulo ha sido eliminado de la BD")
                msgBox.exec()
                conexion.Conexion.cargarTablaProd()

            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El articulo no ha sido eliminado de la BD")
                msgBox.exec()

        except Exception as error:
            print('Problemas eliminar articulo', error)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Aviso")
            msgBox.setIcon((QtWidgets.QMessageBox.Warning))
            msgBox.setText("Error al eliminar articulo  en la BD")
            msgBox.exec()
    def buscaCliente(self):
        try:

            dni=var.ui.txtDNI.text().upper()
            query = QtSql.QSqlQuery()
            index=0
            query.prepare('SELECT dni,alta,apellidos,nombre,pagos FROM CLIENTES WHERE dni=:dni ORDER BY apellidos')
            query.bindValue(':dni', str(dni))
            if query.exec_():

                while query.next():
                    dni=query.value(0)
                    alta=query.value(1)
                    apellidos=query.value(2)
                    nombre=query.value(3)
                    pago=query.value(4)
                    var.ui.tabClientes.setRowCount(index+1)
                    var.ui.tabClientes.setItem(index,0,QtWidgets.QTableWidgetItem(dni))
                    var.ui.tabClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(apellidos))
                    var.ui.tabClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(nombre))
                    var.ui.tabClientes.setItem(index, 3, QtWidgets.QTableWidgetItem(alta))
                    var.ui.tabClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(pago))
                    index+=1
            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El cliente no ha sido encontrado en la BD")
                msgBox.exec()
        except Exception as error:
            print('Problemas buscar cliente ', error)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Aviso")
            msgBox.setIcon((QtWidgets.QMessageBox.Warning))
            msgBox.setText("Error al buscar cliente")
            msgBox.exec()
    def buscaArt(self):
        try:

            nomart=var.ui.txtNomArt.text().title()
            query = QtSql.QSqlQuery()
            index=0
            query.prepare('SELECT codigo,nombre,precio FROM articulos WHERE nombre=:nombre ORDER BY codigo')
            query.bindValue(':nombre', str(nomart))
            if query.exec_():

                while query.next():
                    codigo=query.value(0)
                    nombre=query.value(1)
                    precio=query.value(2)

                    var.ui.tabClientes.setRowCount(index+1)
                    var.ui.tabClientes.setItem(index,0,QtWidgets.QTableWidgetItem(codigo))
                    var.ui.tabClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(nombre))
                    var.ui.tabClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(precio))

                    index+=1
            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("El articulo no ha sido encontrado en la BD")
                msgBox.exec()
        except Exception as error:
            print('Problemas buscar articulo ', error)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Aviso")
            msgBox.setIcon((QtWidgets.QMessageBox.Warning))
            msgBox.setText("Error al buscar articulo")
            msgBox.exec()

    '''
    Gestion facturas
    '''
    def buscaCliFac(dni):
        try:
            registro=[]

            query = QtSql.QSqlQuery()
            query.prepare(
                'SELECT dni,apellidos, nombre from clientes where dni=:dni')
            query.bindValue(':dni', dni)
            if query.exec_():
                while query.next():
                    registro.append(query.value(1))
                    registro.append(query.value(2))

            return registro
        except Exception as error:
            print('Problemas buscar cliente factura', error)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Aviso")
            msgBox.setIcon((QtWidgets.QMessageBox.Warning))
            msgBox.setText("Error al buscar cliente en factura")
            msgBox.exec()

    def altaFact(registro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into facturas(dni,fechafac)values(:dni,:fecha)')
            query.bindValue(':dni', registro[0])

            query.bindValue(':fecha', registro[1])
            if query.exec_():
                print('Inserción correcta')
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Insercion")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("La factura ha sido guardada en la BD")
                msgBox.exec()
                conexion.Conexion.cargarTablaFac()
            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("La factura no ha sido guardada en la BD")
                msgBox.exec()
        except Exception as error:
            print('Problemas alta factura', error)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Aviso")
            msgBox.setIcon((QtWidgets.QMessageBox.Warning))
            msgBox.setText("Error al facturar")
            msgBox.exec()

    def cargarTablaFac():
        try:

            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('SELECT codfac,fechafac FROM facturas order by substr(fechafac,7)||substr(fechafac,4,2)||substr(fechafac,1,2) desc')
            if query.exec_():
                while query.next():
                    codigo = str(query.value(0))
                    fecha = query.value(1)
                    var.btnfacdel = QtWidgets.QPushButton()
                    icopapelera = QtGui.QPixmap("img/papelera.png")
                    var.btnfacdel.setFixedSize(24,24)
                    var.btnfacdel.setIcon(QtGui.QIcon(icopapelera))
                    var.ui.tabFact.setRowCount(index + 1)  # creamos la fila y luego cargamos datos
                    var.ui.tabFact.setItem(index, 0, QtWidgets.QTableWidgetItem(codigo))
                    var.ui.tabFact.setItem(index, 1, QtWidgets.QTableWidgetItem(fecha))
                    cell_widget = QtWidgets.QWidget()
                    lay_out = QtWidgets.QHBoxLayout(cell_widget)
                    lay_out.addWidget(var.btnfacdel)
                    var.btnfacdel.clicked.connect(conexion.Conexion.bajaFact)
                    lay_out.setAlignment(QtCore.Qt.AlignVCenter)
                    var.ui.tabFact.setCellWidget(index, 2, cell_widget)
                    var.ui.tabFact.item(index, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                    var.ui.tabFact.item(index, 1).setTextAlignment(QtCore.Qt.AlignCenter)

                    index += 1
            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("La factura no ha sido cargada")
                msgBox.exec()
        except Exception as error:
            print("Problemas en cargarTablaFac", error)

    def bajaFact():

        try:

            numfac = var.ui.lblnumfac.text()
            query = QtSql.QSqlQuery()
            query.prepare('delete from facturas where codfac = :codfac')
            query.bindValue(':codfac', int(numfac))
            if query.exec_():
                Conexion.cargarTablaFac()
                msgBox = QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Information)
                msgBox.setText("La factura ha sido dada de baja")
                msgBox.setWindowTitle("Aviso")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()
                invoice.Facturas.vaciarTabVentas()

            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("La factura no ha sido dada de baja. Recuerda seleccionarla antes de eliminarla")
                msgBox.exec()

        except Exception as error:
          print('Error en dar baja factura', error)

    def cargarCmbproducto():
        try:
            var.cmbProducto.clear()
            var.cmbProducto.addItem('') # la primera linea en blanco
            query2 = QtSql.QSqlQuery()
            query2.prepare('select  nombre from articulos')


            if query2.exec_():
                while query2.next():
                    var.cmbProducto.addItem(str(query2.value(0)))
            else:
                print('Error:', query2.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("La factura no ha sido cargada")
                msgBox.exec()


        except Exception as error:
            print('Error cargar combox de productos', error)

    def obtenerCodPrecio(articulo):
        try:
            dato = []
            query = QtSql.QSqlQuery()
            query.prepare('select precio,codigo from articulos where nombre =:nombre ')
            query.bindValue(':nombre', str(articulo))
            if query.exec_():
                while query.next():
                    dato.append(query.value(0))
                    dato.append(str(query.value(1)))
            else:
                print('Error:', query.lastError().text())
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("La factura no ha sido cargada")
                msgBox.exec()

            return  dato

        except Exception as error:
            print('Error cargar codigo precio en conexion', error)

    def cargarVenta(venta):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into ventas (codfacf, codprof, precio, cantidad) values (:codfac, :codpro, :precio, :cantidad)')
            query.bindValue(':codfac', int(venta[0]))
            query.bindValue(':codpro', int(venta[1]))
            query.bindValue(':precio', float(venta[2]))
            query.bindValue(':cantidad', int(venta[3]))
            if query.exec_():
                var.ui.lbl_venta.setText("Venta realizada")
                var.ui.lbl_venta.setStyleSheet("background-color:rgb(82, 190, 128);")


            else:
                var.ui.lbl_venta.setText("Error en venta")
                var.ui.lbl_venta.setStyleSheet("background-color:rgb(240, 128, 128);")

        except Exception as error:
            pass

    def buscaCodFac(self):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select codfac from facturas order by codfac desc  limit 1')
            if query.exec_():
                while query.next():
                     dato = query.value(0)
                     return  dato

        except Exception as error:
            print('Error obtener código factura', error)

    def cargarLineasVenta(codfac):
        try:
            suma=0
            index = 1
            query = QtSql.QSqlQuery()
            query.prepare('select codven,codprof,precio,cantidad from ventas where codfacf = :codfac')
            query.bindValue(':codfac', int(codfac))

            if query.exec_():
                while query.next():
                    codventa = query.value(0)
                    producto = conexion.Conexion.nombreDeArticulo(query.value(1))
                    cantidad=query.value(3)
                    precio=query.value(2)
                    total_linea = round(float(precio) * float(cantidad), 2)
                    suma=suma+total_linea
                    var.ui.tabClientes.setRowCount(index + 1)
                    var.ui.tabClientes.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codventa)))
                    var.ui.tabClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(str(producto)))
                    var.ui.tabClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(str('{:.2f}'.format(precio))))
                    var.ui.tabClientes.setItem(index, 3, QtWidgets.QTableWidgetItem(str(cantidad)))
                    var.ui.tabClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(str('{:.2f}'.format(total_linea))+'€'))
                    var.ui.tabClientes.item(index, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                    var.ui.tabClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignRight)
                    var.ui.tabClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignRight)
                    var.ui.tabClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignRight)
                    index = index + 1
                iva = suma * 0.21
                total = suma + iva
                # Para el test:
                # return total
                # Damos formato a los totales
                var.ui.txtSubtotal.setText(str('{:.2f}'.format(round(suma, 2))) + '€')
                var.ui.txtIva.setText(str('{:.2f}'.format(round(iva, 2))) + '€')
                var.ui.txtTotal.setText(str('{:.2f}'.format(round(total, 2))) + '€')

        except Exception as error:
            print('Error cargar lineas ventas en conexion', error)

    def nombreDeArticulo(codpro):

        """
        Método que devuelve el nombre del artículo al que corresponde el código que recibe.
        :return: Nombre del artículo
        :rtype: String

        """
        try:
            nombre=''
            query = QtSql.QSqlQuery()
            query.prepare('select nombre from articulos where codigo = :codpro')
            query.bindValue(':codpro', int(codpro))
            if query.exec_():
                while query.next():
                    nombre=query.value(0)
            return nombre
        except Exception as error:
            print('Error al obtener nombre de articulo en conexión: ',error)

    def buscaDatosFac(codigo):
        """

        Recibe el código de una factura y devuelve el dni del cliente asociado a ella.
        :return: Dni del cliente
        :rtype: String

        """
        datosFac = []
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'SELECT dni FROM facturas WHERE codfac =:codigo')
            query.bindValue(':codigo', str(codigo))
            if query.exec_():
                while query.next():
                    datosFac.append(query.value(0))


        except Exception as error:
            print('Error en buscar datos factura (conexión) ', error)
        return datosFac
    def eliminarLineaVenta(codigo):
        """

        Método que elimina una linea de venta en concreto de la bbdd.
        También muestra el mensaje correspondiente.

        """
        try:
            numfac = var.ui.lblnumfac.text()
            query = QtSql.QSqlQuery()
            query.prepare('delete from ventas where codven = :codigo')
            query.bindValue(':codigo', int(codigo))
            if query.exec_():
                Conexion.cargarLineasVenta(numfac)
                var.ui.lbl_venta.setText('Venta Eliminada')
                var.ui.lbl_venta.setStyleSheet('QLabel{color:blue;}')
            else:
                var.ui.lbl_venta.setText('Error al eliminar venta')
                var.ui.lbl_venta.setStyleSheet('QLabel{color:red;}')


        except Exception as error:
          print('Error en eliminar venta conexion', error)