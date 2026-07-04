import json
import os

def cargar_datos_json(nombre_archivo="test_data.json"):
    """
    Carga datos JSON desde el directorio data/.
    """
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(dir_actual, "..", "data", nombre_archivo)
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        return json.load(f)
