from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class PaginaCarrito(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.boton_checkout = (By.ID, "checkout")
        self.nombre_item_carrito = (By.CSS_SELECTOR, ".inventory_item_name")

    def obtener_nombres_items_carrito(self):
        """Recupera los nombres de todos los productos actualmente en el carrito sin esperar."""
        try:
            elementos = self.driver.find_elements(*self.nombre_item_carrito)
            return [el.text for el in elementos]
        except Exception:
            return []

    def eliminar_producto_del_carrito(self, nombre_producto):
        """Elimina un producto específico del carrito por su nombre y espera a que desaparezca."""
        xpath_boton = f"//div[contains(@class, 'inventory_item_name') and text()='{nombre_producto}']/ancestor::div[contains(@class, 'cart_item')]//button"
        self.hacer_clic_js((By.XPATH, xpath_boton))
        
        # Espera hasta que el elemento eliminado ya no esté presente/visible en el DOM
        from selenium.webdriver.support import expected_conditions as EC
        xpath_item = f"//div[contains(@class, 'inventory_item_name') and text()='{nombre_producto}']"
        self.wait.until(EC.invisibility_of_element_located((By.XPATH, xpath_item)))

    def ir_a_checkout(self):
        """Hace clic en el botón de checkout para proceder al formulario de pago."""
        self.hacer_clic_js(self.boton_checkout)
