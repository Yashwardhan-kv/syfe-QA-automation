import pytest
from selenium import webdriver
from pages.login_page import LoginPage  # Import the LoginPage class
from pages.cart_page import CartPage  # Import the CartPage class
from selenium.webdriver.common.by import By

@pytest.fixture(scope="function")
def setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

class TestAddItemsToCart:
    def test_add_items_to_cart(self, setup):
        login_page = LoginPage(setup)  # Create an instance of LoginPage
        login_page.login("standard_user", "secret_sauce")  # Login using the login method
        cart_page = CartPage(setup)  # Create an instance of CartPage
        cart_page.open_cart()  # Open the cart
        cart_page.add_items_to_cart()  # Call add_items_to_cart method from CartPage
        cart_count = setup.find_element(By.CLASS_NAME, "shopping_cart_badge").text  # Get cart count
        assert cart_count == "2", "Items not added to cart"

    def test_add_item_from_product_page(self, setup):
        login_page = LoginPage(setup)  # Create an instance of LoginPage
        login_page.login("standard_user", "secret_sauce")  # Login using the login method
        cart_page = CartPage(setup)  # Create an instance of CartPage
        cart_page.add_items_from_product_page()  # Add item from the product page
        cart_count = setup.find_element(By.CLASS_NAME, "shopping_cart_badge").text  # Get cart count
        assert cart_count == "3", "Item not added from product page"

class TestRemoveItemsFromCart:
    def test_remove_item_from_cart(self, setup):
        login_page = LoginPage(setup)  # Create an instance of LoginPage
        login_page.login("standard_user", "secret_sauce")  # Login using the login method
        cart_page = CartPage(setup)  # Create an instance of CartPage
        cart_page.add_items_to_cart()  # Add items to cart first
        cart_page.remove_items_from_cart()  # Remove items from cart
        cart_count = setup.find_element(By.CLASS_NAME, "shopping_cart_badge").text  # Get cart count
        assert cart_count == "1", "Item not removed from cart"
