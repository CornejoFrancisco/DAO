from database import obtener_conexion
from datetime import datetime, timedelta
import locale

def validar_longitud_isbn(P):
    # Verificar que el texto tenga una longitud mayor o igual a cantMin y menor o igual a cantMax
    longitud = len(P)
    
    if 10 <= longitud <= 13:
        return True
    else:
        return False

def validar_longitud_texto(P):
    # Verificar que el texto tenga una longitud mayor o igual a cantMin y menor o igual a cantMax
    longitud = len(P)
    
    if 0 < longitud <= 50:
        return True
    else:
        return False

def validar_numeros_positivos(P):
    try:
        # Intentar convertir el texto a un número entero
        numero = int(P)
        # Verificar si el número es positivo
        return numero > 0
    except ValueError:
        # Si no se puede convertir el texto a un número entero, retornar False
        return False
    
def validar_anio_input(P):
    try:
        # Comprobar si el valor es numérico
        anio = int(P)
        if 1900 <= anio <= 2024 or P == "":  # Permitimos el valor vacío también
            return True
        else:
            return False
    except ValueError:
        return False  # No es un número, entonces no se permite

def obtener_autores():
    """Función para obtener una lista de autores desde la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, apellido, nacionalidad FROM Autor")
    autores = cursor.fetchall()
    conexion.close()
    return autores

def validar_numeros(P):
    # Verifica si el texto está vacío o contiene solo dígitos
    return P.isdigit()

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
    
def prestamos_vencidos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    print(fecha_actual)

    # Obtener los préstamos cuya fecha de devolución sea menor a la fecha actual
    cursor.execute("""
        SELECT 
            u.nombre || ' ' || u.apellido AS usuario, 
            l.titulo AS libro, 
            p.fecha_prestamo, 
            julianday(?) - julianday(p.fecha_devolucion_estimada) AS dias_vencidos
        FROM Prestamo p
        JOIN Usuario u ON p.id = u.id
        JOIN Libro l ON p.codigo_ISBN = l.codigo_ISBN
        WHERE p.fecha_devolucion_estimada < ? 
        AND p.fecha_devolucion_estimada IS NOT NULL 
        AND p.fecha_devolucion_real IS NULL
    """, (fecha_actual, fecha_actual))

    prestamos_vencidos = cursor.fetchall()

    # Cerrar la conexión
    conexion.close()

    # Si hay resultados, formatearlos como una tupla (encabezado, datos)
    if prestamos_vencidos:
        encabezado = ["Usuario", "Libro", "Fecha Préstamo", "Días Vencidos"]
        datos = [(p[0], p[1], p[2], round(p[3])) for p in prestamos_vencidos]  # Calcular los días vencidos y redondear
        return (encabezado, datos)
    else:
        # Si no hay resultados, devolver un encabezado vacío y una lista vacía
        return (["Usuario", "Libro", "Fecha Préstamo", "Días Vencidos"], [])
    
def obtener_mes_anterior():
    # Establecer la configuración regional a español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    # Obtener la fecha actual
    hoy = datetime.today()

    # Restar un mes a la fecha actual
    primer_dia_mes = hoy.replace(day=1)
    ultimo_mes = primer_dia_mes - timedelta(days=1)

    # Obtener el nombre del mes anterior en español
    mes_anterior = ultimo_mes.strftime('%B')

    return mes_anterior

def libros_mas_prestados():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Obtener los libros más prestados en el último mes, agrupando por título y sumando la cantidad
    cursor.execute("""
        SELECT l.titulo, COUNT(p.codigo_ISBN) AS cantidad, l.genero
        FROM Prestamo p
        JOIN Libro l ON p.codigo_ISBN = l.codigo_ISBN
        WHERE p.fecha_prestamo >= DATE('now', '-1 month')
        GROUP BY l.titulo  -- Agrupar por título de libro
        ORDER BY cantidad DESC
    """)
    libros_mas_prestados = cursor.fetchall()
    conexion.close()

    if libros_mas_prestados:
        # Definir el encabezado
        encabezado = ["Título del Libro", "Cantidad de Préstamos", "Genero"]
        # El resultado contiene los títulos de los libros y la cantidad de préstamos
        resultado = [(l[0], l[1], l[2]) for l in libros_mas_prestados]
        return encabezado, resultado
    else:
        return ["Título del Libro", "Cantidad de Préstamos"], "No hay préstamos en el último mes."


def usuarios_con_mas_prestamos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Obtener los usuarios con más préstamos
    cursor.execute("""
        SELECT u.nombre, u.apellido, COUNT(p.usuario_id) AS cantidad, u.tipo_usuario
        FROM Prestamo p
        JOIN Usuario u ON p.usuario_id = u.id
        GROUP BY p.usuario_id
        ORDER BY cantidad DESC
        LIMIT 5
    """)
    usuarios_con_mas_prestamos = cursor.fetchall()
    conexion.close()

    # Si hay resultados, devolverlos en el formato correcto
    if usuarios_con_mas_prestamos:
        encabezado = ["Usuario", "Cantidad de Préstamos", "Rol"]
        datos = [(f"{u[0]} {u[1]}", u[2], u[3]) for u in usuarios_con_mas_prestamos]
        return (encabezado, datos)
    else:
        # Si no hay resultados, devolver un encabezado vacío y una lista vacía
        return (["Usuario", "Cantidad de Préstamos", "Rol"], [])
