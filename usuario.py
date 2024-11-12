import tkinter as tk
from tkinter import messagebox, ttk
from clase import Usuario
from comun import *

def mostrar_usuarios(self):
    # Limpiar el frame actual antes de mostrar los autores
    ventana_usuario = tk.Toplevel(self.root)
    ventana_usuario.title("Mostrar usuarios")
    
    # Hacer que la ventana esté al frente
    ventana_usuario.lift()
    ventana_usuario.attributes("-topmost", True)
    ventana_usuario.after(100, lambda: ventana_usuario.attributes("-topmost", False)) 

    # Crear la grilla (Treeview) para mostrar los autores
    columnas = ("Nombre", "Apellido", "Usuario", "Direccion", "Telefono")
    tree = ttk.Treeview(ventana_usuario, columns=columnas, show='headings')
    tree.pack(pady=20)

    # Definir las columnas
    for col in columnas:
        tree.heading(col, text=col)
        
        # Función para actualizar los datos en el Treeview y poner la ventana al frente
    def actualizar_usuarios():
        for row in tree.get_children():
            tree.delete(row)
        usuarios = obtener_usuarios()
        for usuario in usuarios:
            tree.insert('', 'end', values=usuario)
        # Poner la ventana al frente cada vez que se actualizan los autores
        ventana_usuario.lift()
        ventana_usuario.attributes("-topmost", True)
        ventana_usuario.after(100, lambda: ventana_usuario.attributes("-topmost", False))

    actualizar_usuarios()  # Cargar autores al abrir la ventana
        
    # Crear un botón para registrar nuevos autores
    tk.Button(ventana_usuario, text="Registrar usuario", command=lambda: registrar_usuario(self, actualizar_usuarios)).pack(pady=10)
        
def registrar_usuario(self, actualizar_usuarios):
    ventana_usuario = tk.Toplevel(self.root)
    ventana_usuario.title("Registrar Usuario")
    
    vcmd = (ventana_usuario.register(validar_longitud_texto), "%P")
        
    tk.Label(ventana_usuario, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    nombre_entry = tk.Entry(ventana_usuario, validate="key", validatecommand=vcmd)
    nombre_entry.grid(row=0, column=1)
    
    tk.Label(ventana_usuario, text="Apellido:").grid(row=1, column=0, padx=5, pady=5)
    apellido_entry = tk.Entry(ventana_usuario, validate="key", validatecommand=vcmd)
    apellido_entry.grid(row=1, column=1)
    
    tk.Label(ventana_usuario, text="Tipo de Usuario:").grid(row=2, column=0, padx=5, pady=5)
    tipos_usuario = ["Estudiante", "Profesor"]
    tipo_usuario_combobox = ttk.Combobox(ventana_usuario, values=tipos_usuario, state="readonly")
    tipo_usuario_combobox.grid(row=2, column=1)
    tipo_usuario_combobox.set("Seleccionar tipo de usuario")
    
    tk.Label(ventana_usuario, text="Dirección:").grid(row=3, column=0, padx=5, pady=5)
    direccion_entry = tk.Entry(ventana_usuario, validate="key", validatecommand=vcmd)
    direccion_entry.grid(row=3, column=1)
    
    # Validador longitud texto
    vcmd = (ventana_usuario.register(validar_numeros), '%P')

    tk.Label(ventana_usuario, text="Teléfono:").grid(row=4, column=0, padx=5, pady=5)
    telefono_entry = tk.Entry(ventana_usuario, validate="key", validatecommand=vcmd)
    telefono_entry.grid(row=4, column=1)
    
    def guardar_usuario():
        usuario = Usuario(
            nombre_entry.get(), apellido_entry.get(), tipo_usuario_combobox.get(),
            direccion_entry.get(), telefono_entry.get()
        )
        usuario.guardar()
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        actualizar_usuarios()
        cerrarVentana(ventana_usuario)
    
    tk.Button(ventana_usuario, text="Guardar", command=guardar_usuario).grid(row=5, column=0, columnspan=2, pady=10)
    tk.Button(ventana_usuario, text="Cancelar", command=lambda: cerrarVentana(ventana_usuario)).grid(row=5, column=1, columnspan=2, pady=10)