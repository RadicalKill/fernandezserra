from PyQt5 import QtSql,QtWidgets

import clients
import conexion
import event
import var

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
                          ' provincia, municipio, genero, pago )VALUES (:dni, :alta, :apellidos, '
                          ':nombre, :direccion, :provincia, :municipio, :genero, :pago)')
            query.bindValue(':dni', str(newclie[0]))
            query.bindValue(':alta', str(newclie[1]))
            query.bindValue(':apellidos', str(newclie[2]))
            query.bindValue(':nombre', str(newclie[3]))
            query.bindValue(':direccion', str(newclie[4]))
            query.bindValue(':provincia', str(newclie[5]))
            query.bindValue(':municipio', str(newclie[6]))
            query.bindValue(':genero', str(newclie[7]))
            query.bindValue(':pago', str(newclie[8]))
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

    def cargarTablaCli(self):
        try:

            index=0
            query=QtSql.QSqlQuery()
            query.prepare('SELECT dni,apellidos,nombre,alta,pago FROM CLIENTES ORDER BY apellidos')
            if query.exec_():
                while query.next():
                    dni=query.value(0)
                    alta=query.value(3)
                    apellidos=query.value(1)
                    nombre=query.value(2)
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
            query.prepare('UPDATE clientes SET alta=:alta,apellidos=:apellidos,nombre=:nombre,direccion=:direccion,provincia=:provincia,genero=:genero,pago=:pago WHERE dni=:dni')
            query.bindValue(':dni', str(newclie[0]))
            query.bindValue(':alta', str(newclie[1]))
            query.bindValue(':apellidos', str(newclie[2]))
            query.bindValue(':nombre', str(newclie[3]))
            query.bindValue(':direccion', str(newclie[4]))
            query.bindValue(':provincia', str(newclie[5]))
            query.bindValue(':municipio', str(newclie[6]))
            query.bindValue(':genero', str(newclie[7]))
            query.bindValue(':pago', str(newclie[8]))
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
                conexion.Conexion.cargarTablaCli(self)
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