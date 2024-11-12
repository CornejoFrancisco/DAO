import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from tkcalendar import Calendar 
from clase import Prestamo
from comun import *

def mostrar_prestamos(self):
    # Ventana para mostrar los préstamos
    ventana_usuario = tk.Toplevel(self.root)
    ventana_usuario.title("Mostrar préstamos")

    # Crear la grilla (Treeview) para mostrar los préstamos
    columnas = ("Usuario", "Libro", "Fecha Préstamo", "Días Devolución")
    tree = ttk.Treeview(ventana_usuario, columns=columnas, show='headings')
    tree.pack(pady=20)
    
    # Definir las columnas
    for col in columnas:
        tree.heading(col, text=col)

    # Obtener la lista de préstamos desde la base de datos
    prestamos = obtener_prestamos_sin_devolucion()
    fecha_hoy = datetime.now().date()
    
    def devolver_libro(prestamo_id):
        # Función para actualizar la fecha de devolución real en la base de datos
        try:
            # Actualiza la fecha de devolución en la base de datos (implementa esta función en tu sistema)
            actualizar_fecha_devolucion(prestamo_id, fecha_hoy)
            messagebox.showinfo("Éxito", "El libro ha sido devuelto.")
            # Refrescar la ventana para mostrar los cambios
            ventana_usuario.destroy()
            mostrar_prestamos(self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la devolución: {e}")

    # Insertar los datos en la grilla
    for prestamo in prestamos:
        usuario, libro, fecha_prestamo, fecha_devolucion_estimada = prestamo
        
        # Calcular los días restantes o de atraso
        fecha_devolucion_estimada = datetime.strptime(fecha_devolucion_estimada, '%Y-%m-%d').date()
        dias_diferencia = (fecha_devolucion_estimada - fecha_hoy).days

        if dias_diferencia > 0:
            dias_devolucion = f"{dias_diferencia} días restantes"
        elif dias_diferencia < 0:
            dias_devolucion = f"{abs(dias_diferencia)} días atrasado"
        else:
            dias_devolucion = "Hoy es el último día"

        # Insertar la fila en el Treeview sin el botón
        tree.insert('', 'end', values=(usuario, libro, fecha_prestamo, dias_devolucion))
        
    # Botón para registrar nuevos préstamos
    tk.Button(ventana_usuario, text="Registrar préstamo", command=lambda: registrar_prestamo(self)).pack(pady=10)

    # Función para manejar el doble clic en una fila
    def on_row_double_click(event):
        # Obtener el elemento seleccionado
        item_id = tree.selection()[0]
        index = tree.index(item_id)
        prestamo_id = prestamos[index][0]  # Suponiendo que el ID del préstamo está en la primera posición de `prestamos`

        # Confirmar la devolución
        if messagebox.askyesno("Confirmar devolución", "¿Estás seguro de devolver este libro?"):
            devolver_libro(prestamo_id)

    # Asociar el evento de doble clic con la función
    tree.bind("<Double-1>", on_row_double_click)

def registrar_prestamo(self):
    ventana_prestamo = tk.Toplevel(self.root)
    ventana_prestamo.title("Registrar Préstamos Libro")    
    
    # Desplegable para usuarios
    tk.Label(ventana_prestamo, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
    usuarios = obtener_usuarios()
    usuarios_nombres = [f"{usr[1]} {usr[2]}" for usr in usuarios]
    usuario_combobox = ttk.Combobox(ventana_prestamo, values=usuarios_nombres, state="readonly")
    usuario_combobox.grid(row=0, column=1)
    usuario_combobox.set("Seleccionar un usuario")
    
    # Desplegable para libros
    tk.Label(ventana_prestamo, text="Libro:").grid(row=1, column=0, padx=5, pady=5)
    libros = obtener_libros()
    libros_titulos = [f"{libro[1]}" for libro in libros]
    libro_combobox = ttk.Combobox(ventana_prestamo, values=libros_titulos, state="readonly")
    libro_combobox.grid(row=1, column=1)
    libro_combobox.set("Seleccionar un libro")
    
    # Campo de texto para la "Fecha de Préstamo" con la fecha de hoy y deshabilitado
    tk.Label(ventana_prestamo, text="Fecha de Préstamo:").grid(row=2, column=0, padx=5, pady=5)
    fecha_prestamo_text = tk.Entry(ventana_prestamo)
    fecha_prestamo_text.insert(0, datetime.now().strftime("%d-%m-%Y"))  # Establece la fecha de hoy
    fecha_prestamo_text.config(state="readonly")  # Ahora cambia el estado a readonly
    fecha_prestamo_text.grid(row=2, column=1, padx=5, pady=5)

    # Etiqueta para "Fecha de devolución" con el widget Calendar
    tk.Label(ventana_prestamo, text="Fecha de devolución:").grid(row=3, column=0, padx=5, pady=5)
    fecha_devolucion_cal = Calendar(
        ventana_prestamo,
        selectmode='day',
        date_pattern="yyyy-mm-dd"
    )
    fecha_devolucion_cal.grid(row=3, column=1, padx=5, pady=5)
    
    def guardar_prestamo():
        try:
            # Obtener el ID del usuario seleccionado en el combobox
            usuario_index = usuario_combobox.current()
            if usuario_index == -1:
                raise ValueError("Seleccione un usuario válido.")
            usuario_id = usuarios[usuario_index][0]  # ID del usuario seleccionado
            
            # Obtener el ID del libro seleccionado en el combobox
            libro_index = libro_combobox.current()
            if libro_index == -1:
                raise ValueError("Seleccione un libro válido.")
            libro_id = libros[libro_index][0] 
            
            # Obtener la fecha de préstamo (de la entrada de texto) y la fecha de devolución
            fecha_prestamo = fecha_prestamo_text.get()
            fecha_devolucion = fecha_devolucion_cal.get_date()
            
            prestamo = Prestamo(
                usuario_id,
                libro_id,
                fecha_prestamo,
                fecha_devolucion
            )
            prestamo.guardar()
            messagebox.showinfo("Éxito", "Préstamo registrado correctamente.")
            cerrarVentana(ventana_prestamo)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    tk.Button(ventana_prestamo, text="Guardar", command=guardar_prestamo).grid(row=4, column=0, columnspan=2, pady=10)
    tk.Button(ventana_prestamo, text="Cancelar", command=lambda: cerrarVentana(ventana_prestamo)).grid(row=4, column=1, columnspan=2, pady=10)
