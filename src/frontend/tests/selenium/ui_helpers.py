from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

def find_by_id(driver, widget_id):
    """ Support function to find an element by its ID. """
    return driver.find_element(By.ID, widget_id)

def find_by_id_return_num(driver, widget_id):
    """ Support function to find elements by ID and return the count. """
    elements = driver.find_elements(By.ID, widget_id)
    return len(elements)

def find_by_xpath(driver, xpath):
    """ Support function to find an element by its XPath. """
    return driver.find_element(By.XPATH, xpath)

def user_login(driver, wait, username, password):
    """ Support function to log in a user. """
    driver.get("http://localhost:5173")

    wait.until(EC.element_to_be_clickable((By.ID, 'login-link')))

    login_link = find_by_id(driver, 'login-link')
    login_link.click()

    wait.until(EC.visibility_of_element_located((By.ID, 'login-identifier')))
    time.sleep(1)

    email_box = find_by_id(driver, 'login-identifier')
    email_box.clear()
    email_box.send_keys(username)
    time.sleep(1)
    
    password_box = find_by_id(driver, 'login-password')
    password_box.clear()
    password_box.send_keys(password)
    time.sleep(1)

    submit_btn = find_by_id(driver, 'login-submit')
    submit_btn.click()