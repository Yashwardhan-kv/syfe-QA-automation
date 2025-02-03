import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class SauceDemoAutomation:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.saucedemo.com/"
        self.wait = WebDriverWait(driver, 10)

    def open_site(self):
        """Opens the SauceDemo website."""
        self.driver.get(self.url)

    def login(self, username, password):
        """Performs login operation."""
        self.driver.find_element(By.ID, 'user-name').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.ID, 'login-button').click()

    def validate_login(self, valid=True):
        """Validates successful or failed login attempts."""
        if valid:
            self.wait.until(EC.url_contains("/inventory.html"))
            assert "/inventory.html" in self.driver.current_url, "Login failed!"
        else:
            error_msg = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "error-message-container")))
            assert "Epic sadface: Username and password do not match any user in this service" in error_msg.text, "Error message not displayed!"

    def sort_items_by_price(self):
        """Sorts inventory items from low to high price."""
        sort_dropdown = self.driver.find_element(By.CLASS_NAME, "product_sort_container")
        sort_dropdown.click()
        sort_dropdown.find_element(By.XPATH, "//option[@value='lohi']").click()

    def add_item_to_cart(self, item_name):
        """Adds an item to the cart."""
        item = self.driver.find_element(By.XPATH, f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']")
        item.find_element(By.CSS_SELECTOR, '.btn_inventory').click()

    def add_item_from_details_page(self, item_name):
        """Navigates to product details page and adds the item to cart."""
        self.driver.find_element(By.XPATH, f"//div[text()='{item_name}']").click()
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn_inventory"))).click()

    def validate_cart_count(self, expected_count):
        """Validates the cart count matches the expected count."""
        try:
            cart_count = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        except:
            cart_count = "0"
        assert cart_count == str(expected_count), f"Expected {expected_count} items, but found {cart_count}"

    def remove_item_from_cart(self, price_range):
        """Removes an item from the cart within the specified price range ($8-$10)."""
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        for item in items:
            price = float(item.find_element(By.CLASS_NAME, "inventory_item_price").text.replace("$", ""))
            if price_range[0] <= price <= price_range[1]:
                item.find_element(By.CLASS_NAME, "cart_button").click()
                break

    def checkout(self, first_name, last_name, postal_code):
        """Performs checkout operation."""
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        self.wait.until(EC.element_to_be_clickable((By.ID, 'checkout'))).click()
        self.driver.find_element(By.ID, 'first-name').send_keys(first_name)
        self.driver.find_element(By.ID, 'last-name').send_keys(last_name)
        self.driver.find_element(By.ID, 'postal-code').send_keys(postal_code)
        self.driver.find_element(By.ID, 'continue').click()

    def validate_checkout_total(self):
        """Prints the total amount from checkout overview page."""
        total_amount = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))).text
        print(f"Total Amount: {total_amount}")

    def complete_purchase(self):
        """Completes the purchase process and validates success message."""
        self.driver.find_element(By.ID, "finish").click()
        success_message = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))).text
        assert success_message == "THANK YOU FOR YOUR ORDER", "Order confirmation failed!"

    def logout(self):
        """Logs out and validates redirection to the login page."""
        self.driver.find_element(By.ID, 'react-burger-menu-btn').click()
        self.wait.until(EC.element_to_be_clickable((By.ID, 'logout_sidebar_link'))).click()
        self.wait.until(EC.url_to_be(self.url))  # Ensures logout redirects to login page

def pytest_runtest_logreport(report):
    """Customize the test result output to show 'PASS' or 'FAIL'."""
    if report.when == "call":  # Only log actual test run results
        if report.passed:
            print(f"\n✅ TEST PASSED: {report.nodeid}")
        elif report.failed:
            print(f"\n❌ TEST FAILED: {report.nodeid}")
        elif report.skipped:
            print(f"\n⚠️ TEST SKIPPED: {report.nodeid}")

# ----- Pytest Setup & Test Cases -----

@pytest.fixture(scope="module")
def setup():
    """Initializes WebDriver and cleans up after tests."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()

def test_valid_login(setup):
    automation = SauceDemoAutomation(setup)
    automation.open_site()
    automation.login("standard_user", "secret_sauce")
    automation.validate_login(valid=True)

def test_invalid_login(setup):
    automation = SauceDemoAutomation(setup)
    automation.open_site()
    automation.login("invalid_user", "wrong_password")
    automation.validate_login(valid=False)

def test_add_items_inventory(setup):
    automation = SauceDemoAutomation(setup)
    automation.open_site()
    automation.login("standard_user", "secret_sauce")
    automation.sort_items_by_price()
    automation.add_item_to_cart("Sauce Labs Backpack")
    automation.add_item_to_cart("Sauce Labs Bike Light")
    automation.validate_cart_count(2)

def test_add_item_from_details(setup):
    automation = SauceDemoAutomation(setup)
    automation.open_site()
    automation.login("standard_user", "secret_sauce")
    automation.add_item_from_details_page("Sauce Labs Onesie")
    automation.validate_cart_count(3)

def test_remove_item(setup):
    automation = SauceDemoAutomation(setup)
    automation.open_site()
    automation.login("standard_user", "secret_sauce")
    automation.remove_item_from_cart((8, 10))
    automation.validate_cart_count(2)

def test_checkout(setup):
    automation = SauceDemoAutomation(setup)
    automation.open_site()
    automation.login("standard_user", "secret_sauce")
    automation.checkout("Yashwardhan", "Katkamwar", "440034")
    automation.validate_checkout_total()
    automation.complete_purchase()

def test_logout(setup):
    automation = SauceDemoAutomation(setup)
    automation.open_site()
    automation.login("standard_user", "secret_sauce")
    automation.logout()

if __name__ == "__main__":
    pytest.main()
