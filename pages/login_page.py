from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.username_input = (By.ID, "user-name")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.error_container = (By.CSS_SELECTOR, "[data-test='error']")

    def login(self, username, password):
        """Performs a login action with username and password."""
        self.send_keys(self.username_input, username)
        self.send_keys(self.password_input, password)
        self.click(self.login_button)

    def get_error_message(self):
        """Retrieves the error message text displayed on login failure."""
        return self.get_text(self.error_container)
