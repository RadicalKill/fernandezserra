

import var
import sys

class Eventos():
    def Salir(self):
        try:
            sys.exit()
        except Exception as error:
            print("Error al salir",error)