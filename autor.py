import tkinter as tk
from tkinter import messagebox, ttk
from clase import Autor
from comun import *

def mostrar_autores(self):
    # Limpiar el frame actual antes de mostrar los autores
    ventana_autores = tk.Toplevel(self.root)
    ventana_autores.title("Mostrar autor")
    
    # Hacer que la ventana esté al frente
    ventana_autores.lift()
    ventana_autores.attributes("-topmost", True)
    ventana_autores.after(100, lambda: ventana_autores.attributes("-topmost", False))  # Se desactiva el topmost después de 100 ms
    
    # Crear la grilla (Treeview) para mostrar los autores
    columnas = ('Nombre', 'Apellido', 'Nacionalidad')
    tree = ttk.Treeview(ventana_autores, columns=columnas, show='headings')
    tree.pack(pady=20)
    
    for col in columnas:
        tree.heading(col, text=col)
    
    # Función para actualizar los datos en el Treeview y poner la ventana al frente
    def actualizar_autores():
        for row in tree.get_children():
            tree.delete(row)
        autores = obtener_autores()
        for autor in autores:
            tree.insert('', 'end', values=autor)
        # Poner la ventana al frente cada vez que se actualizan los autores
        ventana_autores.lift()
        ventana_autores.attributes("-topmost", True)
        ventana_autores.after(100, lambda: ventana_autores.attributes("-topmost", False))

    actualizar_autores()  # Cargar autores al abrir la ventana
    
    # Crear un botón para registrar nuevos autores
    tk.Button(
        ventana_autores, text="Registrar autor", 
        command=lambda: registrar_autor(self, actualizar_autores)
    ).pack(pady=10)


def registrar_autor(self, actualizar_autores):
    ventana_autor = tk.Toplevel(self.root)
    ventana_autor.title("Registrar Autor")        
        
    vcmd = (ventana_autor.register(validar_longitud_texto), "%P")
    
    tk.Label(ventana_autor, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    nombre_entry = tk.Entry(ventana_autor, validate="key", validatecommand=vcmd)
    nombre_entry.grid(row=0, column=1)
    
    tk.Label(ventana_autor, text="Apellido:").grid(row=1, column=0, padx=5, pady=5)
    apellido_entry = tk.Entry(ventana_autor, validate="key", validatecommand=vcmd)
    apellido_entry.grid(row=1, column=1)
    
    tk.Label(ventana_autor, text="Nacionalidad:").grid(row=2, column=0, padx=5, pady=5)
    nacionalidades = [
        "Argentina", "Brasil", "Chile", "Colombia", "México", "Perú", "Uruguay", "Venezuela", "Estados Unidos",
        "España", "Francia", "Italia", "Alemania", "Reino Unido", "Japón", "China", "India", "Australia"
    ]
    nacionalidad_combobox = ttk.Combobox(ventana_autor, values=nacionalidades, state="readonly")
    nacionalidad_combobox.grid(row=2, column=1)
    nacionalidad_combobox.set("Seleccionar nacionalidad")
    
    def guardar_autor():
        autor = Autor(nombre_entry.get(), apellido_entry.get(), nacionalidad_combobox.get())
        autor.guardar()
        messagebox.showinfo("Éxito", "Autor registrado correctamente.")
        actualizar_autores()
        cerrarVentana(ventana_autor)
    
    tk.Button(ventana_autor, text="Guardar", command=guardar_autor).grid(row=3, column=0, columnspan=2, pady=10)
    tk.Button(ventana_autor, text="Cancelar", command=lambda: cerrarVentana(ventana_autor)).grid(row=3, column=1, columnspan=2, pady=10)
