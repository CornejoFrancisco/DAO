import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage
from clase import Autor
from comun import *

def mostrar_autores(self):
    icon_image = PhotoImage(file="UTN_logo.png")  


    # Limpiar el frame actual antes de mostrar los autores
    ventana_autores = tk.Toplevel(self.root)
    ventana_autores.title("Mostrar autor")
    ventana_autores.geometry("650x350") 
    ventana_autores.minsize(650, 350) 
    
    ventana_autores.iconphoto(True, icon_image)
    # Hacer que la ventana este al frente
    ventana_autores.lift()
    ventana_autores.attributes("-topmost", True)
    ventana_autores.after(100, lambda: ventana_autores.attributes("-topmost", False))
    
    # Crear la grilla para mostrar los autores
    #columnas = ('Nombre', 'Apellido', 'Nacionalidad')
    #tree = ttk.Treeview(ventana_autores, columns=columnas, show='headings')
    #tree.pack(pady=20)

    frame_tree = tk.Frame(ventana_autores)
    frame_tree.pack(fill="both", expand=True, pady=20)

    # Crear el Treeview con el scrollbar
    columnas = ('Nombre', 'Apellido', 'Nacionalidad')
    tree = ttk.Treeview(frame_tree, columns=columnas, show='headings')
    tree.pack(side="left", fill="both", expand=True)
    
    scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    
    for col in columnas:
        tree.heading(col, text=col)
    
    # Funcion para actualizar los datos en el Treeview y poner la ventana al frente
    def actualizar_autores():
        for row in tree.get_children():
            tree.delete(row)
        autores = obtener_autores()
        for autor in autores:
            tree.insert('', 'end', values=autor[1:])
        # Poner la ventana al frente cada vez que se actualizan los autores
        ventana_autores.lift()
        ventana_autores.attributes("-topmost", True)
        ventana_autores.after(100, lambda: ventana_autores.attributes("-topmost", False))

    actualizar_autores()
    
    # Crear un boton para registrar nuevos autores
    tk.Button(
        ventana_autores, text="Registrar autor", 
        command=lambda: registrar_autor(self, actualizar_autores),
        bg="green",
        fg="white"
    ).pack(pady=10)


def registrar_autor(self, actualizar_autores):
    ventana_autor = tk.Toplevel(self.root)
    ventana_autor.title("Registrar Autor")
    ventana_autor.geometry("250x200")
    ventana_autor.minsize(250, 200)

    ventana_autor.lift()
    ventana_autor.attributes("-topmost", True)
    ventana_autor.after(100, lambda: ventana_autor.attributes("-topmost", False))        
            
    tk.Label(ventana_autor, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    nombre_entry = tk.Entry(ventana_autor)
    nombre_entry.grid(row=0, column=1)
    
    tk.Label(ventana_autor, text="Apellido:").grid(row=1, column=0, padx=5, pady=5)
    apellido_entry = tk.Entry(ventana_autor)
    apellido_entry.grid(row=1, column=1)
    
    tk.Label(ventana_autor, text="Nacionalidad:").grid(row=2, column=0, padx=5, pady=5)
    nacionalidades = [
        "Argentina", "Brasil", "Chile", "Colombia", "Mexico", "Peru", "Uruguay", "Venezuela", "Estados Unidos",
        "España", "Francia", "Italia", "Alemania", "Reino Unido", "Japon", "China", "India", "Australia"
    ]
    nacionalidad_combobox = ttk.Combobox(ventana_autor, values=nacionalidades, state="readonly")
    nacionalidad_combobox.grid(row=2, column=1)
    nacionalidad_combobox.set("Seleccionar nacionalidad")
    
    def guardar_autor():
        try:
            # Validaciones
            if not validar_longitud_texto(nombre_entry.get()):
                raise ValueError("El nombre debe tener mas de 0 caracteres y menos de 50 caracteres")
            
            if not validar_longitud_texto(apellido_entry.get()):
                raise ValueError("El apellido debe tener mas de 0 caracteres y menos de 50 caracteres")
            
            if nacionalidad_combobox.get() == "Seleccionar nacionalidad":
                raise ValueError("Debe seleccionar una nacionalidad")

            autor = Autor(nombre_entry.get(), apellido_entry.get(), nacionalidad_combobox.get())
            autor.guardar()
            messagebox.showinfo("Exito", "Autor registrado correctamente.")
            actualizar_autores()
            cerrarVentana(ventana_autor)
        except ValueError as e:
            ventana_autor.lift()
            ventana_autor.attributes("-topmost", True)
            ventana_autor.after(100, lambda: ventana_autor.attributes("-topmost", False))
            messagebox.showerror("Error", str(e))
    
    botones_frame = tk.Frame(ventana_autor)
    botones_frame.grid(row=5, column=0, columnspan=2, pady=10)
    tk.Button(botones_frame, text="Guardar", command=guardar_autor).pack(side="left", padx=(0, 10))
    tk.Button(botones_frame, text="Cancelar", command=lambda: cerrarVentana(ventana_autor)).pack(side="left")
    