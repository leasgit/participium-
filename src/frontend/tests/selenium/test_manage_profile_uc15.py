import os

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ui_helpers import user_login, find_by_id

def test_manage_profile_valid_upload_uc15(driver):
    wait = WebDriverWait(driver, 10)

    # 0. Precondition: User is logged in
    user_login(driver, wait, "citizen@example.com", "Citizen123!")

    wait.until(EC.visibility_of_element_located((By.XPATH, '//h1[text()="User dashboard"]')))

    # 1. Main Scenario: Open Manage Profile Page (Steps 1-2)
    wait.until(EC.visibility_of_element_located((By.ID, "profile-email-notifications")))

    notif_checkbox = find_by_id(driver, "profile-email-notifications")
    initial_state = notif_checkbox.is_selected()

    # 2. Main Scenario: Toggle Email Notifications, upload new profile picture and Save (Steps 3-4)
    notif_checkbox.click()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    valid_image_path = os.path.join(current_dir, "test_data", "valid_profile_pic.png")

    assert os.path.exists(valid_image_path), f"ERRORE: Selenium non trova il file in {valid_image_path}"

    file_input = find_by_id(driver, "profile-picture")
    file_input.send_keys(valid_image_path)

    save_btn = find_by_id(driver, "profile-save")
    save_btn.click()

    # 3. Assertions: Success Guarantees

    success_message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "success-text")))
    assert "profile updated" in success_message.text.lower()

    time.sleep(2)

    driver.refresh()

    wait.until(EC.visibility_of_element_located((By.ID, "profile-section")))

    notif_checkbox_reloaded = find_by_id(driver, "profile-email-notifications")
    new_state = notif_checkbox_reloaded.is_selected()

    assert new_state != initial_state, "Email notification setting should be toggled and saved correctly"

    time.sleep(3)

def test_manage_profile_cancel_update_uc15(driver):
    wait = WebDriverWait(driver, 10)

    # 0. Precondition: User is logged in
    user_login(driver, wait, "citizen@example.com", "Citizen123!")

    time.sleep(1)

    wait.until(EC.visibility_of_element_located((By.XPATH, '//h1[text()="User dashboard"]')))

    # 1. Main Scenario: Upload valid Profile Picture, change email notification setting and don't save
    notif_checkbox = find_by_id(driver, "profile-email-notifications")
    initial_state = notif_checkbox.is_selected()
    notif_checkbox.click()
    
    invalid_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data", "valid_profile_pic.png")

    file_input = find_by_id(driver, "profile-picture")
    file_input.send_keys(invalid_image_path)

    driver.refresh()

    time.sleep(1)

    # 2. Assertions: Minimum Guarantees
    wait.until(EC.visibility_of_element_located((By.ID, "profile-section")))
    notif_checkbox_reloaded = find_by_id(driver, "profile-email-notifications")
    reloaded_state = notif_checkbox_reloaded.is_selected()

    assert reloaded_state == initial_state, "Email notification setting should not be changed without saving"
    