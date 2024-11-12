from database import obtener_conexion

def obtener_autores():
    """Función para obtener una lista de autores desde la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, apellido, nacionalidad FROM Autor")
    autores = cursor.fetchall()
    conexion.close()
    return autores

def validar_longitud_texto(texto, cantMin=0, cantMax=100):
    # Verificar que el texto tenga una longitud mayor o igual a cantMin y menor o igual a cantMax
    longitud = len(texto)
    
    if cantMin <= longitud <= cantMax:
        return True
    else:
        return False

def validar_numeros_positivos(texto):
    try:
        # Intentar convertir el texto a un número entero
        numero = int(texto)
        # Verificar si el número es positivo
        return numero > 0
    except ValueError:
        # Si no se puede convertir el texto a un número entero, retornar False
        return False

def obtener_usuarios():
    """Función para obtener una lista de usuarios desde la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, apellido, tipo_usuario, direccion, telefono FROM Usuario")
    usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

def obtener_libros():
    """Función para obtener una lista de libros con los datos del autor desde la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT 
            L.codigo_ISBN, 
            L.titulo, 
            L.genero, 
            L.anio_publicacion, 
            A.nombre AS nombre_autor, 
            A.apellido AS apellido_autor, 
            L.cantidad_disponible 
        FROM 
            Libro L
        INNER JOIN 
            Autor A ON L.autor_id = A.id
    """)
    libros = cursor.fetchall()
    conexion.close()
    return libros

def obtener_prestamos():
    """Obtiene una lista de préstamos, ordenados por la fecha de devolución real (null primero, luego los no null)."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT 
            Usuario.nombre || ' ' || Usuario.apellido AS usuario_nombre, 
            Libro.titulo, 
            fecha_prestamo, 
            fecha_devolucion_estimada
        FROM 
            Prestamo
        JOIN 
            Usuario ON Prestamo.usuario_id = Usuario.id
        JOIN 
            Libro ON Prestamo.codigo_ISBN = Libro.codigo_ISBN
        ORDER BY 
            fecha_devolucion_real IS NULL DESC,  -- Primero los préstamos sin devolución real (NULL)
            fecha_devolucion_estimada ASC       -- Luego por fecha de devolución estimada (más cercana primero)
    """)
    prestamos = cursor.fetchall()
    conexion.close()
    return prestamos

def obtener_prestamos_sin_devolucion():
    """Obtiene una lista de préstamos sin fecha de devolución, incluyendo el nombre del usuario y el título del libro."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT 
            Usuario.nombre || ' ' || Usuario.apellido AS usuario_nombre, 
            Libro.titulo, 
            fecha_prestamo, 
            fecha_devolucion_estimada
        FROM Prestamo
        JOIN Usuario ON Prestamo.usuario_id = Usuario.id
        JOIN Libro ON Prestamo.codigo_ISBN = Libro.codigo_ISBN
        WHERE Prestamo.fecha_devolucion_real IS NULL
    """)
    prestamos = cursor.fetchall()
    conexion.close()
    return prestamos

def actualizar_fecha_devolucion(prestamo_id, fecha_hoy):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE Prestamo
        SET fecha_devolucion_real = ?
        WHERE id = ?
    """, (fecha_hoy, prestamo_id))
    conexion.commit()
    conexion.close()

def cerrarVentana(ventana):
    """Función que cierra la ventana pasada como argumento."""
    ventana.destroy()
