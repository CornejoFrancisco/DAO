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
        self.root.geometry("600x600")
        self.root.minsize(600, 600)
        self.root.config(bg="#f0f0f0")  # Fondo claro

        # Crear título
        self.create_title()

        # Crear botones de acciones
        self.create_buttons()

    def create_title(self):
        title_label = tk.Label(self.root, text="Gestión de Biblioteca", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333")
        title_label.pack(side=tk.TOP, pady=20)

    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(side=tk.TOP, pady=10, padx=20)

        # Configuración de estilo de los botones
        button_style = {
            "bg": "#4CAF50",             # Fondo verde
            "fg": "white",               # Texto blanco
            "font": ("Helvetica", 12, "bold"),  # Fuente del texto
            "width": 20,                 # Ancho del botón
            "height": 2,                 # Alto del botón
            "relief": "raised",          # Efecto 3D
            "bd": 3                      # Grosor del borde
        }

        # Crear botones con el estilo definido
        tk.Button(button_frame, text="Autores", command=lambda: mostrar_autores(self), **button_style).pack(pady=10)
        tk.Button(button_frame, text="Libros", command=lambda: mostrar_libros(self), **button_style).pack(pady=10)
        tk.Button(button_frame, text="Usuarios", command=lambda: mostrar_usuarios(self), **button_style).pack(pady=10)
        tk.Button(button_frame, text="Préstamos", command=lambda: mostrar_prestamos(self), **button_style).pack(pady=10)
        tk.Button(button_frame, text="Reportes", command=lambda: mostrar_opciones_reportes(self), **button_style).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()
