import pytest
from utils.data_reader import cargar_datos_json
from utils.logger import obtener_logger
from pages.login_page import PaginaLogin
from pages.inventory_page import PaginaInventario
from pages.cart_page import PaginaCarrito
from pages.checkout_page import PaginaCheckout

# Configurar logger de UI
logger = obtener_logger("Pruebas_UI")

# Cargar datos de prueba una vez para el módulo
datos = cargar_datos_json()

def test_inicio_sesion_exitoso(driver):
    """Prueba 1: Verificación de inicio de sesión exitoso."""
    logger.info("--- INICIANDO PRUEBA: test_inicio_sesion_exitoso ---")
    pagina_login = PaginaLogin(driver)
    
    logger.info(f"Navegando a {datos['url']}")
    driver.get(datos["url"])
    
    logger.info(f"Iniciando sesión con el usuario: '{datos['valid_user']['username']}'")
    pagina_login.iniciar_sesion(datos["valid_user"]["username"], datos["valid_user"]["password"])
    
    logger.info("Verificando redirección a inventory.html")
    assert "inventory.html" in driver.current_url
    logger.info("--- PRUEBA EXITOSA: test_inicio_sesion_exitoso ---")

def test_inicio_sesion_fallido(driver):
    """Prueba 2: Escenario negativo - Inicio de sesión con credenciales inválidas."""
    logger.info("--- INICIANDO PRUEBA: test_inicio_sesion_fallido ---")
    pagina_login = PaginaLogin(driver)
    
    logger.info(f"Navegando a {datos['url']}")
    driver.get(datos["url"])
    
    logger.info(f"Iniciando sesión con el usuario inválido: '{datos['invalid_user']['username']}'")
    pagina_login.iniciar_sesion(datos["invalid_user"]["username"], datos["invalid_user"]["password"])
    
    logger.info("Verificando que el contenedor del mensaje de error coincida con el texto esperado")
    mensaje_error = pagina_login.obtener_mensaje_error()
    assert "Username and password do not match" in mensaje_error
    logger.info("--- PRUEBA EXITOSA: test_inicio_sesion_fallido ---")

def test_agregar_al_carrito(driver):
    """Prueba 3: Agregar productos al carrito y verificar contenido."""
    logger.info("--- INICIANDO PRUEBA: test_agregar_al_carrito ---")
    pagina_login = PaginaLogin(driver)
    pagina_inventario = PaginaInventario(driver)
    pagina_carrito = PaginaCarrito(driver)
    
    logger.info(f"Navegando a {datos['url']} e iniciando sesión")
    driver.get(datos["url"])
    pagina_login.iniciar_sesion(datos["valid_user"]["username"], datos["valid_user"]["password"])
    
    logger.info("Agregando 'Sauce Labs Backpack' al carrito")
    pagina_inventario.agregar_producto_al_carrito("Sauce Labs Backpack")
    logger.info("Agregando 'Sauce Labs Bike Light' al carrito")
    pagina_inventario.agregar_producto_al_carrito("Sauce Labs Bike Light")
    
    logger.info("Verificando que la insignia del carrito de compras cuente 2 artículos")
    assert pagina_inventario.obtener_cantidad_insignia_carrito() == 2
    
    logger.info("Navegando a la página del carrito de compras")
    pagina_inventario.ir_al_carrito()
    articulos_carrito = pagina_carrito.obtener_nombres_items_carrito()
    
    logger.info("Verificando que los productos existan dentro de la lista del carrito de compras")
    assert "Sauce Labs Backpack" in articulos_carrito
    assert "Sauce Labs Bike Light" in articulos_carrito
    logger.info("--- PRUEBA EXITOSA: test_agregar_al_carrito ---")

def test_eliminar_del_carrito(driver):
    """Prueba 4: Eliminar producto del carrito y verificar que quede vacío."""
    logger.info("--- INICIANDO PRUEBA: test_eliminar_del_carrito ---")
    pagina_login = PaginaLogin(driver)
    pagina_inventario = PaginaInventario(driver)
    pagina_carrito = PaginaCarrito(driver)
    
    logger.info(f"Navegando a {datos['url']} e iniciando sesión")
    driver.get(datos["url"])
    pagina_login.iniciar_sesion(datos["valid_user"]["username"], datos["valid_user"]["password"])
    
    logger.info("Agregando 'Sauce Labs Backpack' al carrito")
    pagina_inventario.agregar_producto_al_carrito("Sauce Labs Backpack")
    assert pagina_inventario.obtener_cantidad_insignia_carrito() == 1
    
    logger.info("Navegando al carrito y eliminando el producto")
    pagina_inventario.ir_al_carrito()
    pagina_carrito.eliminar_producto_del_carrito("Sauce Labs Backpack")
    
    logger.info("Verificando que el carrito contenga 0 artículos y la insignia se haya limpiado")
    assert len(pagina_carrito.obtener_nombres_items_carrito()) == 0
    assert pagina_inventario.obtener_cantidad_insignia_carrito() == 0
    logger.info("--- PRUEBA EXITOSA: test_eliminar_del_carrito ---")

def test_checkout_completo(driver):
    """Prueba 5: Flujo completo de compra (E2E) con checkout exitoso."""
    logger.info("--- INICIANDO PRUEBA: test_checkout_completo ---")
    pagina_login = PaginaLogin(driver)
    pagina_inventario = PaginaInventario(driver)
    pagina_carrito = PaginaCarrito(driver)
    pagina_checkout = PaginaCheckout(driver)
    
    logger.info(f"Navegando a {datos['url']} e iniciando sesión")
    driver.get(datos["url"])
    pagina_login.iniciar_sesion(datos["valid_user"]["username"], datos["valid_user"]["password"])
    
    logger.info("Agregando 'Sauce Labs Backpack' al carrito")
    pagina_inventario.agregar_producto_al_carrito("Sauce Labs Backpack")
    
    logger.info("Procediendo al formulario de pago (checkout)")
    pagina_inventario.ir_al_carrito()
    pagina_carrito.ir_a_checkout()
    
    info = datos["checkout_info"]
    logger.info(f"Completando información de pago: Nombre='{info['first_name']}', Apellido='{info['last_name']}', Código Postal='{info['postal_code']}'")
    pagina_checkout.completar_info_checkout(info["first_name"], info["last_name"], info["postal_code"])
    
    logger.info("Finalizando el paso de resumen de compra")
    pagina_checkout.finalizar_checkout()
    
    logger.info("Verificando el texto del encabezado de finalización del pedido de checkout")
    texto_exito = pagina_checkout.obtener_texto_encabezado_completo()
    assert "Thank you for your order!" in texto_exito
    logger.info("--- PRUEBA EXITOSA: test_checkout_completo ---")
