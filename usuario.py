import tkinter as tk
from tkinter import messagebox, ttk
from clase import Usuario
from comun import *

def mostrar_usuarios(self):
    # Limpiar el frame actual antes de mostrar los autores
    ventana_usuario = tk.Toplevel(self.root)
    ventana_usuario.title("Mostrar usuarios")
    
    # Hacer que la ventana este al frente
    ventana_usuario.lift()
    ventana_usuario.attributes("-topmost", True)
    ventana_usuario.after(100, lambda: ventana_usuario.attributes("-topmost", False)) 

    # Crear la grilla para mostrar los autores
    columnas = ("Nombre", "Apellido", "Rol", "Direccion", "Telefono")
    tree = ttk.Treeview(ventana_usuario, columns=columnas, show='headings')
    tree.pack(pady=20)

    for col in columnas:
        tree.heading(col, text=col)
        
    def actualizar_usuarios():
        for row in tree.get_children():
            tree.delete(row)
        usuarios = obtener_usuarios()
        for usuario in usuarios:
            tree.insert('', 'end', values=usuario[1:])
        # Poner la ventana al frente cada vez que se actualizan los autores
        ventana_usuario.lift()
        ventana_usuario.attributes("-topmost", True)
        ventana_usuario.after(100, lambda: ventana_usuario.attributes("-topmost", False))

    actualizar_usuarios()
        
    # Crear un boton para registrar nuevos autores
    tk.Button(ventana_usuario, text="Registrar usuario", command=lambda: registrar_usuario(self, actualizar_usuarios)).pack(pady=10)
        
def registrar_usuario(self, actualizar_usuarios):
    ventana_usuario = tk.Toplevel(self.root)
    ventana_usuario.title("Registrar Usuario")
            
    tk.Label(ventana_usuario, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    nombre_entry = tk.Entry(ventana_usuario)
    nombre_entry.grid(row=0, column=1)
    
    tk.Label(ventana_usuario, text="Apellido:").grid(row=1, column=0, padx=5, pady=5)
    apellido_entry = tk.Entry(ventana_usuario)
    apellido_entry.grid(row=1, column=1)
    
    # Desplegable para tipo de usuario
    tk.Label(ventana_usuario, text="Tipo de Usuario:").grid(row=2, column=0, padx=5, pady=5)
    tipos_usuario = ["Estudiante", "Profesor"]
    tipo_usuario_combobox = ttk.Combobox(ventana_usuario, values=tipos_usuario, state="readonly")
    tipo_usuario_combobox.grid(row=2, column=1)
    tipo_usuario_combobox.set("Seleccionar tipo de usuario")
    
    tk.Label(ventana_usuario, text="Direccion:").grid(row=3, column=0, padx=5, pady=5)
    direccion_entry = tk.Entry(ventana_usuario)
    direccion_entry.grid(row=3, column=1)
    
    tk.Label(ventana_usuario, text="Telefono:").grid(row=4, column=0, padx=5, pady=5)
    telefono_entry = tk.Entry(ventana_usuario)
    telefono_entry.grid(row=4, column=1)
    
    def guardar_usuario():
        try:
            # Validaciones
            if not validar_longitud_texto(nombre_entry.get()):
                raise ValueError("El nombre debe tener mas de 0 caracteres y menos de 50 caracteres")
            
            if not validar_longitud_texto(apellido_entry.get()):
                raise ValueError("El apellido debe tener mas de 0 caracteres y menos de 50 caracteres")

            if tipo_usuario_combobox.get() == "Seleccionar tipo de usuario":
                raise ValueError("Debe seleccionar un tipo de usuario")
            
            if not validar_longitud_texto(direccion_entry.get()):
                raise ValueError("La direccion debe tener mas de 0 caracteres y menos de 50 caracteres")
            
            if not validar_numeros_positivos(telefono_entry.get()):
                raise ValueError("El numero no puede ser vacio ni contener letras")
            
            usuario = Usuario(
                nombre_entry.get(), apellido_entry.get(), tipo_usuario_combobox.get(),
                direccion_entry.get(), telefono_entry.get()
            )
            usuario.guardar()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            actualizar_usuarios()
            cerrarVentana(ventana_usuario)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    tk.Button(ventana_usuario, text="Guardar", command=guardar_usuario).grid(row=5, column=0, columnspan=2, pady=10)
    tk.Button(ventana_usuario, text="Cancelar", command=lambda: cerrarVentana(ventana_usuario)).grid(row=5, column=1, columnspan=2, pady=10)