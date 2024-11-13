import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from tkcalendar import Calendar 
from clase import Prestamo
from comun import *

def mostrar_prestamos(self):
    # Ventana para mostrar los prestamos
    ventana_prestamos = tk.Toplevel(self.root)
    ventana_prestamos.title("Mostrar prestamos")
    
    # Hacer que la ventana este al frente
    ventana_prestamos.lift()
    ventana_prestamos.attributes("-topmost", True)
    ventana_prestamos.after(100, lambda: ventana_prestamos.attributes("-topmost", False)) 

    # Crear la grilla para mostrar los prestamos
    columnas = ("Usuario", "Libro", "Fecha Prestamo", "Dias Devolucion")
    tree = ttk.Treeview(ventana_prestamos, columns=columnas, show='headings')
    tree.pack(pady=20)
    
    for col in columnas:
        tree.heading(col, text=col)

    # Obtener la lista de prestamos desde la base de datos
    prestamos = obtener_prestamos_sin_devolucion()
    fecha_hoy = datetime.now().date()
    
    def devolver_libro():
        # Obtener el elemento seleccionado
        selected_item = tree.selection()
        if selected_item:
            item_id = selected_item[0]
            index = tree.index(item_id)
            prestamo_id = prestamos[index][0]
            libro = tree.item(selected_item)['values'][1]
            print(libro)
            
            if messagebox.askyesno("Confirmar devolucion", f"¿Realizar devolucion del libro {libro}?"):
                try:
                    # Actualizar la fecha de devolucion en la base de datos
                    actualizar_fecha_devolucion(prestamo_id, fecha_hoy)
                    messagebox.showinfo("Exito", "El libro ha sido devuelto.")
                    
                    # Refrescar la ventana para mostrar los cambios
                    ventana_prestamos.destroy()
                    mostrar_prestamos(self)
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo registrar la devolucion: {e}")
        else:
            messagebox.showwarning("Seleccion requerida", "Seleccione un libro para devolver.")
    
    # Insertar los datos en la grilla
    for prestamo in prestamos:
        usuario, libro, fecha_prestamo, fecha_devolucion_estimada = prestamo
        
        # Calcular los dias restantes o de atraso
        fecha_devolucion_estimada = datetime.strptime(fecha_devolucion_estimada, '%Y-%m-%d').date()
        dias_diferencia = (fecha_devolucion_estimada - fecha_hoy).days

        if dias_diferencia > 0:
            dias_devolucion = f"{dias_diferencia} dias restantes"
        elif dias_diferencia < 0:
            dias_devolucion = f"{abs(dias_diferencia)} dias atrasado"
        else:
            dias_devolucion = "Hoy es el ultimo dia"

        # Insertar la fila en el Treeview
        tree.insert('', 'end', values=(usuario, libro, fecha_prestamo, dias_devolucion))
        
    # Crear un Frame para los botones y colocarlos uno al lado del otro
    botones_frame = tk.Frame(ventana_prestamos)
    botones_frame.pack(pady=10)

    # Botón para registrar nuevos préstamos (color verde)
    boton_registrar = tk.Button(
        botones_frame, 
        text="Registrar préstamo", 
        command=lambda: registrar_prestamo(self, ventana_prestamos),
        bg="green", 
        fg="white"
    )
    boton_registrar.pack(side="left", padx=5)

    # Botón para devolver el libro seleccionado (color azul)
    boton_devolver = tk.Button(
        botones_frame, 
        text="Devolver libro", 
        command=devolver_libro,
        bg="blue", 
        fg="white"
    )
    boton_devolver.pack(side="left", padx=5)

def registrar_prestamo(self, ventana_prestamos, isbn=None, titulo=None):
    ventana_prestamo = tk.Toplevel(self.root)
    ventana_prestamo.title("Registrar Prestamo de Libro")
    
    # Desplegable para usuarios
    tk.Label(ventana_prestamo, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
    usuarios = obtener_usuarios()
    usuarios_nombres = [f"{usr[1]} {usr[2]}" for usr in usuarios]
    usuario_combobox = ttk.Combobox(ventana_prestamo, values=usuarios_nombres, state="readonly")
    usuario_combobox.grid(row=0, column=1)
    usuario_combobox.set("Seleccionar un usuario")
    
    # Desplegable para libros
    tk.Label(ventana_prestamo, text="Libro:").grid(row=1, column=0, padx=5, pady=5)
    if isbn and titulo:
        libros_titulos = [f"{titulo}"]
        libros = [(isbn, titulo)]
        combobox_state = "disabled"
    else:
        libros = obtener_libros_con_ejemplares()
        libros_titulos = [f"{libro[1]}" for libro in libros]
        combobox_state = "readonly"
    
    libro_combobox = ttk.Combobox(ventana_prestamo, values=libros_titulos, state=combobox_state)
    libro_combobox.grid(row=1, column=1)
    libro_combobox.set("Seleccionar un libro" if not isbn else libros_titulos[0])
    
    # Campo de Fecha de Prestamo
    tk.Label(ventana_prestamo, text="Fecha de Prestamo:").grid(row=2, column=0, padx=5, pady=5)
    fecha_prestamo_text = tk.Entry(ventana_prestamo)
    fecha_prestamo_text.insert(0, datetime.now().strftime("%d-%m-%Y"))
    fecha_prestamo_text.config(state="readonly")
    fecha_prestamo_text.grid(row=2, column=1, padx=5, pady=5)

    # Etiqueta para "Fecha de devolucion" con el widget Calendar
    tk.Label(ventana_prestamo, text="Fecha de devolucion:").grid(row=3, column=0, padx=5, pady=5)
    fecha_devolucion_cal = Calendar(
        ventana_prestamo,
        selectmode='day',
        date_pattern="yyyy-mm-dd"
    )
    fecha_devolucion_cal.grid(row=3, column=1, padx=5, pady=5)
    
    def guardar_prestamo():
        try:
            # Validaciones
            if usuario_combobox.get() == "Seleccionar un usuario":
                raise ValueError("Debe seleccionar un usuario")
            
            if libro_combobox.get() == "Seleccionar un libro":
                raise ValueError("Debe seleccionar un libro")
            
            if not validar_fecha_devolucion(fecha_prestamo_text.get(), fecha_devolucion_cal.get_date()):
                raise ValueError("La fecha de devolucion debe ser mayor o igual al dia de hoy")
            
            usuario_index = usuario_combobox.current()
            if usuario_index == -1:
                raise ValueError("Seleccione un usuario valido.")
            usuario_id = usuarios[usuario_index][0]

            libro_index = libro_combobox.current()
            if libro_index == -1:
                raise ValueError("Seleccione un libro valido.")
            libro_id = libros[libro_index][0] 

            fecha_prestamo = datetime.strptime(fecha_prestamo_text.get(), "%d-%m-%Y").strftime("%Y-%m-%d")
            fecha_devolucion = fecha_devolucion_cal.get_date()

            prestamo = Prestamo(
                usuario_id,
                libro_id,
                fecha_prestamo,
                fecha_devolucion
            )
            prestamo.guardar()
            messagebox.showinfo("Exito", "Prestamo registrado correctamente.")
            cerrarVentana(ventana_prestamos)
            cerrarVentana(ventana_prestamo)

            # Actualizar la lista de prestamos despues de registrar uno nuevo
            mostrar_prestamos(self)

        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    tk.Button(ventana_prestamo, text="Guardar", command=guardar_prestamo).grid(row=4, column=0, columnspan=2, pady=10)
    tk.Button(ventana_prestamo, text="Cancelar", command=lambda: cerrarVentana(ventana_prestamo)).grid(row=4, column=1, columnspan=2, pady=10)
