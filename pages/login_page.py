from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    DASHBOARD = (By.XPATH, "//h6[normalize-space()='Dashboard']")
    USER_DROPDOWN = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    LOGOUT = (By.XPATH, "//a[normalize-space()='Logout']")
    LOGIN_HEADING = (By.XPATH, "//h5[normalize-space()='Login']")

    def open(self, url):
        self.driver.get(url)
        self.wait_until_loaded()

    def login(self, username, password):
        self.fill(self.USERNAME, username)
        self.fill(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        self.find_visible(self.DASHBOARD)
        assert "/dashboard" in self.driver.current_url.lower(), (
            f"Expected dashboard after login, got {self.driver.current_url}"
        )

    def logout(self, base_url):
        self.click(self.USER_DROPDOWN)
        self.click(self.LOGOUT)
        self.find_visible(self.LOGIN_HEADING)
        assert "login" in self.driver.current_url.lower(), "Logout did not return to login page"
        # Verify session is no longer authorized by opening a protected route.
        self.driver.get(f"{base_url.rstrip('/')}/web/index.php/pim/viewEmployeeList")
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_HEADING))
        assert "login" in self.driver.current_url.lower(), (
            "Protected page remained accessible after logout"
        )
