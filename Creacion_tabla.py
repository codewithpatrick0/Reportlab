from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate
from reportlab.lib import colors
elementos = []
doc = SimpleDocTemplate("TABLA_DATOS.pdf", pagesize=A4)

datos = [
    ["Nombre", "Departamento", "Salario", "Categoría"],  # header
    ["Juan Carlos", "Ventas", "S/ 3,500.00", "Mid"],
    ["Maria Garcia", "Marketing", "S/ 3,200.00", "Mid"],
    ["Carlos Ruiz", "Sistemas", "S/ 4,500.00", "Senior"],
]

tabla = Table(datos, colWidths=[150, 120, 100, 80])
tabla.setStyle([
    #HEADER 
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#78abdd")), # CON COORDENADAS PERSONALIZAMOS LAS FILAS , BACKGROUND : FONDO
    ("TEXTCOLOR", (0,0), (-1,-0), colors.white), # COLOR DEL TEXTO, COLORS.(COLOR) O COLOR. HEXCOLOR ÑPARA SELCCIONAR COLOR
    ("ALIGN", (0,0), (-1,0), "CENTER"), # ALINEAR TEXTO
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), # SELECCIONAR FUENTE DEL TEXTO

    #CUERPO
    ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE", (0,1), (-1,-1), 10), # TAMAÑO DEL TEXTO
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#3ed8ff"), colors.HexColor("#ecf0f1")]), # SELECCIONAR COLOR DE FONDO, MAS DE UN COLOR
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey) # ASIGNAR BORDES DE LAS CELDAS
])
elementos.append(tabla)

doc.build(elementos)
print("TABLA GENERADA EN PDF CORRECTAMENTE")
