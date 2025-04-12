from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware  # Importar CORS
from scan import extract_barcode
from database import execute_query
from nutrition_label import generate_nutrition_label
import os
import json


temp_dir = "C:/temp"
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

app = FastAPI()

# Servir imágenes generadas
app.mount("/labels", StaticFiles(directory="C:/temp"), name="labels")

# Configuración de CORS para permitir que el frontend se comunique con el backend
origins = [
    "http://localhost:5173",  # Para desarrollo local  # Cambia esto cuando despliegues en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/scan_barcode/")
async def scan_barcode(file: UploadFile = File(...)):
    """
    Ruta que recibe una imagen, extrae el código de barras y consulta la base de datos.
    """
    try:
        # Leer la imagen del archivo cargado
        image_bytes = await file.read()
        
        # Crear un directorio temporal en Windows
        image_path = os.path.join(temp_dir, "temp_image.jpg")

        # Guardar el archivo en el sistema temporal
        with open(image_path, "wb") as f:
            f.write(image_bytes)

        # Obtener el código de barras de la imagen
        barcode = extract_barcode(image_path)

        if barcode:
            # Realizar la consulta a la base de datos con el código de barras
            query = f"SELECT * FROM NUTRIAPP_BBDD.PROCESSED_DATA.FOOD_DATA_TRANSFORMED WHERE CODE = '{barcode}'"
            results = execute_query(query)

            if results:
                # Convertir el primer resultado a JSON para usar en la etiqueta
                results = results[0]
                nutriments_json = results[3] # El campo que nos interesa es el 3º

                # Asegurarse de que el JSON sea un diccionario
                nutrients_data = json.loads(nutriments_json)

                # Ruta de salida para la imagen
                label_path = os.path.join(temp_dir, f"label_{barcode}.png")

                # Generar etiqueta
                generate_nutrition_label(nutrients_data, output_path=label_path)

                return {
                    "barcode": barcode,
                    "data": results,
                    "label_image": label_path
                }
            else:
                return {"error": "No se encontraron resultados para el código de barras."}
        else:
            return {"error": "No se detectó un código de barras en la imagen."}

    except Exception as e:
        return {"error": str(e)}
