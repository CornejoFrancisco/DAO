from database import obtener_conexion
from datetime import datetime, timedelta
import locale

def validar_longitud_texto(text, min=0, max=100):
    if min < len(text) < max:
        return True
    else:
        return False

def validar_numeros_positivos(num, min=0):
    try:
        numero = int(num)
        return numero > min
    except ValueError:
        return False
    
def validar_anio_input(anio):
    try:
        a = int(anio)
        if 1900 <= a <= 2024:
            return True
        else:
            return False
    except ValueError:
        return False

def validar_fecha_devolucion(fecha_prestamo, fecha_devolucion):
    fecha_prestamo_obj = datetime.strptime(fecha_prestamo, "%d-%m-%Y")
    fecha_devolucion_obj = datetime.strptime(fecha_devolucion, "%Y-%m-%d")
    
    if fecha_devolucion_obj >= fecha_prestamo_obj:
        return True
    else:
        return False

def obtener_autores():
    """Funcion para obtener una lista de autores desde la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, apellido, nacionalidad FROM Autor")
    autores = cursor.fetchall()
    conexion.close()
    return autores

def obtener_usuarios():
    """Funcion para obtener una lista de usuarios desde la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, apellido, tipo_usuario, direccion, telefono FROM Usuario")
    usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

def obtener_libros():
    """Funcion para obtener una lista de libros con los datos del autor desde la base de datos."""
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
    """Obtiene una lista de prestamos, ordenados por la fecha de devolucion real (null primero, luego los no null)."""
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
            fecha_devolucion_real IS NULL DESC,  -- Primero los prestamos sin devolucion real (NULL)
            fecha_devolucion_estimada ASC       -- Luego por fecha de devolucion estimada (mas cercana primero)
    """)
    prestamos = cursor.fetchall()
    conexion.close()
    return prestamos

def obtener_prestamos_sin_devolucion():
    """Obtiene una lista de prestamos sin fecha de devolucion, incluyendo el nombre del usuario y el titulo del libro."""
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
    """Funcion que cierra la ventana pasada como argumento."""
    ventana.destroy()
    
def prestamos_vencidos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    print(fecha_actual)

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
    conexion.close()
    if prestamos_vencidos:
        encabezado = ["Usuario", "Libro", "Fecha Prestamo", "Dias Vencidos"]
        datos = [(p[0], p[1], p[2], round(p[3])) for p in prestamos_vencidos]  # Calcular los dias vencidos y redondear
        return (encabezado, datos)
    else:
        return (["Usuario", "Libro", "Fecha Prestamo", "Dias Vencidos"], [])
    
def obtener_mes_anterior():
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    hoy = datetime.today()

    primer_dia_mes = hoy.replace(day=1)
    ultimo_mes = primer_dia_mes - timedelta(days=1)

    mes_anterior = ultimo_mes.strftime('%B')

    return mes_anterior

def libros_mas_prestados():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT l.titulo, COUNT(p.codigo_ISBN) AS cantidad, l.genero
        FROM Prestamo p
        JOIN Libro l ON p.codigo_ISBN = l.codigo_ISBN
        WHERE p.fecha_prestamo >= DATE('now', '-1 month')
        GROUP BY l.titulo  -- Agrupar por titulo de libro
        ORDER BY cantidad DESC
    """)
    libros_mas_prestados = cursor.fetchall()
    conexion.close()

    if libros_mas_prestados:
        encabezado = ["Titulo del Libro", "Cantidad de Prestamos", "Genero"]
        resultado = [(l[0], l[1], l[2]) for l in libros_mas_prestados]
        return encabezado, resultado
    else:
        return ["Titulo del Libro", "Cantidad de Prestamos"], "No hay prestamos en el ultimo mes."


def usuarios_con_mas_prestamos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

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

    if usuarios_con_mas_prestamos:
        encabezado = ["Usuario", "Cantidad de Prestamos", "Rol"]
        datos = [(f"{u[0]} {u[1]}", u[2], u[3]) for u in usuarios_con_mas_prestamos]
        return (encabezado, datos)
    else:
        return (["Usuario", "Cantidad de Prestamos", "Rol"], [])
