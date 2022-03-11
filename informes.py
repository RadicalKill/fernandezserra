import locale
import os, var
from PyQt5 import QtSql, QtWidgets
from reportlab.pdfgen import canvas
from datetime import date, datetime

import conexion


class Informes():

    def cabecera_(self):
        try:
            logo = ".\\img\logo.png"
            var.cv.line(40, 800, 500, 800)
            var.cv.line(40, 700, 500, 700)
            var.cv.setFont('Helvetica-Bold', 14)
            var.cv.drawString(50, 785, 'Import-Export Vigo')
            var.cv.setFont('Helvetica-Bold', 10)
            var.cv.drawString(50, 770, 'Cif: A00000000F')
            var.cv.drawString(50, 755, 'Direcion: A00000000F')
            var.cv.drawString(50, 740, 'Vigo: A00000000F')
            var.cv.drawString(50, 725, 'Correo: A00000000F')
            var.cv.drawImage(logo, 455, 730)



        except Exception as error:
            print('Error en cabecera informe', error)

    def pie(texto):
        try:
            var.cv.line(50, 50, 530, 50)
            fecha = datetime.today()
            fecha = fecha.strftime("%d.%m.%Y %H.%M.%S")
            var.cv.setFont("Helvetica", size=6)
            var.cv.drawString(70, 40, str(fecha))
            var.cv.drawString(255, 40, str(texto))
            var.cv.drawString(510, 40, str("Página %s" % var.cv.getPageNumber()))
        except Exception as error:
            print("Error en cabecera informes", error)

    def listadoClientes(self):
        try:
            var.cv = canvas.Canvas('informes/listadoClientes.pdf')
            Informes.cabecera_(self)
            var.cv.setFont('Helvetica-Bold', size=9)
            var.cv.setTitle('Listado Clientes')
            var.cv.setAuthor('Departamento de administración')
            textoTitulo = 'Listado Clientes'
            var.cv.drawString(255, 690, textoTitulo)
            var.cv.line(40, 685, 530, 685)
            items = ["DNI", "Nombre", "Formas de pago"]
            var.cv.drawString(70, 675, items[0])
            var.cv.drawString(220, 675, items[1])
            var.cv.drawString(330, 675, items[2])
            var.cv.line(40, 670, 530, 670)
            query = QtSql.QSqlQuery()
            query.prepare("select dni, apellidos, nombre, pagos from clientes order by apellidos, nombre")

            if query.exec_():
                x = 50
                y = 655
                while query.next():
                    if y >= 80:
                        var.cv.setFont("Helvetica", size=8)
                        var.cv.drawString(x, y, str(query.value(0)))
                        var.cv.drawString(x + 150, y, str(query.value(1)) + "    " + query.value(2))
                        var.cv.drawString(x + 280, y, str(query.value(3)))
                        y = y - 20
                    else:
                        var.cv.drawString(460, 30, "Página siguiente....")
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
                        x = 50
                        y = 655
            Informes.pie(textoTitulo)
            var.cv.save()
            rootPath = '.\\informes'
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('listadoClientes.pdf'):
                    os.startfile('%s/%s' % (rootPath, file))
                cont += 1


        except Exception as error:
            print('Error en informes', error)

    def listadoProductos(self):
        try:
            var.cv = canvas.Canvas('informes/listadoProductos.pdf')
            Informes.cabecera_(self)
            var.cv.setFont('Helvetica-Bold', size=9)
            var.cv.setTitle('Listado Productos')
            var.cv.setAuthor('Departamento de administración')
            textoTitulo = 'Listado Productos'
            var.cv.drawString(255, 690, textoTitulo)
            var.cv.line(40, 685, 530, 685)
            items = ["Codigo", "Nombre", "Precio/Unidad"]
            var.cv.drawString(70, 675, items[0])
            var.cv.drawString(220, 675, items[1])
            var.cv.drawString(420, 675, items[2])
            var.cv.line(40, 670, 530, 670)
            query = QtSql.QSqlQuery()
            query.prepare("select codigo, nombre, precio from articulos order by codigo")

            if query.exec_():
                x = 80
                y = 655
                while query.next():
                    if y >= 80:
                        var.cv.setFont("Helvetica", size=8)
                        var.cv.drawString(x, y, str(query.value(0)))
                        var.cv.drawString(x + 140, y, str(query.value(1)))
                        var.cv.drawString(x + 360, y, str(query.value(2)))
                        y = y - 20
                    else:
                        var.cv.drawString(460, 30, "Página siguiente....")
                        var.cv.showPage()
                        Informes.cabecera_(self)
                        Informes.pie(textoTitulo)
                        var.cv.line(40, 685, 530, 685)
                        items = ["Codigo", "Nombre", "Precio/Unidad"]
                        var.cv.setFont('Helvetica-Bold', size=9)
                        var.cv.drawString(70, 675, items[0])
                        var.cv.drawString(220, 675, items[1])
                        var.cv.drawString(330, 675, items[2])
                        var.cv.line(40, 670, 530, 670)
                        x = 50
                        y = 655
            Informes.pie(textoTitulo)
            var.cv.save()
            rootPath = '.\\informes'
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('listadoProductos.pdf'):
                    os.startfile('%s/%s' % (rootPath, file))
                cont += 1


        except Exception as error:
            print('Error en informes', error)

    def factura(self):
        """

        Módulo para crear el informe de una determinada factura con las líneas de ventas
        de  esta en formato PDF

        """
        try:

            codfac = var.ui.lblnumfac.text()
            var.cv: canvas.Canvas
            var.cv = canvas.Canvas('informes/factura.pdf')
            var.cv.setTitle('Factura')
            var.cv.setAuthor('Departamento de administracion')
            datos_cliente = []
            datos_cliente = conexion.Conexion.buscaCliFac(var.ui.txtDNIFact.text())


            var.cv.setFont('Helvetica-Bold', 8)
            var.cv.drawString(260, 785, 'Datos cliente: ')
            var.cv.drawString(250, 770, 'DNI/CIF: ' + var.ui.txtDNIFact.text())
            var.cv.drawString(250, 755, 'Cliente: ' + var.ui.lblCliFac.text())
            var.cv.drawString(250, 740, 'Dirección: ' + str(datos_cliente[2]))
            var.cv.drawString(250, 725, 'Municipio: ' + str(datos_cliente[3] + " Provincia: " + str(datos_cliente[4])))

            var.cv.setFont('Helvetica-Bold', 10)
            textoTitulo = 'Factura'
            Informes.cabecera_(self)
            Informes.pie(textoTitulo)
            var.cv.setFont('Helvetica-Bold', 10)
            var.cv.drawString(255, 690, textoTitulo + ':' + str(codfac))
            var.cv.line(40, 685, 530, 685)
            items = ['Venta', 'Artículo', 'Precio', 'Cantidad', 'Total']
            var.cv.drawString(65, 675, items[0])
            var.cv.drawString(150, 675, items[1])
            var.cv.drawString(290, 675, items[2])
            var.cv.drawString(390, 675, items[3])
            var.cv.drawString(490, 675, items[4])
            var.cv.line(40, 670, 530, 670)

            suma = 0.0
            iva = 0.0
            total = 0.0

            index = 0
            var.num_index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select codven, precio, cantidad, codprof from ventas where codfacf = :codfac')
            query.bindValue(':codfac', int(codfac))
            if query.exec_():
                i = 50
                j = 655

                while query.next():
                    codventa = query.value(0)
                    articulo = query.value(3)
                    nombre_articulo = conexion.Conexion.nombreDeArticulo(articulo)

                    precio = query.value(1)
                    precio = str('{:.2f}'.format(precio))
                    cantidad = query.value(2)
                    precio_convertido = str(precio).replace(',', '.')
                    print(precio_convertido)
                    precio_convertido = round(float(precio), 2)
                    total_linea = round(precio_convertido * cantidad, 2)
                    subtotal = total_linea
                    suma = suma + float(subtotal)
                    iva = suma * 0.21
                    total = suma + iva
                    subtotal_format = str('{:.2f}'.format(suma))
                    iva_format = str('{:.2f}'.format(iva))

                    total = str('{:.2f}'.format(total))
                    total_linea = str(total_linea) + " €"

                    if j <= 80:
                        # Para saltar de página y colocar pie y cabecera en la nueva
                        var.cv.drawString(460, 30, 'Página siguiente...')  # Ellos están poniendo esta línea más abajo
                        var.cv.showPage()  # Avanza la página
                        var.cv.setFont('Helvetica-Bold', 10)
                        var.cv.drawString(255, 690, textoTitulo + ':' + str(codfac))
                        var.cv.line(40, 685, 530, 685)
                        items = ['Venta', 'Artículo', 'Precio', 'Cantidad', 'Total']
                        var.cv.drawString(65, 675, items[0])
                        var.cv.drawString(150, 675, items[1])
                        var.cv.drawString(290, 675, items[2])
                        var.cv.drawString(390, 675, items[3])
                        var.cv.drawString(490, 675, items[4])
                        var.cv.line(40, 670, 530, 670)
                        Informes.cabecera(self)
                        Informes.pie(textoTitulo)
                        i = 50
                        j = 655
                    var.cv.setFont('Helvetica', 8)
                    var.cv.drawRightString(i + 20, j, str(codventa))
                    var.cv.drawString(i + 100, j, str(nombre_articulo))
                    var.cv.drawRightString(i + 270, j, str(locale.currency(float(precio))))
                    cantidad = str('{:.2f}'.format(cantidad))
                    var.cv.drawRightString(i + 370, j, str(cantidad))
                    var.cv.drawRightString(i + 470, j, str(locale.currency(float(subtotal))))
                    j -= 20
                    var.num_index = index


                if j <= 65 or j > 100:
                    var.cv.line(40, j, 530, j)
                    var.cv.setFont('Helvetica', 8)

                    var.cv.drawRightString(i + 420, j - 10, str("Subtotal: "))
                    var.cv.drawRightString(i + 475, j - 10, str(subtotal_format + " €"))
                    var.cv.drawRightString(i + 420, j - 20, str("IVA: "))
                    var.cv.drawRightString(i + 475, j - 20, iva_format + " €")
                    var.cv.drawRightString(i + 420, j - 30, str("Total venta: "))
                    var.cv.drawRightString(i + 475, j - 30, str(total + " €"))
                else:
                    var.cv.drawString(460, 65, 'Página siguiente...')  # Ellos están poniendo esta línea más abajo
                    var.cv.showPage()  # Avanza la página
                    var.cv.setFont('Helvetica-Bold', 10)
                    var.cv.drawString(255, 690, textoTitulo + ':' + str(codfac))
                    var.cv.line(40, 685, 530, 685)
                    # var.cv.line(40, 670, 530, 670)
                    Informes.cabecera(self)
                    Informes.pie(textoTitulo)
                    i = 50
                    j = 655
                    var.cv.drawRightString(i + 420, j - 10, str("Subtotal: "))
                    var.cv.drawRightString(i + 475, j - 10, str(subtotal_format + " €"))
                    var.cv.drawRightString(i + 420, j - 20, str("IVA: "))
                    var.cv.drawRightString(i + 475, j - 20, iva_format + " €")
                    var.cv.drawRightString(i + 420, j - 30, str("Total venta: "))
                    var.cv.drawRightString(i + 475, j - 30, str(total + " €"))




            else:
                print('Error:', query.lastError().text())

            var.cv.save()
            rootPath = '.\\Informes'
            cont = 0

            # Abrimos el archivo. Usa un for porque le quedó así de "veces anteriores"
            # dice que luego puede ser útil
            for file in os.listdir(rootPath):
                if file.endswith('factura.pdf'):
                    os.startfile('%s/%s' % (rootPath, file))





        except Exception as error:
            print('Error en  informe factura', error)
