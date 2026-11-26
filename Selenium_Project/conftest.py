import os
import re
import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()
#     if report.when == "call":
#         driver = item.funcargs.get("driver")
#         if driver:
#             status = "PASS" if report.passed else "FAIL"
#             safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", item.name)
#             os.makedirs("evidence", exist_ok=True)
#             driver.save_screenshot(f"evidence/{status}_{safe_name}.png")

# python -m pytest test_w3.py -v
# python -m pytest test_w3.py -v -k "search"
# python -m pytest test_w3.py -v -k "try_it"