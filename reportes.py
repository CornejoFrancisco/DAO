import matplotlib.pyplot as plt
from io import BytesIO
import tkinter as tk
from tkinter import messagebox
from comun import *
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import  A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet


def generar_grafico_por_genero(datos):
    # Contar libros por género usando los datos del reporte específico
    generos = {}
    for item in datos:
        genero = item[2]  # Tercer elemento en cada registro es el género
        generos[genero] = generos.get(genero, 0) + 1

    # Datos para el gráfico
    labels = list(generos.keys())
    data = list(generos.values())
    
    # Crear un gráfico de pastel
    plt.figure(figsize=(6, 4))
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Mantener la proporción circular

    # Guardar el gráfico en un búfer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()  # Cerrar el gráfico para liberar memoria
    
    return buffer  # Retornar el gráfico como objeto de BytesIO


def mostrar_opciones_reportes(self):
    # Crear una nueva ventana para los reportes
    ventana_reportes = tk.Toplevel(self.root)
    ventana_reportes.title("Generar Reportes")
    ventana_reportes.minsize(300, 250)

    
    tk.Button(ventana_reportes, text="Prestamos vencidos", command=lambda: mostrar_prestamos_vencidos(self)).pack(pady=10)
    tk.Button(ventana_reportes, text="Libros mas prestados del ultimo mes", command=lambda: mostrar_libros_mas_prestados(self)).pack(pady=10)
    tk.Button(ventana_reportes, text="Usuarios con mas prestamos", command=lambda: mostrar_usuarios_con_mas_prestamos(self)).pack(pady=10)
    tk.Button(ventana_reportes, text="Volver", command=lambda: cerrarVentana(ventana_reportes)).pack(pady=10)

def mostrar_prestamos_vencidos(self):
    report = prestamos_vencidos()
    mostrar_resultado(self, report, "prestamos vencidos", f"Prestamos vencidos")

def mostrar_libros_mas_prestados(self):
    report = libros_mas_prestados()
    mostrar_resultado(self, report, "libros mas prestados", f"Libros mas prestados de {obtener_mes_anterior()}")

def mostrar_usuarios_con_mas_prestamos(self):
    report = usuarios_con_mas_prestamos()
    mostrar_resultado(self, report, "usuarios con mas prestamos", "Top 5 Usuarios con mas prestamos")

def mostrar_resultado(self, resultado, nombre, titulo):
    # Crear un archivo PDF
    pdf_file = nombre + ".pdf"
    
    # Crear un documento PDF
    doc = SimpleDocTemplate(pdf_file, pagesize=A4)
    
    # Crear una lista para almacenar los elementos del informe
    elements = []
    styles = getSampleStyleSheet()
    
    elements.append(Paragraph(titulo, styles['Title']))
    
    # Crear la tabla con los datos
    table_data = []
    encabezado, datos = resultado  # resultado es una tupla (encabezado, datos)
    table_data.append(encabezado)  # Añadir encabezado
    
    # Añadir las filas de datos
    for item in datos:
        table_data.append(item)  # Cada fila es una tupla (titulo del libro, cantidad)
    
    # Crear la tabla con los datos
    table = Table(table_data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightslategray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
    table.setStyle(style)
    
    elements.append(Spacer(10, 10))
    elements.append(table)

    # Agregar el gráfico solo si el reporte es "Libros más prestados"
    if nombre == "libros mas prestados":
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Distribución de Libros por Género", styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        grafico_buffer = generar_grafico_por_genero(datos)
        elements.append(Image(grafico_buffer, width=400, height=250))
    
    # Construir el documento con el título, tabla y, si corresponde, el gráfico
    doc.build(elements)

    # Notificar al usuario que el PDF ha sido generado
    messagebox.showinfo("Generar PDF", f"El reporte ha sido generado y guardado como: \"{pdf_file}\"")
