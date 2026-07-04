from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.logger = get_logger(self.__class__.__name__)

    def find_element(self, locator):
        """Finds a single element, waiting for it to be present."""
        self.logger.debug(f"Locating element: {locator}")
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Finds all elements matching a locator."""
        self.logger.debug(f"Locating elements: {locator}")
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        """Clicks an element once it is clickable."""
        self.logger.info(f"Clicking element: {locator}")
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def js_click(self, locator):
        """Clicks an element using JavaScript execution."""
        self.logger.info(f"JS Clicking element: {locator}")
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def send_keys(self, locator, text):
        """Clears and types text into an element, verifying the value persisted.

        On SPA (React) controlled inputs reached via client-side navigation,
        keystrokes sent before the component finishes rendering can be silently
        dropped. This left the checkout form empty in headless CI and made the
        'Continue' validation fail ('First Name is required'), so the flow never
        reached the overview step. We wait until the field is interactable, then
        confirm the value stuck and retry if it did not.
        """
        is_secret = "password" in str(locator).lower() or "password" in text.lower()
        if is_secret:
            self.logger.info(f"Typing into element {locator}: ******")
        else:
            self.logger.info(f"Typing '{text}' into element: {locator}")

        attempts = 3
        for attempt in range(1, attempts + 1):
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.clear()
            element.send_keys(text)
            if element.get_attribute("value") == text:
                return
            self.logger.warning(
                f"Value for {locator} did not persist (attempt {attempt}/{attempts}); retrying"
            )
        raise AssertionError(
            f"Failed to enter text into {locator} after {attempts} attempts "
            f"(field did not retain the expected value)"
        )

    def get_text(self, locator):
        """Gets the text of an element."""
        element = self.find_element(locator)
        text = element.text
        self.logger.info(f"Retrieved text '{text}' from: {locator}")
        return text

    def is_displayed(self, locator):
        """Checks if an element is visible on the page without waiting."""
        try:
            elements = self.driver.find_elements(*locator)
            if elements:
                visible = elements[0].is_displayed()
                self.logger.debug(f"Element {locator} visibility state: {visible}")
                return visible
            return False
        except Exception:
            self.logger.debug(f"Element {locator} is not visible or not found")
            return False
