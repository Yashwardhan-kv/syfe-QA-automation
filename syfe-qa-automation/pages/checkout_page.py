from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.first_name = (By.ID, "first-name")
        self.last_name = (By.ID, "last-name")
        self.postal_code = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.finish_button = (By.ID, "finish")
        self.success_message = (By.CLASS_NAME, "complete-header")

    def fill_checkout_form(self, first, last, postal):
        """Fills in the checkout form"""
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.first_name)).send_keys(first)
        self.driver.find_element(*self.last_name).send_keys(last)
        self.driver.find_element(*self.postal_code).send_keys(postal)
        self.driver.find_element(*self.continue_button).click()

    def complete_purchase(self):
        """Clicks the finish button to complete the purchase"""
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.finish_button)).click()

    def get_success_message(self):
        """Returns the order completion message"""
        return self.driver.find_element(*self.success_message).text
