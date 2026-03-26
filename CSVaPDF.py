import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime

# 1. Leer y procesar datos
df = pd.read_csv("empleados.csv")
df = df.dropna(subset=["nombre"])
df["nombre"] = df["nombre"].str.strip().str.title()
df["salario"] = pd.to_numeric(df["salario"], errors="coerce").fillna(0)
df = df.drop_duplicates(subset=["nombre"])

# 2. Generar gráfico
df.groupby("departamento")["salario"].mean().plot(kind="bar", color="#3498db", figsize=(8, 4))
plt.title("Salario por departamento")
plt.tight_layout()
plt.savefig("grafico_temp.png", dpi=150, bbox_inches="tight")
plt.close()

# 3. Generar PDF
doc = SimpleDocTemplate("reporte_empleados.pdf", pagesize=A4)
elementos = []
estilos = getSampleStyleSheet()
fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

#header
estilos_titulo = estilos["Title"]
estilos.spaceAfter = 20
elementos.append(Paragraph("REPORTE DE EMPLEADOS", estilos_titulo))
elementos.append(Paragraph(f"Generado el: {fecha}",  estilos["Normal"]))
elementos.append(Spacer(1, 20))

#TABLA DESDE DF
header = ["Nombre", "Departamento", "Salario"]
filas = [[
    row["nombre"], row["departamento"], f"S/ {row["salario"]}"]
          for _, row in df.iterrows()]

tabla = Table([header] + filas, colWidths=[180, 150, 100])
tabla.setStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#54a3f1")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("ALIGN", (0,0), (-1,0), "CENTER"),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#ecf0f1")]),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
])

elementos.append(tabla)
elementos.append(Spacer(1, 20))
elementos.append(Image("grafico_temp.png", width=450, height=250))

doc.build(elementos)
print("REPORTE DE EMPLEADOS GENERADO CORRECTAMENTE")
