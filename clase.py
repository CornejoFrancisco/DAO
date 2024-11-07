from database import obtener_conexion
from database import crear_tablas
import datetime
import unicodedata

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
    
    def buscar_por_disponibilidad(titulo):
        """Busca un libro por su título sin distinguir entre mayúsculas, minúsculas y acentos."""
        # Normalizamos el título para eliminar acentos y pasarlo a minúsculas
        titulo_normalizado = unicodedata.normalize('NFKD', titulo).encode('ASCII', 'ignore').decode('ASCII').lower()

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT codigo_ISBN, titulo, genero, anio_publicacion, cantidad_disponible 
            FROM Libro 
            WHERE LOWER(titulo) = ?
        """, (titulo_normalizado,))
        
        libro = cursor.fetchone()
        
        conexion.close()
        
        if libro:
            return {
                'codigo_ISBN': libro[0],
                'titulo': libro[1],
                'genero': libro[2],
                'anio_publicacion': libro[3],
                'cantidad_disponible': libro[4]
            }
        else:
            return None
    
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
    def __init__(self, usuario_id, codigo_ISBN, fecha_prestamo, fecha_devolucion_estimada):
        self.usuario_id = usuario_id
        self.codigo_ISBN = codigo_ISBN
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion_estimada = fecha_devolucion_estimada
    
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
            SET fecha_devolucion_real = ?
            WHERE usuario_id = ? AND nombre_libro = ? AND fecha_devolucion_real IS NULL
            """,
            (fecha_actual, usuario_id, libro)  # Asegúrate de pasar los valores correctos
        )

        conexion.commit()
        conexion.close()
    
    @staticmethod
    def buscar_prestamo(usuario_id, codigo_ISBN):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        # Realiza un JOIN para obtener los préstamos basados en el nombre del libro
        cursor.execute(
        """
        SELECT P.* 
        FROM Prestamo P
        WHERE P.usuario_id = ? AND P.codigo_ISBN = ?
        """,
        (usuario_id, codigo_ISBN)
        )
        prestamo = cursor.fetchone()
        conexion.close()
        return prestamo is not None
    
    def guardar(self):
        # Verificar si el usuario existe en la base de datos
        if not self.verificar_usuario_existe():
            raise ValueError(f"No se encontró un usuario con ID {self.usuario_id}")

        # Verificar disponibilidad del libro
        with obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT cantidad_disponible FROM Libro WHERE codigo_ISBN = ?", (self.codigo_ISBN,))
            libro = cursor.fetchone()

            if not libro:
                raise ValueError(f"No se encontró el libro '{self.codigo_ISBN}' en la base de datos.")

            cantidad_disponible = libro[0]

            if cantidad_disponible <= 0:
                raise ValueError(f"No hay ejemplares disponibles del libro '{self.codigo_ISBN}'.")

            # Disminuir en 1 la cantidad disponible
            cursor.execute(
                "UPDATE Libro SET cantidad_disponible = cantidad_disponible - 1 WHERE codigo_ISBN = ?",
                (self.codigo_ISBN,),
            )

            # Registrar el préstamo
            cursor.execute(
                "INSERT INTO Prestamo (usuario_id, codigo_ISBN, fecha_prestamo, fecha_devolucion_estimada, fecha_devolucion_real) "
                "VALUES (?, ?, ?, ?, ?)",
                (self.usuario_id, self.codigo_ISBN, self.fecha_prestamo, self.fecha_devolucion_estimada, None),
            )

            # Los cambios se guardan automáticamente al salir del bloque 'with'
        
    @staticmethod
    def prestamos_vencidos():
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Obtener los préstamos cuya fecha de devolución sea menor a la fecha actual
        cursor.execute("""
            SELECT p.id, p.usuario_id, p.codigo_ISBN, p.fecha_prestamo, p.fecha_devolucion_estimada
            FROM Prestamo p
            WHERE p.fecha_devolucion_estimada < DATE('now') AND p.fecha_devolucion_estimada IS NOT NULL
        """)
        prestamos_vencidos = cursor.fetchall()
        conexion.close()

        if prestamos_vencidos:
            return "\n".join([f"ID: {p[0]}, Usuario ID: {p[1]}, ISBN: {p[2]}, Fecha Préstamo: {p[3]}, Fecha Devolución: {p[4]}" for p in prestamos_vencidos])
        else:
            return "No hay préstamos vencidos."
    
    @staticmethod
    def libros_mas_prestados():
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Obtener los libros más prestados en el último mes
        cursor.execute("""
            SELECT l.titulo, COUNT(p.codigo_ISBN) AS cantidad
            FROM Prestamo p
            JOIN Libro l ON p.codigo_ISBN = l.codigo_ISBN
            WHERE p.fecha_prestamo >= DATE('now', '-1 month')
            GROUP BY l.codigo_ISBN
            ORDER BY cantidad DESC
        """)
        libros_mas_prestados = cursor.fetchall()
        conexion.close()

        if libros_mas_prestados:
            return "\n".join([f"Libro: {l[0]}, Cantidad: {l[1]}" for l in libros_mas_prestados])
        else:
            return "No hay préstamos en el último mes."
    
    @staticmethod
    def usuarios_con_mas_prestamos():
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Obtener los usuarios con más préstamos
        cursor.execute("""
            SELECT u.nombre, u.apellido, COUNT(p.usuario_id) AS cantidad
            FROM Prestamo p
            JOIN Usuario u ON p.usuario_id = u.id
            GROUP BY p.usuario_id
            ORDER BY cantidad DESC
        """)
        usuarios_con_mas_prestamos = cursor.fetchall()
        conexion.close()

        if usuarios_con_mas_prestamos:
            return "\n".join([f"Usuario: {u[0]} {u[1]}, Préstamos: {u[2]}" for u in usuarios_con_mas_prestamos])
        else:
            return "No hay usuarios con préstamos registrados."
