from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.cart_icon = (By.CLASS_NAME, "shopping_cart_badge")
        self.sort_dropdown = (By.CLASS_NAME, "product_sort_container")
        self.add_backpack = (By.ID, "add-to-cart-sauce-labs-backpack")

    def sort_items_low_to_high(self):
        dropdown = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.sort_dropdown))
        dropdown.send_keys("Price (low to high)")

    def add_items_to_cart(self):
        self.driver.find_element(*self.add_backpack).click()

    def get_cart_count(self):
        return self.driver.find_element(*self.cart_icon).text
