import os.path
import pathlib
import shutil
import tkinter
import zipfile
import xlrd
import pandas as pd

from PyQt5 import QtPrintSupport
from PyQt5.QtWidgets import QMessageBox

import conexion
from window import *
import sys, var
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
            print("Error al salir", error)

    def abrirCal(self):
        try:
            var.dlgcalendar.show()
        except Exception as error:
            print("Error al abrir el calendario", error)

    def resizeTablaCli(self):
        try:
            header = var.ui.tabClientes.horizontalHeader()
            for i in range(5):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                if i == 2 or i == 0:
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
            fecha = datetime.today().strftime("%Y.%m.%d.%H.%M.%S")
            var.copia = (str(fecha) + "_backup.zip")
            option = QtWidgets.QFileDialog.Options()
            directorio, filename = var.dlgabrir.getSaveFileName(None, "Guardar copia", var.copia, ".zip",
                                                                options=option)
            if var.dlgabrir.Accepted and filename != "":
                fichzip = zipfile.ZipFile(var.copia, "w")
                fichzip.write(var.filedb, os.path.basename(var.filedb), zipfile.ZIP_DEFLATED)
                fichzip.close()

                shutil.move(str(var.copia), str(directorio))
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("Backup creado con éxito")
                msgBox.exec()
        except Exception as error:
            print("Error al crear backup", error)

    def ClearForm(self):
        try:
            cajas = [var.ui.txtApel, var.ui.txtNombre, var.ui.txtDir, var.ui.txtDNI, var.ui.txtFecha]
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

            var.ui.spinEnvio.setValue(0)
            var.ui.cmbProv.setCurrentIndex(0)
            var.ui.cmbMun.setCurrentIndex(0)
            var.ui.ValidarDNI.setText("")
            var.ui.txtDNI.setStyleSheet("background-color:  rgb(0, 255, 255);")
            conexion.Conexion.cargarTablaCli()

        except Exception as error:
            print("Error al limpiar el formulario", error)


        except Exception as error:
            print("Error al salir", error)

    def ClearFormProd(self):
        try:
            cajas = [var.ui.lblCod2, var.ui.txtNomArt, var.ui.txtPrecio]
            for i in cajas:
                i.setText("")

        except Exception as error:
            print("Error al limpiar el formulario", error)


        except Exception as error:
            print("Error al salir", error)

    def RestaurarDB(self):
        try:
            a = ""
            option = QtWidgets.QFileDialog.Options()
            arch = var.dlgabrir.getOpenFileName(None, "Abrir copia", a, "Zip Files (*.zip), *.zip", options=option)
            if var.dlgabrir.Accepted and arch != "":
                ruta_descompresion = pathlib.Path(__file__).parent.absolute()
                with ZipFile(arch[0], 'r') as zipObj:
                    path = zipObj.extract("bbdd.db", ruta_descompresion)

                conexion.Conexion.db_connect(path)
                conexion.Conexion.cargarTablaCli()
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Aviso")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("BD restaurada con éxito")
                msgBox.exec()
        except Exception as error:
            print("Error al restaurar BD", error)

    def Imprimir(self):
        try:
            printDialog = QtPrintSupport.QPrintDialog()
            if printDialog.exec():
                printDialog.show()

        except Exception as error:
            print("Error al imprimir", error)

    def ImportarExcel(self):
        try:
            a = ""
            option = QtWidgets.QFileDialog.Options()
            arch = var.dlgabrir.getOpenFileName(None, "Abrir copia", a, options=option)
            if var.dlgabrir.Accepted and arch != "":
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Confirmacion")
                msgBox.setText("Está seguro de abrir este archivo?")
                msgBox.setStandardButtons(QMessageBox.Yes)
                msgBox.addButton(QMessageBox.No)
                msgBox.setDefaultButton(QMessageBox.No)
                if (msgBox.exec() == QMessageBox.Yes):
                    documento = xlrd.open_workbook(arch[0])
                    excel = documento.sheet_by_index(0)
                    filas = excel.nrows

                    for n in range(filas):
                        if n != 0:
                            dni = str(excel.cell_value(n, 0))
                            alta = excel.cell_value(n, 1)
                            apellidos = excel.cell_value(n, 2)
                            nome = excel.cell_value(n, 3)
                            direccion = excel.cell_value(n, 4)
                            provincia = excel.cell_value(n, 5)
                            municipio = excel.cell_value(n, 6)
                            sexo = excel.cell_value(n, 7)
                            pagos = excel.cell_value(n, 8)
                            envio = excel.cell_value(n, 9)
                            newcli = [dni, alta, apellidos, nome, direccion, provincia, municipio, sexo, pagos, envio]
                            contador = conexion.Conexion.comprobarCliente(dni)
                            if (dni != ""):
                                if contador == "0":
                                    conexion.Conexion.altaCliXL(newcli)
                                else:
                                    conexion.Conexion.modCliXL(newcli)

                    msgBox = QtWidgets.QMessageBox()
                    msgBox.setWindowTitle("Confirmacion")
                    msgBox.setText("Datos importados con éxito")
                    msgBox.exec()

        except Exception as error:
            print("Error al importar", error)

    # Metodo para exportar con pandas(pd)
    def Exportacion(adiciones):
        try:
            df = pd.DataFrame(adiciones,
                              columns=['DNI', 'Alta', 'Apellidos', 'Nombre', 'Direccion', 'Provincia', 'Municipio',
                                       'Sexo', 'Pago', 'Envio'])

            fecha = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            var.copia = (str(fecha) + ".csv")
            option = QtWidgets.QFileDialog.Options()
            directorio, filename = var.dlgabrir.getSaveFileName(None, "Exportar", var.copia, ".csv", options=option)
            if var.dlgabrir.Accepted and filename != "":
                df.to_csv(var.copia, encoding='utf-8', index=False)

                shutil.move(str(var.copia), str(directorio))
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Confirmacion")
                msgBox.setIcon((QtWidgets.QMessageBox.Warning))
                msgBox.setText("BD exportada con éxito")
                msgBox.exec()
        except Exception as error:
            print("Error al exportar", error)

    # Metodo para exportar con la librería xlwt
    def ExportarDatos(self):
        try:
            conexion.Conexion.exportExcel(self)
            try:
                msgBox = QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Information)
                msgBox.setText("Datos exportados con éxito.")
                msgBox.setWindowTitle("Operación completada")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()
            except Exception as error:
                print('Error en mensaje generado exportar datos ', error)
        except Exception as error:
            print('Error en evento exportar datos ', error)

    def ControlEnvio(self):
        try:
            envio = var.ui.spinEnvio.value()
            if (envio == 0):
                var.ui.lblenvio.setText("Envio 0")
            if (envio == 1):
                var.ui.lblenvio.setText("Envio 1")
            if (envio == 2):
                var.ui.lblenvio.setText("Envio 2")
            if (envio == 3):
                var.ui.lblenvio.setText("Envio 3")
        except Exception as error:
            print("Error al exportar", error)

    def Tab(self):
        try:
            _translate = QtCore.QCoreApplication.translate

            if (var.ui.tabPrograma.currentIndex() == 2):
                var.ui.tabPrograma.setGeometry(QtCore.QRect(10, 20, 951, 401))
                var.ui.tabClientes.setGeometry(QtCore.QRect(10, 450, 951, 271))
                var.ui.tabFact.setGeometry(QtCore.QRect(10, 450, 256, 271))
                var.ui.line.setGeometry(QtCore.QRect(10, 430, 941, 20))
                item = QtWidgets.QTableWidgetItem()
                var.ui.tabClientes.setHorizontalHeaderItem(0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(0, 0, 0, 0))
                var.ui.tabClientes.setHorizontalHeaderItem(1, item)
                item = QtWidgets.QTableWidgetItem()
                var.ui.tabClientes.setHorizontalHeaderItem(2, item)
                item = var.ui.tabClientes.horizontalHeaderItem(0)
                item.setText(_translate("MainWindow", "Codigo"))
                item = var.ui.tabClientes.horizontalHeaderItem(1)
                item.setText(_translate("MainWindow", "Nombre"))
                item = var.ui.tabClientes.horizontalHeaderItem(2)
                item.setText(_translate("MainWindow", "Precio-Unidad"))
                var.ui.tabClientes.setRowCount(0)
                Eventos.resizeTablaProd(self)
                conexion.Conexion.cargarTablaProd()
                Eventos.ClearFormProd(self)

                var.ui.tabClientes.setColumnCount(3)
            if (var.ui.tabPrograma.currentIndex() == 0):
                var.ui.line.setGeometry(QtCore.QRect(10, 430, 941, 20))
                var.ui.tabPrograma.setGeometry(QtCore.QRect(10, 20, 951, 401))
                var.ui.tabClientes.setGeometry(QtCore.QRect(10, 450, 951, 271))
                var.ui.tabFact.setGeometry(QtCore.QRect(10, 450, 256, 271))
                var.ui.tabClientes.setColumnCount(5)
                var.ui.tabClientes.setRowCount(0)
                item = QtWidgets.QTableWidgetItem()
                var.ui.tabClientes.setHorizontalHeaderItem(0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(0, 0, 0, 0))
                var.ui.tabClientes.setHorizontalHeaderItem(1, item)
                item = QtWidgets.QTableWidgetItem()
                var.ui.tabClientes.setHorizontalHeaderItem(2, item)
                item = QtWidgets.QTableWidgetItem()
                var.ui.tabClientes.setHorizontalHeaderItem(3, item)
                item = QtWidgets.QTableWidgetItem()
                var.ui.tabClientes.setHorizontalHeaderItem(4, item)
                item = var.ui.tabClientes.horizontalHeaderItem(0)
                item.setText(_translate("MainWindow", "DNI"))
                item = var.ui.tabClientes.horizontalHeaderItem(1)
                item.setText(_translate("MainWindow", "Apellidos"))
                item = var.ui.tabClientes.horizontalHeaderItem(2)
                item.setText(_translate("MainWindow", "Nombre"))
                item = var.ui.tabClientes.horizontalHeaderItem(3)
                item.setText(_translate("MainWindow", "Fecha Alta"))
                item = var.ui.tabClientes.horizontalHeaderItem(4)
                item.setText(_translate("MainWindow", "Forma de pago"))
                Eventos.resizeTablaCli(self)
                conexion.Conexion.cargarTablaCli()
                Eventos.ClearForm(self)
            if (var.ui.tabPrograma.currentIndex() == 1):
                var.ui.line.setGeometry(QtCore.QRect(10, 190, 941, 20))
                var.ui.tabClientes.setGeometry(QtCore.QRect(270, 210, 691, 521))
                var.ui.tabPrograma.setGeometry(QtCore.QRect(10, 20, 951, 171))
                var.ui.tabFact.setGeometry(QtCore.QRect(10, 210, 256, 521))
                Eventos.resizeTablaFac(self)
                conexion.Conexion.cargarTablaFac()
        except Exception as error:
            print("Error al tabular", error)

    def resizeTablaProd(self):
        try:
            header = var.ui.tabClientes.horizontalHeader()
            for i in range(3):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                if i == 0:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        except Exception as error:
            print("Error al cambiar el tamaño de las columnas", error)

    def resizeTablaFac(self):
        try:
            header= var.ui.tabFact.horizontalHeader()
            for i in range(2):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        except Exception as error:
            print("Error al cambiar el tamaño de las columnas", error)
