from database import obtener_conexion
from database import crear_tablas
import datetime

class Libro:
    def __init__(self, codigo_ISBN, titulo, genero, anio_publicacion, autor_id, cantidad_disponible):
        self.codigo_ISBN = codigo_ISBN
        self.titulo = titulo
        self.genero = genero
        self.anio_publicacion = anio_publicacion
        self.autor_id = autor_id
        self.cantidad_disponible = cantidad_disponible
    
    def verificar_autor_existe(self):
        """Verifica si el autor con el autor_id existe en la base de datos."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT id FROM Autor WHERE id = ?", (self.autor_id,))
        autor = cursor.fetchone()  # Retorna None si no encuentra ningún autor

        conexion.close()
        return autor is not None
    
    def buscar_por_disponibliidad(titulo):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT cantidad_disponible FROM Libro WHERE titulo = ?", (titulo,))
        
        libro = cursor.fetchone()
        
        if libro:
            cantidad = libro[0]
        conexion.close()
        return cantidad is not None
    
    def guardar(self):
        if not self.verificar_autor_existe():
            raise ValueError(f"No se encontró un autor con ID {self.autor_id}")

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO Libro (codigo_ISBN, titulo, genero, anio_publicacion, autor_id, cantidad_disponible) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (self.codigo_ISBN, self.titulo, self.genero, self.anio_publicacion, self.autor_id, self.cantidad_disponible)
        )

        conexion.commit()
        conexion.close()
        print(f"Libro '{self.titulo}' guardado exitosamente.")

class Autor:
    def __init__(self, nombre, apellido, nacionalidad):
        
        self.nombre = nombre
        self.apellido = apellido
        self.nacionalidad = nacionalidad
    
    
    def guardar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO Autor (nombre, apellido, nacionalidad) VALUES (?, ?, ?)",
            (self.nombre, self.apellido, self.nacionalidad)
        )
        conexion.commit()
        conexion.close()

class Usuario:
    def __init__(self, nombre, apellido, tipo_usuario, direccion, telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.tipo_usuario = tipo_usuario
        self.direccion = direccion 
        self.telefono = telefono
        
    @classmethod
    def existe_telefono(cls, telefono):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM Usuario WHERE telefono = ?", (telefono,))
        usuario = cursor.fetchone()
        conexion.close()
        
        return usuario is not None        

    def guardar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO Usuario (nombre, apellido, tipo_usuario, direccion, telefono) VALUES (?, ?, ?, ?, ?)",
            (self.nombre, self.apellido, self.tipo_usuario,self.direccion, self.telefono)
        )
        conexion.commit()
        conexion.close()
        
class Prestamo:
    def __init__(self, usuario_id, libro, fecha_prestamo):
        self.usuario_id = usuario_id
        self.libro = libro
        self.fecha_prestamo = fecha_prestamo
        
    
    def verificar_usuario_existe(self):
        """Verifica si el usuario con el autor_id existe en la base de datos."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT id FROM Usuario WHERE id = ?", (self.usuario_id,))
        autor = cursor.fetchone()  # Retorna None si no encuentra ningún autor

        conexion.close()
        return autor is not None
    
    def registrar_devolucion(usuario_id, libro):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")

        cursor.execute(
            """
            UPDATE Prestamo
            SET fecha_devolucion = ?
            WHERE usuario_id = ? AND nombre_libro = ? AND fecha_devolucion IS NULL
            """,
            (fecha_actual, usuario_id, libro)  # Asegúrate de pasar los valores correctos
        )

        conexion.commit()
        conexion.close()
        print(f"Devolución registrada: Libro '{libro}' devuelto por el usuario con ID {usuario_id}.")
    
    @staticmethod
    def buscar_prestamo(usuario_id, nombre_libro):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        print(usuario_id, nombre_libro)
            # Realiza un JOIN para obtener los préstamos basados en el nombre del libro
        cursor.execute(
        """
        SELECT P.* 
        FROM Prestamo P
        WHERE P.usuario_id = ? AND P.nombre_libro = ?
        """,
        (usuario_id, nombre_libro)
        )
        prestamo = cursor.fetchone()
        print(prestamo)
        conexion.close()
        return prestamo is not None
    
    def guardar(self):
        # Verificar si el usuario existe en la base de datos
        if not self.verificar_usuario_existe():
            raise ValueError(f"No se encontró un usuario con ID {self.usuario_id}")

        # Verificar disponibilidad del libro
        with obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT cantidad_disponible FROM Libro WHERE titulo = ?", (self.libro,))
            libro = cursor.fetchone()

            if not libro:
                raise ValueError(f"No se encontró el libro '{self.libro}' en la base de datos.")

            cantidad_disponible = libro[0]

            if cantidad_disponible <= 0:
                raise ValueError(f"No hay ejemplares disponibles del libro '{self.libro}'.")

            # Disminuir en 1 la cantidad disponible
            cursor.execute(
                "UPDATE Libro SET cantidad_disponible = cantidad_disponible - 1 WHERE titulo = ?",
                (self.libro,),
            )

            # Registrar el préstamo
            cursor.execute(
                "INSERT INTO Prestamo (usuario_id, nombre_libro, fecha_prestamo, fecha_devolucion) "
                "VALUES (?, ?, ?, ?)",
                (self.usuario_id, self.libro, self.fecha_prestamo, None),
            )

            # Los cambios se guardan automáticamente al salir del bloque 'with'

        print(f"Préstamo registrado: Libro '{self.libro}' prestado al usuario con ID {self.usuario_id}.")
