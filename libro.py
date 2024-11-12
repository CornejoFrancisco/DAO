import tkinter as tk
from tkinter import messagebox, ttk
from clase import Libro
from comun import *

def mostrar_libros(self):
    # Limpiar el frame actual antes de mostrar los libros
    ventana_libro = tk.Toplevel(self.root)
    ventana_libro.title("Mostrar libro")
    
    # Hacer que la ventana esté al frente
    ventana_libro.lift()
    ventana_libro.attributes("-topmost", True)
    ventana_libro.after(100, lambda: ventana_libro.attributes("-topmost", False))  # Se desactiva el topmost después de 100 ms
    
    # Crear la grilla (Treeview) para mostrar los libros
    columnas = ("ISBN", "Titulo", "Genero", "Anio publicacion", "Autor", "Ejemplares")
    tree = ttk.Treeview(ventana_libro, columns=columnas, show='headings')
    tree.pack(pady=20)

    # Definir las columnas
    for col in columnas:
        tree.heading(col, text=col)

    # Función para actualizar la lista de libros en el Treeview
    def actualizar_libros():
        for row in tree.get_children():
            tree.delete(row)
        libros = obtener_libros()
        for libro in libros:
            # Concatenar el nombre y apellido del autor en una sola columna
            autor_completo = f"{libro[4]} {libro[5]}"  # libro[4] es el nombre y libro[5] es el apellido
            tree.insert('', 'end', values=(libro[0], libro[1], libro[2], libro[3], autor_completo, libro[6]))
                # Poner la ventana al frente cada vez que se actualizan los autores
        ventana_libro.lift()
        ventana_libro.attributes("-topmost", True)
        ventana_libro.after(100, lambda: ventana_libro.attributes("-topmost", False))
    
    # Cargar los libros al abrir la ventana
    actualizar_libros()

    # Crear un botón para registrar nuevos libros y pasar actualizar_libros como callback
    tk.Button(ventana_libro, text="Registrar libro", command=lambda: registrar_libro(self, actualizar_libros)).pack(pady=10)

def registrar_libro(self, callback):
    ventana_libro = tk.Toplevel(self.root)
    ventana_libro.title("Registrar Libro")                    

    tk.Label(ventana_libro, text="ISBN:").grid(row=0, column=0, padx=5, pady=5)
    isbn_entry = tk.Entry(ventana_libro, validate="key")
    isbn_entry.grid(row=0, column=1)
    
    tk.Label(ventana_libro, text="Título:").grid(row=1, column=0, padx=5, pady=5)
    titulo_entry = tk.Entry(ventana_libro, validate="key")
    titulo_entry.grid(row=1, column=1)
    
    tk.Label(ventana_libro, text="Género:").grid(row=2, column=0, padx=5, pady=5)
    generos = ["Ficción", "No Ficción", "Ciencia Ficción", "Fantasía", "Biografía", "Historia", "Romance", "Misterio"]
    genero_combobox = ttk.Combobox(ventana_libro, values=generos, state="readonly")
    genero_combobox.grid(row=2, column=1)
    genero_combobox.set("Seleccionar género")        
    
    tk.Label(ventana_libro, text="Año de Publicación:").grid(row=3, column=0, padx=5, pady=5)
    anio_entry = tk.Entry(ventana_libro, validate="key")
    anio_entry.grid(row=3, column=1)
    
    # Desplegable para autores
    tk.Label(ventana_libro, text="Autor:").grid(row=4, column=0, padx=5, pady=5)
    autores = obtener_autores()
    autores_nombres = [f"{autor[1]} {autor[2]}" for autor in autores]
    autor_combobox = ttk.Combobox(ventana_libro, values=autores_nombres, state="readonly")
    autor_combobox.grid(row=4, column=1)
    autor_combobox.set("Seleccionar un autor")
        
    tk.Label(ventana_libro, text="Cantidad Disponible:").grid(row=5, column=0, padx=5, pady=5)
    cantidad_entry = tk.Entry(ventana_libro, validate="key")
    cantidad_entry.grid(row=5, column=1)

    def guardar_libro():
        try:
            # Obtener el autor seleccionado y su ID
            autor_index = autor_combobox.current()
            if autor_index == -1:
                raise ValueError("Seleccione un autor válido.")
            autor_id = autores[autor_index][0]

            libro = Libro(
                isbn_entry.get(), titulo_entry.get(), genero_combobox.get(),
                int(anio_entry.get()), autor_id, int(cantidad_entry.get())
            )
            libro.guardar()
            messagebox.showinfo("Éxito", "Libro registrado correctamente.")
            callback()
            cerrarVentana(ventana_libro)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    tk.Button(ventana_libro, text="Guardar", command=guardar_libro).grid(row=6, column=0, columnspan=2, pady=10)
    tk.Button(ventana_libro, text="Cancelar", command=lambda: cerrarVentana(ventana_libro)).grid(row=6, column=1, columnspan=2, pady=10)
