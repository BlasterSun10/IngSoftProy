from tkinter import * #para las interfaces, para lo visual
from tkinter import messagebox #para las ventanas emergentes
import pandas as pd 
import mysql.connector #para poder hacer consultas y modificaciones en la base de datos con sql
import menuadmin #para poder usar el main de menuadmin
import Inventario #para poder usar el main de menuadmin
import Inventario_Vendedor #para poder usar el main de Inventario_vendedor.py
#Se importaron las ventanas que se pueden llamar con los botones

def cerrarventana():#si se cierra la ventana
    if messagebox.askokcancel("Atención", "quieres salir de la aplicacion?"):
        ventana.destroy()

#funciones para cambiar de interfaz, se abre una dependiendo del nivel del usuario (admin o vendedor)
def Menu_Admin():
    ventana.destroy() #Destruye la ventana
    #Inventario.main() #Manda a llamar al inventario administrador
    menuadmin.main() #Manda a llamar al inventario administrador

def Mostrar_Inventario_Vendedor():
    ventana.destroy() #Destruye la ventana
    Inventario_Vendedor.main() #Manda a llamar al inventario vendedor


#Funcion para iniciar sesion    
def IniSes():
    #Se establece la conexion con mysql.connector.connect, con los parametros
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')
    
    #Se necesita este cursor para poder realizar las consultas a la BD
    con=conexion.cursor()
    #SELECT * FROM usuarios WHERE Usuario="Blaster" AND ContraUsu="BlasterPass"

    #Aqui se obtiene el nivel de usuario que ingresa y lo guarda en la variable nivel
    sql="SELECT NivelUsu FROM usuarios WHERE Usuario=%s AND ContraUsu=%s" #Consulta principal, en %s van los valores
    datos=( get_correo.get(), get_contra.get()) #Son los valores de los datos que iran en la consulta donde se insertaron los %s
    con.execute(sql,datos) #Ejecucion de la consulta, ya "concatena" o reemplaza los valores de datos en sql
    nivel=con.fetchone() #Fectchone es seleccionar un registro
       
    con=conexion.cursor()
    #SELECT * FROM usuarios WHERE Usuario="Blaster" AND ContraUsu="BlasterPass"

    #Esta consulta dice que, si existe un registro donde el usuario Y contraseña son iguales en el mismo registro, dara de salida "1", de lo contrario, "0"
    sql="SELECT EXISTS(SELECT * FROM usuarios WHERE Usuario=%s AND ContraUsu=%s)"
    datos=( get_correo.get(), get_contra.get())
    con.execute(sql,datos) 
    usu=con.fetchone()
    if usu[0]==1 and nivel[0]=='Administrador': #Si el resultado de la segunda consulta es 1 (si concordaron el usuario y contraseña en el mismo registro) y su nivel es adminsitrador
        messagebox.showinfo("Inicio de sesión exitoso", "Bienvenido, {}".format(datos[0]))
        Menu_Admin() #Llama al menu del administrador (es el mas completo)
    elif usu[0]==1 and nivel[0]=='Vendedor':  #Si el resultado de la segunda consulta es 1 (si concordaron el usuario y contraseña en el mismo registro) y su nivel es vendedor
        messagebox.showinfo("Inicio de sesión exitoso", "Bienvenido, {}".format(datos[0]))
        Mostrar_Inventario_Vendedor() #Muestra el inventario del vendedor
    else:
        messagebox.showerror("No se pudo iniciar sesión", "Una o mas credenciales incorrectas")
        
    con.close() #Termina el cursor
    conexion.close() #Termina la conexion



def MostrarVenIni():
    global ventana, get_contra, get_correo #Variables globales para usarlas en todo el archivo
    ventana=Tk() #Crea ventana
    ventana.geometry('500x500') #Tamaño de la ventana
    #centrar ventana
    ventana.update_idletasks()
    ancho_ventana = ventana.winfo_width()#para saber el ancho de la pantalla
    altura_ventana = ventana.winfo_height()#para saber el largo(altura) de la pantalla
    x = (ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)# // para hacer funcion piso bueno se redondea hacia abajo y queda como entero
    y = (ventana.winfo_screenheight() // 2) - (altura_ventana // 2)
    ventana.geometry('+{}+{}'.format(x, y - 30)) #sele resta 30 a y ya que es lo de la barra de tareas para que no afecte visualmente
    ventana.resizable(0,0) #No se puede modificar el tamaño
    ventana.title('Refaccionaria') #Titulo de la ventana    
        
    frame1=Frame(ventana) #Se utiliza un frame para insertar en el los labels y textbox (no es realmente necesario, pero es para darle orden y formato)
    frame1.grid(column=1, row=0, sticky='nsew') #bicacion del frame, no recuerdo para que era sticky, pero no se necesita modificarlo

    try:
        logo=PhotoImage(file="Toyota86.png") #Foto del logo, la puse provicional, puede cambiarse
        logo=logo.subsample(2) #Tamaño de la imagen
        label_imagen = logo #para evitar que el recolector de basura deseche la imagen 
        lb_logo=Label(frame1, image=logo)
        lb_logo.grid(column=1,row=6,pady=30,padx=20) #Label para insertar la imgane del logo
    except TclError as e:
         # Imprimir un mensaje de error si la imagen no se puede cargar
        print(f"Error al cargar la imagen: {e}")
        # Crear un Label alternativo con un mensaje de error
        lb_logo = Label(frame1, text="Login.")
        lb_logo.grid(column=1,row=6,pady=30,padx=20) #Label para insertar la imgane del logo
    lblRefTit=Label(frame1, text='Refaccionaria automotriz').grid(column=0,row=0,pady=20, padx=10) #Label del titulo

    correo=Label(frame1, text='Usuario', width=10).grid(column=0, row=1, pady=20, padx=10) #Label usuario, con su ubicacion
    get_correo=Entry(frame1, width=20, font=('Arial',12)) #Entrada del correo
    get_correo.grid(column=1, row=1) #Ubicaion de la entrada

    contra=Label(frame1, text='Contraseña', width=10).grid(column=0, row=2, pady=20, padx=10)
    get_contra=Entry(frame1, width=20, font=('Arial',12), show = "*")
    get_contra.grid(column=1, row=2)

    inises = Button(frame1, width=20, font=('Arial', 12, 'bold'), text='Iniciar sesión', bg='orange', bd=5, command=IniSes) #Declaracion del boton, ubicacion, fuente, texto, fondo y comando
    inises.grid(column=1,row=5, pady=20, padx=10) #Ubicacion del boton
    
    ventana.protocol("WM_DELETE_WINDOW", cerrarventana)#si se cierra la ventana
    
    ventana.mainloop()