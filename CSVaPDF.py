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
elementos.append(f"Generado el: {fecha}",  estilos["normal"])
elementos.append(Spacer(1, 20))

#TABLA DESDE DF
header = ["Nombre", "Departamento", "Salario"]
