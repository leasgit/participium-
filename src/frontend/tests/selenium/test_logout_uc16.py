import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from ui_helpers import find_by_id, user_login

def test_logout_uc16(driver):
    wait = WebDriverWait(driver, 10)

    # 1. Precondition: User is logged in
    user_login(driver, wait, "citizen@example.com", "Citizen123!")

    wait.until(EC.visibility_of_element_located((By.XPATH, '//h1[text()="User dashboard"]')))

    # 2. Main Scenario: User clicks on the logout button
    logout_btn = find_by_id(driver, 'logout-button')
    logout_btn.click()

    # 3. Asserts: Check Success Guarantees

    wait.until(EC.visibility_of_element_located((By.ID, 'login-identifier')))

    user_dashboard = driver.find_elements(By.XPATH, '//h1[text()="User dashboard"]')
    assert len(user_dashboard) == 0, "User dashboard should not be visible after logout"

    time.sleep(1)

    driver.get("http://localhost:5173/dashboard")

    wait.until(EC.url_contains("/login"))
    assert "/login" in driver.current_url, "User should be redirected to login page when accessing dashboard after logout"

    time.sleep(3)