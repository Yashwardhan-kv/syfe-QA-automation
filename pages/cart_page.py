# cart_page.py
from selenium.webdriver.common.by import By  # Add this import for 'By'
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.cart_icon = (By.CLASS_NAME, "shopping_cart_link")
        self.checkout_button = (By.ID, "checkout")
        self.add_to_cart_buttons = (By.CLASS_NAME, "btn_inventory")  # Adjust if needed
        self.remove_button = (By.CLASS_NAME, "cart_button")  # Adjust if needed

    def open_cart(self):
        """Opens the shopping cart"""
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.cart_icon)).click()

    def add_items_to_cart(self):
        """Adds items to the cart"""
        items = self.driver.find_elements(*self.add_to_cart_buttons)
        for item in items:
            item.click()

    def add_items_from_product_page(self):
        """Adds an item from the product page"""
        product_button = self.driver.find_element(By.CLASS_NAME, "btn_primary")  # Adjust if needed
        product_button.click()

    def remove_items_from_cart(self):
        """Removes an item from the cart"""
        remove_button = self.driver.find_element(*self.remove_button)
        remove_button.click()
