
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter,legal
from reportlab.pdfgen import canvas
from django.contrib import admin, messages
from zeta.settings import BASE_DIR
import os
import locale


@admin.action(description="Descargar detalle de Pedido")
def generar_reporte(modeladmin, request, queryset):

    #Validacion para que seleccione solo 1 queryset
    if len(queryset) != 1:
        messages.error(request, "Seleccione solo un pedido para generar el informe.")
        return
    #Capturo la ruta actual para la ruta del logo
    current_directory = os.getcwd()
    #el logo esta en la raiz del proyecto
    logo_path = os.path.join(current_directory, 'static/logo.png')
    # Establecer el idioma en español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    # Obtener el primer pedido seleccionado
    pedido = queryset[0]  
    #Crear el objeto
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="presupuesto.pdf"'
    # Crear el lienzo PDF
    p = canvas.Canvas(response, pagesize=legal)

    # Agregar contenido al lienzo
    y = 950  # Posición vertical inicial
    x = 50
        # Verificar si el archivo de imagen del logo existe
    if logo_path:

        # Tamaño y posición del logo
        logo_width = 130  # Ancho del logo
        logo_height = 130  # Alto del logo
        logo_x = 420  # Posición horizontal del logo
        logo_y = 830  # Posición vertical del logo

        # Agregar el logo al lienzo PDF
        p.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height)
    # Titulo del reporte
    p.setFont("Helvetica-Bold", 16)  
    p.drawString(x, y, f"DETALLE PEDIDO #{pedido.pk}")
    y -= 10
    p.setFont("Helvetica", 10)
    p.drawString(x, y, f"ESTADO FINALIZADO")
    y -= 15
    # Numero de cliente
    p.setFont("Helvetica-Bold", 10)  # Fuente en negrita
    p.drawString(x, y, "Cliente #: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    p.drawString(100, y, str(pedido.CLIENTE.NUMERO_CLIENTE))
    y -= 20

    # Nombre y apellido
    p.setFont("Helvetica-Bold", 10)  # Fuente en negrita
    p.drawString(x, y, "Nombre y apellido: ")
    p.setFont("Helvetica", 10)
    p.drawString(150, y, str(pedido.CLIENTE.NOMBRE_Y_APELLIDO))
    y -= 20

    #p.setFont("Helvetica-Bold", 10)  # Fuente en negrita
    #p.drawString(x, y, "Direccion: ")
    #p.setFont("Helvetica", 10)  # Fuente normal
    #p.drawString(105, y, str(pedido.CLIENTE.DIRECCION))
    #y -= 20

    # Email
    p.setFont("Helvetica-Bold", 10)  # Fuente en negrita
    p.drawString(x, y, "Email: ")
    p.setFont("Helvetica", 10)
    p.drawString(90, y, str(pedido.CLIENTE.EMAIL))
    y -= 20

    # Telefono
    p.setFont("Helvetica-Bold", 10)  # Fuente en negrita
    p.drawString(x, y, "Telefono: ")
    p.setFont("Helvetica", 10)
    p.drawString(100, y, str(pedido.CLIENTE.TELEFONO))
    y -= 40

    # Bloque entrega
    p.setFillColorRGB(0, 0, 0)  # Color de texto negro
    p.setFont("Helvetica-Bold", 12)  # Fuente en negrita y tamaño 14
    p.drawString(x, y, f"DETALLE DEL PRODUCTO")
    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Presupuesto #: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str(pedido.CODIGO)
    p.drawString(130, y, codigo_str.zfill(4))
    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Fecha de entrega: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    p.drawString(140, y,  f"{pedido.FECHA_ENTREGA.strftime('%A %d de %B del %Y')}")
    y -= 20

    #Detalle
    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "DETALLES: ")
    y -= 20 
    p.setFont("Helvetica", 10)  # Fuente normal
    detalle = str(pedido.DETALLE)
    posicion_x = 50

    # Dividir el detalle en líneas utilizando "#"
    lineas = detalle.split("\n")

    for linea in lineas:
        # Mostrar la línea en el lienzo PDF
        largo = len(linea)
        linea = linea[:largo-1]
        p.drawString(posicion_x, y, linea)
        # Ajustar la posición vertical para la siguiente línea
        y -= 20

    # Bloque entrega
    p.setFillColorRGB(0, 0, 0)  # Color de texto negro
    p.setFont("Helvetica-Bold", 13)  # Fuente en negrita y tamaño 14
    p.drawString(x, y, f"INSUMOS INCLUIDOS EN EL PRESUPUESTO")
    y -= 25

    p.setFont("Helvetica", 10)  
    p.setFillColorRGB(0, 0, 0)  # Color de texto negro
    articulos = pedido.ARTICULO.split(", ")
    columna_actual = 1  # Variable para controlar la columna actual
    y_inicial = y  # Guardar la posición vertical inicial
    for i, articulo in enumerate(articulos):
        if i % 26 == 0 and i > 0:
            # Cambiar a la siguiente columna
            columna_actual += 1
            y = y_inicial
        p.drawString(x + 270 * (columna_actual - 1), y, f"• {articulo.strip()} Unid.")
        y -= 20


    y = 60
    p.setFont("Helvetica-Bold", 14)
    p.drawString(380, y, "Precio total: ")
    p.setFont("Helvetica", 13)  # Fuente normal
    p.drawString(480, y,  f'$ {pedido.PRECIO:,.2f}')
    y -= 40

    #y = 60
    p.setFont("Helvetica-Bold", 12)
    #p.drawString(150, 20, f"Presupuesto válido hasta el {pedido.FECHA_ENTREGA.strftime('%A %d de %B del %Y')}")
    #p.setFont("Helvetica", 13)  # Fuente normal
    #p.drawString(400, y,  f"{pedido.VALIDO_HASTA.strftime('%A %d de %B del %Y')}")
    #y -= 40

    if y <= 60:
        # Si no hay suficiente espacio en la página actual, crear una nueva página
        p.showPage()
        y = 700

    # Guardar el lienzo PDF
    p.save()

    return response
