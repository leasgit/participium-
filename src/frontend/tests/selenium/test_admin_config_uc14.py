import time
import uuid
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ui_helpers import user_login, find_by_id

def test_manage_categories_success_uc14(driver):
    wait = WebDriverWait(driver, 10)

    # 0. Precondition: Admin user is logged in
    user_login(driver, wait, "admin@example.com", "Admin123!")

    time.sleep(3)

    wait.until(EC.visibility_of_element_located((By.ID, "admin-create-category-title")))

    # 1. Main Scenario: Create a new category
    create_category_button = find_by_id(driver, "admin-new-category-submit")
    name_input = find_by_id(driver, "admin-new-category-name")

    unique_category_name = f"Test Category {uuid.uuid4().hex[:6]}"
    name_input.clear()
    name_input.send_keys(unique_category_name)

    time.sleep(1)

    create_category_button.click()

    time.sleep(1)

    # 2. Assertions: Success Guarantee
    success_message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "success-text")))
    assert "category created" in success_message.text.lower(), "Success message should be displayed after creating a category."

    driver.refresh()

    time.sleep(1)

    wait.until(EC.visibility_of_element_located((By.ID, "admin-categories-title")))

    new_category_input = driver.find_elements(By.XPATH, f'//input[starts-with(@id, "admin-category-name-") and @value="{unique_category_name}"]')
    assert len(new_category_input) == 1, "New category should be visible in the list after creation."

def test_manage_categories_duplicate_uc14(driver):
    wait = WebDriverWait(driver, 10)

    # 0. Precondition: Admin user is logged in
    user_login(driver, wait, "admin@example.com", "Admin123!")

    time.sleep(3)

    wait.until(EC.visibility_of_element_located((By.ID, "admin-create-category-title")))

    # 1. Main Scenario: Attempt to create a duplicate category
    create_category_button = find_by_id(driver, "admin-new-category-submit")
    name_input = find_by_id(driver, "admin-new-category-name")

    duplicate_category_name = "Architectural Barriers"

    name_input.clear()
    name_input.send_keys(duplicate_category_name)

    time.sleep(1)

    create_category_button.click()

    time.sleep(1)

    # 3. Assertions: Minimum Guarantees
    error_message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "error-text")))

    assert "already exists" in error_message.text.lower(), "Error message should be displayed when trying to create a duplicate category."

    driver.refresh()

    time.sleep(1)

    existing_category_input = driver.find_elements(By.XPATH, f'//input[starts-with(@id, "admin-category-name-") and @value="{duplicate_category_name}"]')
    assert len(existing_category_input) == 1, "New category should be visible in the list after creation."

def test_manage_categories_deactivate_uc14(driver):
    wait = WebDriverWait(driver, 10)

    # 0. Precondition: Admin user is logged in
    user_login(driver, wait, "admin@example.com", "Admin123!")

    time.sleep(3)

    wait.until(EC.visibility_of_element_located((By.ID, "admin-create-category-title")))

    # 1. Setup: Create a new category to deactivate
    create_category_button = find_by_id(driver, "admin-new-category-submit")
    name_input = find_by_id(driver, "admin-new-category-name")

    unique_category_name = f"Test Category {uuid.uuid4().hex[:6]}"
    name_input.clear()
    name_input.send_keys(unique_category_name)
    time.sleep(1)
    create_category_button.click()

    time.sleep(1)

    wait.until(EC.visibility_of_element_located((By.ID, "admin-categories-title")))

    time.sleep(1)

    # 2. Main Scenario: Deactivate the category
    category_input_path =  f'//input[starts-with(@id, "admin-category-name-") and @value="{unique_category_name}"]'
    active_checkbox = driver.find_element(By.XPATH, f'{category_input_path}/following::input[@type="checkbox"]')
    active_checkbox.click()

    time.sleep(1)

    save_btn = driver.find_element(By.XPATH, f'{category_input_path}/following::button[contains(@id, "admin-category-save-")]')
    save_btn.click()
    time.sleep(1)

    # 3. Assertions: Success Guarantee
    success_message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "success-text")))
    assert "updated" in success_message.text.lower(), "Success message should be displayed after updating a category."

    driver.refresh()

    time.sleep(1)

    reloaded_checkbox = driver.find_element(By.XPATH, f'{category_input_path}/following::input[@type="checkbox"]')
    assert not reloaded_checkbox.is_selected(), "Category should be deactivated after saving changes."
