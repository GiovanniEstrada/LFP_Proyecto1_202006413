import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import subprocess


def openDoc():
    archivo = filedialog.askopenfilename(title="Abrir archivo")
    if archivo:
        with open(archivo, "r") as f:
            informacion = f.read()
        editor.delete(1.0, tk.END)
        editor.insert(tk.END, informacion)
        informacion = informacion.split("{")
        print(informacion)


def saveDoc():
    archivo = filedialog.asksaveasfilename(title="Guardar archivo")
    if archivo:
        informacion = editor.get(1.0, tk.END)
        with open(archivo, "w") as f:
            f.write(informacion)
        messagebox.showinfo("Guardar", "Archivo guardado exitosamente")


def newDoc():
    archivo = filedialog.asksaveasfilename(title="Guardar como")
    if archivo:
        informacion = editor.get(1.0, tk.END)
        with open(archivo, "w") as f:
            f.write(informacion)


def analizar():
    messagebox.showinfo("Analizar", "Archivo analizado exitosamente")


def errores():
    messagebox.showinfo("Errores", "No se han encontrado errores")


def salir():
    ventana.destroy()


def manual_usuario():
    subprocess.Popen(['open', 'manualUsuario.pdf'], shell=True)


def manual_tecnico():
    subprocess.Popen(['open', 'manualTecnico.pdf'], shell=True)


def temas_ayuda():
    messagebox.showinfo("Temas de ayuda", "Aquí van los temas de ayuda")


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Mi aplicación")

# Crear el widget Text
editor = tk.Text(ventana)
editor.pack(fill=tk.BOTH, expand=True)

# Crear el menú principal
menu_principal = tk.Menu(ventana)
ventana.config(menu=menu_principal)

# Crear las opciones del menú "Archivo"
menu_archivo = tk.Menu(menu_principal, tearoff=0)
menu_principal.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Abrir", command=openDoc)
menu_archivo.add_command(label="Guardar", command=saveDoc)
menu_archivo.add_command(label="Guardar como", command=newDoc)
menu_archivo.add_separator()
menu_archivo.add_command(label="Analizar", command=analizar)
menu_archivo.add_command(label="Errores", command=errores)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=salir)

# Crear las opciones del menú "Ayuda"
menu_ayuda = tk.Menu(menu_principal, tearoff=0)
menu_principal.add_cascade(label="Ayuda", menu=menu_ayuda)
menu_ayuda.add_command(label="Manual de usuario", command=manual_usuario)
menu_ayuda.add_command(label="Manual técnico", command=manual_tecnico)
menu_ayuda.add_command(label="Temas de ayuda", command=temas_ayuda)

# Mostrar la ventana
ventana.mainloop()
