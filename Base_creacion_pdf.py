from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


#CREACION DEL DOCUMENTO
doc = SimpleDocTemplate("REPORTE_GENERAL.pdf", pagesize=A4) #crear el pdf (nombre, tamaño hoja)
elementos = [] #Lista donde estarán los bloques del pdf
estilos =   getSampleStyleSheet()  # Usar paquete listo de estilos para el pdf

#TITULO
estilo_titulo = estilos["Title"]
estilo_titulo.spaceAfter = 20
elementos.append(Paragraph("REPORTE GENERAL", estilo_titulo))

"""O :
elementos.append(Paragraph("Reporte General", estilo["Title"]))
elementos.append(Spacer(1, 20)) # Espacio de 20 puntos, LO MISMO QUE EL ANTERIOR PERO OTRO METODO

"""
"""
estilos = getSampleStyleSheet()

# Los más usados:
estilos["Title"]    # título grande centrado
estilos["Heading1"] # subtítulo grande
estilos["Heading2"] # subtítulo mediano
estilos["Normal"]   # texto normal
estilos["BodyText"] # texto de párrafo
"""

#CONTENIDO
estilo_contenido = estilos["Normal"]
estilo_contenido.spaceAfter = 20
elementos.append(Paragraph("Fecha: 25/03/2026", estilo_contenido))

#CONSTRUIR PDF
doc.build(elementos)
print("PDF GENERADO")