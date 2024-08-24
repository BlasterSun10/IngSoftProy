from tkinter import *
from tkinter import ttk
from tkinter import messagebox #para las ventanas emergentes
import pandas as pd
import mysql.connector
import usuarios
import menuadmin

def cerrar():#si se cierra la ventana
    if messagebox.askokcancel("Atención", "¿Seguro que quieres regresar sin hacer una modificación?"):
        veninv.destroy()
        usuarios.main()

def funcion_regresar():#paar regresar a inventario
    veninv.destroy()
    usuarios.main()

def funcion_regresar2():#para regresar al menu
    veninv.destroy()
    menuadmin.main()

def limpiarlbl(): 
    global nome, ape, contra, usue, veninv, get_value
    nome.config(text="")
    ape.config(text="")
    usue.config(text="")
    contra.config(text="")

#Funcion para mostrar la inforamcion del empleado
def mostrar_info(datos_modi):
    global nome, ape, contra, usue, veninv, get_value
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')
    con=conexion.cursor()
    sql="SELECT * FROM usuarios WHERE IDUsu=%s"#Sentencia para consultar la informacion del usuario segun el ID seleccionado
    con.execute(sql,datos_modi)#Ejecucion de la sentencia con el ID del articulo
    usu=con.fetchone()#tupla con los datos del articulo con la id mandada
        
    nombre=Label(veninv,text='Nombre: ')
    nombre.config(font=('Arial',12,'bold'))
    nombre.grid(row=1,column=0, padx=(150,0), pady=(30,0))
    
    nome=Label(veninv,text=usu[1])
    nome.config(font=('Arial',12,'bold'))
    nome.grid(row=1,column=1, pady=(30,0))
    
    apellido=Label(veninv,text='Apellido: ')
    apellido.config(font=('Arial','12','bold'))
    apellido.grid(row=2,column=0, padx=(150,0))
    
    ape=Label(veninv,text=usu[2])
    ape.config(font=('Arial','12','bold'))
    ape.grid(row=2,column=1)
    
    usuari=Label(veninv,text='Usuario: ')
    usuari.config(font=('Arial','12','bold'))
    usuari.grid(row=3,column=0, padx=(150,0))
    
    usue=Label(veninv,text=usu[3])
    usue.config(font=('Arial','12','bold'))
    usue.grid(row=3,column=1)
    
    contrasenia=Label(veninv,text='Contraseña: ')
    contrasenia.config(font=('Arial','12','bold'))
    contrasenia.grid(row=4,column=0, padx=(150,0))
    
    contra=Label(veninv,text=usu[4])
    contra.config(font=('Arial','12','bold'))
    contra.grid(row=4,column=1)
    
    con.close()
    conexion.close()

#Combobox para seleccionar el valor a modificar del usuario
def combobox_show():
    global selected, combobox, sel, valuescombo
    selected = StringVar()
    valuescombo=['Nombre','Apellido','Usuario','Contraseña']

    combobox=ttk.Combobox(veninv, state="readonly", values=valuescombo, textvariable=selected)
    combobox.grid(column=1, row=8)
    

def modificar_usu(datos_modi):
    global nome, ape, contra, usue, veninv, get_value
    sel=combobox.get()
    valor=get_value.get()
    dat_con="Null"
    
    map_columns = {
        "Nombre": "NombreUsu",
        "Apellido": "ApellidoUsu",
        "Usuario": "Usuario",
        "Contraseña": "ContraUsu"
    }

    dat_con = map_columns.get(sel, "Null")  # Aseguramos que se selecciona una columna válida

    if dat_con == "Null":
        messagebox.showerror("Atención", "No se selecciono nada")#si no se selecciono algo del combobox
        return
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')
    print(conexion)    
    con=conexion.cursor()
    sql = "UPDATE usuarios SET {} = %s WHERE IDUsu = %s".format(dat_con)

    if dat_con == "NombreUsu" or dat_con == "ApellidoUsu":#si es el nombre o apellido no puede tener numeros
        if valor.isalpha():
            datos_consulta=(valor,datos_modi[0])
            con.execute(sql,datos_consulta)
            conexion.commit()
            messagebox.showinfo("Atención", "Se actualizo {} con el valor de: {}".format(dat_con,valor))#mustra que se hizo el cambio
        else:
            messagebox.showerror("Atención", "No debe contener numeros")#si no se selecciono algo del combobox
    else:#si es el usuario o contraseña si pueden tener numeros
        datos_consulta=(valor,datos_modi[0])
        con.execute(sql,datos_consulta)
        conexion.commit()
        messagebox.showinfo("Atención", "Se actualizo {} con el valor de: {}".format(dat_con,valor))#mustra que se hizo el cambio

    con.close()
    conexion.close()
    limpiarlbl()
    mostrar_info(datos_modi)
    get_value.delete(0, 'end')

def main(datos_modi):
    global nome, ape, contra, usue, veninv, get_value
    veninv=Tk()
    veninv.title("Modificar datos empleado")
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
    menuinicio.add_command(label='Regresar a usuarios', command=funcion_regresar)
    menuinicio.add_command(label='Regresar a menu', command=funcion_regresar2)
    camb=Label(veninv, text='Cambiar: ', width=10).grid(column=0, row=8, pady=20, padx=10)
    valor=Label(veninv, text='Nuevo valor: ', width=10).grid(column=0, row=9, pady=20, padx=10)
    get_value=Entry(veninv, width=20, font=('Arial',12))
    get_value.grid(column=1, row=9)
    
    combobox_show()#Llama a la funcion para mostrar el combobox
    mostrar_info(datos_modi)#Muestra la tabla pasando los datos por parametro del objeto a modificar
        
    modificarobj = Button(veninv, width=20, font=('Arial', 12, 'bold'), text='Modificar', bg='blue', bd=5, command=lambda: modificar_usu(datos_modi)) #Boton para modificar los datos de usuario
    modificarobj.grid(column=1, row=10)
        
    veninv.protocol("WM_DELETE_WINDOW", cerrar)#si se cierra la ventana
        
    veninv.mainloop()#para que no se cierre la ventana