from tkinter import *
from tkinter import ttk
from tkinter import messagebox #para las ventanas emergentes
import pandas as pd
import mysql.connector
import Inicio_Sesion_Interfaz
import ConsultaInterfaceVendedor
import Interfaz_Venta
import vendidos
import Obj_Consultado

consultaabierta = FALSE

def cerrarventana():#si se cierra la ventana
    if messagebox.askokcancel("Atención", "¿Seguro que quieres salir de la aplicacion?"):
        veninv.destroy()

def funcion_cerrar():#para que se cierre la ventana y se regrese a iniciar sesion, asi puede cambiar de cuenta
    veninv.destroy()
    Inicio_Sesion_Interfaz.MostrarVenIni()

def funcion_salir():#para cerrar la ventana
    veninv.destroy()

def funcion_vendidos():
    veninv.destroy()
    vendidos.main()
    
def eliminar_inv():#para eliminar el articulo seleccionado
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')#conexion a la base de datos  
    con=conexion.cursor()#cursor para hacer la consulta
    delete_select=tabla.selection()#se consigue lo que se selecciono en la tabla
    if delete_select:#si se selecciono algo
        if messagebox.askokcancel("Atención", "¿Seguro que quieres eliminar el seleccionado?"):#se pregunta si se quiere eliminar o no
            primer_sel=delete_select[0]#el primer renglon que se selecciono
            datos_del=tabla.item(primer_sel,"values")[0]#se condigue el primer indice de la tupla seleccionada el cual es el id
            sql="DELETE FROM articulos WHERE IDArt=%s"
            con.execute(sql,(datos_del,))#se elimina el registro que tenia esa id
            conexion.commit()#se modifica la base de datos
        else:
            messagebox.showinfo("Atención", "0peración cancelada")#se le muestra al usuario que se cancelo
    else:
        messagebox.showerror("Atención", "No se selecciono nada")#si no se selecciono algo de la tabla
    con.close()
    conexion.close()
    messagebox.showinfo("Atención", "{} ha sido eliminado".format(datos_del))#si algun campo esta vacio salta la advertencia
    show_tabla()

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
    style.configure("Treeview", background="#AD16D2", foreground="white")
    tabla=ttk.Treeview(veninv,columns=("ID","Nombre","Precio","Descripcion","Modelo","Anio","Marca","Existencias"),show="headings")#paraponer los encabezados
    
    tabla.grid(columnspan=4, column=0, row=0, pady=(50,5), padx=40)
    
    for col in ("ID","Nombre","Precio","Descripcion","Modelo","Anio","Marca","Existencias"):#encabezados de la tabla
        tabla.column(col,width=90, anchor=CENTER)#dimensiones de cada columna
        tabla.heading(col,text=col)#encabezado de columna
    datos_inventario()#ahora que ya estan los encabezados siguen las filas
    
def funcion_consulta():#para realizar consultas
    veninv.destroy()
    ConsultaInterfaceVendedor.main()
    

def funcion_vender():#e va a venta
    vender=tabla.selection()#se consigue lo que se selecciono en la tabla
    if vender:#si se selecciono algo
        if messagebox.askokcancel("Atención", "¿Seguro que quieres vender el seleccionado?"):#se pregunta si se quiere eliminar o no
            primer_sel=vender[0]#el primer renglon que se selecciono
            id=tabla.item(primer_sel,"values")[0]#se condigue el primer indice de la tupla seleccionada el cual es la id
            nombre=tabla.item(primer_sel,"values")[1]#se condigue el segundo indice de la tupla seleccionada el cual es el nombre
            precio=tabla.item(primer_sel,"values")[2]#se condigue el tercer indice de la tupla seleccionada el cual es el precio
            desc=tabla.item(primer_sel,"values")[3]#se condigue el cuarto indice de la tupla seleccionada el cual es el precio
            modelo=tabla.item(primer_sel,"values")[4]#se condigue el quinto indice de la tupla seleccionada el cual es el modelo
            anio=tabla.item(primer_sel,"values")[5]#se condigue el sexto indice de la tupla seleccionada el cual es el año
            marca=tabla.item(primer_sel,"values")[6]#se condigue el septimo indice de la tupla seleccionada el cual es la marca
            exis=tabla.item(primer_sel,"values")[7]#se condigue el octavo indice de la tupla seleccionada el cual es la existencia
            veninv.destroy()
            Interfaz_Venta.main(id, nombre,precio,desc,modelo,anio,marca,exis)
        else:
            messagebox.showinfo("Atención", "0peración cancelada")#se le muestra al usuario que se cancelo
    else:
        messagebox.showerror("Atención", "No se selecciono nada")#si no se selecciono algo de la tabla

def consultar_refaccion():
    global consultaabierta
    if consultaabierta == False:
        consultaabierta = TRUE
        conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')
        con=conexion.cursor()
        con_select=tabla.selection()
        if con_select:
            primer_sel=con_select[0]
            datos_con=tabla.item(primer_sel,"values")[0]
            Obj_Consultado.main((datos_con,))
        else:
            messagebox.showerror("Atención", "No se selecciono nada")#si no se selecciono algo de la tabla
    else:
        messagebox.showerror("Atención", "Ya estas haciendo una consulta en este momento")#se advierte

        
def main():
    global nome, pre, desc, model, yearentry, marcaentry, exis, veninv
    veninv=Tk()
    veninv.title("Inventario Vendedor")
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
    
    menuinicio.add_command(label='Consulta', command=funcion_consulta)
    menuinicio.add_command(label='Cerrar sesión', command=funcion_cerrar)
    menuinicio.add_command(label='Salir', command=funcion_salir)
    
    vender= Button(veninv, width=20, font=('Arial', 12, 'bold'), text='Vender', bg='green', bd=5, command=funcion_vender)
    vender.grid( column=0, row=1, padx=(30,0))
    
    consulobj = Button(veninv, width=20, font=('Arial', 12, 'bold'), text='Consultar', bg='orange', bd=5, command=consultar_refaccion)
    consulobj.grid(column=1, row=1)

    consulobj = Button(veninv, width=20, font=('Arial', 12, 'bold'), text='Vendidos', bg='pink', bd=5, command=funcion_vendidos)
    consulobj.grid(column=2, row=1)
    
    show_tabla()

    veninv.protocol("WM_DELETE_WINDOW", cerrarventana)#si se cierra la ventana
    
    veninv.mainloop()

    
 
    