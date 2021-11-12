import os.path
import pathlib
import shutil
import zipfile

from PyQt5 import QtPrintSupport

import conexion
from window import *
import sys,var
from datetime import date, datetime
from zipfile import ZipFile


class Eventos():
    def Salir(self):
        try:
            var.dlgaviso.show()
            if var.dlgaviso.exec():
                sys.exit()
            else:
                var.dlgaviso.hide()
        except Exception as error:
            print("Error al salir",error)


    def abrirCal(self):
        try:
            var.dlgcalendar.show()
        except Exception as error: print("Error al abrir el calendario",error)

    def resizeTablaCli(self):
        try:
            header = var.ui.tabClientes.horizontalHeader()
            for i in range(5):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                if i == 2 or i==0:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        except Exception as error:
            print("Error al cambiar el tamaño de las columnas", error)


    def Abrir(self):
        try:
            var.dlgabrir.show()
        except Exception as error:
            print("Error al abrir cuadro dialogo", error)


    def crearBackup(self):
        try:
            fecha= datetime.today().strftime("%Y.%m.%d.%H.%M.%S")
            var.copia= (str(fecha) + "_backup.zip")
            option= QtWidgets.QFileDialog.Options()
            directorio,filename= var.dlgabrir.getSaveFileName(None,"Guardar copia",var.copia,".zip",options=option)
            if var.dlgabrir.Accepted and filename != "":
                fichzip=zipfile.ZipFile(var.copia,"w")
                fichzip.write(var.filedb,os.path.basename(var.filedb),zipfile.ZIP_DEFLATED)
                fichzip.close()

                shutil.move(str(var.copia),str(directorio))
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("Backup creado con éxito")
                msgBox.exec()
        except Exception as error:
            print("Error al crear backup", error)



    def ClearForm(self):
        try:
            cajas=[var.ui.txtApel,var.ui.txtNombre,var.ui.txtDir,var.ui.txtDNI,var.ui.txtFecha]
            for i in cajas:
                i.setText("")
            var.ui.rbtGroupGen.setExclusive(False)
            var.ui.rbtFem.setChecked(False)

            var.ui.rbtHom.setChecked(False)

            var.ui.rbtOtro.setChecked(False)
            var.ui.rbtGroupGen.setExclusive(True)

            var.ui.PagoCuenta.setChecked(False)
            var.ui.PagoEfectivo.setChecked(False)
            var.ui.PagoTarjeta.setChecked(False)
            var.ui.PagoTransfer.setChecked(False)


            var.ui.cmbProv.setCurrentIndex(0)
            var.ui.cmbMun.setCurrentIndex(0)
            var.ui.ValidarDNI.setText("")
            var.ui.txtDNI.setStyleSheet("background-color:  rgb(0, 255, 255);")

        except Exception as error: print("Error al limpiar el formulario",error)


        except Exception as error:
            print("Error al salir",error)

    def RestaurarDB(self):
        try:
            a=""
            option = QtWidgets.QFileDialog.Options()
            arch=var.dlgabrir.getOpenFileName(None,"Abrir copia",a,"Zip Files (*.zip), *.zip",options=option)
            if var.dlgabrir.Accepted and arch != "":
                ruta_descompresion = pathlib.Path(__file__).parent.absolute()
                with ZipFile(arch[0], 'r') as zipObj:
                    path= zipObj.extract("bbdd.db",ruta_descompresion)

                conexion.Conexion.db_connect(path)
                conexion.Conexion.cargarTablaCli(self)
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("BD restaurada con éxito")
                msgBox.exec()
        except Exception as error: print("Error al restaurar BD",error)


    def Imprimir(self):
        try:
            printDialog=QtPrintSupport.QPrintDialog()
            if printDialog.exec():
                printDialog.show()

        except Exception as error: print("Error al imprimir",error)