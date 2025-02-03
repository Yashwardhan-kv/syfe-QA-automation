import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Test Data
BASE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
INVALID_USERNAME = "invalid_user"
INVALID_PASSWORD = "wrong_password"
ERROR_MSG = "Epic sadface: Username and password do not match any user in this service"

@pytest.fixture(scope="function")
def setup():
    """Setup WebDriver before each test and quit after"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def login(driver, username, password):
    """Performs login operation."""
    driver.get(BASE_URL)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

def test_login_validation(setup):
    """Task 1: Login Validation"""
    driver = setup
    
    # Valid Login
    login(driver, USERNAME, PASSWORD)
    WebDriverWait(driver, 15).until(EC.url_contains("inventory.html"))
    assert "inventory.html" in driver.current_url, "Login failed, inventory page not reached!"
    
    driver.get(BASE_URL)  # Logout and go back to login page
    
    # Invalid Login
    login(driver, INVALID_USERNAME, INVALID_PASSWORD)
    error_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h3[@data-test='error']"))).text
    assert ERROR_MSG in error_message, "Expected error message not displayed!"

def test_add_items_to_cart(setup):
    """Task 2: Add Items to Cart from Inventory Page"""
    driver = setup
    login(driver, USERNAME, PASSWORD)
    
    # Change sorting filter to "Price (low to high)"
    sort_dropdown = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "product_sort_container")))
    sort_dropdown.click()
    sort_dropdown.find_element(By.XPATH, "//option[@value='lohi']").click()
    
    # Add two items to the cart
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
    
    # Verify cart count
    cart_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert cart_count == "2", f"Expected cart count 2, but got {cart_count}"

def test_add_item_from_product_page(setup):
    """Task 3: Add Items to Cart from Inventory Item Page"""
    driver = setup
    login(driver, USERNAME, PASSWORD)

    # Add two items first
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
    
    # Click on product
    driver.find_element(By.LINK_TEXT, "Sauce Labs Onesie").click()

    # Ensure the button is visible before clicking
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-onesie"))).click()
    
    # Verify cart count
    cart_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert cart_count == "3", f"Expected cart count 3, but got {cart_count}"

def test_remove_item_from_cart(setup):
    """Task 4: Remove Items from Cart"""
    driver = setup
    login(driver, USERNAME, PASSWORD)
    
    # Add items
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
    driver.find_element(By.LINK_TEXT, "Sauce Labs Onesie").click()
    
    # Ensure the button is visible before clicking
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-onesie"))).click()
    
    # Go to Cart
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    
    # Remove item with price between $8 and $10
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    removed = False
    for item in cart_items:
        price_text = item.find_element(By.CLASS_NAME, "inventory_item_price").text
        price = float(price_text.replace("$", ""))
        if 8 <= price <= 10:
            item.find_element(By.CLASS_NAME, "cart_button").click()
            removed = True
            break
    
    assert removed, "No item found in price range $8-$10 to remove!"

    # Verify if item count decreased
    updated_cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(updated_cart_items) < len(cart_items), "Item was not removed successfully!"

def test_checkout(setup):
    """Task 5: Checkout Workflow"""
    driver = setup
    login(driver, USERNAME, PASSWORD)
    
    # Add items and proceed to checkout
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()
    
    # Fill out checkout form
    driver.find_element(By.ID, "first-name").send_keys("Yashwardhan")
    driver.find_element(By.ID, "last-name").send_keys("Katkamwar")
    driver.find_element(By.ID, "postal-code").send_keys("440034")
    driver.find_element(By.ID, "continue").click()
    
    # Print total amount
    total_amount = driver.find_element(By.CLASS_NAME, "summary_total_label").text
    print(f"Total Amount: {total_amount}")
    
    # Complete the purchase
    driver.find_element(By.ID, "finish").click()
    
    # Verify success message (case-insensitive check)
    success_msg = driver.find_element(By.CLASS_NAME, "complete-header").text
    assert "thank you for your order" in success_msg.lower(), "Order completion message missing!"
