import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="function")
def setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def wait_for_element(driver, by, value):
    """Helper function to wait for elements to load"""
    wait = WebDriverWait(driver, 20)
    return wait.until(EC.presence_of_element_located((by, value)))

def login(driver, username, password):
    driver.get("https://www.saucedemo.com")
    wait_for_element(driver, By.ID, "user-name").send_keys(username)
    wait_for_element(driver, By.ID, "password").send_keys(password)
    wait_for_element(driver, By.ID, "login-button").click()

def validate_login(driver, valid=True):
    """Validate if the login is successful or if error message appears"""
    if valid:
        WebDriverWait(driver, 10).until(EC.url_contains("/inventory.html"))
        assert driver.current_url == "https://www.saucedemo.com/inventory.html", "Login failed"
    else:
        error_message = wait_for_element(driver, By.XPATH, "//h3[@data-test='error']").text
        assert "Epic sadface: Username and password do not match any user in this service." in error_message, "Error message not displayed"
