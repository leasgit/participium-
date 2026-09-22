import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    
    chrome_driver = webdriver.Chrome(options=options)
    yield chrome_driver
    chrome_driver.quit()

def test_user_lifecycle_and_report_submission(driver):
   
    explicit_wait = WebDriverWait(driver, 10)
    unique_marker = int(time.time())
    
    driver.get("http://localhost:5173/register")[cite: 8]
    
    test_username = f"citizen_{unique_marker}"
    test_email = f"citizen_{unique_marker}@polito.it"
    
        explicit_wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(test_username)
    driver.find_element(By.ID, "email").send_keys(test_email)[cite: 8]
    driver.find_element(By.ID, "password").send_keys("SecureCitizenPassword123!")[cite: 8]
    driver.find_element(By.ID, "first_name").send_keys("Zhaleh")[cite: 8]
    driver.find_element(By.ID, "last_name").send_keys("AI")[cite: 8]
    
    driver.find_element(By.ID, "register-submit").click()[cite: 8]
    
    
    success_banner = explicit_wait.until(
        EC.visibility_of_element_located((By.ID, "registration-success-banner"))
    )
    assert success_banner.is_displayed(), "Registration success interface element not displayed."[cite: 8]

   
    driver.get("http://localhost:5173/login")[cite: 8]
    
    explicit_wait.until(EC.presence_of_element_located((By.ID, "login-identifier"))).send_keys("citizen@example.com")
    driver.find_element(By.ID, "login-password").send_keys("Citizen123!")[cite: 8]
    driver.find_element(By.ID, "login-submit").click()[cite: 8]
    
    explicit_wait.until(EC.url_contains("/dashboard"))
    user_menu = explicit_wait.until(EC.visibility_of_element_located((By.ID, "user-profile-menu")))
    assert user_menu.is_displayed(), "User authentication session interface element not accessible."[cite: 8]

    driver.get("http://localhost:5173/reports/submit")
    
    report_title_input = explicit_wait.until(EC.presence_of_element_located((By.ID, "report-title")))
    dynamic_title = f"Urban Waste Accumulation {unique_marker}"
    
    report_title_input.send_keys(dynamic_title)
    driver.find_element(By.ID, "report-description").send_keys(
        "There is an accumulation of bulk rubbish left near the intersection block."
    )[cite: 8]
    
    category_dropdown = driver.find_element(By.ID, "report-category-select")[cite: 8]
    category_dropdown.click()
    driver.find_element(By.ID, "report-category-option-5").click()
    
    map_viewport = driver.find_element(By.ID, "submission-map")[cite: 8]
    map_viewport.click()
    
    lat_val = driver.find_element(By.ID, "report-latitude").get_attribute("value")
    lng_val = driver.find_element(By.ID, "report-longitude").get_attribute("value")
    assert lat_val and lng_val, "Map pointer click interface failed to populate geolocation boundaries."[cite: 8]
    
    driver.find_element(By.ID, "report-anonymous-toggle").click()
    
    driver.find_element(By.ID, "report-submit-button").click()[cite: 8]
    
    submission_success = explicit_wait.until(
        EC.visibility_of_element_located((By.ID, "submission-success-modal"))
    )
    assert submission_success.is_displayed(), "Report submission receipt asset not confirmed by UI."[cite: 8]