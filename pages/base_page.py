from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import obtener_logger

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.logger = obtener_logger(self.__class__.__name__)

    def buscar_elemento(self, localizador):
        """Busca un solo elemento, esperando a que esté presente."""
        self.logger.debug(f"Buscando elemento: {localizador}")
        return self.wait.until(EC.presence_of_element_located(localizador))

    def buscar_elementos(self, localizador):
        """Busca todos los elementos que coincidan con un localizador."""
        self.logger.debug(f"Buscando elementos: {localizador}")
        return self.wait.until(EC.presence_of_all_elements_located(localizador))

    def hacer_clic(self, localizador):
        """Hace clic en un elemento una vez que es clicable."""
        self.logger.info(f"Haciendo clic en el elemento: {localizador}")
        elemento = self.wait.until(EC.element_to_be_clickable(localizador))
        elemento.click()

    def hacer_clic_js(self, localizador):
        """Hace clic en un elemento utilizando la ejecución de JavaScript."""
        self.logger.info(f"Haciendo clic por JS en el elemento: {localizador}")
        elemento = self.wait.until(EC.element_to_be_clickable(localizador))
        self.driver.execute_script("arguments[0].click();", elemento)

    def hacer_clic_js_y_esperar_url(self, localizador, fragmento_url, intentos=3):
        """Hace clic por JS en un elemento y confirma que la página realmente navegó.

        En los controles de envío de SauceDemo, un clic puede fallar intermitentemente en
        el CI headless (el manejador nunca se ejecuta, por lo que la página no cambia sin arrojar error).
        Hacer clic repetidamente hasta que la URL avance hace que la transición del paso sea confiable
        y falle con un mensaje claro en lugar de un timeout posterior.
        """
        for intento in range(1, intentos + 1):
            if fragmento_url in self.driver.current_url:
                return
            self.hacer_clic_js(localizador)
            try:
                self.wait.until(EC.url_contains(fragmento_url))
                return
            except TimeoutException:
                self.logger.warning(
                    f"La URL no llegó a '{fragmento_url}' después de hacer clic "
                    f"(intento {intento}/{intentos}); reintentando"
                )
        raise TimeoutException(
            f"La página no navegó a '{fragmento_url}' después de {intentos} clics en {localizador}"
        )

    def _establecer_valor_input_react(self, elemento, texto):
        """Establece un valor en un input controlado (React) a través del setter nativo.

        En CI headless, los eventos de teclado sintéticos de ``send_keys`` son descartados por
        los inputs del checkout de SauceDemo, por lo que el campo queda vacío. Asignar a través
        del setter de valor nativo del prototipo y despachar un evento ``input`` es la forma
        confiable de hacer que React registre el cambio en su propio estado, que es lo que
        realmente lee la validación del formulario.
        """
        self.driver.execute_script(
            "const el = arguments[0], val = arguments[1];"
            "const setter = Object.getOwnPropertyDescriptor("
            "window.HTMLInputElement.prototype, 'value').set;"
            "setter.call(el, val);"
            "el.dispatchEvent(new Event('input', { bubbles: true }));"
            "el.dispatchEvent(new Event('change', { bubbles: true }));",
            elemento, texto,
        )

    def escribir_texto(self, localizador, texto):
        """Escribe texto en un elemento y garantiza que el valor realmente persistió.

        Intenta la escritura nativa primero (ruta realista). Si el valor no se mantiene
        -- lo cual ocurre en los inputs de checkout de React de SauceDemo en CI headless,
        donde los eventos de teclado se descartan silenciosamente y el formulario se envía vacío
        ('First Name is required') -- recurre a establecer el valor a través del mecanismo de
        input controlado de React, luego verifica y reintenta.
        """
        es_secreto = "password" in str(localizador).lower() or "password" in texto.lower()
        if es_secreto:
            self.logger.info(f"Escribiendo en el elemento {localizador}: ******")
        else:
            self.logger.info(f"Escribiendo '{texto}' en el elemento: {localizador}")

        intentos = 3
        for intento in range(1, intentos + 1):
            elemento = self.wait.until(EC.element_to_be_clickable(localizador))
            elemento.clear()
            elemento.send_keys(texto)
            if elemento.get_attribute("value") != texto:
                # Las pulsaciones de teclas nativas se descartaron -> pasar el valor a través de React.
                self._establecer_valor_input_react(elemento, texto)
            if elemento.get_attribute("value") == texto:
                return
            self.logger.warning(
                f"El valor para {localizador} no persistió (intento {intento}/{intentos}); reintentando"
            )
        raise AssertionError(
            f"Fallo al ingresar texto en {localizador} después de {intentos} intentos "
            f"(el campo no retuvo el valor esperado)"
        )

    def obtener_texto(self, localizador):
        """Obtiene el texto de un elemento."""
        elemento = self.buscar_elemento(localizador)
        texto = elemento.text
        self.logger.info(f"Texto recuperado '{texto}' de: {localizador}")
        return texto

    def esta_visible(self, localizador):
        """Verifica si un elemento es visible en la página sin esperar."""
        try:
            elementos = self.driver.find_elements(*localizador)
            if elementos:
                visible = elementos[0].is_displayed()
                self.logger.debug(f"Estado de visibilidad del elemento {localizador}: {visible}")
                return visible
            return False
        except Exception:
            self.logger.debug(f"El elemento {localizador} no es visible o no fue encontrado")
            return False
