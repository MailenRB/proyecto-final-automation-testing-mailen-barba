from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10
        self.wait = WebDriverWait(self.driver, self.timeout)

    def find_element(self, locator):
        """Finds a single element, waiting for it to be present."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Finds all elements matching a locator."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        """Clicks an element once it is clickable."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def js_click(self, locator):
        """Clicks an element using JavaScript execution."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def send_keys(self, locator, text):
        """Clears and sends keys to an element."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Gets the text of an element."""
        element = self.find_element(locator)
        return element.text

    def is_displayed(self, locator):
        """Checks if an element is visible on the page."""
        try:
            element = self.find_element(locator)
            return element.is_displayed()
        except Exception:
            return False
