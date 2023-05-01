import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import subprocess
from Analizador import Analizador

glbArchivo = ""
errores = []


def newDoc():
    menu_archivo.entryconfig("Guardar", state="disabled")
    global glbArchivo
    glbArchivo = ""
    editor.delete(1.0, tk.END)


def openDoc():
    archivo = filedialog.askopenfilename(title="Abrir archivo")
    global glbArchivo
    glbArchivo = archivo
    if archivo:
        with open(archivo, "r", encoding="utf-8") as f:
            menu_archivo.entryconfig("Guardar", state="normal")
            informacion = f.read()
        editor.delete(1.0, tk.END)
        editor.insert(tk.END, informacion)
        informacion = informacion.split("{")
        print(informacion)


def saveDoc():
    if glbArchivo:
        informacion = editor.get(1.0, tk.END)
        with open(glbArchivo, "w", encoding="utf-8") as f:
            f.write(informacion)
        messagebox.showinfo("Guardar", "Archivo guardado exitosamente")
    else:
        messagebox.showinfo("Guardar", "No se ha abierto ningun archivo aún")


def saveAsDoc():
    archivo = filedialog.asksaveasfilename(title="Guardar como")
    glbArchivo = archivo
    if archivo:
        informacion = editor.get(1.0, tk.END)
        menu_archivo.entryconfig("Guardar", state="normal")
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(informacion)


def analizar():
    global glbArchivo
    global a
    if glbArchivo == "":
        messagebox.showerror(
            "Error", "No se ha abierto un archivo o no se ha guardado")
        return
    print(glbArchivo)

    archivo = open(glbArchivo, 'r', encoding="utf-8")
    lineas = ''
    for i in archivo.readlines():
        lineas += i
    global errores
    a = Analizador(lineas)
    a._compile()
    print(a.MaestroFormulas)
    print(a.ListaErrores)
    print(a.TokenList)
    if a.ListaErrores != []:
        messagebox.showerror(
            "Error de compilacion", "Se ha encontrado errores de compilacion, revisa en pestaña de errores")
    else:
        messagebox.showinfo("Analizar", "Archivo analizado exitosamente")


def errores():
    global errores
    if errores == []:
        print(errores)
    else:
        messagebox.showinfo("Errores", "No se han encontrado errores")


def create_table():
    global a
    print(a.TokenList)
    ventana = tk.Tk()
    ventana.title("Tabla de información")

    tabla = ttk.Treeview(ventana)
    tabla['columns'] = ('id', 'Token', 'Lexema')
    tabla.column('#0', width=0, stretch=tk.NO)
    tabla.column('id', anchor=tk.CENTER, width=50)
    tabla.column('Token', anchor=tk.W, width=100)
    tabla.column('Lexema', anchor=tk.W, width=100)

    tabla.heading('#0', text='', anchor=tk.CENTER)
    tabla.heading('id', text='ID', anchor=tk.CENTER)
    tabla.heading('Token', text='Token', anchor=tk.CENTER)
    tabla.heading('Lexema', text='Lexema', anchor=tk.CENTER)

    for i, fila in enumerate(a.TokenList):
        print(fila)
        tabla.insert(parent='', index=i, iid=i,
                     values=(fila[0], fila[1], fila[2]))

    # Mostrar tabla
    tabla.pack(padx=10, pady=10)
    ventana.mainloop()


def error_table():
    global a
    print(a.ListaErrores)
    ventana = tk.Tk()
    ventana.title("Lista de errores")

    tabla = ttk.Treeview(ventana)
    tabla['columns'] = ('Tipo', 'Linea', 'Posicion', 'Token', 'Descripcion')
    tabla.column('#0', width=0, stretch=tk.NO)
    tabla.column('Tipo', anchor=tk.CENTER, width=100)
    tabla.column('Linea', anchor=tk.W, width=100)
    tabla.column('Posicion', anchor=tk.W, width=100)
    tabla.column('Token', anchor=tk.W, width=100)
    tabla.column('Descripcion', anchor=tk.W, width=200)

    tabla.heading('#0', text='', anchor=tk.CENTER)
    tabla.heading('Tipo', text='Tipo', anchor=tk.CENTER)
    tabla.heading('Linea', text='Linea', anchor=tk.CENTER)
    tabla.heading('Posicion', text='Posicion', anchor=tk.CENTER)
    tabla.heading('Token', text='Token', anchor=tk.CENTER)
    tabla.heading('Descripcion', text='Descripcion', anchor=tk.CENTER)

    for i, fila in enumerate(a.ListaErrores):
        print(fila)
        tabla.insert(parent='', index=i, iid=i,
                     values=('Sintactico', fila[1], fila[2], fila[3], fila[4]))

    # Mostrar tabla
    tabla.pack(padx=10, pady=10)
    ventana.mainloop()


def salir():
    ventana.destroy()


def manual_usuario():
    subprocess.Popen(['start', 'manualUsuario.pdf'], shell=True)


def manual_tecnico():
    subprocess.Popen(['start', 'manualTecnico.pdf'], shell=True)


def temas_ayuda():
    user()


def user():

    ventana_usuario = tk.Tk()
    ventana_usuario.title("Temas de ayuda")

    nombre = tk.Label(
        ventana_usuario, text="Nombre: Cristian Giovanni Estrada Ramirez")
    carnet = tk.Label(ventana_usuario, text="Carnet: 202006413")
    gmail = tk.Label(
        ventana_usuario, text="Correo: 2991897830101@ingenieria.usac.edu.gt")
    curso = tk.Label(
        ventana_usuario, text="Lenguajes Formales de Programacion")

    nombre.pack()
    carnet.pack()
    gmail.pack()
    curso.pack()


ventana = tk.Tk()
ventana.title("Mi aplicación")

editor = tk.Text(ventana)
editor.pack(fill=tk.BOTH, expand=True)

menu_principal = tk.Menu(ventana)
ventana.config(menu=menu_principal)

menu_archivo = tk.Menu(menu_principal, tearoff=0)
menu_principal.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Nuevo", command=newDoc)
menu_archivo.add_command(label="Abrir", command=openDoc)
menu_archivo.add_command(label="Guardar", command=saveDoc)
menu_archivo.add_command(label="Guardar Como", command=saveAsDoc)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=salir)
menu_archivo.entryconfig("Guardar", state="disabled")

menu_analisis = tk.Menu(menu_principal, tearoff=0)
menu_principal.add_cascade(label="Analisis", menu=menu_analisis)
menu_analisis.add_command(label="Generar sentencias", command=analizar)

menu_principal.add_command(label="Tokens", command=create_table)
menu_principal.add_command(label="Errores", command=error_table)


# menu_ayuda.add_command(label="Manual de usuario", command=manual_usuario)
# menu_ayuda.add_command(label="Manual técnico", command=manual_tecnico)
# menu_ayuda.add_command(label="Temas de ayuda", command=temas_ayuda)

# Mostrar la ventana
ventana.mainloop()
