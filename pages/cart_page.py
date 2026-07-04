from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.checkout_button = (By.ID, "checkout")
        self.cart_item_name = (By.CSS_SELECTOR, ".inventory_item_name")

    def get_cart_item_names(self):
        """Retrieves names of all products currently in the cart."""
        try:
            elements = self.find_elements(self.cart_item_name)
            return [el.text for el in elements]
        except Exception:
            return []

    def remove_product_from_cart(self, product_name):
        """Removes a specific product from the cart by its name."""
        btn_xpath = f"//div[contains(@class, 'inventory_item_name') and text()='{product_name}']/ancestor::div[contains(@class, 'cart_item')]//button"
        self.click((By.XPATH, btn_xpath))

    def go_to_checkout(self):
        """Clicks the checkout button to proceed to the checkout form."""
        self.click(self.checkout_button)
