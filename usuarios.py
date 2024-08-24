from tkinter import *
from tkinter import ttk
from tkinter import messagebox #para las ventanas emergentes
from numpy import pad
import pandas as pd
import mysql.connector
import Inicio_Sesion_Interfaz #para poder cerrar sesion
import Empleado_alta
import menuadmin
import Modificar_Interfaz_Usu

def cerrarventana():#si se cierra la ventana
    if messagebox.askokcancel("Atención", "¿Seguro que quieres salir de la aplicacion?"):
        veninv.destroy()

def agregar_empleado():#para ir a agregar empleados
    veninv.destroy()
    Empleado_alta.main()

def funcion_regresar():#para regresar al menu
    veninv.destroy()
    menuadmin.main()

def funcion_cerrar():#para que se cierre la ventana y se regrese a iniciar sesion, asi puede cambiar de cuenta
    veninv.destroy()
    Inicio_Sesion_Interfaz.MostrarVenIni()
    
def eliminar_inv():#para eliminar el usuario seleccionado
        conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')#conexion a la base de datos
        con=conexion.cursor()#cursor para hacer la consulta
        delete_select=tabla.selection()#se consigue lo que se selecciono en la tabla
        if delete_select:#si se selecciono algo
            if messagebox.askokcancel("Atención", "¿Seguro que quieres eliminar el seleccionado?"):#se pregunta si se quiere eliminar o no
                primer_sel=delete_select[0]#el primer renglon que se selecciono
                datos_del=tabla.item(primer_sel,"values")[0]#se condigue el primer indice de la tupla seleccionada el cual es el id
                sql="DELETE FROM usuarios WHERE IDUsu=%s"
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
    sql="SELECT * FROM usuarios"#consulta
    con.execute(sql)#se ejecuta la consulta
    usus=con.fetchall()#se consiguen todos los registros o filas que coinciden
    for x in usus:
        tabla.insert('','end',values=x)

def show_tabla():#para los encabezados
    global tabla
    style = ttk.Style()#crear un estilo
    style.configure("Treeview", background="#29AEAE", foreground="white")
    tabla=ttk.Treeview(veninv,columns=("ID","Nombre","Apellido","Usuario","Contraseña","Nivel"),show="headings")#paraponer los encabezados
    
    tabla.grid(columnspan=4, column=0, row=0, pady=(50,5), padx=100)
    
    for col in ("ID","Nombre","Apellido","Usuario","Contraseña","Nivel"):#encabezados de la tabla
        tabla.column(col,width=100, anchor=CENTER)#dimensiones de cada columna
        tabla.heading(col,text=col)#encabezado de columna
    datos_inventario()#ahora que ya estan los encabezados siguen las filas

def funcion_modificar():#para modificar el seleccionado
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')#conexion a la base de datos   
    con=conexion.cursor()#cursos para hacer la consulta
    mod_select=tabla.selection()#se consigue lo que se selecciono en la tabla
    if mod_select:#si se selecciono algo
        primer_sel=mod_select[0]#el primer renglon que se selecciono
        datos_modi=tabla.item(primer_sel,"values")[0]#se condigue el primer indice de la tupla seleccionada el cual es el id
        veninv.destroy()
        Modificar_Interfaz_Usu.main((datos_modi,))#se manda la id a la interfaz de modificar
    else:
        messagebox.showerror("Atención", "No se selecciono nada")#si no se selecciono algo de la tabla

def funcion_salir():
    veninv.destroy()

def main():
    global veninv#para que las demas funciones puedan usar la ventana
    veninv=Tk()
    veninv.title("Usuarios")
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
    menuinicio.add_command(label='Regresar a menu', command=funcion_regresar)
    menuinicio.add_command(label='Cerrar sesion', command=funcion_cerrar)
    menuinicio.add_command(label='Salir', command=funcion_salir)
    
    show_tabla()#para mostrar la tabla de usuarios
    #botones
    eliminar = Button(veninv, width=20, font=('Arial', 12, 'bold'), text='Eliminar seleccionado', bg='green', bd=5, command=eliminar_inv)#command llama el metodo eliminar_inv
    eliminar.grid(column=0, row=2, padx=(30,0))
    
    modificar = Button(veninv, width=20, font=('Arial', 12, 'bold'), text='Modificar seleccionado', bg='blue', bd=5, command=funcion_modificar)#command llama el metodo funcion_modificar
    modificar.grid(column=1, row=2)

    agregar = Button(veninv, width=20, font=('Arial', 12, 'bold'), text='Agregar nuevo', bg='orange', bd=5, command=agregar_empleado)#command llama el metodo agregar_empleado
    agregar.grid(column=2, row=2)
    
    veninv.protocol("WM_DELETE_WINDOW", cerrarventana)#si se cierra la ventana
    
    veninv.mainloop()#para que no se cierre la ventana

    
 