from tkinter import *
from tkinter import ttk #para el estilo y la tabla
from tkinter import messagebox #para las ventanas emergentes
import pandas as pd
import mysql.connector
import Inicio_Sesion_Interfaz #para poder cerrar sesion
import Interfaz_Venta
import Inventario_Vendedor

def cerrarventana():#si se cierra la ventana
    if messagebox.askokcancel("Atención", "¿Seguro que quieres salir de la aplicacion?"):
        veninv.destroy()

def funcion_regresar():#para regresar al menu
    veninv.destroy()
    Inventario_Vendedor.main()

    
def eliminar_inv():#para eliminar el articulo seleccionado
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')#conexion a la base de datos
    con=conexion.cursor()#cursor para hacer la consulta
    delete_select=tabla.selection()#se consigue lo que se selecciono en la tabla
    if delete_select:#si se selecciono algo
        if messagebox.askokcancel("Atención", "¿Seguro que quieres eliminar el seleccionado?"):#se pregunta si se quiere eliminar o no
            primer_sel=delete_select[0]#el primer renglon que se selecciono
            datos_del=tabla.item(primer_sel,"values")[0]#se condigue el primer indice de la tupla seleccionada el cual es el id
            sql="DELETE FROM vendidos WHERE IDArt=%s"
            con.execute(sql,(datos_del,))#se elimina el registro que tenia esa id
            conexion.commit()#se modifica la base de datos
        else:
            messagebox.showinfo("Atención", "0peración cancelada")#se le muestra al usuario que se cancelo
    else:
        messagebox.showerror("Atención", "No se selecciono nada")#si no se selecciono algo de la tabla
    con.close()
    conexion.close()
    messagebox.showinfo("Atención", "Ha sido eliminado")#se elimino
    show_tabla()
        

def datos_inventario():#para las filas de la tabla
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')#conexion a la base de datos
    con=conexion.cursor()#cursor para hacer la consulta
    sql="SELECT * FROM vendidos"#consulta
    con.execute(sql)#se ejecuta la consulta
    inv=con.fetchall()#se consiguen todos los registros o filas que coinciden
    for x in inv:
        tabla.insert('','end',values=x)

def show_tabla():#para los encabezados
    global tabla
    style = ttk.Style()#crear un estilo
    style.configure("Treeview", background="#5D0E9C", foreground="white")
    tabla=ttk.Treeview(veninv,columns=("ID","Nombre","Precio","Pagado","Descripcion","Modelo","Anio","Marca","Cantidad","Fecha"),show="headings")#paraponer los encabezados
    
    tabla.grid(columnspan=4, column=0, row=0, pady=(50,5), padx=20)
    
    for col in ("ID","Nombre","Precio","Pagado","Descripcion","Modelo","Anio","Marca","Cantidad","Fecha"):#encabezados de la tabla
        tabla.column(col,width=90, anchor=CENTER)#dimensiones de cada columna
        tabla.heading(col,text=col)#encabezado de columna
    datos_inventario()#ahora que ya estan los encabezados siguen las filas
    

def funcion_cerrar():#para que se cierre la ventana y se regrese a iniciar sesion, asi puede cambiar de cuenta
    veninv.destroy()
    Inicio_Sesion_Interfaz.MostrarVenIni()

def funcion_salir():
    veninv.destroy()


def main():
    global veninv#para que las demas funciones puedan usar la ventana
    veninv=Tk()
    veninv.title("Vendidos")
    veninv.geometry('950x500')
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

    menuinicio.add_command(label='Regresar', command=funcion_regresar)
    menuinicio.add_command(label='Cerrar sesion', command=funcion_cerrar)
    menuinicio.add_command(label='Salir', command=funcion_salir)
    
    
    show_tabla()#para mostrar la tabla de inventario
    
    #botones
    eliminar = Button(veninv, width=18, font=('Arial', 12, 'bold'), text='Eliminar seleccionado', bg='green', bd=5, command=eliminar_inv)#command llama el metodo eliminar_inv
    eliminar.grid(column=0, row=2, padx=(300,0))
    
    veninv.protocol("WM_DELETE_WINDOW", cerrarventana)#si se cierra la ventana

    veninv.mainloop()#para que no se cierre la ventana

    
 
    