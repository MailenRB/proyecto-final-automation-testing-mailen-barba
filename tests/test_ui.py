import pytest
from utils.data_reader import load_json_data
from utils.logger import get_logger
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

# Set up UI logger
logger = get_logger("UI_Tests")

# Load test data once for the module
data = load_json_data()

def test_login_success(driver):
    """Test 1: Verification of successful login."""
    logger.info("--- STARTING TEST: test_login_success ---")
    login_page = LoginPage(driver)
    
    logger.info(f"Navigating to {data['url']}")
    driver.get(data["url"])
    
    logger.info(f"Logging in with user: '{data['valid_user']['username']}'")
    login_page.login(data["valid_user"]["username"], data["valid_user"]["password"])
    
    logger.info("Verifying redirection to inventory.html")
    assert "inventory.html" in driver.current_url
    logger.info("--- TEST PASSED: test_login_success ---")

def test_login_failure(driver):
    """Test 2: Escenario negativo - Login con credenciales invalidas."""
    logger.info("--- STARTING TEST: test_login_failure ---")
    login_page = LoginPage(driver)
    
    logger.info(f"Navigating to {data['url']}")
    driver.get(data["url"])
    
    logger.info(f"Logging in with invalid user: '{data['invalid_user']['username']}'")
    login_page.login(data["invalid_user"]["username"], data["invalid_user"]["password"])
    
    logger.info("Verifying error message container matches expected text")
    error_msg = login_page.get_error_message()
    assert "Username and password do not match" in error_msg
    logger.info("--- TEST PASSED: test_login_failure ---")

def test_add_to_cart(driver):
    """Test 3: Agregar productos al carrito y verificar contenido."""
    logger.info("--- STARTING TEST: test_add_to_cart ---")
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    
    logger.info(f"Navigating to {data['url']} and logging in")
    driver.get(data["url"])
    login_page.login(data["valid_user"]["username"], data["valid_user"]["password"])
    
    logger.info("Adding 'Sauce Labs Backpack' to cart")
    inventory_page.add_product_to_cart("Sauce Labs Backpack")
    logger.info("Adding 'Sauce Labs Bike Light' to cart")
    inventory_page.add_product_to_cart("Sauce Labs Bike Light")
    
    logger.info("Verifying shopping cart badge counts 2 items")
    assert inventory_page.get_cart_badge_count() == 2
    
    logger.info("Navigating to shopping cart page")
    inventory_page.go_to_cart()
    cart_items = cart_page.get_cart_item_names()
    
    logger.info("Verifying products exist inside shopping cart list")
    assert "Sauce Labs Backpack" in cart_items
    assert "Sauce Labs Bike Light" in cart_items
    logger.info("--- TEST PASSED: test_add_to_cart ---")

def test_remove_from_cart(driver):
    """Test 4: Remover producto del carrito y verificar que quede vacio."""
    logger.info("--- STARTING TEST: test_remove_from_cart ---")
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    
    logger.info(f"Navigating to {data['url']} and logging in")
    driver.get(data["url"])
    login_page.login(data["valid_user"]["username"], data["valid_user"]["password"])
    
    logger.info("Adding 'Sauce Labs Backpack' to cart")
    inventory_page.add_product_to_cart("Sauce Labs Backpack")
    assert inventory_page.get_cart_badge_count() == 1
    
    logger.info("Navigating to cart and removing product")
    inventory_page.go_to_cart()
    cart_page.remove_product_from_cart("Sauce Labs Backpack")
    
    logger.info("Verifying cart contains 0 items and badge is cleared")
    assert len(cart_page.get_cart_item_names()) == 0
    assert inventory_page.get_cart_badge_count() == 0
    logger.info("--- TEST PASSED: test_remove_from_cart ---")

def test_checkout_complete(driver):
    """Test 5: Flujo completo de compra (E2E) con checkout exitoso."""
    logger.info("--- STARTING TEST: test_checkout_complete ---")
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)
    
    logger.info(f"Navigating to {data['url']} and logging in")
    driver.get(data["url"])
    login_page.login(data["valid_user"]["username"], data["valid_user"]["password"])
    
    logger.info("Adding 'Sauce Labs Backpack' to cart")
    inventory_page.add_product_to_cart("Sauce Labs Backpack")
    
    logger.info("Proceeding to checkout form")
    inventory_page.go_to_cart()
    cart_page.go_to_checkout()
    
    info = data["checkout_info"]
    logger.info(f"Filling checkout info: First Name='{info['first_name']}', Last Name='{info['last_name']}', Postal Code='{info['postal_code']}'")
    checkout_page.fill_checkout_info(info["first_name"], info["last_name"], info["postal_code"])
    
    logger.info("Finishing purchase overview step")
    checkout_page.finish_checkout()
    
    logger.info("Verifying checkout order completion header text")
    success_text = checkout_page.get_complete_header_text()
    assert "Thank you for your order!" in success_text
    logger.info("--- TEST PASSED: test_checkout_complete ---")
