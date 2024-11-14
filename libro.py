import tkinter as tk
from tkinter import messagebox, ttk
from clase import Libro
from comun import *
from prestamo import registrar_prestamo

def mostrar_libros(self):
    # Limpiar el frame actual antes de mostrar los libros
    ventana_libro = tk.Toplevel(self.root)
    ventana_libro.title("Mostrar libro")
    ventana_libro.geometry("650x350") 
    ventana_libro.minsize(650, 350) 
    
    # Hacer que la ventana este al frente
    ventana_libro.lift()
    ventana_libro.attributes("-topmost", True)
    ventana_libro.after(100, lambda: ventana_libro.attributes("-topmost", False))
    
    # Crear la grilla para mostrar los libros
    #columnas = ("ISBN", "Titulo", "Genero", "Anio publicacion", "Autor", "Ejemplares")
    #tree = ttk.Treeview(ventana_libro, columns=columnas, show='headings')
    #tree.pack(pady=20)

    frame_tree = tk.Frame(ventana_libro)
    frame_tree.pack(fill="both", expand=True, pady=20)
    # Crear el Treeview con el scrollbar
    columnas = ("ISBN", "Titulo", "Genero", "Anio publicacion", "Autor", "Ejemplares")
    tree = ttk.Treeview(frame_tree, columns=columnas, show='headings')
    tree.pack(side="left", fill="both", expand=True)
    
    scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    for col in columnas:
        tree.heading(col, text=col)

    # Funcion para actualizar la lista de libros
    def actualizar_libros():
        for row in tree.get_children():
            tree.delete(row)
        libros = obtener_libros()
        for libro in libros:
            # Concatenar el nombre y apellido del autor en una sola columna
            autor_completo = f"{libro[4]} {libro[5]}"
            tree.insert('', 'end', values=(libro[0], libro[1], libro[2], libro[3], autor_completo, libro[6]))
        ventana_libro.lift()
        ventana_libro.attributes("-topmost", True)
        ventana_libro.after(100, lambda: ventana_libro.attributes("-topmost", False))
    
    actualizar_libros()

    # Funcion para realizar un prestamo de un libro seleccionado
    def realizar_prestamo():
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            libro_info = item['values']
            isbn = libro_info[0]
            titulo = libro_info[1]
            ejemplares = libro_info[5]
            
            if ejemplares == 0:
                messagebox.showwarning("Sin ejemplares", "No hay ejemplares disponibles para realizar el prestamo.")
                return

            registrar_prestamo(self, ventana_libro, isbn, titulo)
            actualizar_libros()  # Actualiza la lista despues del prestamo
        else:
            messagebox.showwarning("Seleccion requerida", "Seleccione un libro para realizar el prestamo.")

    # Crear un Frame para los botones y colocarlos uno al lado del otro
    botones_frame = tk.Frame(ventana_libro)
    botones_frame.pack(pady=10)

    # Botón para registrar nuevos préstamos (color verde)
    boton_registrar = tk.Button(
        botones_frame, 
        text="Registrar libro",
        command=lambda: registrar_libro(self, actualizar_libros),
        bg="green", 
        fg="white"
    )
    boton_registrar.pack(side="left", padx=5)

    # Botón para devolver el libro seleccionado (color azul)
    boton_devolver = tk.Button(
        botones_frame, 
        text="Realizar prestamo",
        command=realizar_prestamo,
        bg="blue", 
        fg="white"
    )
    boton_devolver.pack(side="left", padx=5)
    
def registrar_libro(self, callback):
    ventana_libro = tk.Toplevel(self.root)
    ventana_libro.title("Registrar Libro")
    ventana_libro.geometry("350x250") 
    ventana_libro.minsize(350, 250) 

    tk.Label(ventana_libro, text="ISBN:").grid(row=0, column=0, padx=5, pady=5)
    isbn_entry = tk.Entry(ventana_libro)
    isbn_entry.grid(row=0, column=1)
    
    tk.Label(ventana_libro, text="Titulo:").grid(row=1, column=0, padx=5, pady=5)
    titulo_entry = tk.Entry(ventana_libro)
    titulo_entry.grid(row=1, column=1)
    
    # Desplegable para genero de libros
    tk.Label(ventana_libro, text="Genero:").grid(row=2, column=0, padx=5, pady=5)
    generos = ["Ficcion", "No Ficcion", "Ciencia Ficcion", "Fantasia", "Biografia", "Historia", "Romance", "Misterio"]
    genero_combobox = ttk.Combobox(ventana_libro, values=generos, state="readonly")
    genero_combobox.grid(row=2, column=1)
    genero_combobox.set("Seleccionar genero")
    
    tk.Label(ventana_libro, text="Año de Publicacion:").grid(row=3, column=0, padx=5, pady=5)
    anio_entry = tk.Entry(ventana_libro)
    anio_entry.grid(row=3, column=1)
    
    # Desplegable para autores
    tk.Label(ventana_libro, text="Autor:").grid(row=4, column=0, padx=5, pady=5)
    autores = obtener_autores()
    autores_nombres = [f"{autor[1]} {autor[2]}" for autor in autores]
    autor_combobox = ttk.Combobox(ventana_libro, values=autores_nombres, state="readonly")
    autor_combobox.grid(row=4, column=1)
    autor_combobox.set("Seleccionar un autor")
    
    tk.Label(ventana_libro, text="Cantidad Disponible:").grid(row=5, column=0, padx=5, pady=5)
    cantidad_entry = tk.Entry(ventana_libro)
    cantidad_entry.grid(row=5, column=1)

    def guardar_libro():
        try:
            # Validaciones
            if not validar_longitud_texto(isbn_entry.get(), 0, 14):
                raise ValueError("El isbn debe tener mas de 0 caracteres y menos de 14 caracteres")
            
            if not validar_longitud_texto(titulo_entry.get()):
                raise ValueError("El titulo debe tener mas de 0 caracteres y menos de 50 caracteres")
            
            if genero_combobox.get() == "Seleccionar genero":
                raise ValueError("Debe seleccionar un genero")

            if not validar_anio_input(anio_entry.get()):
                raise ValueError("El año debe ser mayor a 1900 y menor a 2024")

            if autor_combobox.get() == "Seleccionar un autor":
                raise ValueError("Debe seleccionar un autor")
            
            if not validar_numeros_positivos(cantidad_entry.get()):
                raise ValueError("La cantidad debe ser un numero positivo")
            
            autor_index = autor_combobox.current()
            if autor_index == -1:
                raise ValueError("Seleccione un autor valido.")
            autor_id = autores[autor_index][0]

            libro = Libro(
                isbn_entry.get(), titulo_entry.get(), genero_combobox.get(),
                int(anio_entry.get()), autor_id, int(cantidad_entry.get())
            )
            libro.guardar()
            messagebox.showinfo("Exito", "Libro registrado correctamente.")
            callback()
            cerrarVentana(ventana_libro)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    tk.Button(ventana_libro, text="Guardar", command=guardar_libro).grid(row=6, column=0, columnspan=2, pady=10)
    tk.Button(ventana_libro, text="Cancelar", command=lambda: cerrarVentana(ventana_libro)).grid(row=6, column=1, columnspan=2, pady=10)
