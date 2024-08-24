from tkinter import *
from tkinter import ttk
import pandas as pd
import mysql.connector
import ConsultaInterface
import Inventario_Vendedor
import Inicio_Sesion_Interfaz
from generapdf import *
import datetime#para la fecha

def cerrarventana():#si se cierra la ventana
    if messagebox.askokcancel("Atención", "¿Seguro que quieres regresar sin hacer una venta?"):
        veninv.destroy()
        Inventario_Vendedor.main()

def funcion_cerrar():#para que se cierre la ventana y se regrese a iniciar sesion, asi puede cambiar de cuenta
    veninv.destroy()
    Inicio_Sesion_Interfaz.MostrarVenIni()

def funcion_salir():#para cerrar la ventana
    veninv.destroy()

def funcion_regresar():#paar regresar a inventario
    veninv.destroy()
    Inventario_Vendedor.main()

def agregar_datos(nome,pre,pago2,desc,modelo,anio,marca,cant2):
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')
    con=conexion.cursor()
    sql="INSERT INTO vendidos (IDArt, NomArt, PrecioArt, Pagado, DescArti, ModeloArt, AnioArt, MarcaArt, Cantidad, fecha, ImagenArt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    datos = ('', nome, pre, pago2, desc, modelo, anio, marca, cant2, datetime.datetime.now(),'')
    con.execute(sql, datos)
    conexion.commit()
    con.close()
    conexion.close()
    limpiar_entradas()

def limpiar_entradas():
    cantidad.delete(0, 'end')  # Borra el texto desde el inicio hasta el final
    pago.delete(0, 'end')


def datos_inventario(id):#para las filas de la tabla
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')#conexion a la base de datos
    con=conexion.cursor()#cursor para hacer la consulta
    consulta = "SELECT * FROM articulos WHERE IDArt = %s"#busca la fila con esa id
    con.execute(consulta, (id,))#se checa si todos estos datos coinciden, y si lo hacen ese articulo ya existe
    encontrado = con.fetchall()#para conseguir lo que se regresa

    for x in encontrado:#se muestra la coincidencia
        tabla.insert('','end',values=x)

def show_tabla(id):
    global tabla
    style = ttk.Style()#crear un estilo
    style.configure("Treeview", background="#C64815", foreground="white")
    tabla=ttk.Treeview(veninv,columns=("ID","Nombre","Precio","Descripcion","Modelo","Anio","Marca","Existencias"),show="headings", height=1)#paraponer los encabezados, height cambia la altura de la tabla (numero de renglones)
    
    tabla.grid(columnspan=4, column=0, row=0, pady=(80,5), padx=(10,0))
    
    for col in ("ID","Nombre","Precio","Descripcion","Modelo","Anio","Marca","Existencias"):
        tabla.column(col,width=80, anchor=CENTER)#dimensiones de cada columna
        tabla.heading(col,text=col)#encabezado de columna
    datos_inventario(id)#ahora que ya estan los encabezados siguen las filas
    

def venderyrecibo(id, nome,pre,desc,modelo,anio,marca,exis):
    conexion=mysql.connector.connect(user='root', host='localhost', database='refaccionaria', port='3306')
    con=conexion.cursor()#creacion del cursor
    sql = "UPDATE articulos SET ExistArt = %s WHERE IDArt = %s" #Consulta, SET {} es la parte obtenida del combobox, pero al obtener el valor del combobox, se tiene que usar la funcion format
    if pago.get().isdigit() and cantidad.get().isdigit():#si son numeros
        #se hace entero el valor puesto en el entry
        pago2 = int(pago.get())
        cant2 = int(cantidad.get())
        if cant2 > 0 and pago2 >0:#si ambos son mayores a 0
            if cant2 <= int(exis):
                if pago2 >= float(pre) * cant2:
                    #se hce la modificacion
                    agregar_datos(nome,pre,pago2,desc,modelo,anio,marca,cant2)
                    #swe hace la modificacion en articulos
                    con.execute(sql, ((int(exis)-cant2),id))
                    conexion.commit()
                    con.close()
                    conexion.close()
                    messagebox.showinfo("Atención", "Se vendieron {} piezas de: {}".format(cant2,nome))#se bende
                    funcion_recibo(id, pago2, cant2)#se manda la id y lo que se pago
                    funcion_regresar()
                else:
                    messagebox.showinfo("Atención", "La cantidad a pagar debe ser igual o mayor a el precio")#sla cantidad no es posible
            else:
                messagebox.showinfo("Atención", "La cantidad no puede ser mayor a las existencias")#sla cantidad no es posible
        else:
            messagebox.showinfo("Atención", "Debe ser mayor a 0")#se muestra que la cantidad wue metio es 0 o menor
    else:
        messagebox.showerror("Atención", "Debe ser una cantidad numerica")#si puso letras
            
    
    


def main(id, nome,pre,desc,modelo,anio,marca,exis):
    global veninv, cantidad, pago
    veninv=Tk()
    veninv.title("Venta de articulos")
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

    menuinicio.add_command(label='Regresar a inventario', command=funcion_regresar)
    menuinicio.add_command(label='Cerrar sesion', command=funcion_cerrar)
    menuinicio.add_command(label='Salir', command=funcion_salir)

    show_tabla(id)#se muestra la tabla

    can=Label(veninv, text='Cantidad a vender: ', width=20).grid(column=0, row=1, pady=20, padx=(50,0))
    cantidad=Entry(veninv, width=10, font=('Arial',12))
    cantidad.grid(column=1, row=1, padx=(0, 200))

    valor=Label(veninv, text='Cantidad que se esta pagando: ', width=40).grid(column=0, row=2, pady=20, padx=(50,0))
    pago=Entry(veninv, width=10, font=('Arial',12))
    pago.grid(column=1, row=2, padx=(0, 200))

    venta = Button(veninv, width=20, font=('Arial', 12, 'bold'), text='Vender', bg='blue', bd=5, command=lambda:venderyrecibo(id, nome,pre,desc,modelo,anio,marca,exis))#la lambda es para que me acepte poner parametros, de otro modo la funcion corre sin necesidad de presionar el boton
    venta.grid( column=0, row=3, padx=(250,0), pady=30)
    
    
    veninv.protocol("WM_DELETE_WINDOW", cerrarventana)#si se cierra la ventana
    veninv.mainloop()#pata que no se cierre la ventana

    
 
    