import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False, help="run tests in headless mode")

@pytest.fixture(scope="function")
def driver(request):
    headless = request.config.getoption("--headless")
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        if "driver" in item.fixturenames:
            web_driver = item.funcargs["driver"]
            # Create reports and screenshots directory
            base_dir = os.path.dirname(os.path.abspath(__file__))
            reports_dir = os.path.join(base_dir, "reports")
            screenshots_dir = os.path.join(reports_dir, "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            test_name = item.name
            file_name = f"{test_name}_{now}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            
            web_driver.save_screenshot(file_path)
            
            # Embed in Pytest HTML Report
            extra = getattr(rep, "extra", [])
            relative_path = f"screenshots/{file_name}"
            
            try:
                import pytest_html
                extra.append(pytest_html.extras.image(relative_path))
            except Exception:
                # Direct HTML tag fallback
                html = f'<div><img src="{relative_path}" alt="screenshot" style="width:300px;height:225px;" onclick="window.open(this.src)" align="right"/></div>'
                extra.append(html)
            
            rep.extra = extra
