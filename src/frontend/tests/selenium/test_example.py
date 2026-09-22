import pytest

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time


def find_by_id(webdriver, widget_id):
    return webdriver.find_element(By.ID, widget_id)


# @pytest.fixture
# def driver():
#     d = webdriver.Chrome()
#     yield d
#     d.quit()

@pytest.mark.skip(reason="This is just an example test, not meant to be run")
def test_example_1(driver):

    driver.get("URL")

    time.sleep(5)

    #1) find stuff on the page
    pl1 = driver.find_element(By.ID, "id")
    pl2 = driver.find_element(By.XPATH, "xpath")

    #2) interact with stuff
    pl1.click()

    #3) asserting oracles
    time.sleep(2)
    pl_field = driver.find_element(By.XPATH, "xpath")
    assert pl_field.is_displayed


    time.sleep(3)

@pytest.mark.skip(reason="This is just an example test, not meant to be run")
def test_example_2(driver):

    driver.get("URL")

    wait = WebDriverWait(driver, 10)

    wait.until(expected_conditions.element_to_be_clickable((By.ID, 'searchInput')))
    
    search_bar = find_by_id(driver, 'searchInput')

    search_bar.send_keys("text")

    search_btn = driver.find_element(By.CLASS_NAME, "searchButton")

    search_btn.click()

    # Wait for the new page to load

    wait.until(expected_conditions.visibility_of_element_located((By.ID, 'firstHeading')))

    heading = find_by_id(driver, 'firstHeading')

    assert 'text' in heading.text

    time.sleep(5)

@pytest.mark.skip(reason="This is just an example test, not meant to be run")
def test_login_ok(driver):

    driver.get("http://localhost:5173")
    wait = WebDriverWait(driver, 10)

    # wait for the username box to appear
    wait.until(expected_conditions.visibility_of_element_located((By.XPATH, 'path')))
    time.sleep(2)

    # type the username in the box
    username_box = driver.find_element(By.XPATH, 'path')
    username_box.clear()
    username_box.send_keys("admin")

    time.sleep(2)

    # type the password in the box
    password_box = driver.find_element(By.XPATH, 'path')
    password_box.clear()
    password_box.send_keys("admin")

    time.sleep(2)
    
    # click the login button
    login_btn = driver.find_element(By.XPATH, 'path')
    login_btn.click()

    # wait for the profile badge to show
    wait.until(expected_conditions.visibility_of_element_located((By.XPATH, 'path')))
    
    # store the profile badge in a webelement
    profile_badge = driver.find_element(By.XPATH, 'path')
    time.sleep(2)
    assert "admin_demo" in profile_badge.text

    time.sleep(10)