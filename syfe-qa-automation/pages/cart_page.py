from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.cart_icon = (By.CLASS_NAME, "shopping_cart_link")
        self.checkout_button = (By.ID, "checkout")

    def open_cart(self):
        """Opens the shopping cart"""
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.cart_icon)).click()

    def proceed_to_checkout(self):
        """Clicks on the checkout button"""
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.checkout_button)).click()
