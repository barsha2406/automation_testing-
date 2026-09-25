from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import settings

@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1440,1080")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if settings.headless:
        options.add_argument("--headless=new")
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    browser.implicitly_wait(0)
    request.node.driver = browser
    yield browser
    browser.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        browser = getattr(item, "driver", None)
        if browser:
            settings.artifact_dir.mkdir(parents=True, exist_ok=True)
            browser.save_screenshot(str(settings.artifact_dir / f"{item.name}-failure.png"))
