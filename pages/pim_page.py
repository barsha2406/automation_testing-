from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class PimPage(BasePage):
    PIM_MENU = (By.XPATH, "//span[normalize-space()='PIM']/ancestor::a")
    ADD_EMPLOYEE = (By.XPATH, "//a[normalize-space()='Add Employee']")
    FIRST_NAME = (By.NAME, "firstName")
    LAST_NAME = (By.NAME, "lastName")
    EMPLOYEE_ID = (By.XPATH, "//label[normalize-space()='Employee Id']/ancestor::div[contains(@class,'oxd-input-group')]//input")
    PHOTO = (By.CSS_SELECTOR, "input[type='file']")
    SAVE = (By.CSS_SELECTOR, "button[type='submit']")
    PERSONAL_DETAILS = (By.XPATH, "//h6[normalize-space()='Personal Details']")
    EMPLOYEE_LIST = (By.XPATH, "//a[normalize-space()='Employee List']")
    SEARCH = (By.XPATH, "//button[normalize-space()='Search']")
    JOB_TAB = (By.XPATH, "//a[normalize-space()='Job']")
    CONFIRM_DELETE = (By.XPATH, "//button[normalize-space()='Yes, Delete']")

    def open_add_employee(self):
        self.click(self.PIM_MENU)
        self.click(self.ADD_EMPLOYEE)
        self.find_visible(self.FIRST_NAME)

    def add_employee(self, first_name, last_name, employee_id, photo_path):
        self.fill(self.FIRST_NAME, first_name)
        self.fill(self.LAST_NAME, last_name)
        self.fill(self.EMPLOYEE_ID, employee_id)
        self.find_present(self.PHOTO).send_keys(str(photo_path))
        self.click(self.SAVE)
        self.find_visible(self.PERSONAL_DETAILS)
        url_tail = self.driver.current_url.rstrip("/").split("/")[-1]
        assert url_tail.isdigit(), f"Could not derive employee number from URL: {self.driver.current_url}"
        return int(url_tail)

    def _employee_id_search_field(self):
        return (By.XPATH, "//label[normalize-space()='Employee Id']/ancestor::div[contains(@class,'oxd-input-group')]//input")

    def row_for(self, employee_id):
        return (By.XPATH, f"//div[contains(@class,'oxd-table-card')][.//div[normalize-space()='{employee_id}']]")

    def search_by_employee_id(self, employee_id):
        self.click(self.PIM_MENU)
        self.click(self.EMPLOYEE_LIST)
        self.find_visible(self._employee_id_search_field())
        self.fill(self._employee_id_search_field(), employee_id)
        self.click(self.SEARCH)
        self.wait.until(lambda d: d.find_elements(*self.row_for(employee_id)) or "No Records Found" in d.page_source)

    def open_employee(self, employee_id):
        self.search_by_employee_id(employee_id)
        row = self.find_visible(self.row_for(employee_id))
        # Click the employee ID/name cell's first clickable link where available.
        links = row.find_elements(By.CSS_SELECTOR, "a")
        if links:
            links[0].click()
        else:
            cells = row.find_elements(By.CSS_SELECTOR, ".oxd-table-cell")
            cells[1].click()
        self.find_visible(self.PERSONAL_DETAILS)

    def update_job(self, employee_id, job_title, employment_status):
        self.open_employee(employee_id)
        self.click(self.JOB_TAB)
        self.wait.until(EC.url_contains("viewJobDetails"))
        self._choose_dropdown("Job Title", job_title)
        self._choose_dropdown("Employment Status", employment_status)
        self.click(self.SAVE)
        self.wait_for_toast("Successfully Updated")
        assert self._dropdown_value("Job Title") == job_title, "Job title was not persisted in UI"
        assert self._dropdown_value("Employment Status") == employment_status, "Employment status was not persisted in UI"

    def _choose_dropdown(self, label, value):
        locator = (By.XPATH, f"//label[normalize-space()='{label}']/ancestor::div[contains(@class,'oxd-input-group')]//div[contains(@class,'oxd-select-text')]")
        self.click(locator)
        self.click((By.XPATH, f"//div[@role='listbox']//span[normalize-space()='{value}']"))

    def _dropdown_value(self, label):
        locator = (By.XPATH, f"//label[normalize-space()='{label}']/ancestor::div[contains(@class,'oxd-input-group')]//div[contains(@class,'oxd-select-text-input')]")
        return self.find_visible(locator).text.strip()

    def delete_employee(self, employee_id):
        self.search_by_employee_id(employee_id)
        row = self.find_visible(self.row_for(employee_id))
        row.find_element(By.CSS_SELECTOR, "button i.bi-trash").click()
        self.click(self.CONFIRM_DELETE)
        self.wait_for_toast("Successfully Deleted")
        self.search_by_employee_id(employee_id)
        assert "No Records Found" in self.driver.page_source, f"Employee {employee_id} still appears after deletion"
