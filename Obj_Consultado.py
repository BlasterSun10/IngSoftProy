from tkinter import *
from tkinter import ttk
import pandas as pd
import mysql.connector
import Inventario_Vendedor
import Inventario
from generapdf import *


def cerrarventana():#si se cierra la ventana
    Inventario_Vendedor.consultaabierta = FALSE
    Inventario.consultaabierta = FALSE
    veninv.destroy()

def funcion_iradatos(id):#se genera el reporte y se cierra la ventana
    funcion_datos(id)
    Inventario_Vendedor.consultaabierta = FALSE
    Inventario.consultaabierta = FALSE
    veninv.destroy()

#Solo muestra el objeto consultado, no permite ninguna otra accion
def main(datos_con):
    global veninv
    veninv=Tk()
    veninv.title("Articulo consultado")
    veninv.geometry('600x500')
    #centrar ventana
    veninv.update_idletasks()
    ancho_ventana = veninv.winfo_width()#para saber el ancho de la pantalla
    altura_ventana = veninv.winfo_height()#para saber el largo(altura) de la pantalla
    x = (veninv.winfo_screenwidth() // 2) - (ancho_ventana // 2)# // para hacer funcion piso bueno se redondea hacia abajo y queda como entero
    y = (veninv.winfo_screenheight() // 2) - (altura_ventana // 2)
    veninv.geometry('+{}+{}'.format(x, y - 30)) #sele resta 30 a y ya que es lo de la barra de tareas para que no afecte visualmente
    veninv.resizable(0,0)
    #root.iconbitmap()
    
    bm=Menu()
    veninv.config(menu=bm, width=300, height=300)
    
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')
    con=conexion.cursor()
    sql="SELECT * FROM articulos WHERE IDArt=%s"
    con.execute(sql,datos_con) 
    usu=con.fetchone()
    
    IDArti=Label(veninv,text='ID: ')
    IDArti.config(font=('Arial',12,'bold'))
    IDArti.grid(row=0,column=0)
    
    IDArtip=Label(veninv,text=usu[0])
    IDArtip.config(font=('Arial',12,'bold'))
    IDArtip.grid(row=0,column=1)
    
    nombre=Label(veninv,text='Nombre: ')
    nombre.config(font=('Arial',12,'bold'))
    nombre.grid(row=1,column=0)
    
    nombrep=Label(veninv,text=usu[1])
    nombrep.config(font=('Arial',12,'bold'))
    nombrep.grid(row=1,column=1)
    
    precio=Label(veninv,text='Precio: ')
    precio.config(font=('Arial','12','bold'))
    precio.grid(row=2,column=0)
    
    preciop=Label(veninv,text=usu[2])
    preciop.config(font=('Arial','12','bold'))
    preciop.grid(row=2,column=1)
    
    descripcion=Label(veninv,text='Descripcion: ')
    descripcion.config(font=('Arial','12','bold'))
    descripcion.grid(row=3,column=0)
    
    descripcionp=Label(veninv,text=usu[3])
    descripcionp.config(font=('Arial','12','bold'))
    descripcionp.grid(row=3,column=1)
    
    modelo=Label(veninv,text='Modelo: ')
    modelo.config(font=('Arial','12','bold'))
    modelo.grid(row=4,column=0)
    
    modelop=Label(veninv,text=usu[4])
    modelop.config(font=('Arial','12','bold'))
    modelop.grid(row=4,column=1)
    
    year=Label(veninv,text='Año: ')
    year.config(font=('Arial','12','bold'))
    year.grid(row=5,column=0)
    
    yearp=Label(veninv,text=usu[5])
    yearp.config(font=('Arial','12','bold'))
    yearp.grid(row=5,column=1)

    marca=Label(veninv,text='Marca: ')
    marca.config(font=('Arial','12','bold'))
    marca.grid(row=6,column=0)
    
    marcap=Label(veninv,text=usu[6])
    marcap.config(font=('Arial','12','bold'))
    marcap.grid(row=6,column=1)
    
    existencias=Label(veninv,text='Existencias: ')
    existencias.config(font=('Arial','12','bold'))
    existencias.grid(row=7,column=0)
    
    existenciasp=Label(veninv,text=usu[7])
    existenciasp.config(font=('Arial','12','bold'))
    existenciasp.grid(row=7,column=1)

    con.close()
    conexion.close()

    consulobj = Button(veninv, width=30, font=('Arial', 12, 'bold'), text='Guardar información en archivo', bg='pink', bd=5, command=lambda:funcion_iradatos(usu[0]))#la lambda es para que me acepte poner parametros, de otro modo la funcion corre sin necesidad de presionar el boton
    consulobj.grid(column=1, row=8, padx = (10,0), pady = 30)
    
    veninv.protocol("WM_DELETE_WINDOW", cerrarventana)#si se cierra la ventana

    veninv.mainloop()