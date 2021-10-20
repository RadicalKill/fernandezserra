

from window import *
import sys,var

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