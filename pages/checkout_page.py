from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.checkout_button = (By.ID, "checkout")
        self.first_name_input = (By.ID, "first-name")
        self.last_name_input = (By.ID, "last-name")
        self.zip_code_input = (By.ID, "postal-code")
        self.finish_button = (By.ID, "finish")
        self.summary_total_label = (By.CLASS_NAME, "summary_total_label")

    def proceed_to_checkout(self):
        """Click the checkout button"""
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.checkout_button)
        ).click()  # Click the checkout button once it's clickable

    def fill_checkout_form(self, first_name, last_name, zip_code):
        """Fill out the checkout form with required data"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.first_name_input)).send_keys(first_name)
        self.driver.find_element(*self.last_name_input).send_keys(last_name)
        self.driver.find_element(*self.zip_code_input).send_keys(zip_code)

    def complete_checkout(self):
        """Complete the checkout process"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.finish_button)).click()

    def validate_checkout(self):
        """Validation after checkout"""
        # Ensure that the total label is present (this confirms that checkout details are loaded)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(self.summary_total_label))

        # Validate page title for successful checkout
        print(f"Page Title: {self.driver.title}")
        
        # Check if "Checkout Complete" is in the page title
        assert "Checkout Complete" in self.driver.title, f"Checkout failed: {self.driver.title}"
        
        # Optionally, you could check the presence of confirmation messages or any other element that signifies completion
        # Example: Check if there's a success message on the page (adjust this based on actual confirmation text in your app)
        confirmation_message = (By.CLASS_NAME, "complete-header")  # Change class if necessary
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(confirmation_message))
        print("Checkout successfully completed.")
