from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class PaginaCheckout(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.input_nombre = (By.ID, "first-name")
        self.input_apellido = (By.ID, "last-name")
        self.input_codigo_postal = (By.ID, "postal-code")
        self.boton_continuar = (By.ID, "continue")
        self.boton_finalizar = (By.ID, "finish")
        self.encabezado_completo = (By.CSS_SELECTOR, ".complete-header")

    def completar_info_checkout(self, nombre, apellido, codigo_postal):
        """Completa el formulario de información de pago (checkout) y lo envía."""
        self.escribir_texto(self.input_nombre, nombre)
        self.escribir_texto(self.input_apellido, apellido)
        self.escribir_texto(self.input_codigo_postal, codigo_postal)
        self.hacer_clic_js_y_esperar_url(self.boton_continuar, "checkout-step-two")

    def finalizar_checkout(self):
        """Hace clic en el botón de finalizar en la página de resumen de compra."""
        self.hacer_clic_js_y_esperar_url(self.boton_finalizar, "checkout-complete")

    def obtener_texto_encabezado_completo(self):
        """Recupera el texto del encabezado de finalización (por ejemplo, 'Thank you for your order!')."""
        return self.obtener_texto(self.encabezado_completo)
