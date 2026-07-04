from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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

    def js_click_and_wait_for_url(self, locator, url_fragment, attempts=3):
        """JS-clicks an element and confirms the page actually navigated.

        On SauceDemo's submit controls a click can intermittently fail to fire in
        headless CI (the handler never runs, so the page stays put with no error).
        Re-clicking until the URL advances makes the step transition reliable and
        fails with a clear message instead of a downstream timeout.
        """
        for attempt in range(1, attempts + 1):
            if url_fragment in self.driver.current_url:
                return
            self.js_click(locator)
            try:
                self.wait.until(EC.url_contains(url_fragment))
                return
            except TimeoutException:
                self.logger.warning(
                    f"URL did not reach '{url_fragment}' after click "
                    f"(attempt {attempt}/{attempts}); retrying"
                )
        raise TimeoutException(
            f"Page did not navigate to '{url_fragment}' after {attempts} clicks on {locator}"
        )

    def _set_react_input_value(self, element, text):
        """Sets a value on a controlled (React) input via the native setter.

        On headless CI the synthetic key events from ``send_keys`` are dropped by
        SauceDemo's checkout inputs, so the field stays empty. Assigning through
        the prototype's native value setter and dispatching an ``input`` event is
        the reliable way to make React register the change in its own state,
        which is what the form validation actually reads.
        """
        self.driver.execute_script(
            "const el = arguments[0], val = arguments[1];"
            "const setter = Object.getOwnPropertyDescriptor("
            "window.HTMLInputElement.prototype, 'value').set;"
            "setter.call(el, val);"
            "el.dispatchEvent(new Event('input', { bubbles: true }));"
            "el.dispatchEvent(new Event('change', { bubbles: true }));",
            element, text,
        )

    def send_keys(self, locator, text):
        """Types text into an element and guarantees the value actually persisted.

        Tries native typing first (realistic path). If the value does not stick
        -- which happens on SauceDemo's React checkout inputs in headless CI,
        where key events are silently dropped and the form submits empty
        ('First Name is required') -- it falls back to setting the value through
        React's controlled-input mechanism, then verifies and retries.
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
            if element.get_attribute("value") != text:
                # Native keystrokes were dropped -> drive the value through React.
                self._set_react_input_value(element, text)
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
