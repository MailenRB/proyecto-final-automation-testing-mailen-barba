import logging
import os

def obtener_logger(nombre):
    """
    Crea u obtiene un logger configurado para escribir en la consola y en un archivo.
    """
    logger = logging.getLogger(nombre)
    # Previene manejadores duplicados si el logger se obtiene múltiples veces
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Resuelve dinámicamente el directorio de logs relativo a la ubicación de esta utilidad
        dir_actual = os.path.dirname(os.path.abspath(__file__))
        dir_logs = os.path.join(dir_actual, "..", "logs")
        os.makedirs(dir_logs, exist_ok=True)
        
        archivo_log = os.path.join(dir_logs, "execution.log")
        
        # Patrón de formateo
        formateador = logging.Formatter(
            fmt='%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Manejador de archivo para persistencia de logs locales
        manejador_archivo = logging.FileHandler(archivo_log, encoding='utf-8')
        manejador_archivo.setFormatter(formateador)
        logger.addHandler(manejador_archivo)
        
        # Manejador de consola para enviar logs a los ejecutores de pruebas
        manejador_consola = logging.StreamHandler()
        manejador_consola.setFormatter(formateador)
        logger.addHandler(manejador_consola)
        
    return logger
