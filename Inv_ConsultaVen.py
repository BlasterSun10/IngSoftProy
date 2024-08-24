from tkinter import *
from tkinter import ttk
from tkinter import messagebox #para las ventanas emergentes
import pandas as pd
import mysql.connector
import Obj_Consultado
import Inventario_Vendedor
import ConsultaInterfaceVendedor
import Modificar_Interfaz 

def cerrarventana():#si se cierra la ventana
    if messagebox.askokcancel("Atención", "¿Seguro que quieres regresar a consulta?"):
        veninv.destroy()
        ConsultaInterfaceVendedor.main()

def funcion_regresar():#paar regresar a inventario
    veninv.destroy()
    Inventario_Vendedor.main()

def funcion_regresar2():#para regresar a consulta
    veninv.destroy()
    ConsultaInterfaceVendedor.main()

def datos_inventario(idar,nombre,precio,descripcion,modelo,anio,marca):#para las filas de la tabla
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')#conexion a la base de datos
    con=conexion.cursor()#cursor para hacer la consulta
    sql="SELECT * FROM articulos WHERE IDArt=%s OR NomArt=%s OR PrecioArt=%s OR DescArti=%s OR ModeloArt=%s OR AnioArt=%s OR MarcaArt=%s"#de esta manera conque envies un dato te kostraria las coincidencias, entre mas datos pongas maas certera sera la busqueda
    datos=(idar,nombre,precio,descripcion,modelo,anio,marca)
    con.execute(sql,datos)
    inv=con.fetchall()#se consiguen todos los registros o filas que coinciden
    for x in inv:
        tabla.insert('','end',values=x)

def show_tabla(idar,nombre,precio,descripcion,modelo,anio,marca):#para los encabezados
    global tabla
    style = ttk.Style()#crear un estilo
    style.configure("Treeview", background="#BEA80D", foreground="white")
    tabla=ttk.Treeview(veninv,columns=("ID","Nombre","Precio","Descripcion","Modelo","Anio","Marca","Existencias"),show="headings")#paraponer los encabezados
    
    tabla.grid(columnspan=4, column=0, row=0, pady=(50,5), padx=40)
    
    for col in ("ID","Nombre","Precio","Descripcion","Modelo","Anio","Marca","Existencias"):#encabezados de la tabla
        tabla.column(col,width=90, anchor=CENTER)#dimensiones de cada columna
        tabla.heading(col,text=col)#encabezado de columna
    datos_inventario(idar,nombre,precio,descripcion,modelo,anio,marca)#ahora que ya estan los encabezados siguen las filas
    
def consultar_refaccion():
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')
    con=conexion.cursor()
    con_select=tabla.selection()
    if con_select:
        primer_sel=con_select[0]
        datos_con=tabla.item(primer_sel,"values")[0]
        Obj_Consultado.main((datos_con,))
    else:
        messagebox.showerror("Atención", "No se selecciono nada")#si no se selecciono algo de la tabla 

def main(idar,nombre,precio,descripcion,modelo,anio,marca):
    global nome, pre, desc, model, yearentry, marcaentry, exis, veninv
    veninv=Tk()
    veninv.title("Consulta")
    veninv.geometry('800x500')
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
    menuinicio.add_command(label='Regresar a consultar', command=funcion_regresar2)
    menuinicio.add_command(label='Regresar a inventario', command=funcion_regresar)
    
    
    consulobj = Button(veninv, width=20, font=('Arial', 12, 'bold'), text='Consultar', bg='orange', bd=5, command=consultar_refaccion)
    consulobj.grid(column=1, row=1, padx=(130,0))
    
    show_tabla(idar,nombre,precio,descripcion,modelo,anio,marca)

    veninv.protocol("WM_DELETE_WINDOW", cerrarventana)#si se cierra la ventana
    
    veninv.mainloop()

    
 
    