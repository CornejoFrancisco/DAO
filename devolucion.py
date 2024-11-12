import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from tkcalendar import Calendar 
from database import obtener_conexion
from clase import Libro, Autor, Usuario, Prestamo

def devolucion_libro(self):
    ventana_devolucion = tk.Toplevel(self.root)
    ventana_devolucion.title("Registrar Devolucion Libro")    

    # Titulo
    tk.Label(ventana_devolucion, text="Devolucion de Libro").grid(row=0, column=0, columnspan=2, pady=10)

    # Obtener prestamos sin fecha de devolucion
    prestamos = self.obtener_prestamos_sin_devolucion()
    if not prestamos:
        messagebox.showinfo("Informacion", "No hay prestamos pendientes de devolucion.")
        return

    # Crear lista de opciones con el titulo del libro y nombre del usuario
    prestamos_info = [f"{p[1]} - {p[2]}" for p in prestamos]  # Muestra "Titulo del libro - Nombre del usuario"
    prestamo_combobox = ttk.Combobox(ventana_devolucion, values=prestamos_info, state="readonly")
    prestamo_combobox.grid(row=1, column=1)
    prestamo_combobox.set("Seleccionar un prestamo")

    def guardar_devolucion():
        try:
            prestamo_index = prestamo_combobox.current()
            if prestamo_index == -1:
                raise ValueError("Seleccione un prestamo valido.")
            prestamo_id = prestamos[prestamo_index][0]

            # Actualizar la fecha de devolucion en la base de datos con la fecha actual
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
            messagebox.showinfo("Éxito", "Devolucion registrada correctamente.")
            self.clear_frame()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    tk.Button(ventana_devolucion, text="Guardar Devolucion", command=guardar_devolucion).grid(row=2, column=0, columnspan=2, pady=10)
