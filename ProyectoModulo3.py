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
    df_antes = len(df)
    df = df.dropna(subset=["vendedor"])
    df_final = len(df)
    descartados = df_antes - df_final
    df["vendedor"] = df["vendedor"].str.strip().str.title()
    df["cantidad"] = pd.to_numeric( df["cantidad"], errors="coerce").fillna(0)
    df["precio_unitario"] = pd.to_numeric( df["precio_unitario"], errors="coerce").fillna(0)
    df = df.drop_duplicates(subset=["vendedor", "producto", "fecha"])
    
    return df, descartados

def procesar_datos(df) :
    df["venta_total"] = df["cantidad"] * df["precio_unitario"]
    ventas_por_vendedor = df.groupby("vendedor")["cantidad"].sum()
    max_unidades_vendidas_por_vendedor = ventas_por_vendedor.max()
    ventas_por_region = df.groupby("region")["venta_total"].sum()
    max_vendedor = ventas_por_vendedor.idxmax()
    max_producto = df.groupby("producto")["cantidad"].sum().idxmax()
    ventas_totales = df["venta_total"].sum()
    max_cantidad_producto = (df.groupby("producto")["cantidad"].sum()).max()
    
    resumen = {
        "mejor_cantidad_producto" : max_cantidad_producto,
        "mejor_vendedor_cantidad" : max_unidades_vendidas_por_vendedor,
        "ventas_por_vendedor": ventas_por_vendedor,
        "ventas_por_region": ventas_por_region,
        "mejor_vendedor": max_vendedor,
        "producto_mas_vendido": max_producto,
        "ventas_totales" : ventas_totales
    } 
    return df, resumen
    
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
    img = fig.savefig("grafico.png", dpi=150, bbox_inches="tight")
    plt.close()
    
    return "grafico.png"

def generar_pdf(df, resumen) :
    doc = SimpleDocTemplate("REPORTE_VENTAS.pdf",pagesize=A4)
    elementos = []
    estilos = getSampleStyleSheet()
    
    #HEADER
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    estilos_titulo = estilos["Title"]
    estilos_titulo.spaceAfter = 20
    elementos.append(Paragraph("REPORTE DE VENTAS 03/26", estilos_titulo))
    elementos.append(Paragraph(f"Generado el: {fecha}", estilos["Normal"]))
    elementos.append(Spacer(1, 20))
    elementos.append(Paragraph(f"Total de ventas: S/{resumen["ventas_totales"]:,.2f}", estilos["Normal"]))
    elementos.append(Spacer(1,10))
    elementos.append(Paragraph(f"Mejor vendedor: {resumen["mejor_vendedor"]} - {resumen["mejor_vendedor_cantidad"]} unidades de productos vendidos", estilos["Normal"]))
    elementos.append(Spacer(1,10))
    elementos.append(Paragraph(f"Producto más vendido: {resumen["producto_mas_vendido"]} - {resumen["mejor_cantidad_producto"]} unidades.", estilos["Normal"]))
    elementos.append(Spacer(1,10))
    elementos.append(Paragraph(f"Registros eliminados: {resumen["descartados"]}", estilos["Normal"]))
    elementos.append(Spacer(1, 20))
    
    columnas_df = ["vendedor", "producto", "cantidad", "precio_unitario", "fecha", "region", "venta_total"]
    header = ["Vendedor", "Producto", "Cantidad", "Precio Unitario", "Fecha", "Región", "Venta Total"] 
    df_fmt = df.copy()
    df_fmt["precio_unitario"] = df_fmt["precio_unitario"].apply(lambda x : f"S/{x:,.2f}")
    df_fmt["venta_total"] = df_fmt["venta_total"].apply(lambda x : f"S/{x:,.2f}")
    
    datos = [header]
    datos.extend(df_fmt[columnas_df].values.tolist())
    
    tabla = Table(datos, colWidths=[90, 80, 40, 70, 80, 80, 80])
    tabla.setStyle(TableStyle([
        # HEADER
        ("BACKGROUND", (0,0), (-1, 0), colors.HexColor("#6cdd68")),
        ("TEXTCOLOR", (0,0), (-1, 0), colors.HexColor("#000000")),
        ("FONTNAME", (0,0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0,0), (-1, 0), "CENTER"),  # <--- AQUÍ FALTABA LA COMA
        
        # CONTENT
        ("ROWBACKGROUNDS", (0,1), (-1, -1), [colors.white, colors.HexColor("#cce963")]),
        ("GRID", (0,1), (-1, -1), 0.5, colors.HexColor("#6c6b7434")),
    ]))
    
    elementos.append(tabla)
    elementos.append(Spacer(1, 20))
    
    ruta_imagen = generar_graficos(df)
    imagen = Image(ruta_imagen, width=450, height=250)
    elementos.append(imagen)
    
    doc.build(elementos)
    print("REPORTE DE EMPLEADOS GENERADO CORRECTAMENTE")
    
def generar_csv(df, nombre_archivo="ventas_marzo_limpias.csv") :
    df.to_csv(nombre_archivo, index=False, sep=";", encoding="utf-8-sig")
    
    return nombre_archivo
    
    
def ejecutar(archivo) :
    try :
        #Leer
        print("Ejecutando archivo...")
        df_sucio = pd.read_csv(archivo)
        print("ARCHIVO ORIGINAL CARGADO")
        
        #Limpiar
        print("Limpiando datos...")
        df_limpio, descartados = limpiar_datos(df_sucio)
        print("ARCHIVO EDITADO CORRECTAMENTE")
        
        #Procesar
        print("Procesando datos")
        df_listo, resumen = procesar_datos(df_limpio)
        print("DATOS PROCESADOS CORRECTAMENTE")
        
        #DESCARTADOS
        resumen["descartados"] = descartados
        
        #Generar CSV
        print("Generando CSV  actualizado")
        csv_nuevo = generar_csv(df_limpio)
        print(f"CSV ACTUALIZADO Y GUARDADO CORRECTAMENTE EN: {csv_nuevo}")
        #Generar PDF
        print("Generando PDF...")
        generar_pdf(df_listo, resumen)
        print("PDF GENERADO CORRECTAMENTE")

        print("----------------------")
        print("REPORTE COMPLETADO CORRECTAMENTE")
        print("----------------------")
    except Exception as e :
        print(f"Error en la ejecución: {e}")
        
if __name__ == "__main__":
    ejecutar("ventas.csv")