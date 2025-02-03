import pytest
from selenium import webdriver
from pages.login_page import LoginPage  # Correct import

@pytest.fixture(scope="function")
def setup():
    """Setup WebDriver before each test and quit after"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

class TestLogin:

    def test_valid_login(self, setup):
        """Test for valid login"""
        login_page = LoginPage(setup)
        login_page.open_login_page("https://www.saucedemo.com")  # Open login page
        login_page.login("standard_user", "secret_sauce")  # Perform login
        # Validate successful login
        assert "inventory" in setup.current_url, "Login failed"

    def test_invalid_login_username(self, setup):
        """Test for invalid username"""
        login_page = LoginPage(setup)
        login_page.open_login_page("https://www.saucedemo.com")  # Open login page
        login_page.login("invalid_user", "secret_sauce")  # Attempt login with invalid username
        # Validate error message
        error_message = login_page.get_error_message()
        assert "Epic sadface: Username and password do not match any user in this service" in error_message, "Error message not displayed"

    def test_invalid_login_password(self, setup):
        """Test for invalid password"""
        login_page = LoginPage(setup)
        login_page.open_login_page("https://www.saucedemo.com")  # Open login page
        login_page.login("standard_user", "wrong_password")  # Attempt login with wrong password
        # Validate error message
        error_message = login_page.get_error_message()
        assert "Epic sadface: Username and password do not match any user in this service" in error_message, "Error message not displayed"
