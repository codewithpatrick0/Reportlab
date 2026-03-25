from reportlab.platypus import Image, SimpleDocTemplate

image = Image("perro.png", width=100, height=100) # Guardamos la imagen con la funcion Image
elementos = []
elementos.append(image)
doc = SimpleDocTemplate("IMAGEN_DE_PERRO.PDF")

doc.build(elementos)
print("Imagen en PDF GENERADA")

