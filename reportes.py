import tkinter as tk
from clase import Prestamo
from comun import *

def mostrar_opciones_reportes(self):
    # Crear una nueva ventana para los reportes
    ventana_reportes = tk.Toplevel(self.root)
    ventana_reportes.title("Generar Reportes")
    
    tk.Button(ventana_reportes, text="Préstamos vencidos", command=lambda: mostrar_prestamos_vencidos(self)).pack(pady=10)
    tk.Button(ventana_reportes, text="Libros más prestados del último mes", command=lambda: mostrar_libros_mas_prestados(self)).pack(pady=10)
    tk.Button(ventana_reportes, text="Usuarios con más préstamos", command=lambda: mostrar_usuarios_con_mas_prestamos(self)).pack(pady=10)
    tk.Button(ventana_reportes, text="Volver", command=lambda: cerrarVentana(ventana_reportes)).pack(pady=10)


def mostrar_prestamos_vencidos(self):
    report = Prestamo.prestamos_vencidos()
    mostrar_resultado(self, report)

def mostrar_libros_mas_prestados(self):
    report = Prestamo.libros_mas_prestados()
    mostrar_resultado(self, report)

def mostrar_usuarios_con_mas_prestamos(self):
    report = Prestamo.usuarios_con_mas_prestamos()
    mostrar_resultado(self, report)

def mostrar_resultado(self, resultado):
    # Aquí se muestra la información en un widget de Tkinter
    result_window = tk.Toplevel(self.root)  # Crea una nueva ventana para mostrar los resultados
    result_window.title("Reporte")
    
    result_text = tk.Text(result_window, height=15, width=50)
    result_text.pack(padx=10, pady=10)
    
    result_text.insert(tk.END, resultado)
    result_text.config(state=tk.DISABLED)  # Para que no se pueda editar el texto