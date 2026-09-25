from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def fill(self, locator, value):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(value)

    def find_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_present(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_until_loaded(self):
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def wait_for_toast(self, text):
        locator = ("xpath", f"//*[contains(@class,'oxd-toast-content')]//*[contains(normalize-space(),'{text}')]")
        return self.find_visible(locator)
