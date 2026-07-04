from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class PaginaInventario(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.insignia_carrito = (By.CSS_SELECTOR, ".shopping_cart_badge")
        self.enlace_carrito = (By.CSS_SELECTOR, ".shopping_cart_link")
        self.desplegable_orden = (By.CSS_SELECTOR, ".product_sort_container")
        self.nombre_item_inventario = (By.CSS_SELECTOR, ".inventory_item_name")

    def agregar_producto_al_carrito(self, nombre_producto):
        """Agrega un producto específico al carrito por su nombre visible."""
        xpath_boton = f"//div[contains(@class, 'inventory_item_name') and text()='{nombre_producto}']/ancestor::div[contains(@class, 'inventory_item')]//button"
        self.hacer_clic_js((By.XPATH, xpath_boton))

    def eliminar_producto_del_inventario(self, nombre_producto):
        """Elimina un producto específico de la página de inventario por su nombre visible."""
        xpath_boton = f"//div[contains(@class, 'inventory_item_name') and text()='{nombre_producto}']/ancestor::div[contains(@class, 'inventory_item')]//button"
        self.hacer_clic_js((By.XPATH, xpath_boton))

    def obtener_cantidad_insignia_carrito(self):
        """Obtiene la cantidad actual de artículos que se muestran en la insignia del carrito de compras."""
        if self.esta_visible(self.insignia_carrito):
            return int(self.obtener_texto(self.insignia_carrito))
        return 0

    def ir_al_carrito(self):
        """Navega a la página del carrito de compras."""
        self.hacer_clic_js(self.enlace_carrito)

    def ordenar_productos_por(self, valor_opcion):
        """
        Ordena los productos usando el desplegable.
        Opciones: 'az', 'za', 'lohi', 'hilo'
        """
        desplegable = self.buscar_elemento(self.desplegable_orden)
        for opcion in desplegable.find_elements(By.TAG_NAME, "option"):
            if opcion.get_attribute("value") == valor_opcion:
                opcion.click()
                break

    def obtener_nombres_productos(self):
        """Obtiene una lista con los nombres de todos los productos que se muestran en la página de inventario."""
        elementos = self.buscar_elementos(self.nombre_item_inventario)
        return [el.text for el in elementos]
