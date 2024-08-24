from tkinter import *
from tkinter import ttk
from tkinter import messagebox #para las ventanas emergentes
import pandas as pd
import mysql.connector
import Inventario
import Inv_Consulta
import menuadmin
from datetime import datetime#para el año actual

def cerrar():#si se cierra la ventana
    if venia == 0:#si venia de inventario.py
        if messagebox.askokcancel("Atención", "¿Seguro que quieres regresar sin hacer una modificación?"):
            veninv.destroy()
            Inventario.main()
    else:
        if messagebox.askokcancel("Atención", "¿Seguro que quieres regresar sin hacer una modificación?"):
            veninv.destroy()
            Inv_Consulta.main(usu[0], usu[1], usu[2], usu[3], usu[4], usu[5], usu[6])

def funcion_regresar():#paar regresar a inventario
    if venia == 0:
        veninv.destroy()
        Inventario.main()
    else:
        veninv.destroy()
        Inv_Consulta.main(usu[0], usu[1], usu[2], usu[3], usu[4], usu[5], usu[6])
    

def funcion_regresar2():#para regresar al menu
    veninv.destroy()
    menuadmin.main()

#Funcion que limpia los labels
def limpairlbl(): 
    
    nombrep.config(text="")
    preciop.config(text="")
    descripcionp.config(text="")
    modelop.config(text="")
    yearp.config(text="")
    marcap.config(text="") 
    existenciasp.config(text="")

#Funcion para mostrar la inforamcion del articulo
def mostrar_info(datos_modi):
    global nombrep,preciop, descripcionp, modelop, yearp, marcap, existenciasp, usu
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')  
    con=conexion.cursor()
    sql="SELECT * FROM articulos WHERE IDArt=%s"#Sentencia para consultar la informacion del articulo segun el ID seleccionado
    con.execute(sql,datos_modi)#Ejecucion de la sentencia con el ID del articulo
    usu=con.fetchone()#tupla con los datos del articulo con la id mandada
        
    nombre=Label(veninv,text='Nombre: ')
    nombre.config(font=('Arial',12,'bold'))
    nombre.grid(row=1,column=0, padx=(150,0), pady=(30,0))
    
    nombrep=Label(veninv,text=usu[1])#se pone en el label el segundo elemto de la tupla
    nombrep.config(font=('Arial',12,'bold'))
    nombrep.grid(row=1,column=1, pady=(30,0))
    
    precio=Label(veninv,text='Precio: ')
    precio.config(font=('Arial','12','bold'))
    precio.grid(row=2,column=0, padx=(150,0))
    
    preciop=Label(veninv,text=usu[2])#se pone en el label el tercero elemto de la tupla
    preciop.config(font=('Arial','12','bold'))
    preciop.grid(row=2,column=1)
    
    descripcion=Label(veninv,text='Descripcion: ')
    descripcion.config(font=('Arial','12','bold'))
    descripcion.grid(row=3,column=0, padx=(150,0))
    
    descripcionp=Label(veninv,text=usu[3])#se pone en el label el cuerto elemto de la tupla
    descripcionp.config(font=('Arial','12','bold'))
    descripcionp.grid(row=3,column=1)
    
    modelo=Label(veninv,text='Modelo: ')
    modelo.config(font=('Arial','12','bold'))
    modelo.grid(row=4,column=0, padx=(150,0))
    
    modelop=Label(veninv,text=usu[4])#se pone en el label el quinto elemto de la tupla
    modelop.config(font=('Arial','12','bold'))
    modelop.grid(row=4,column=1)
    
    year=Label(veninv,text='Año: ')
    year.config(font=('Arial','12','bold'))
    year.grid(row=5,column=0, padx=(150,0))
    
    yearp=Label(veninv,text=usu[5])#se pone en el label el sexto elemto de la tupla
    yearp.config(font=('Arial','12','bold'))
    yearp.grid(row=5,column=1)

    marca=Label(veninv,text='Marca: ')
    marca.config(font=('Arial','12','bold'))
    marca.grid(row=6,column=0, padx=(150,0))
    
    marcap=Label(veninv,text=usu[6])#se pone en el label el septimo elemto de la tupla
    marcap.config(font=('Arial','12','bold'))
    marcap.grid(row=6,column=1)
    
    existencias=Label(veninv,text='Existencias: ')
    existencias.config(font=('Arial','12','bold'))
    existencias.grid(row=7,column=0, padx=(150,0))
    
    existenciasp=Label(veninv,text=usu[7])#se pone en el label el octavo elemto de la tupla
    existenciasp.config(font=('Arial','12','bold'))
    existenciasp.grid(row=7,column=1)
    
    con.close()
    conexion.close()

#Funcion para mostrar el combobox
def combobox_show():
    global selected, combobox, sel, valuescombo
    selected = StringVar() #Esta funcion se necesita para saber el tipo de valor obtenido en el combobox
    valuescombo=['Nombre','Precio','Descripcion','Modelo','Año','Marca','Existencias'] #Valores del combobox (los parametros que se van a poder modificar)

    combobox=ttk.Combobox(veninv, state="readonly", values=valuescombo, textvariable=selected) #Creacion del combobox, el estado es solo para obtener datos, no escribir algo, en values, se inserta la lista anterior y en el text variable, el tipo de dato
    combobox.grid(column=1, row=8) #Ubicacion del combobox
    
#Funcion que permite modifcar un parametro del objeto
def modificar_objeto(datos_modi):
    sel=combobox.get() #Se obtiene el dato seleccionado en el combobox
    valor=get_value.get() #Se obtiene el valor obtenido en el textbox (valor con el que se modificara)
    dat_con="Null" #Aqui se tomara el valor que se insertara en la consulta 
    
    #Este mapa traduce el combobox al nombre del campo de la BD
    map_columns = {
        "Nombre": "NomArt",
        "Precio": "PrecioArt",
        "Descripcion": "DescArti",
        "Modelo": "ModeloArt",
        "Año": "AnioArt",
        "Marca": "MarcaArt",
        "Existencias": "ExistArt"
    }

    dat_con = map_columns.get(sel, "Null")  # Aseguramos que se selecciona una columna válida

    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')
    con=conexion.cursor()#creacion del cursor
    sql = "UPDATE articulos SET {} = %s WHERE IDArt = %s".format(dat_con) #Consulta, SET {} es la parte obtenida del combobox, pero al obtener el valor del combobox, se tiene que usar la funcion format
    
    if dat_con == "Null":#Se asegura de obtener un valor del combobox
        messagebox.showerror("Atención", "No se selecciono nada")#si no se selecciono algo del combobox
        return
    else:#se comprueba si el dato en verdad puede ser colocado
        if dat_con == "PrecioArt" or dat_con == "ExistArt" :#deben ser cantidades mayores a 0
            if valor.isdigit():#si son numeros
                cant = int(valor)#se hace entero el valor puesto en el entry
                if cant >= 0:
                    datos_consulta=(valor,datos_modi[0])#se completa la consulta con los datos de el valor a poner y la id del registro que sera modificado
                    con.execute(sql,datos_consulta)#se ejecuta la consulta
                    conexion.commit()#se actualiza la base de datos
                    messagebox.showinfo("Atención", "Se actualizo {} con el valor de: {}".format(dat_con,valor))#mustra que se hizo el cambio
                else:
                    messagebox.showinfo("Atención", "La cantidad debe ser mayo a 0")#mustra que se hizo el cambio
            else:
                messagebox.showerror("Atención", "Debe ser una cantidad numerica")#si no se selecciono algo del combobox
            
        elif dat_con == "AnioArt":#se checara que no sea mayor al año actual
            if valor.isdigit():#si son numeros
                cant = int(valor)#se hace entero el valor puesto en el entry
                if cant >= 1886 and cant <= datetime.now().year:#se checa que la fecha sea entre 1886 ya que es la fecha del primer coche y la año actual
                    datos_consulta=(valor,datos_modi[0])#se completa la consulta con los datos de el valor a poner y la id del registro que sera modificado
                    con.execute(sql,datos_consulta)#se ejecuta la consulta
                    conexion.commit()#se actualiza la base de datos
                    messagebox.showinfo("Atención", "Se actualizo {} con el valor de: {}".format(dat_con,valor))#mustra que se hizo el cambio
                else:
                    messagebox.showinfo("Atención", "el año debe ser veridico")#mustra que se hizo el cambio
            else:
                messagebox.showerror("Atención", "Debe ser una cantidad numerica")#si no se selecciono algo del combobox
        else:
            #si no debe ser numerico afuerzas, entinces simplemente se actualiza
            datos_consulta=(valor,datos_modi[0])#se completa la consulta con los datos de el valor a poner y la id del registro que sera modificado
            con.execute(sql,datos_consulta)#se ejecuta la consulta
            conexion.commit()#se actualiza la base de datos
            messagebox.showinfo("Atención", "Se actualizo {} con el valor de: {}".format(dat_con,valor))#mustra que se hizo el cambio

    con.close()#se cierra el cursor
    conexion.close()#se cierra la conexion con la base de datos
    limpairlbl() #Llama a la funcion para limpiar los labels y no se sobrepongan la informacion al actualziar
    mostrar_info(datos_modi) #Actualiza la informacioon
    get_value.delete(0, 'end') #Limpia la entrada


def main(datos_modi, viene):#recibe el dato a modificar y la ventana de la que proviene
    global veninv, get_value, venia
    venia = viene#se guarda el valor de la ventana desde la que viene
    veninv=Tk()
    veninv.title("Modificar articulo")
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
    
    #es para crear un menu
    bm=Menu()
    veninv.config(menu=bm, width=300, height=300)
    
    menuinicio=Menu(bm, tearoff=0)#tearoff en 0 para que el menu no se pueda desprender
    bm.add_cascade(label='Menu', menu=menuinicio)#se le pone Menu como texto
    
    #opciones del menu
    menuinicio.add_command(label='Regresar', command=funcion_regresar)
    menuinicio.add_command(label='Regresar a menu', command=funcion_regresar2)


    camb=Label(veninv, text='Cambiar: ', width=10).grid(column=0, row=8, pady=20, padx=10)
    valor=Label(veninv, text='Nuevo valor: ', width=10).grid(column=0, row=9, pady=20, padx=10)
    get_value=Entry(veninv, width=20, font=('Arial',12))
    get_value.grid(column=1, row=9)
    
    combobox_show() #Llama a la funcion para mostrar el combobox
    mostrar_info(datos_modi)  #Muestra la tabla pasando los datos por parametro del objeto a modificar
        
    modificarobj = Button(veninv, width=20, font=('Arial', 12, 'bold'), text='Modificar', bg='blue', bd=5, command=lambda: modificar_objeto(datos_modi)) #Boton para modificar el objeto, el lambda es para pasar el parametro que es una tupla (solo para tuplas, de otro modo no es necesario)
    modificarobj.grid(column=1, row=10)

    veninv.protocol("WM_DELETE_WINDOW", cerrar)#si se cierra la ventana
        
    veninv.mainloop()#para que no se cierre la ventana