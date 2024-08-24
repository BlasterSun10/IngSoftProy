import mysql.connector
from fpdf import FPDF
from estilos import *
import datetime
import tkinter as tk #para que sea mas facil el uso de la libreria usamos el alias tk si no puesieramos esto tendriamos que poner tkiner a cada rato
from tkinter import messagebox #para las ventanas emergentes


def funcion_recibo(id, pago, cant):
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')
    sql = "SELECT * FROM articulos WHERE IDArt = %s"#para conseguir los datos del articulo vendido
    cursor = conexion.cursor()


    cursor.execute(sql, (id,))
    if cursor:
        pdf = FPDF(orientation='L', unit='mm', format='A4')#orientacion de la pagina, unidad de medida (milimetros), formato de la hoja (tamaño)

        pdf.alias_nb_pages()
        pdf.add_page()#se crea una pagina en el pdf

        pdf.set_font('Arial','B',25)#estilo del texto
        pdf.cell(80)
        
        fecha = datetime.datetime.strftime(datetime.datetime.now(),"%d/%m/%Y")#fecha para agregarla en la parte de arriba
        pdf.cell(90,30,'Recibo de compra '+ fecha,0,1,'C',0)#titulo
        pdf.ln(20)#salto de linea


        #Metadatos, informacion del documento
        pdf.set_title("Recibo de pago")
        pdf.set_author("Refaccionaria")
        pdf.set_creator("Refaccionaria")
        pdf.set_keywords("recibo, PDF")
        pdf.set_subject("recibo de compra")

        #Encabezados
        pdf.set_font('Arial','B',10)
        backcol(pdf,"gris")
        pdf.cell(30, 15, "Articulo", 1, 0, "C", 1)#parametros = ancho, alto, texto, tiene borde o no, salta a la siguiente linea o no, alineacion del texto, si tiene color de relleno
        pdf.cell(20, 15, "Precio", 1, 0, "C", 1)
        pdf.cell(20, 15, "Pagado", 1, 0, "C", 1)
        pdf.cell(20, 15, "Sobrante", 1, 0, "C", 1)
        pdf.cell(40, 15, "Descripción", 1, 0, "C", 1)
        pdf.cell(20, 15, "Modelo", 1, 0, "C", 1)
        pdf.cell(20, 15, "Año", 1, 0, "C", 1)
        pdf.cell(20, 15, "Marca", 1, 0, "C", 1)
        pdf.cell(20, 15, "Cantidad", 1, 0, "C", 1)
        pdf.cell(50, 15, "Fecha de compra", 1, 1, "C", 1)

        pdf.set_font('Arial','',8)
        for dato in cursor:
            backcol(pdf,"blanco")
            pdf.cell(30, 15, str(dato[1]), 1, 0, "C", 1)#parametros = ancho, alto, texto, tiene borde o no, salta a la siguiente linea o no, alineacion del texto, si tiene color de relleno
            pdf.cell(20, 15, str(dato[2]), 1, 0, "C", 1)
            pdf.cell(20, 15, str(pago), 1, 0, "C", 1)
            pdf.cell(20, 15, str(pago-int(dato[2])), 1, 0, "C", 1)#sobrante es la resta entre el pago realizado y el precio del producto
            pdf.cell(40, 15, str(dato[3]), 1, 0, "C", 1)
            pdf.cell(20, 15, str(dato[4]), 1, 0, "C", 1)
            pdf.cell(20, 15, str(dato[5]), 1, 0, "C", 1)
            pdf.cell(20, 15, str(dato[6]), 1, 0, "C", 1)
            pdf.cell(20, 15, str(cant), 1, 0, "C", 1)
            pdf.cell(50, 15, str(datetime.datetime.now()), 1, 1, "C", 1)

        ruta = "recibos/recibo-"+datetime.datetime.strftime(datetime.datetime.now(),"%d-%m-%Y-%H-%M-%S")+".pdf"
        pdf.output(ruta,'F')#la F hace que se guarde en los archivos, existen otras opciones como abrrilo en el navegador o forzar descarga
        messagebox.showinfo("recibo generado", "se genero un recibo en recibos")
    else:
        messagebox.showinfo("recibo no generado", "no se genero un recibo en recibos")
    conexion.close()


def funcion_datos(id):
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')
    sql = "SELECT * FROM articulos WHERE IDArt = %s"#para conseguir los datos del articulo vendido
    cursor = conexion.cursor()


    cursor.execute(sql, (id,))
    if cursor:
        pdf = FPDF(orientation='L', unit='mm', format=(150, 100))#orientacion de la pagina, unidad de medida (milimetros), formato de la hoja (tamaño)

        pdf.alias_nb_pages()
        pdf.add_page()

        pdf.set_font('Arial','B',12)#estilo del texto
        pdf.cell(30,15,'Datos del articulo',0,1,'C',0)#titulo
        pdf.ln(10)#salto de linea


        #Metadatos, informacion del documento
        pdf.set_title("Datos de articulo")
        pdf.set_author("Refaccionaria")
        pdf.set_creator("Refaccionaria")
        pdf.set_keywords("datos, PDF")
        pdf.set_subject("Datos de articulo")

    
        pdf.set_font('Arial','B',10)
        for dato in cursor:
            #se muestran los datos obtenidos
            pdf.cell(0, 11, f"ID: \t{dato[0]}", 0, 1)#parametros = ancho, alto, texto, tiene borde o no, salta a la siguiente linea o no
            pdf.cell(0, 11, f"Nombre: \t{dato[1]}", 0, 1)
            pdf.cell(0, 11, f"Precio: \t{dato[2]}", 0, 1)
            pdf.cell(0, 11, f"Descripcion: \t{dato[3]}", 0, 1)
            pdf.cell(0, 11, f"Modelo: \t{dato[4]}", 0, 1)
            pdf.cell(0, 11, f"Año: \t{dato[5]}", 0, 1)
            pdf.cell(0, 11, f"Marca: \t{dato[6]}", 0, 1)
            pdf.cell(0, 11, f"Existencias: \t{dato[7]}", 0, 1)
        ruta = "datos/Datos de-"+str(dato[1])+" Modelo - "+str(dato[4])+" Año - "+str(dato[5])+" Marca - "+str(dato[6])+".pdf"
        pdf.output(ruta,'F')#la F hace que se guarde en los archivos, existen otras opciones como abrrilo en el navegador o forzar descarga
        messagebox.showinfo("generado", "se genero un archivo de datos en datos")
    else:
        messagebox.showinfo("no generado", "no se genero un archivo de datos en datos")
    conexion.close()