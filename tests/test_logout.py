import pytest
from selenium import webdriver
from pages.login_page import LoginPage  # Import the LoginPage class

class TestLogout:
    @pytest.fixture(scope="function")
    def setup(self):
        """Setup WebDriver before each test and quit after"""
        driver = webdriver.Chrome()
        driver.maximize_window()
        yield driver
        driver.quit()

    def test_logout(self, setup):
        """Test for logout"""
        login_page = LoginPage(setup)
        login_page.open_login_page("https://www.saucedemo.com")  # Open login page
        login_page.login("standard_user", "secret_sauce")  # Perform login
        # Logout (you will need to define the logout method in your LoginPage or another page)
        login_page.logout()  # Assuming you have implemented a logout method
        # Validate successful logout, for example, checking the login page is displayed again
        assert "login" in setup.current_url, "Logout failed"
