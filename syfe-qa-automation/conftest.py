import pytest
from selenium import webdriver

@pytest.fixture(scope="function")
def setup():
    """Setup WebDriver before each test and quit after"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
