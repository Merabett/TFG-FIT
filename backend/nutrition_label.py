
from PIL import Image, ImageDraw, ImageFont
import json
import os

def generate_nutrition_label(nutriments_json, output_path='nutrition_label.png'):
    # Parsear datos
    data = nutriments_json
    servings_per_container = 3  # Este valor no se usa, ya que no estamos calculando el valor del envase

    # Configuraciones básicas
    width = 410
    padding = 10
    row_height = 30
    spacing_above_otros = 10

    # Cargar fuentes
    font_dir = r'C:\Users\Ismam\Desktop\TFG\TFG-FIT\backend\fonts'
    title_font = ImageFont.truetype(os.path.join(font_dir, 'ARIALBD.TTF'), 32)
    section_font = ImageFont.truetype(os.path.join(font_dir, 'ARIALBD.TTF'), 24)
    bold_font = ImageFont.truetype(os.path.join(font_dir, 'ARIALBD.TTF'), 18)
    regular_font = ImageFont.truetype(os.path.join(font_dir, 'ARIAL.TTF'), 16)

    # Paso 1: Calcular la altura necesaria
    y = 0
    y += 40  # Título
    y += 20  # Raciones
    y += 25  # Tamaño ración
    y += 10 + 5  # Línea gruesa
    y += 25  # Encabezados "Por envase" y "Por ración"
    y += 2 + 10  # Línea intermedia + espacio
    y += 30  # Calorías
    y += 5 + 10  # Línea gruesa + espacio

    # Simular dibujo para calcular altura final
    found_salt = False
    added_secondary_header = False
    for nutrient in data:
        if nutrient in ["Calorías", "Energia (kcal)"]:
            continue

        if found_salt and not added_secondary_header:
            y += spacing_above_otros
            y += row_height - 10
            added_secondary_header = True

        y += row_height - 5

        if nutrient == "Sal":
            y += 4  # Línea gruesa después de Sal
        elif not found_salt:
            y += 1  # Línea gris

        if nutrient == "Sal":
            found_salt = True

    total_height = y + padding

    # Paso 2: Crear imagen con altura final
    image = Image.new('RGB', (width, total_height), 'white')
    draw = ImageDraw.Draw(image)

    # Paso 3: Dibujar contenido real
    y = padding
    draw.text((padding, y), "Información Nutricional", font=title_font, fill='black')
    y += 40
    draw.text((padding, y), f"{servings_per_container} raciones por envase", font=regular_font, fill='black')
    y += 20
    draw.text((padding, y), "Tamaño de ración", font=bold_font, fill='black')
    draw.text((padding + 160, y), "3 pretzels (28g)", font=regular_font, fill='black')
    y += 25
    draw.line((0, y, width, y), fill='black', width=5)
    y += 10

    draw.text((padding + 170, y), "Por 100g", font=bold_font, fill='black')
    draw.text((padding + 300, y), "Por ración", font=bold_font, fill='black')
    y += 25
    draw.line((0, y, width, y), fill='black', width=2)

    # Calorías
    y += 10
    calorias = data.get("Energia (kcal)", data.get("Calorías", {}))
    calorias_por_racion = calorias.get("serving", 0)
    calorias_por_100g = calorias.get("100g", 0)

    draw.text((padding, y), "Calorías", font=section_font, fill='black')
    draw.text((padding + 180, y), str(calorias_por_100g), font=section_font, fill='black')  # Mostrar 100g
    draw.text((padding + 310, y), str(calorias_por_racion), font=section_font, fill='black')  # Mostrar serving
    y += 30
    draw.line((0, y, width, y), fill='black', width=5)
    y += 10

    # Nutrientes
    found_salt = False
    added_secondary_header = False

    for nutrient, values in data.items():
        if nutrient in ["Calorías", "Energia (kcal)"]:
            continue

        indent = 20 if nutrient in ["Grasas saturadas", "Azucares", "Fibra alimentaria"] else 0
        valor_racion = values.get("serving", 0)  # Usamos solo el valor de "serving"
        valor_100g = values.get("100g", 0)  # Usamos el valor de "100g"
        is_secondary = found_salt

        if nutrient == "Sal":
            found_salt = True

        if is_secondary and not added_secondary_header:
            y += spacing_above_otros
            draw.text((padding, y), "Otros nutrientes", font=bold_font, fill='black')
            y += row_height - 10
            added_secondary_header = True

        draw.text((padding + indent, y), nutrient,
                  font=regular_font if is_secondary or indent > 0 else bold_font,
                  fill='black')

        draw.text((padding + 200, y), str(valor_100g), font=regular_font, fill='black')  # Mostrar 100g
        draw.text((padding + 320, y), str(valor_racion), font=regular_font, fill='black')  # Mostrar serving
        y += row_height - 5

        if nutrient == "Sal":
            draw.line((padding, y, width - padding, y), fill='black', width=4)
        elif not is_secondary:
            draw.line((padding, y, width - padding, y), fill="#cccccc", width=1)

    # Guardar imagen
    image.save(output_path)
    print(f"Etiqueta guardada en {output_path}")