import requests
from utils.data_reader import cargar_datos_json
from utils.logger import obtener_logger

# Configurar logger de API
logger = obtener_logger("Pruebas_API")

# Cargar datos de configuración
datos = cargar_datos_json()
URL_BASE = datos["api_url"]

def test_obtener_usuarios():
    """Prueba 1: Solicitud GET - Listar usuarios y validar estructura."""
    logger.info("--- INICIANDO PRUEBA: test_obtener_usuarios ---")
    url = f"{URL_BASE}/users"
    logger.info(f"Enviando solicitud GET a: {url}")
    respuesta = requests.get(url)
    
    logger.info(f"Estado de respuesta recibido: {respuesta.status_code}")
    assert respuesta.status_code == 200, f"Se esperaba 200, pero se obtuvo {respuesta.status_code}"
    
    json_res = respuesta.json()
    
    logger.info("Verificando que la respuesta sea una lista y contenga elementos")
    assert isinstance(json_res, list), "Se esperaba que la respuesta fuera una lista de usuarios"
    assert len(json_res) > 0, "Se esperaba que la lista de usuarios no estuviera vacía"
    
    logger.info("Verificando claves en el primer elemento de usuario")
    primer_usuario = json_res[0]
    claves_esperadas = ["id", "name", "username", "email", "address"]
    for clave in claves_esperadas:
        assert clave in primer_usuario, f"Al elemento de usuario le falta la clave '{clave}'"
    logger.info("--- PRUEBA EXITOSA: test_obtener_usuarios ---")

def test_crear_usuario():
    """Prueba 2: Solicitud POST - Crear un usuario y validar la respuesta."""
    logger.info("--- INICIANDO PRUEBA: test_crear_usuario ---")
    url = f"{URL_BASE}/users"
    payload = {
        "name": "Mailen Barba",
        "username": "mailen",
        "email": "mailen@example.com"
    }
    logger.info(f"Enviando solicitud POST a: {url} con el payload: {payload}")
    respuesta = requests.post(url, json=payload)
    
    logger.info(f"Estado de respuesta recibido: {respuesta.status_code}")
    assert respuesta.status_code == 201, f"Se esperaba 201, pero se obtuvo {respuesta.status_code}"
    
    json_res = respuesta.json()
    logger.info("Verificando que los campos del usuario coincidan con el payload de la solicitud")
    assert json_res["name"] == payload["name"], f"Se esperaba el nombre '{payload['name']}', pero se obtuvo '{json_res['name']}'"
    assert json_res["username"] == payload["username"], f"Se esperaba el nombre de usuario '{payload['username']}', pero se obtuvo '{json_res['username']}'"
    assert json_res["email"] == payload["email"], f"Se esperaba el email '{payload['email']}', pero se obtuvo '{json_res['email']}'"
    
    logger.info(f"Verificando el campo autogenerado 'id': {json_res.get('id')}")
    assert "id" in json_res, "Falta el campo autogenerado 'id' en la respuesta"
    logger.info("--- PRUEBA EXITOSA: test_crear_usuario ---")

def test_eliminar_usuario():
    """Prueba 3: Solicitud DELETE - Eliminar un usuario y validar el código de estado."""
    logger.info("--- INICIANDO PRUEBA: test_eliminar_usuario ---")
    url = f"{URL_BASE}/users/1"
    logger.info(f"Enviando solicitud DELETE a: {url}")
    respuesta = requests.delete(url)
    
    logger.info(f"Estado de respuesta recibido: {respuesta.status_code}")
    assert respuesta.status_code == 200, f"Se esperaba 200, pero se obtuvo {respuesta.status_code}"
    logger.info("--- PRUEBA EXITOSA: test_eliminar_usuario ---")

def test_encadenamiento_obtener_detalles_usuario():
    """Prueba 4: Encadenamiento de solicitudes (GET -> GET) - Extraer ID de la lista y luego obtener detalles."""
    logger.info("--- INICIANDO PRUEBA: test_encadenamiento_obtener_detalles_usuario ---")
    
    # Paso 1: Obtener lista de usuarios (GET)
    url_lista = f"{URL_BASE}/users"
    logger.info(f"[Paso 1 del Encadenamiento] Enviando solicitud GET a: {url_lista}")
    respuesta_lista = requests.get(url_lista)
    assert respuesta_lista.status_code == 200
    
    usuarios = respuesta_lista.json()
    assert len(usuarios) > 0, "No se encontraron usuarios"
    
    # Extraer detalles del primer usuario
    usuario_objetivo = usuarios[0]
    id_objetivo = usuario_objetivo["id"]
    email_objetivo = usuario_objetivo["email"]
    nombre_objetivo = usuario_objetivo["name"]
    logger.info(f"[Paso 1 del Encadenamiento] ID de usuario extraído: {id_objetivo}, Nombre: '{nombre_objetivo}', Email: '{email_objetivo}'")
    
    # Paso 2: Obtener detalles del usuario específico (GET)
    url_detalle = f"{URL_BASE}/users/{id_objetivo}"
    logger.info(f"[Paso 2 del Encadenamiento] Enviando solicitud GET a: {url_detalle}")
    respuesta_detalle = requests.get(url_detalle)
    
    logger.info(f"[Paso 2 del Encadenamiento] Estado de respuesta recibido: {respuesta_detalle.status_code}")
    assert respuesta_detalle.status_code == 200, f"Se esperaba 200, pero se obtuvo {respuesta_detalle.status_code}"
    
    detalle_usuario = respuesta_detalle.json()
    logger.info("[Paso 2 del Encadenamiento] Validando que los detalles devueltos del usuario coincidan con la extracción del paso 1")
    assert detalle_usuario["id"] == id_objetivo, f"Se esperaba el ID {id_objetivo}, pero se obtuvo {detalle_usuario['id']}"
    assert detalle_usuario["email"] == email_objetivo, f"Se esperaba el email {email_objetivo}, pero se obtuvo {detalle_usuario['email']}"
    assert detalle_usuario["name"] == nombre_objetivo, f"Se esperaba el nombre {nombre_objetivo}, pero se obtuvo {detalle_usuario['name']}"
    logger.info("--- PRUEBA EXITOSA: test_encadenamiento_obtener_detalles_usuario ---")

def test_encadenamiento_leer_actualizar_eliminar():
    """Prueba 5: Encadenamiento de solicitudes (GET -> PUT -> DELETE) - Obtener, actualizar y limpiar un usuario."""
    logger.info("--- INICIANDO PRUEBA: test_encadenamiento_leer_actualizar_eliminar ---")
    
    # Paso 1: Obtener detalles del usuario 1 para tener datos base (GET)
    url_usuario = f"{URL_BASE}/users/1"
    logger.info(f"[Paso 1 del Encadenamiento] Obteniendo detalles del usuario 1 desde: {url_usuario}")
    respuesta_get = requests.get(url_usuario)
    assert respuesta_get.status_code == 200
    
    datos_usuario = respuesta_get.json()
    nombre_original = datos_usuario["name"]
    logger.info(f"[Paso 1 del Encadenamiento] Nombre de usuario extraído: '{nombre_original}'")
    
    # Paso 2: PUT para actualizar el nombre
    payload_actualizacion = {
        "name": f"{nombre_original} Actualizado",
        "username": datos_usuario["username"],
        "email": datos_usuario["email"]
    }
    logger.info(f"[Paso 2 del Encadenamiento] Enviando solicitud PUT a {url_usuario} con el payload: {payload_actualizacion}")
    respuesta_put = requests.put(url_usuario, json=payload_actualizacion)
    
    logger.info(f"[Paso 2 del Encadenamiento] Estado de respuesta recibido: {respuesta_put.status_code}")
    assert respuesta_put.status_code == 200, f"Se esperaba 200, pero se obtuvo {respuesta_put.status_code}"
    
    json_put = respuesta_put.json()
    logger.info("Verificando que la actualización del nombre por PUT sea correcta")
    assert json_put["name"] == payload_actualizacion["name"]
    
    # Paso 3: DELETE para eliminar el recurso
    logger.info(f"[Paso 3 del Encadenamiento] Enviando solicitud DELETE a: {url_usuario}")
    respuesta_delete = requests.delete(url_usuario)
    
    logger.info(f"[Paso 3 del Encadenamiento] Estado de respuesta recibido: {respuesta_delete.status_code}")
    assert respuesta_delete.status_code == 200, f"Se esperaba 200, pero se obtuvo {respuesta_delete.status_code}"
    logger.info("--- PRUEBA EXITOSA: test_encadenamiento_leer_actualizar_eliminar ---")
