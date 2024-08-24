from tkinter import *
from tkinter import ttk
from tkinter import messagebox #para las ventanas emergentes
import pandas as pd
import Inv_Consulta
import Inventario
import menuadmin

def cerrarventana():#si se cierra la ventana
    if messagebox.askokcancel("Atención", "¿Seguro que quieres regresar sin hacer una consulta?"):
        veninv.destroy()
        Inventario.main()

def funcion_regresar():#paar regresar a inventario
    veninv.destroy()
    Inventario.main()

def funcion_regresar2():#para regresar al menu
    veninv.destroy()
    menuadmin.main()

#Funcion para limpiar las entradas (textbox) 
def limpiar_entradas():
    nome.delete(0, 'end')  # Borra el texto desde el inicio hasta el final
    pre.delete(0, 'end')
    desc.delete(0, 'end')
    model.delete(0, 'end')
    yearentry.delete(0, 'end')
    marcaentry.delete(0, 'end')
    exis.delete(0, 'end')
    
#Funcion para consultar los datos
def consultar_datos():
    idar=idartE.get() #Se nombra la entrada y se obtiene el texto con la funcion .get()
    nombre=nome.get()
    precio=pre.get()
    descripcion=desc.get()
    modelo=model.get()
    anio=yearentry.get()
    marca=marcaentry.get()
    campos = [idar, nombre, precio, descripcion, modelo, anio, marca]#una lista con cada uno de los contenidos de los entrys
    if any(campos):#si almenos uno esta lleno puede ir a inv_consultaven
        veninv.destroy()
        Inv_Consulta.main(idar,nombre,precio,descripcion,modelo,anio,marca) #LLama la ventana de la consulta pasando parametros
    else:
        messagebox.showerror("Atencion", "Debes llenar al menos uno de los campos")

    

#VETANA PRINCIPAL
def main():
    global idartE, nome, pre, desc, model, yearentry, marcaentry, exis, veninv 
    veninv=Tk() #Crea la ventana
    veninv.title("Consultar articulo") #Titulo de la ventana
    veninv.geometry('700x300') #Tamaño de la ventana
    #centrar ventana
    veninv.update_idletasks()
    ancho_ventana = veninv.winfo_width()#para saber el ancho de la pantalla
    altura_ventana = veninv.winfo_height()#para saber el largo(altura) de la pantalla
    x = (veninv.winfo_screenwidth() // 2) - (ancho_ventana // 2)# // para hacer funcion piso bueno se redondea hacia abajo y queda como entero
    y = (veninv.winfo_screenheight() // 2) - (altura_ventana // 2)
    veninv.geometry('+{}+{}'.format(x, y - 30)) #sele resta 30 a y ya que es lo de la barra de tareas para que no afecte visualmente
    veninv.resizable(0,0) #No se puede modificar el tamaño
    #root.iconbitmap()
    
    #es para crear un menu
    bm=Menu()
    veninv.config(menu=bm, width=300, height=300)
    
    menuinicio=Menu(bm, tearoff=0)#tearoff en 0 para que el menu no se pueda desprender
    bm.add_cascade(label='Menu', menu=menuinicio)#se le pone Menu como texto
    
    #opciones del menu
    menuinicio.add_command(label='Regresar a inventario', command=funcion_regresar)
    menuinicio.add_command(label='Regresar a menu', command=funcion_regresar2)
    
    idart=Label(veninv,text='ID: ') #Declaracion de label
    idart.config(font=('Arial',12,'bold')) #Se configura con el tipo de letra, tamaño y estilo
    idart.grid(row=0,column=0, padx=(30,0)) #Ubicacion en la ventana, fila y columna
    
    idartE=Entry(veninv) #Declaracion de entrada (es un textbox)
    idartE.config(width=50, font=('Arial',12)) #Se configura tamño y fuente
    idartE.grid(row=0,column=1) #Ubicacion en la ventana
    
    nombre=Label(veninv,text='Nombre: ')
    nombre.config(font=('Arial',12,'bold'))
    nombre.grid(row=1,column=0, padx=(30,0))
    
    nome=Entry(veninv)
    nome.config(width=50, font=('Arial',12))
    nome.grid(row=1,column=1)
    
    precio=Label(veninv,text='Precio: ')
    precio.config(font=('Arial','12','bold'))
    precio.grid(row=2,column=0, padx=(30,0))
    
    pre=Entry(veninv)
    pre.config(width=50, font=('Arial',12))
    pre.grid(row=2,column=1)
    
    descripcion=Label(veninv,text='Descripcion: ')
    descripcion.config(font=('Arial','12','bold'))
    descripcion.grid(row=3,column=0, padx=(30,0))
    
    desc=Entry(veninv)
    desc.config(width=50, font=('Arial',12))
    desc.grid(row=3,column=1)
    
    modelo=Label(veninv,text='Modelo: ')
    modelo.config(font=('Arial','12','bold'))
    modelo.grid(row=4,column=0, padx=(30,0))
    
    model=Entry(veninv)
    model.config(width=50, font=('Arial',12))
    model.grid(row=4,column=1)
    
    year=Label(veninv,text='Año: ')
    year.config(font=('Arial','12','bold'))
    year.grid(row=5,column=0, padx=(30,0))
    
    yearentry=Entry(veninv)
    yearentry.config(width=50, font=('Arial',12))
    yearentry.grid(row=5,column=1)
    
    marca=Label(veninv,text='Marca: ')
    marca.config(font=('Arial','12','bold'))
    marca.grid(row=6,column=0, padx=(30,0))
    
    marcaentry=Entry(veninv)
    marcaentry.config(width=50, font=('Arial',12))
    marcaentry.grid(row=6,column=1)
    
    existencias=Label(veninv,text='Existencias: ')
    existencias.config(font=('Arial','12','bold'))
    existencias.grid(row=7,column=0, padx=(30,0))
    
    exis=Entry(veninv)
    exis.config(width=50, font=('Arial',12))
    exis.grid(row=7,column=1)

    consultar = Button(veninv, width=20, font=('Arial', 12, 'bold'), text='Consultar', bg='orange', bd=5, command=consultar_datos) #Se declara el boton, en que parte se pone (veninv), tamaño, fuente, texto, fondo y el comando es la funcion a la que llama, en este caso a consultar los datos
    consultar.grid(column=1, row=8) #Ubicacion del boton
    
    veninv.protocol("WM_DELETE_WINDOW", cerrarventana)#si se cierra la ventana
    
    veninv.mainloop()#para que no se cierre a ventana

    