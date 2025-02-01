import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config import BASE_URL, VALID_USERNAME, VALID_PASSWORD, INVALID_USERNAME, INVALID_PASSWORD

@pytest.fixture
def setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_login_valid(setup):
    login_page = LoginPage(setup)
    login_page.open_login_page(BASE_URL)
    login_page.login(VALID_USERNAME, VALID_PASSWORD)
    assert "/inventory.html" in setup.current_url

def test_login_invalid(setup):
    login_page = LoginPage(setup)
    login_page.open_login_page(BASE_URL)
    login_page.login(INVALID_USERNAME, INVALID_PASSWORD)
    assert "Epic sadface: Username and password do not match" in login_page.get_error_message()

def test_add_to_cart(setup):
    login_page = LoginPage(setup)
    inventory_page = InventoryPage(setup)

    login_page.open_login_page(BASE_URL)
    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    inventory_page.sort_items_low_to_high()
    inventory_page.add_items_to_cart()
    assert inventory_page.get_cart_count() == "1"
