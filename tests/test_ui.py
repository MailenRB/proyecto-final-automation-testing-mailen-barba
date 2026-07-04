import pytest
from utils.data_reader import load_json_data
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

# Load test data once for the module
data = load_json_data()

def test_login_success(driver):
    """Test 1: Verification of successful login."""
    login_page = LoginPage(driver)
    driver.get(data["url"])
    
    login_page.login(data["valid_user"]["username"], data["valid_user"]["password"])
    
    # Assert redirection to inventory page
    assert "inventory.html" in driver.current_url

def test_login_failure(driver):
    """Test 2: Escenario negativo - Login con credenciales invalidas."""
    login_page = LoginPage(driver)
    driver.get(data["url"])
    
    login_page.login(data["invalid_user"]["username"], data["invalid_user"]["password"])
    
    # Assert error message is displayed
    error_msg = login_page.get_error_message()
    assert "Username and password do not match" in error_msg

def test_add_to_cart(driver):
    """Test 3: Agregar productos al carrito y verificar contenido."""
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    
    driver.get(data["url"])
    login_page.login(data["valid_user"]["username"], data["valid_user"]["password"])
    
    # Add products
    inventory_page.add_product_to_cart("Sauce Labs Backpack")
    inventory_page.add_product_to_cart("Sauce Labs Bike Light")
    
    # Assert badge count is updated
    assert inventory_page.get_cart_badge_count() == 2
    
    # Go to cart and verify items are present
    inventory_page.go_to_cart()
    cart_items = cart_page.get_cart_item_names()
    assert "Sauce Labs Backpack" in cart_items
    assert "Sauce Labs Bike Light" in cart_items

def test_remove_from_cart(driver):
    """Test 4: Remover producto del carrito y verificar que quede vacio."""
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    
    driver.get(data["url"])
    login_page.login(data["valid_user"]["username"], data["valid_user"]["password"])
    
    # Add product and verify badge
    inventory_page.add_product_to_cart("Sauce Labs Backpack")
    assert inventory_page.get_cart_badge_count() == 1
    
    # Go to cart and remove the product
    inventory_page.go_to_cart()
    cart_page.remove_product_from_cart("Sauce Labs Backpack")
    
    # Assert cart is empty
    assert len(cart_page.get_cart_item_names()) == 0
    assert inventory_page.get_cart_badge_count() == 0

def test_checkout_complete(driver):
    """Test 5: Flujo completo de compra (E2E) con checkout exitoso."""
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)
    
    driver.get(data["url"])
    login_page.login(data["valid_user"]["username"], data["valid_user"]["password"])
    
    # Add a product
    inventory_page.add_product_to_cart("Sauce Labs Backpack")
    
    # Proceed to checkout
    inventory_page.go_to_cart()
    cart_page.go_to_checkout()
    
    # Fill checkout info and finish purchase
    info = data["checkout_info"]
    checkout_page.fill_checkout_info(info["first_name"], info["last_name"], info["postal_code"])
    checkout_page.finish_checkout()
    
    # Assert checkout complete header
    success_text = checkout_page.get_complete_header_text()
    assert "Thank you for your order!" in success_text
