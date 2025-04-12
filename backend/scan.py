import cv2
from pyzbar.pyzbar import decode

def extract_barcode(image_path):
    """
    Extrae el código de barras de una imagen y devuelve el código.
    """
    # Cargar la imagen
    image = cv2.imread(image_path)

    # Decodificar el código de barras
    barcodes = decode(image)

    if not barcodes:
        return "No se detectó ningún código de barras."

    # Extraer los datos del código de barras
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")  # Convertir bytes a texto
        barcode_type = barcode.type
        return barcode_data  # Solo devuelve el código de barras

    return None  # En caso de no detectar ningún código
