
import sqlite3

# Crear y conectar a la base de datos
def obtener_conexion():
    return sqlite3.connect("biblioteca.db")

# Crear las tablas si no existen
def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Autor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            nacionalidad TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Libro (
            codigo_ISBN TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            genero TEXT NOT NULL,
            anio_publicacion INTEGER NOT NULL,
            autor_id INTEGER NOT NULL,
            cantidad_disponible INTEGER NOT NULL,
            FOREIGN KEY (autor_id) REFERENCES Autor (id)
        )
    """)
    
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            tipo_usuario TEXT NOT NULL,
            direccion TEXT NOT NULL,
            telefono INTEGER NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Prestamo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            codigo_ISBN TEXT NOT NULL,
            fecha_prestamo TEXT NOT NULL,
            fecha_devolucion_estimada TEXT,
            fecha_devolucion_real TEXT,
            FOREIGN KEY (usuario_id) REFERENCES Usuario (id),
            FOREIGN KEY (codigo_ISBN) REFERENCES Libro (codigo_ISBN)
        )
    """)

    conexion.commit()
    conexion.close()

