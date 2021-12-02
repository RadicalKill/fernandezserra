from datetime import datetime

import xlwt as xlwt
from PyQt5 import QtSql,QtWidgets

import clients
import conexion
import event
import var
import pandas as pd

class Conexion():
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

            print(newclie)
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