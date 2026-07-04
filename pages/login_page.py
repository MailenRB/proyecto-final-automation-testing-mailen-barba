from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class PaginaLogin(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.input_usuario = (By.ID, "user-name")
        self.input_contrasena = (By.ID, "password")
        self.boton_login = (By.ID, "login-button")
        self.contenedor_error = (By.CSS_SELECTOR, "[data-test='error']")

    def iniciar_sesion(self, usuario, contrasena):
        """Realiza una acción de inicio de sesión con el nombre de usuario y contraseña."""
        self.escribir_texto(self.input_usuario, usuario)
        self.escribir_texto(self.input_contrasena, contrasena)
        self.hacer_clic(self.boton_login)

    def obtener_mensaje_error(self):
        """Recupera el texto del mensaje de error mostrado al fallar el inicio de sesión."""
        return self.obtener_texto(self.contenedor_error)
