from tkinter import *
from tkinter import ttk
from tkinter import messagebox #para las ventanas emergentes
import pandas as pd
import mysql.connector
import usuarios
import menuadmin

def cerrarventana():#si se cierra la ventana
    if messagebox.askokcancel("Atención", "quieres salir de la aplicacion?"):
        veninv.destroy()

def funcion_regresar():#paar regresar a usuarios
    veninv.destroy()
    usuarios.main()

def funcion_regresar2():#para regresar al menu
    veninv.destroy()
    menuadmin.main()


def guardar_datos():
    global conexion, con, nome, ape, usue, contra, veninv#para que se puedan usar en otras partes
    sel=combobox.get()#se consigue lo que se puso en el combobox (la lista de opciones)
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')
    con=conexion.cursor()#creacion del cursor
    if nome.get().strip()=="" or ape.get().strip()=="" or usue.get().strip()=="" or contra.get().strip()=="":#los strip quitan espacios, y con los or se checa si alguno de los entrys estaba vacio
        messagebox.showerror("Atención", "Debes llenar todos los campos")#si algun campo esta vacio salta la advertencia
    else:#si esta todo lleno
        if nome.get().isalpha() and ape.get().isalpha():#si el nombre y apellido son puras letras
            #se checa si ya esta en la base de datos
            consulta = "SELECT * FROM usuarios WHERE Usuario = %s"#consulta, para ver si el usuario ya existe en la base de datos
            con.execute(consulta, (usue.get(),))#ejecucion de la consulta se pone una coma despues ya que es una tupla y si es una tupla de solo un elemento siempre debe agregarse la coma al final
            encontrado = con.fetchall()#para conseguir todas las filas de la tabla en caso de que el valor se repita
            if encontrado:#si el usuario ya existe
                messagebox.showerror("Atención", "Este empleado ya existe")#si ya existe se advierte
            else:#si no existe el usuario en la base de dato se puede insertar
                sql="INSERT INTO usuarios (IDUsu, NombreUsu, ApellidoUsu, Usuario, ContraUsu, NivelUsu) VALUES (%s, %s, %s, %s, %s, %s)"
                datos = ('', nome.get(), ape.get(), usue.get(), contra.get(), sel)#se llenan los %s que se pusieron en la consulta con los datos agarrados de los entrys
                messagebox.showinfo("Accion realizada", "empleado {}, agregado correctamente".format(usue.get()))#si algun campo esta vacio salta la advertencia
                con.execute(sql, datos)#se ejecuta la consulta
                conexion.commit()#commit actualiza la base de datos
                con.close()#se cieera el cursor
                conexion.close()#se cierra la conexion
                limpiar_entradas()#se limpian todos los entrys
        else:
            messagebox.showerror("Atención", "El nombre y apellido deben ser palabras sin numeros")#si ya existe se advierte
    show_tabla()

 
def limpiar_entradas():
    nome.delete(0, 'end')  # Borra el texto desde el inicio hasta el final
    ape.delete(0, 'end')
    usue.delete(0, 'end')
    contra.delete(0, 'end')
    combobox.set("")
    
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
    
    tabla.grid(columnspan=4, column=0, row=6, pady=5, padx=100)
    
    for col in ("ID","Nombre","Apellido","Usuario","Contraseña","Nivel"):#encabezados de la tabla
        tabla.column(col,width=100, anchor=CENTER)#dimensiones de cada columna
        tabla.heading(col,text=col)#encabezado de columna
    datos_inventario()#ahora que ya estan los encabezados siguen las filas

def combobox_show():
    global selected, combobox, sel, valuescombo
    selected = StringVar()
    valuescombo=['Administrador','Vendedor']
    combobox=ttk.Combobox(veninv, state="readonly", values=valuescombo, textvariable=selected)
    combobox.set(valuescombo[1])#para que aparesca ya con un valor (vendedor)
    combobox.grid(row=4,column=1)

def main():
    global nome, ape, usue, contra, veninv
    veninv=Tk()
    veninv.title("Registro de empleados")
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
    menuinicio.add_command(label='Regresar a usuarios', command=funcion_regresar)
    menuinicio.add_command(label='Regresar a menu', command=funcion_regresar2)
    
    nombre=Label(veninv,text='Nombre: ')
    nombre.config(font=('Arial',12,'bold'))
    nombre.grid(row=0,column=0, padx=(120,0), pady=(50,0))
    
    nome=Entry(veninv)
    nome.config(width=50, font=('Arial',12))
    nome.grid(row=0,column=1, pady=(50,0))
    
    apellido=Label(veninv,text='Apellido: ')
    apellido.config(font=('Arial','12','bold'))
    apellido.grid(row=1,column=0, padx=(120,0))
    
    ape=Entry(veninv)
    ape.config(width=50, font=('Arial',12))
    ape.grid(row=1,column=1)
    
    usuario=Label(veninv,text='Usuario: ')
    usuario.config(font=('Arial','12','bold'))
    usuario.grid(row=2,column=0, padx=(120,0))
    
    usue=Entry(veninv)
    usue.config(width=50, font=('Arial',12))
    usue.grid(row=2,column=1)
    
    contrasenia=Label(veninv,text='Contraseña: ')
    contrasenia.config(font=('Arial','12','bold'))
    contrasenia.grid(row=3,column=0, padx=(120,0))
    
    contra=Entry(veninv)
    contra.config(width=50, font=('Arial',12))
    contra.grid(row=3,column=1)
    
    nivel=Label(veninv,text='Nivel: ')
    nivel.config(font=('Arial','12','bold'))
    nivel.grid(row=4,column=0, padx=(120,0))
    
    #boton
    agregar = Button(veninv, width=20, font=('Arial', 12, 'bold'), text='Confirmar', bg='orange', bd=5, command=guardar_datos)#command llama el metodo guardar_datos
    agregar.grid(column=1, row=5, pady=50)
    
    combobox_show()#para hacer el combobox y llenarlo

    show_tabla()#mostrar tabla

    veninv.protocol("WM_DELETE_WINDOW", cerrarventana)#si se cierra la ventana
    veninv.mainloop()#para que no se cierre la ventana

    
 
    