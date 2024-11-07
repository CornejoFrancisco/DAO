import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from tkcalendar import Calendar 
from database import obtener_conexion
from clase import Libro, Autor, Usuario, Prestamo

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Biblioteca - Gestión")
        self.root.geometry("800x600")
        
        # Crear botones de acciones
        self.create_buttons()
        self.create_frames()

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.TOP, pady=10)
        
        tk.Button(button_frame, text="Registrar Autor", command=self.registrar_autor).grid(row=0, column=0, pady=5)
        tk.Button(button_frame, text="Registrar Libro", command=self.registrar_libro).grid(row=1, column=0, pady=5)
        tk.Button(button_frame, text="Registrar Usuario", command=self.registrar_usuario).grid(row=2, column=0, pady=5)
        tk.Button(button_frame, text="Préstamo de Libro", command=self.prestamo_libro).grid(row=3, column=0, pady=5)
        tk.Button(button_frame, text="Devolución de Libro", command=self.devolucion_libro).grid(row=4, column=0, pady=5)
        tk.Button(button_frame, text="Consultar Disponibilidad", command=self.consultar_disponibilidad).grid(row=5, column=0, pady=5)
        tk.Button(button_frame, text="Generar Reportes", command=self.generar_reportes).grid(row=6, column=0, pady=5)
    
    def create_frames(self):
        # Frame para formulario dinámico
        self.form_frame = tk.Frame(self.root)
        self.form_frame.pack(pady=20)
    
    def registrar_autor(self):
        self.clear_frame()
        
        tk.Label(self.form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        nombre_entry = tk.Entry(self.form_frame)
        nombre_entry.grid(row=0, column=1)
        
        tk.Label(self.form_frame, text="Apellido:").grid(row=1, column=0, padx=5, pady=5)
        apellido_entry = tk.Entry(self.form_frame)
        apellido_entry.grid(row=1, column=1)
        
        tk.Label(self.form_frame, text="Nacionalidad:").grid(row=2, column=0, padx=5, pady=5)

        # Lista de nacionalidades
        nacionalidades = [
            "Argentina", "Brasil", "Chile", "Colombia", "México", "Perú", "Uruguay", "Venezuela", "Estados Unidos",
            "España", "Francia", "Italia", "Alemania", "Reino Unido", "Japón", "China", "India", "Australia"
        ]
        
        # Combobox para seleccionar la nacionalidad
        nacionalidad_combobox = ttk.Combobox(self.form_frame, values=nacionalidades)
        nacionalidad_combobox.grid(row=2, column=1)
        nacionalidad_combobox.set("Seleccionar nacionalidad")  # Texto inicial
        
        def guardar_autor():
            autor = Autor(nombre_entry.get(), apellido_entry.get(), nacionalidad_combobox.get())
            autor.guardar()
            messagebox.showinfo("Éxito", "Autor registrado correctamente.")
            self.clear_frame()
        
        tk.Button(self.form_frame, text="Guardar", command=guardar_autor).grid(row=3, column=0, columnspan=2, pady=10)
    
    def obtener_autores(self):
        """Función para obtener una lista de autores desde la base de datos."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, apellido FROM Autor")
        autores = cursor.fetchall()
        conexion.close()
        return autores

    def registrar_libro(self):
        self.clear_frame()
        
        tk.Label(self.form_frame, text="ISBN:").grid(row=0, column=0, padx=5, pady=5)
        isbn_entry = tk.Entry(self.form_frame)
        isbn_entry.grid(row=0, column=1)
        
        tk.Label(self.form_frame, text="Título:").grid(row=1, column=0, padx=5, pady=5)
        titulo_entry = tk.Entry(self.form_frame)
        titulo_entry.grid(row=1, column=1)
        
        tk.Label(self.form_frame, text="Género:").grid(row=2, column=0, padx=5, pady=5)
        generos = ["Ficción", "No Ficción", "Ciencia Ficción", "Fantasía", "Biografía", "Historia", "Romance", "Misterio"]
        genero_combobox = ttk.Combobox(self.form_frame, values=generos)
        genero_combobox.grid(row=2, column=1)
        genero_combobox.set("Seleccionar género")
        
        tk.Label(self.form_frame, text="Año de Publicación:").grid(row=3, column=0, padx=5, pady=5)
        anio_entry = tk.Entry(self.form_frame)
        anio_entry.grid(row=3, column=1)
        
        # Desplegable para autores
        tk.Label(self.form_frame, text="Autor:").grid(row=4, column=0, padx=5, pady=5)
        autores = self.obtener_autores()
        autores_nombres = [f"{autor[1]} {autor[2]}" for autor in autores]
        autor_combobox = ttk.Combobox(self.form_frame, values=autores_nombres)
        autor_combobox.grid(row=4, column=1)
        autor_combobox.set("Seleccionar un autor")
        
        tk.Label(self.form_frame, text="Cantidad Disponible:").grid(row=5, column=0, padx=5, pady=5)
        cantidad_entry = tk.Entry(self.form_frame)
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
                self.clear_frame()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.form_frame, text="Guardar", command=guardar_libro).grid(row=6, column=0, columnspan=2, pady=10)

    def registrar_usuario(self):
        self.clear_frame()
        
        tk.Label(self.form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        nombre_entry = tk.Entry(self.form_frame)
        nombre_entry.grid(row=0, column=1)
        
        tk.Label(self.form_frame, text="Apellido:").grid(row=1, column=0, padx=5, pady=5)
        apellido_entry = tk.Entry(self.form_frame)
        apellido_entry.grid(row=1, column=1)
        
        tk.Label(self.form_frame, text="Tipo de Usuario:").grid(row=2, column=0, padx=5, pady=5)
        tipos_usuario = ["Estudiante", "Profesor"]
        tipo_usuario_combobox = ttk.Combobox(self.form_frame, values=tipos_usuario)
        tipo_usuario_combobox.grid(row=2, column=1)
        tipo_usuario_combobox.set("Seleccionar tipo de usuario")
        
        tk.Label(self.form_frame, text="Dirección:").grid(row=3, column=0, padx=5, pady=5)
        direccion_entry = tk.Entry(self.form_frame)
        direccion_entry.grid(row=3, column=1)
        
        tk.Label(self.form_frame, text="Teléfono:").grid(row=4, column=0, padx=5, pady=5)
        telefono_entry = tk.Entry(self.form_frame)
        telefono_entry.grid(row=4, column=1)
        
        def guardar_usuario():
            usuario = Usuario(
                nombre_entry.get(), apellido_entry.get(), tipo_usuario_combobox.get(),
                direccion_entry.get(), telefono_entry.get()
            )
            usuario.guardar()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.clear_frame()
        
        tk.Button(self.form_frame, text="Guardar", command=guardar_usuario).grid(row=5, column=0, columnspan=2, pady=10)
    
    def obtener_usuarios(self):
        """Función para obtener una lista de usuarios desde la base de datos."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, apellido FROM Usuario")
        usuarios = cursor.fetchall()
        conexion.close()
        return usuarios
    
    def obtener_libros(self):
        """Función para obtener una lista de libros desde la base de datos."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT codigo_ISBN, titulo FROM Libro")
        libros = cursor.fetchall()
        conexion.close()
        return libros
    
    def prestamo_libro(self):
        self.clear_frame()
        
        # Desplegable para usuarios
        tk.Label(self.form_frame, text="Usuario:").grid(row=0, column=1, padx=5, pady=5)
        usuarios = self.obtener_usuarios()
        usuarios_nombres = [f"{usr[1]} {usr[2]}" for usr in usuarios]
        usuario_combobox = ttk.Combobox(self.form_frame, values=usuarios_nombres)
        usuario_combobox.grid(row=0, column=2)
        usuario_combobox.set("Seleccionar un usuario")
        
        # Desplegable para libros
        tk.Label(self.form_frame, text="Libro:").grid(row=1, column=1, padx=5, pady=5)
        libros = self.obtener_libros()
        libros_titulos = [f"{libro[1]}" for libro in libros]
        libro_combobox = ttk.Combobox(self.form_frame, values=libros_titulos)
        libro_combobox.grid(row=1, column=2)
        libro_combobox.set("Seleccionar un libro")
        
        # Etiqueta para "Fecha de Préstamo" con el widget Calendar en vez de un Entry
        tk.Label(self.form_frame, text="Fecha de Préstamo:").grid(row=2, column=0, padx=5, pady=5)
        fecha_prestamo_cal = Calendar(
            self.form_frame,
            selectmode='day',
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day,
            date_pattern="yyyy-mm-dd"
        )
        fecha_prestamo_cal.grid(row=2, column=1, padx=5, pady=5)
        
        # Etiqueta para "Fecha de devolucion" con el widget Calendar en vez de un Entry
        tk.Label(self.form_frame, text="Fecha de devolucion:").grid(row=2, column=2, padx=5, pady=5)
        fecha_devolucion_cal = Calendar(
            self.form_frame,
            selectmode='day',
            date_pattern="yyyy-mm-dd"
        )
        fecha_devolucion_cal.grid(row=2, column=3, padx=5, pady=5)
        
        def guardar_prestamo():
            try:
                # Obtener el ID del usuario seleccionado en el combobox
                usuario_index = usuario_combobox.current()
                if usuario_index == -1:
                    raise ValueError("Seleccione un usuario válido.")
                usuario_id = usuarios[usuario_index][0]  # ID del usuario seleccionado
                
                # Obtener el ID del libro seleccionado en el combobox
                libro_index = libro_combobox.current()
                print(libro_index)
                if libro_index == -1:
                    raise ValueError("Seleccione un libro válido.")
                libro_id = libros[libro_index][0] 
                
                # Obtener la fecha seleccionada del calendario
                fecha_prestamo = fecha_prestamo_cal.get_date()
                fecha_devolucion = fecha_devolucion_cal.get_date()
                
                prestamo = Prestamo(
                    usuario_id,
                    libro_id,
                    fecha_prestamo,
                    fecha_devolucion
                )
                prestamo.guardar()
                messagebox.showinfo("Éxito", "Préstamo registrado correctamente.")
                self.clear_frame()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(self.form_frame, text="Guardar", command=guardar_prestamo).grid(row=3, column=1, columnspan=2, pady=10)

    def obtener_prestamos_sin_devolucion(self):
        """Obtiene una lista de préstamos sin fecha de devolución, incluyendo el nombre del usuario y el título del libro."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT Prestamo.id, Libro.titulo, Usuario.nombre || ' ' || Usuario.apellido AS usuario_nombre
            FROM Prestamo
            JOIN Usuario ON Prestamo.usuario_id = Usuario.id
            JOIN Libro ON Prestamo.codigo_ISBN = Libro.codigo_ISBN
            WHERE Prestamo.fecha_devolucion_real IS NULL
        """)
        prestamos = cursor.fetchall()
        conexion.close()
        return prestamos

    def devolucion_libro(self):
        self.clear_frame()

        # Título
        tk.Label(self.form_frame, text="Devolución de Libro").grid(row=0, column=0, columnspan=2, pady=10)

        # Obtener préstamos sin fecha de devolución
        prestamos = self.obtener_prestamos_sin_devolucion()
        if not prestamos:
            messagebox.showinfo("Información", "No hay préstamos pendientes de devolución.")
            return

        # Crear lista de opciones con el título del libro y nombre del usuario
        prestamos_info = [f"{p[1]} - {p[2]}" for p in prestamos]  # Muestra "Título del libro - Nombre del usuario"
        prestamo_combobox = ttk.Combobox(self.form_frame, values=prestamos_info)
        prestamo_combobox.grid(row=1, column=1)
        prestamo_combobox.set("Seleccionar un préstamo")

        def guardar_devolucion():
            try:
                prestamo_index = prestamo_combobox.current()
                if prestamo_index == -1:
                    raise ValueError("Seleccione un préstamo válido.")
                prestamo_id = prestamos[prestamo_index][0]

                # Actualizar la fecha de devolución en la base de datos con la fecha actual
                fecha_devolucion = datetime.now().strftime('%Y-%m-%d')
                conexion = obtener_conexion()
                cursor = conexion.cursor()
                cursor.execute("""
                    UPDATE Prestamo
                    SET fecha_devolucion_real = ?
                    WHERE id = ?
                """, (fecha_devolucion, prestamo_id))
                conexion.commit()
                conexion.close()
                messagebox.showinfo("Éxito", "Devolución registrada correctamente.")
                self.clear_frame()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.form_frame, text="Guardar Devolución", command=guardar_devolucion).grid(row=2, column=0, columnspan=2, pady=10)

    def consultar_disponibilidad(self):
        """Consulta la disponibilidad de un libro en base al título ingresado."""
        # Etiqueta para el título
        tk.Label(self.form_frame, text="Título:").grid(row=0, column=0, padx=5, pady=5)
        
        # Entrada de texto para el título
        titulo_entry = tk.Entry(self.form_frame)
        titulo_entry.grid(row=0, column=1, padx=5, pady=5)
        
        def mostrar_disponibilidad():
            # Obtener el título ingresado
            titulo = titulo_entry.get().strip()
            
            if not titulo:
                messagebox.showerror("Error", "Por favor ingrese un título.")
                return
            
            # Consultar la disponibilidad
            libro_info = Libro.buscar_por_disponibilidad(titulo)
            
            if libro_info:
                # Mostrar la información del libro
                tk.Label(self.form_frame, text=f"Código ISBN: {libro_info['codigo_ISBN']}").grid(row=1, column=1, padx=5, pady=5)
                tk.Label(self.form_frame, text=f"Título: {libro_info['titulo']}").grid(row=2, column=1, padx=5, pady=5)
                tk.Label(self.form_frame, text=f"Género: {libro_info['genero']}").grid(row=3, column=1, padx=5, pady=5)
                tk.Label(self.form_frame, text=f"Año de Publicación: {libro_info['anio_publicacion']}").grid(row=4, column=1, padx=5, pady=5)
                tk.Label(self.form_frame, text=f"Cantidad Disponible: {libro_info['cantidad_disponible']}").grid(row=5, column=1, padx=5, pady=5)
            else:
                messagebox.showinfo("No Encontrado", "No se encontró un libro con ese título.")
        
        # Botón para consultar la disponibilidad
        tk.Button(self.form_frame, text="Consultar", command=mostrar_disponibilidad).grid(row=0, column=2, padx=5, pady=5)

    def generar_reportes(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.TOP, pady=10)

        # Creación de botones para generar reportes
        tk.Button(button_frame, text="Préstamos vencidos", command=self.mostrar_prestamos_vencidos).grid(row=6, column=0, pady=5)
        tk.Button(button_frame, text="Libros más prestados del último mes", command=self.mostrar_libros_mas_prestados).grid(row=7, column=0, pady=5)
        tk.Button(button_frame, text="Usuarios con más préstamos", command=self.mostrar_usuarios_con_mas_prestamos).grid(row=8, column=0, pady=5)

    def mostrar_prestamos_vencidos(self):
        report = Prestamo.prestamos_vencidos()  # Llamada al método de la clase Prestamo
        self.mostrar_resultado(report)

    def mostrar_libros_mas_prestados(self):
        report = Prestamo.libros_mas_prestados()
        self.mostrar_resultado(report)

    def mostrar_usuarios_con_mas_prestamos(self):
        report = Prestamo.usuarios_con_mas_prestamos()
        self.mostrar_resultado(report)

    def mostrar_resultado(self, resultado):
        # Aquí se muestra la información en un widget de Tkinter
        result_window = tk.Toplevel(self.root)  # Crea una nueva ventana para mostrar los resultados
        result_window.title("Reporte")
        
        result_text = tk.Text(result_window, height=15, width=50)
        result_text.pack(padx=10, pady=10)
        
        result_text.insert(tk.END, resultado)
        result_text.config(state=tk.DISABLED)  # Para que no se pueda editar el texto

    def clear_frame(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()
