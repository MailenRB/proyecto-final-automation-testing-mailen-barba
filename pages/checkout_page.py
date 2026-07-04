from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.first_name_input = (By.ID, "first-name")
        self.last_name_input = (By.ID, "last-name")
        self.postal_code_input = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.finish_button = (By.ID, "finish")
        self.complete_header = (By.CSS_SELECTOR, ".complete-header")

    def fill_checkout_info(self, first_name, last_name, postal_code):
        """Fills the checkout information form and submits it."""
        self.send_keys(self.first_name_input, first_name)
        self.send_keys(self.last_name_input, last_name)
        self.send_keys(self.postal_code_input, postal_code)
        self.js_click_and_wait_for_url(self.continue_button, "checkout-step-two")

    def finish_checkout(self):
        """Clicks the finish button on the overview page."""
        self.js_click_and_wait_for_url(self.finish_button, "checkout-complete")

    def get_complete_header_text(self):
        """Retrieves the completion header text (e.g., 'Thank you for your order!')."""
        return self.get_text(self.complete_header)
