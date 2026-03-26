import pandas as pd
import matplotlib
matplotlib.use("agg") # Para guardar img sin necesidad de mostrar ventanas
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime

def limpiar_datos(df) :
    df = df.dropna(subset=["vendedor"])
    df["vendedor"] = df["vendedor"].str.strip().str.title()
    df["cantidad"] = pd.to_numeric( df["cantidad"], errors="coerce").fillna(0)
    df["precio_unitario"] = pd.to_numeric( df["precio_unitario"], errors="coerce").fillna(0)
    df = df.drop_duplicates(subset=["vendedor", "producto", "fecha"])
    
    return df

def procesar_datos(df) :
    df["venta_total"] = df["cantidad"] * df["precio_unitario"]
    ventas_por_vendedor = df.groupby("vendedor")["total_venta"].sum()
    ventas_por_region = df.groupby("region")["venta_total"].sum()
    max_vendedor = ventas_por_vendedor.idxmax()
    max_producto = df.groupby("producto")["cantidad"].sum().idxmax()
    
    return {
        "ventas_por_vendedor": ventas_por_vendedor,
        "ventas_por_region": ventas_por_region,
        "mejor_vendedor": max_vendedor,
        "producto_mas_vendido": max_producto
    } 
    
def generar_graficos(df) :
    fig, axes = plt.subplots(1, 3, figsize=(10, 6))
    ventas_vendedor = df.groupby("vendedor")["venta_total"].sum()
    ventas_vendedor.plot(kind="bar", ax = axes[0], color="skyblue")
    axes[0].set_title("TOTAL DE VENTAS POR VENDEDOR")
    axes[0].set_xlabel("Vendedores")
    axes[0].set_ylabel("S/ VENTAS")
    
    ventas_region = df.groupby("region")["venta_total"].sum()
    ventas_region.plot(kind="pie", ax=axes[1], autopct="%1.1f%%")
    axes[1].set_title("VENTAS POR REGIÓN")
    
    productos_cantidad = df.groupby("producto")["cantidad"].sum()
    productos_cantidad.plot(kind="barh", ax = axes[2], color="red")
    axes[2].set_title("PRODUCTOS MAS VENDIDOS")
    
    fig.tight_layout()                   # ajusta márgenes automáticamente
    fig.savefig("grafico.png", dpi=150, bbox_inches="tight")
    
    
    