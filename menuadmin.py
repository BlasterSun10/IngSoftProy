from tkinter import *
from tkinter import messagebox #para las ventanas emergentes
import pandas as pd
import Inicio_Sesion_Interfaz #para poder cerrar sesion
import usuarios
import Inventario

def cerrarventana():#si se cierra la ventana
    if messagebox.askokcancel("Atención", "¿Seguro que quieres salir de la aplicacion?"):
        venmenu.destroy()

def funcion_usuarios():#se abre la interfaz de usuarios
    venmenu.destroy()
    usuarios.main()
    
def ver_inventario():#para ir a la interfaz de ver inventario
    venmenu.destroy()
    Inventario.main()

def funcion_cerrar():#para que se cierre la ventana y se regrese a iniciar sesion, asi puede cambiar de cuenta
    venmenu.destroy()
    Inicio_Sesion_Interfaz.MostrarVenIni()

def funcion_salir():#para cerrar la ventana
    venmenu.destroy()



def main():
    global venmenu#para que se pueda destruir la ventana en las funciones de arriba
    venmenu=Tk()
    venmenu.title("Menu Administrador")
    venmenu.geometry('500x500')
    #centrar ventana
    venmenu.update_idletasks()
    ancho_ventana = venmenu.winfo_width()#para saber el ancho de la pantalla
    altura_ventana = venmenu.winfo_height()#para saber el largo(altura) de la pantalla
    x = (venmenu.winfo_screenwidth() // 2) - (ancho_ventana // 2)# // para hacer funcion piso bueno se redondea hacia abajo y queda como entero
    y = (venmenu.winfo_screenheight() // 2) - (altura_ventana // 2)
    venmenu.geometry('+{}+{}'.format(x, y - 30)) #sele resta 30 a y ya que es lo de la barra de tareas para que no afecte visualmente
    venmenu.resizable(0,0)
    #root.iconbitmap()

    #es para crear un menu
    bm=Menu()
    venmenu.config(menu=bm, width=300, height=300)
    #el menu 
    menuinicio=Menu(bm, tearoff=0)#tearoff en 0 para que el menu no se pueda desprender
    bm.add_cascade(label='Menu', menu=menuinicio)#se le pone Menu como texto
    
    #pequeño menu que esta aen la parte de arriba de la ventana donde dice Menu
    menuinicio.add_command(label='Cerrar sesión', command=funcion_cerrar)
    menuinicio.add_command(label='Salir', command=funcion_salir)
    
    #botones
    agregar_emp = Button(venmenu, width=20, font=('Arial', 12, 'bold'), text='Empleados', bg='yellow', bd=5, command=funcion_usuarios)#command llama el metodo funcion_usuarios
    agregar_emp.pack(pady=(70, 20))#acomar boton en ventana
    
    consulobj = Button(venmenu, width=20, font=('Arial', 12, 'bold'), text='Inventario', bg='orange', bd=5, command=ver_inventario)#command llama el metodo ver_inventario
    consulobj.pack(pady=5)#acomar boton en ventana

    venmenu.protocol("WM_DELETE_WINDOW", cerrarventana)#si se cierra la ventana

    venmenu.mainloop()#para que no se cierre la ventana

    
 
    