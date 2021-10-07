'''
gestion clientes
'''
import var
from window import *


class Clientes():
    def validarDNI():
        try:
            dni= var.ui.txtDNI.text()
            tabla="TRWAGMYFPDXBNJZSQVHLCKE" #Letra DNI
            dig_ext= "XYZ"  #DIGITO EXTRANJEROS
            reemp_dig_ext= {"X":0,"Y":1,"Z":2}
            numeros= "1234567890"
            dni= dni.upper()
            if len(dni)==9:
                dig_control= dni[8]
                dni=dni[:8]
                if dni[0] in dig_ext:
                    dni= dni.replace(dni[0],reemp_dig_ext(dni[0]))
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni)%23] == dig_control:
                    var.ui.ValidarDNI.setStyleSheet ("QLabel{color:green;}")
                    var.ui.ValidarDNI.setText("Menudo cumbiote cabron")
                else:
                    var.ui.ValidarDNI.setStyleSheet("QLabel{color:red;}")
                    var.ui.ValidarDNI.setText("La erraste pendejo")



        except Exception as error: print("Error en modulo validarDNI")
