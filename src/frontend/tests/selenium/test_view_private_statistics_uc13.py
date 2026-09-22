import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

from ui_helpers import user_login, find_by_id_return_num

def test_private_stats_citizen_denied_uc13(driver):
    wait = WebDriverWait(driver, 10)

    # 0. Precondition: Login as a citizen
    user_login(driver, wait, "citizen@example.com", "Citizen123!")

    wait.until(EC.presence_of_element_located((By.ID, "dashboard-title")))

    # 1. Attempt to access private statistics
    driver.get("http://localhost:5173/admin")

    # 2. Assertions: Minimum Guarantees
    wait.until(EC.url_changes("http://localhost:5173/admin"))
    assert "admin" not in driver.current_url.lower(), "Citizen should not access admin page"

def test_private_stats_admin_success_uc13(driver):
    wait = WebDriverWait(driver, 10)

    # 0. Precondition: Login as an admin
    user_login(driver, wait, "admin@example.com", "Admin123!")

    # 1. Main Scenario: Access private statistics
    wait.until(EC.presence_of_element_located((By.ID, "admin-title")))

    time.sleep(1)

    # 2. Assertions: Success Guarantees
    assert find_by_id_return_num(driver, 'admin-metric-item-reports-by-status-title') == 1, "Admin should see 'Reports by Status' metric"
    assert find_by_id_return_num(driver, 'admin-metric-item-reports-by-type') == 1, "Admin should see 'Reports by Type' metric"
    assert find_by_id_return_num(driver, 'admin-metric-item-reports-by-reporter') == 1, "Admin should see 'Reports by Reporter' metric"
    assert find_by_id_return_num(driver, 'admin-metric-item-top-1-percent-by-type') == 1, "Admin should see 'Top 1% by Type' metric"
    assert find_by_id_return_num(driver, 'admin-metric-item-top-5-percent-by-type') == 1, "Admin should see 'Top 5% by Type' metric"

