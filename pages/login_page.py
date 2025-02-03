from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "user-name")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.error_message = (By.XPATH, "//h3[@data-test='error']")

    def open_login_page(self, base_url):
        """Open the login page of the application."""
        self.driver.get(base_url)
    
    def _wait_for_element(self, locator, timeout=10):
        """Helper function to wait for an element to become visible."""
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def login(self, username, password):
        """Perform login action."""
        # Wait for the username field to become visible, then send the username
        self._wait_for_element(self.username_input).send_keys(username)
        # Wait for the password field to become visible, then send the password
        self._wait_for_element(self.password_input).send_keys(password)
        # Wait for the login button to be clickable, then click it
        self._wait_for_element(self.login_button).click()

      
    def logout(self):
        """Perform logout action."""
        # Locate the logout button and click it
        logout_button = (By.ID, "logout-button")  # Assuming there's a logout button with this ID
        self._wait_for_element(logout_button).click()


    def get_error_message(self):
        """Get the error message displayed after a failed login."""
        try:
            # Wait for the error message to be visible, return it
            error_elem = self._wait_for_element(self.error_message, timeout=5)
            return error_elem.text
        except:
            return None  # Return None if no error message is found
