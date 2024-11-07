from database import crear_tablas

from clase import Autor, Libro, Usuario, Prestamo
import datetime

def registrar_autor():
    """Registrar un nuevo autor en el sistema."""
    nombre = input("Ingrese el nombre del autor: ")
    apellido = input("Ingrese el apellido del autor: ")
    nacionalidad = input("Ingrese la nacionalidad del autor: ")

    nuevo_autor = Autor(nombre=nombre, apellido=apellido, nacionalidad=nacionalidad)
    nuevo_autor.guardar()  # Asumiendo que tienes un método `guardar` en la clase Autor

    print(f"Autor '{nombre} {apellido}' registrado exitosamente.")

def registrar_libro():
    """Registrar un nuevo libro y asignarlo a un autor."""
    codigo_ISBN = input("Ingrese el código ISBN del libro: ")
    titulo = input("Ingrese el título del libro: ")
    genero = input("Ingrese el género del libro: ")
    anio_publicacion = int(input("Ingrese el año de publicación: "))
    autor_id = int(input("Ingrese el ID del autor: "))
    cantidad_disponible = int(input("Ingrese la cantidad disponible: "))

    nuevo_libro = Libro(codigo_ISBN, titulo, genero, anio_publicacion, autor_id, cantidad_disponible)
    
    try:
        nuevo_libro.guardar()  # Asumiendo que tienes un método `guardar` en la clase Libro
        print(f"Libro '{titulo}' registrado exitosamente.")
    except ValueError as e:
        print(e)  # Mostrar error si el autor no existe

def registrar_usuario():
    """Registrar un nuevo usuario en el sistema."""
    nombre = input("Ingrese el nombre del usuario: ")
    
    apellido = input("Ingrese el apellido del usuario: ")
    tipo_usuario = input("Ingrese el tipo de usuario: ")
    direccion = input("Ingrese la dirección del usuario: ")
    telefono = input("Ingrese el teléfono del usuario: ")

    if Usuario.existe_telefono(telefono):
        print(f"Error: El usuario con teléfono '{telefono}' ya está registrado.")
    else:
        nuevo_usuario = Usuario(nombre=nombre, apellido=apellido, tipo_usuario=tipo_usuario, direccion=direccion, telefono=telefono)
        nuevo_usuario.guardar()  # Asumiendo que tienes un método `guardar` en la clase Usuario
        print(f"Usuario '{nombre}' registrado exitosamente.")

def prestar_libro():
    """Registrar el préstamo de un libro a un usuario."""
    nombre = input("Ingrese el nombre del libro: ")
    usuario_id = int(input("Ingrese el ID del usuario: "))
    fecha_prestamo = datetime.datetime.now().strftime("%Y-%m-%d")
    fecha_devolucion = None
    

    nuevo_prestamo = Prestamo(codigo_ISBN=nombre, usuario_id=usuario_id, fecha_prestamo=fecha_prestamo)
    nuevo_prestamo.guardar()  # Asumiendo que tienes un método `guardar` en la clase Prestamo

    print(f"Libro '{nombre}' prestado al usuario con ID '{usuario_id}'.")

def devolver_libro():
    """Registrar la devolución de un libro."""
    libro = str(input("Ingrese nombre del libro: "))
    usuario_id = int(input("Ingrese el ID del usuario: "))

    # Aquí puedes incluir lógica para verificar el estado del libro antes de devolverlo

    prestamo = Prestamo.buscar_prestamo(usuario_id, libro)  # Asumiendo que tienes un método para buscar préstamos
    print("prestamo", prestamo)
    if prestamo:
        Prestamo.registrar_devolucion(usuario_id, libro)  # Asumiendo que tienes un método `registrar_devolucion`
        print(f"Libro con nombre '{libro}' devuelto exitosamente.")
    else:
        print("No se encontró un préstamo para este libro y usuario.")

def consultar_disponibilidad():
    """Consultar la disponibilidad de un libro."""
    titulo = input("Ingrese el nombre del libro: ")
    cantidad_disponible = Libro.buscar_por_disponibliidad(titulo)  # Asumiendo que tienes un método para buscar libros

    if cantidad_disponible is not None:
        print(f"Disponibilidad el libro:  '{titulo}': {cantidad_disponible[1]} copias disponibles.")
    else:
        print("Libro no encontrado.")

def main():
    crear_tablas()  # Crear tablas si no existen

    while True:
        print("\nOperaciones:")
        print("1. Registro de Autores")
        print("2. Registro de Libros")
        print("3. Registro de Usuarios")
        print("4. Préstamo de Libros")
        print("5. Devolución de Libros")
        print("6. Consulta de Disponibilidad")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_autor()
        elif opcion == "2":
            registrar_libro()
        elif opcion == "3":
            registrar_usuario()
        elif opcion == "4":
            prestar_libro()
        elif opcion == "5":
            devolver_libro()
        elif opcion == "6":
            consultar_disponibilidad()
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
