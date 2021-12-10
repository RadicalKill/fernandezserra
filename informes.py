import os, var
from PyQt5 import QtSql,QtWidgets
from reportlab.pdfgen import canvas
from datetime import date, datetime

class Informes():

    def cabecera_(self):
        try:
            logo = "img/calend.png"
            var.cv.line(40, 800, 500, 800)
            var.cv.line(40, 700, 500, 700)
            var.cv.setFont('Helvetica-Bold', 14)
            var.cv.drawString(50, 785, 'Import-Export Vigo')
            var.cv.setFont('Helvetica-Bold', 10)
            var.cv.drawString(50, 770, 'Cif: A00000000F')
            var.cv.drawString(50, 755, 'Direcion: A00000000F')
            var.cv.drawString(50, 740, 'Vigo: A00000000F')
            var.cv.drawString(50, 725, 'Correo: A00000000F')
            var.cv.drawImage(logo,425,700)



        except Exception as error:
            print('Error en cabecera informe', error)

    def pie(texto):
        try:
            var.cv.line(50,50,530,50)
            fecha=datetime.today()
            fecha=fecha.strftime("%d.%m.%Y %H.%M.%S")
            var.cv.setFont("Helvetica",size=6)
            var.cv.drawString(70,40,str(fecha))
            var.cv.drawString(255,40,str(texto))
            var.cv.drawString(510,40,str("Página %s"%var.cv.getPageNumber()))
        except Exception as error: print("Error en cabecera informes", error)

    def listadoClientes(self):
        try:
            var.cv = canvas.Canvas('informes/listadoClientes.pdf')
            Informes.cabecera_(self)
            var.cv.setFont('Helvetica-Bold', size=9)
            var.cv.setTitle('Listado Clientes')
            var.cv.setAuthor('Departamento de administración')
            textoTitulo= 'Listado Clientes'
            var.cv.drawString(255,690,textoTitulo)
            var.cv.line(40,685,530,685)
            items=["DNI","Nombre","Formas de pago"]
            var.cv.drawString(70,675,items[0])
            var.cv.drawString(220,675,items[1])
            var.cv.drawString(330,675,items[2])
            var.cv.line(40,670,530,670)
            query = QtSql.QSqlQuery()
            query.prepare("select dni, apellidos, nombre, pagos from clientes order by apellidos, nombre")

            if query.exec_():
                x=50
                y=655
                while query.next():
                    if y>=80:
                        var.cv.setFont("Helvetica", size=8)
                        var.cv.drawString(x,y,str(query.value(0)))
                        var.cv.drawString(x+150,y,str(query.value(1))+"    " + query.value(2))
                        var.cv.drawString(x+280,y,str(query.value(3)))
                        y= y-20
                    else:
                        var.cv.drawString(460,30,"Página siguiente....")
                        var.cv.showPage()
                        Informes.cabecera_(self)
                        Informes.pie(textoTitulo)
                        var.cv.line(40, 685, 530, 685)
                        items = ["DNI", "Nombre", "Formas de pago"]
                        var.cv.setFont('Helvetica-Bold', size=9)
                        var.cv.drawString(70, 675, items[0])
                        var.cv.drawString(220, 675, items[1])
                        var.cv.drawString(330, 675, items[2])
                        var.cv.line(40, 670, 530, 670)
                        x=50
                        y=655
            Informes.pie(textoTitulo)
            var.cv.save()
            rootPath = '.\\informes'
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('.pdf'):
                    os.startfile('%s/%s' % (rootPath, file))
                cont += 1


        except Exception as error:
            print('Error en informes', error)
