# 
# Agenda en tkinter python3 y sqlite3
# Juan Manuel Fernandez
# https://github.com/juanmfer
#
#
import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3
from sqlite3 import Error
from tkinter import font
from tkcalendar import Calendar, DateEntry
from tkinter  import messagebox
from pathlib import Path
import os.path
#################### SQLITE3 base de datos - create db, table connection - creo db, tablas y conexion
def crear_conexion(basedatos):
    """ crear una conexión de base de datos a la base de datos SQLite
        especificada en basedatos
    :paramametro basedatos, archivo de base de datos
    :retorna conexion o no
    """
    conn = None
    try:
        conn = sqlite3.connect(basedatos)
        return conn
    except Error as e:
        print(e)
    return conn

def creo_tabla(conn, crear_tabla_sql):
    try:
        c = conn.cursor()
        c.execute(crear_tabla_sql)
    except Error as e:
        print(e)

def iniciodb(): ######  creo base de datos - create db
##### Selecciona tu ubicacion 
    database = r"agenda.db"
    #database = os.path.dirname(os.path.abspath(__file__)) + '/agenda.db'

    sql_crear_tabla_agenda = """ CREATE TABLE IF NOT EXISTS agenda(
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        fecha text NOT NULL,
                                        agendar text NOT NULL
                                    ); """
    # creo conexion a base de datos - create a database connection
    conn = crear_conexion(database)
    # creo las tablas - create tables
    if conn is not None:
        # creo la tabla agenda - create agenda table
        creo_tabla(conn, sql_crear_tabla_agenda)
    else:
        print("No se puede crear la base de datos - cannot create the database connection.")

###################################### SQLITE3 SELECT INSERT DELETE
###### insertar informacion
def agrego():
    conn = sqlite3.connect(r"agenda.db")
    #conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + '/agenda.db')
    c = conn.cursor()
    fecha = str(fechavar.get())
    agendar = str(agendarvar.get())
    c.execute("INSERT INTO agenda VALUES (NULL,?,?);",(fecha,agendar)) #laid
    conn.commit()
    muestro()
    conn.close()

###### Actualizo Tree
def actualizar():
    conn = sqlite3.connect(r"agenda.db")
    #conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + '/agenda.db')
    c = conn.cursor()
    c.execute("SELECT * FROM agenda ORDER BY id DESC")
    registros = c.fetchall()
    #registros = c.fetchone()
    for reg in tree.get_children():
        tree.delete(reg)
    for i in registros:
        tree.insert("", tk.END, values=i)
    conn.close()

###### Muestro datos en Tree
def muestro():
    conn = sqlite3.connect(r"agenda.db")
    #conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + '/agenda.db')
    c = conn.cursor()
    c.execute("SELECT * FROM agenda ORDER BY id DESC")
    registros = c.fetchall()
    for reg in tree.get_children():
        tree.delete(reg)
    for i in registros:
        tree.insert("", tk.END, values=i)
    conn.close() 

###### Elimino Registros seleccionados en Tree
def EliminarReg():
    conn = sqlite3.connect("agenda.db")
    #conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + '/agenda.db')
    cur = conn.cursor()
    try:
        messageDelete = messagebox.askyesno("Confirmar", "Deseas eliminar permanentemente el recordatorio?")
        if messageDelete > 0:
            for selected_item in tree.selection():
                cur.execute("DELETE FROM agenda WHERE id=?", (tree.set(selected_item, '#1'),))
                conn.commit()
                tree.delete(selected_item)
            conn.close()
    except Exception as e:
        print(e)

##### Muestro registros por dia
def muestrodia():
    conn = sqlite3.connect(r"agenda.db")
    fechavardiam = str(fechavardia.get())
    #conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + '/agenda.db')
    c = conn.cursor()
    c.execute("SELECT * FROM agenda WHERE fecha = ?", (fechavardiam, ))
    registros = c.fetchall()
    for reg in tree.get_children():
        tree.delete(reg)
    for i in registros:
        tree.insert("", tk.END, values=i)
    conn.close() 

if __name__ == '__main__':
###### ventana principal - root window
    root = tk.Tk()
    root.geometry('1000x900')
    root.title('Agenda Sqlite')
    root.resizable(False, False)
######  Estilos entry - style entry
    style = ttk.Style()
    style.configure(
    "MyEntry.TEntry",
    padding=5
    )

    micalendario = Calendar(root,selectmode = "day") ######  crear calendario - create calendar
    fechavar = StringVar() ###### variable fecha
    agendarvar = StringVar() ###### variable recordatorio
    fechavardia = StringVar() ###### variable fecha
    
###### textos - text
    seleccionar = ttk.Label(text='Seleccionar Fecha',font=font.Font(family="Verdana", size=11))
    seleccioning('Recordatorio', text=" Recordatorio", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=80)
    tree.column('#2', stretch=NO, minwidth=0, width=200)
    tree.column('#3', stretch=NO, minwidth=0, width=610)
    iniciodb() ######  creo db si es necesario
    root.mainloop()ar.place(x=50, y=40)
    agendartxt = ttk.Label(text='Recordatorio',font=font.Font(family="Verdana", size=11))
    agendartxt.place(x=50, y=90)

###### Calendarios - calendar
    micalendario = DateEntry(width=20, background='darkblue',foreground='white', borderwidth=20,font=font.Font(family="Verdana", size=11), textvariable=fechavar)
    micalendario.pack(padx=10, pady=10)
    micalendario.place(x=200, y=40)

######  Textbox recordatorio
    agendar = ttk.Entry( justify=tk.LEFT, show="", width=50, font=font.Font(family="Verdana", size=14),style="MyEntry.TEntry",  textvariable=agendarvar)
    agendar.place(x=200, y=85)

###### Botones
    guardodb = Button(text="Guardar", width=14, font=font.Font(family="Verdana", size=11), command=agrego)
    guardodb.place(x=816, y=86)

##### labelframe - Eliminar - delete selection
    delselectreg = ttk.LabelFrame(root, text='Eliminar Selección')
    delselectreg .place(x=740, y=780)
    borrodato = Button(delselectreg, text="Borrar Registro", width=14, font=font.Font(family="Verdana", size=11), command=EliminarReg)
    borrodato.pack(padx=15, pady=27)

##### labelFrame - Todos los recordatorios - all reg
    mostrartodosr = ttk.LabelFrame(root, text='Todos los Recordatorios')
    mostrartodosr .place(x=500, y=780)
    actualizo = Button(mostrartodosr, text="Actualizar", width=14, font=font.Font(family="Verdana", size=11), command=actualizar)
    actualizo.pack(padx=15, pady=27)

##### LabelFrame - Diario - day
    lfdiario = ttk.LabelFrame(root, text='Recordatorios Diarios')
    lfdiario.place(x=40, y=780)
    micalendario2 = DateEntry(lfdiario, width=20, background='darkblue',foreground='white', borderwidth=20,font=font.Font(family="Verdana", size=11), textvariable=fechavardia)
    micalendario2.pack(padx=15, pady=5)
    mostrardia = Button(lfdiario,text="Mostrar", width=14, font=font.Font(family="Verdana", size=11), command=muestrodia)
    mostrardia.pack(padx=15, pady=10)

######  Treeview Muestro registros - 
    tree = ttk.Treeview(root,columns=("Registro", "Fecha", "Recordatorio"),height=30, selectmode='browse', padding=10)
    tree.place(x=40, y=140)
    vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview) ###### Scrollbar treeview
    vsb.place(x=30+910+2, y=143, height=600+20)
    tree.configure(yscrollcommand=vsb.set, padding=4)
    tree.heading('Registro', text=" Registro", anchor=W)
    tree.heading('Fecha', text=" Fecha", anchor=W)
    tree.heading('Recordatorio', text=" Recordatorio", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=80)
    tree.column('#2', stretch=NO, minwidth=0, width=200)
    tree.column('#3', stretch=NO, minwidth=0, width=610)
    iniciodb() ######  creo db si es necesario
    root.mainloop()
