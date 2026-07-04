from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InventoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.cart_badge = (By.CSS_SELECTOR, ".shopping_cart_badge")
        self.cart_link = (By.CSS_SELECTOR, ".shopping_cart_link")
        self.sort_dropdown = (By.CSS_SELECTOR, ".product_sort_container")
        self.inventory_item_name = (By.CSS_SELECTOR, ".inventory_item_name")

    def add_product_to_cart(self, product_name):
        """Adds a specific product to the cart by its visible name."""
        btn_xpath = f"//div[contains(@class, 'inventory_item_name') and text()='{product_name}']/ancestor::div[contains(@class, 'inventory_item')]//button"
        self.click((By.XPATH, btn_xpath))

    def remove_product_from_inventory(self, product_name):
        """Removes a specific product from the inventory page by its visible name."""
        btn_xpath = f"//div[contains(@class, 'inventory_item_name') and text()='{product_name}']/ancestor::div[contains(@class, 'inventory_item')]//button"
        self.click((By.XPATH, btn_xpath))

    def get_cart_badge_count(self):
        """Gets the current number of items displayed in the shopping cart badge."""
        if self.is_displayed(self.cart_badge):
            return int(self.get_text(self.cart_badge))
        return 0

    def go_to_cart(self):
        """Navigates to the shopping cart page."""
        self.js_click(self.cart_link)

    def sort_products_by(self, option_value):
        """
        Sorts the products using the dropdown.
        Options: 'az', 'za', 'lohi', 'hilo'
        """
        dropdown = self.find_element(self.sort_dropdown)
        for option in dropdown.find_elements(By.TAG_NAME, "option"):
            if option.get_attribute("value") == option_value:
                option.click()
                break

    def get_product_names(self):
        """Gets a list of all product names displayed on the inventory page."""
        elements = self.find_elements(self.inventory_item_name)
        return [el.text for el in elements]
