from PyQt5 import QtSql,QtWidgets


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

    def altaCli(newcli):
        try:
            pass
        except Exception as error:
            print("Problemas en altaCli", error)
