import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from tkcalendar import Calendar 
from database import obtener_conexion
from clase import Libro, Autor, Usuario, Prestamo

def devolucion_libro(self):
    ventana_devolucion = tk.Toplevel(self.root)
    ventana_devolucion.title("Registrar Devolucion Libro")    

    # Título
    tk.Label(ventana_devolucion, text="Devolución de Libro").grid(row=0, column=0, columnspan=2, pady=10)

    # Obtener préstamos sin fecha de devolución
    prestamos = self.obtener_prestamos_sin_devolucion()
    if not prestamos:
        messagebox.showinfo("Información", "No hay préstamos pendientes de devolución.")
        return

    # Crear lista de opciones con el título del libro y nombre del usuario
    prestamos_info = [f"{p[1]} - {p[2]}" for p in prestamos]  # Muestra "Título del libro - Nombre del usuario"
    prestamo_combobox = ttk.Combobox(ventana_devolucion, values=prestamos_info, state="readonly")
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

    tk.Button(ventana_devolucion, text="Guardar Devolución", command=guardar_devolucion).grid(row=2, column=0, columnspan=2, pady=10)
