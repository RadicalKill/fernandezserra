'''
Gestion facturacion
'''
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
            var.ui.txtCliFac.setText(nombre)

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