from tkinter import *
from tkinter import ttk #para el estilo y la tabla
from tkinter import messagebox #para las ventanas emergentes
import pandas as pd
import mysql.connector
import Inventario
import menuadmin
from datetime import datetime#para el año actual

def cerrarventana():#si se cierra la ventana
    if messagebox.askokcancel("Atención", "¿Seguro que quieres salir de la aplicacion?"):
        veninv.destroy()

def funcion_regresar():#paar regresar a inventario
    veninv.destroy()
    Inventario.main()

def funcion_regresar2():#para regresar al menu
    veninv.destroy()
    menuadmin.main()

def guardar_datos():
    global conexion, con, nome, pre, desc, model, yearentry, marcaentry, exis, veninv#para que se puedan usar en otras partes
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')
    con=conexion.cursor()#creacion del cursor
    if nome.get().strip()=="" or pre.get().strip()=="" or desc.get().strip()=="" or model.get().strip()=="" or yearentry.get().strip()=="" or marcaentry.get().strip()=="" or exis.get().strip()=="":#los strip quitan espacios, y con los or se checa si alguno de los entrys estaba vacio
        messagebox.showerror("Atención", "Debes llenar todos los campos")#si algun campo esta vacio salta la advertencia
    else:#si esta todo lleno
        if pre.get().isdigit() and exis.get().isdigit() and yearentry.get().isdigit():#si todos son numeros nomas se puede avanzar
            if int(pre.get()) < 0 or int(exis.get()) < 0:
                messagebox.showinfo("Atención", "Las cantidades deben ser mayor a 0")#mustra que se hizo el cambio
            else:
                if int(yearentry.get()) >= 1886 and int(yearentry.get()) <= datetime.now().year:
                    #se checa si ya esta en la base de datos
                    consulta = "SELECT * FROM articulos WHERE NomArt = %s AND ModeloArt = %s AND AnioART = %s AND MarcaArt = %s"#consulta, para ver si el usuario ya existe en la base de datos
                    con.execute(consulta, (nome.get(), model.get(), yearentry.get(), marcaentry.get()))#se checa si todos estos datos coinciden, y si lo hacen ese articulo ya existe
                    encontrado = con.fetchall()#para conseguir todas las filas de la tabla en caso de que el valor se repita
                    if encontrado:#si el articulo ya existe
                        messagebox.showerror("Atención", "Este articulo ya existe")#si ya existe se advierte
                    else:#si no existe el articulo en la base de dato se puede insertar
                        sql="INSERT INTO articulos (IDArt, NomArt, PrecioArt, DescArti, ModeloArt, AnioArt, MarcaArt, ExistArt, ImagenArt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        datos = ('', nome.get(), pre.get(), desc.get(), model.get(), yearentry.get(), marcaentry.get(), exis.get(), '')#se llenan los %s que se pusieron en la consulta con los datos agarrados de los entrys
                        messagebox.showinfo("Accion realizada", "articulo {}, agregado correctamente".format(nome.get()))#si esta todo correcto se añade
                        con.execute(sql, datos)#se ejecuta la consulta
                        conexion.commit()#commit actualiza la base de datos
                        con.close()#se cieera el cursor
                        conexion.close()#se cierra la conexion
                        limpiar_entradas()#se limpian todos los entrys
                else: 
                    messagebox.showinfo("Atención", "el año debe ser veridico")#mustra que se hizo el cambio
        else:
            messagebox.showinfo("Atención", "precio, existencias y año deben ser cantidades numericas")#mustra que se hizo el cambio
    show_tabla()

 
def limpiar_entradas():
    nome.delete(0, 'end')  # Borra el texto desde el inicio hasta el final
    pre.delete(0, 'end')
    desc.delete(0, 'end')
    model.delete(0, 'end')
    yearentry.delete(0, 'end')
    marcaentry.delete(0, 'end')
    exis.delete(0, 'end')

def datos_inventario():#para las filas de la tabla
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')#conexion a la base de datos  
    con=conexion.cursor()#cursor para hacer la consulta
    sql="SELECT * FROM articulos"#consulta
    con.execute(sql)#se ejecuta la consulta
    inv=con.fetchall()#se consiguen todos los registros o filas que coinciden
    for x in inv:
        tabla.insert('','end',values=x)

def show_tabla():#para los encabezados
    global tabla
    style = ttk.Style()#crear un estilo
    style.configure("Treeview", background="#3EA116", foreground="white")
    tabla=ttk.Treeview(veninv,columns=("ID","Nombre","Precio","Descripcion","Modelo","Anio","Marca","Existencias"),show="headings")#paraponer los encabezados
    
    tabla.grid(columnspan=4, column=0, row=9, pady=5, padx=20)
    
    for col in ("ID","Nombre","Precio","Descripcion","Modelo","Anio","Marca","Existencias"):#encabezados de la tabla
        tabla.column(col,width=90, anchor=CENTER)#dimensiones de cada columna
        tabla.heading(col,text=col)#encabezado de columna
    datos_inventario()#ahora que ya estan los encabezados siguen las filas
    

def main():
    global nome, pre, desc, model, yearentry, marcaentry, exis, veninv
    veninv=Tk()
    veninv.title("Registrar articulos")
    veninv.geometry('800x600')
    #centrar ventana
    veninv.update_idletasks()
    ancho_ventana = veninv.winfo_width()#para saber el ancho de la pantalla
    altura_ventana = veninv.winfo_height()#para saber el largo(altura) de la pantalla
    x = (veninv.winfo_screenwidth() // 2) - (ancho_ventana // 2)# // para hacer funcion piso bueno se redondea hacia abajo y queda como entero
    y = (veninv.winfo_screenheight() // 2) - (altura_ventana // 2)
    veninv.geometry('+{}+{}'.format(x, y - 30)) #sele resta 30 a y ya que es lo de la barra de tareas para que no afecte visualmente
    veninv.resizable(0,0)
    #root.iconbitmap()
    
    #es para crear un menu
    bm=Menu()
    veninv.config(menu=bm, width=300, height=300)
    
    menuinicio=Menu(bm, tearoff=0)#tearoff en 0 para que el menu no se pueda desprender
    bm.add_cascade(label='Menu', menu=menuinicio)#se le pone Menu como texto
    
    #opciones del menu
    menuinicio.add_command(label='Regresar a inventario', command=funcion_regresar)
    menuinicio.add_command(label='Regresar a menu', command=funcion_regresar2)
    
    nombre=Label(veninv,text='Nombre: ')
    nombre.config(font=('Arial',12,'bold'))
    nombre.grid(row=0,column=0, padx=(120,0), pady=(50,0))
    
    nome=Entry(veninv)
    nome.config(width=50, font=('Arial',12))
    nome.grid(row=0,column=1, pady=(50,0))
    
    precio=Label(veninv,text='Precio: ')
    precio.config(font=('Arial','12','bold'))
    precio.grid(row=1,column=0, padx=(120,0))
    
    pre=Entry(veninv)
    pre.config(width=50, font=('Arial',12))
    pre.grid(row=1,column=1)
    
    descripcion=Label(veninv,text='Descripcion: ')
    descripcion.config(font=('Arial','12','bold'))
    descripcion.grid(row=2,column=0, padx=(120,0))
    
    desc=Entry(veninv)
    desc.config(width=50, font=('Arial',12))
    desc.grid(row=2,column=1)
    
    modelo=Label(veninv,text='Modelo: ')
    modelo.config(font=('Arial','12','bold'))
    modelo.grid(row=3,column=0, padx=(120,0))
    
    model=Entry(veninv)
    model.config(width=50, font=('Arial',12))
    model.grid(row=3,column=1)
    
    year=Label(veninv,text='Año: ')
    year.config(font=('Arial','12','bold'))
    year.grid(row=4,column=0, padx=(120,0))
    
    yearentry=Entry(veninv)
    yearentry.config(width=50, font=('Arial',12))
    yearentry.grid(row=4,column=1)
    
    marca=Label(veninv,text='Marca: ')
    marca.config(font=('Arial','12','bold'))
    marca.grid(row=5,column=0, padx=(120,0))
    
    marcaentry=Entry(veninv)
    marcaentry.config(width=50, font=('Arial',12))
    marcaentry.grid(row=5,column=1)
    
    existencias=Label(veninv,text='Existencias: ')
    existencias.config(font=('Arial','12','bold'))
    existencias.grid(row=6,column=0, padx=(120,0))
    
    exis=Entry(veninv)
    exis.config(width=50, font=('Arial',12))
    exis.grid(row=6,column=1)

    #boton
    agregar = Button(veninv, width=20, font=('Arial', 12, 'bold'), text='Agregar', bg='orange', bd=5, command=guardar_datos)
    agregar.grid(column=1, row=8, pady=(30, 20))
    
    show_tabla()#mostrar tabla

    veninv.protocol("WM_DELETE_WINDOW", cerrarventana)#si se cierra la ventana
    
    veninv.mainloop()#para que no se cierre la ventana

    
 
    