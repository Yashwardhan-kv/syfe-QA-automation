import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from selenium.webdriver.common.by import By

@pytest.fixture(scope="function")
def setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

class TestCheckout:

    def test_checkout_process(self, setup):
        """Test the complete checkout process"""
        # Login
        login_page = LoginPage(setup)
        login_page.open_login_page("https://www.saucedemo.com")
        login_page.login("standard_user", "secret_sauce")

        # Add items to cart
        cart_page = CartPage(setup)
        cart_page.add_items_to_cart()

        # Proceed to checkout
        checkout_page = CheckoutPage(setup)
        checkout_page.proceed_to_checkout()

        # Validate the total amount
        total_amount = setup.find_element(By.CLASS_NAME, "summary_total_label").text
        assert float(total_amount[1:]) > 0, "Total amount is incorrect"

    def test_checkout_validation(self, setup):
        """Test checkout validation"""
        # Login
        login_page = LoginPage(setup)
        login_page.open_login_page("https://www.saucedemo.com")
        login_page.login("standard_user", "secret_sauce")

        # Add items to cart
        cart_page = CartPage(setup)
        cart_page.add_items_to_cart()

        # Proceed to checkout
        checkout_page = CheckoutPage(setup)
        checkout_page.proceed_to_checkout()

        # Validate checkout
        checkout_page.validate_checkout()  # This function should handle final validation steps
