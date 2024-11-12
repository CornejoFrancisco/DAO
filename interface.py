import tkinter as tk
from autor import mostrar_autores
from libro import mostrar_libros
from usuario import mostrar_usuarios
from prestamo import mostrar_prestamos
from reportes import mostrar_opciones_reportes
from clase import *

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Biblioteca - Gestión")
        self.root.geometry("800x600")
        
        # Crear botones de acciones
        self.create_buttons()

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.TOP, pady=10)
        
        tk.Button(button_frame, text="Autores", command=lambda: mostrar_autores(self)).pack(pady=10)
        tk.Button(button_frame, text="Libros", command=lambda: mostrar_libros(self)).pack(pady=10)
        tk.Button(button_frame, text="Usuarios", command=lambda: mostrar_usuarios(self)).pack(pady=10)
        tk.Button(button_frame, text="Prestamos", command=lambda: mostrar_prestamos(self)).pack(pady=10)
        tk.Button(button_frame, text="Reportes", command=lambda: mostrar_opciones_reportes(self)).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()
