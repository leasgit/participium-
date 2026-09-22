import os
import re

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException



FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:5173")


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--window-size=1440,1000")
    # 本地调试想看浏览器就不要启用 headless。
    # CI 或自动跑时可以打开下面这一行。
    # options.add_argument("--headless=new")

    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()


def wait_visible(driver, element_id: str, timeout: int = 10):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, element_id))
    )


def wait_clickable(driver, element_id: str, timeout: int = 10):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.ID, element_id))
    )


def click_element(driver, element):
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
        element,
    )
    try:
        element.click()
    except Exception:
        driver.execute_script("arguments[0].click();", element)

def click_by_id(driver, element_id: str, timeout: int = 10, js_event: bool = False):
    def attempt_click(current_driver):
        try:
            element = current_driver.find_element(By.ID, element_id)
            current_driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                element,
            )

            if js_event:
                return current_driver.execute_script(
                    """
                    const element = document.getElementById(arguments[0]);
                    if (!element) return false;
                    element.dispatchEvent(new MouseEvent('click', {
                        bubbles: true,
                        cancelable: true,
                        view: window
                    }));
                    return true;
                    """,
                    element_id,
                )

            element.click()
            return True

        except StaleElementReferenceException:
            return False

    WebDriverWait(driver, timeout).until(attempt_click)

def first_public_report_row(driver, timeout: int = 10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, "//tr[starts-with(@id, 'public-report-row-')]")
        )
    )


def extract_report_id_from_row(row_id: str) -> str:
    match = re.fullmatch(r"public-report-row-(\d+)", row_id)
    assert match is not None, f"Unexpected public report row id: {row_id}"
    return match.group(1)


def test_uc04_browse_reports_on_map(driver):
    """
    UC04 - Browse reports on map.

    Visitor opens the public portal, sees the public map, selects a report marker,
    sees marker summary information, and opens the selected report detail page.
    """
    driver.get(FRONTEND_BASE_URL)

    wait_visible(driver, "home-page")
    wait_visible(driver, "public-map-card")
    wait_visible(driver, "public-map")

    row = first_public_report_row(driver)
    row_id = row.get_attribute("id")
    report_id = extract_report_id_from_row(row_id)

    title_id = f"{row_id}-title"
    status_id = f"{row_id}-status"
    open_link_id = f"{row_id}-open-link"
    marker_id = f"{row_id}-map-marker"
    popup_id = f"{row_id}-map-popup"

    report_title = wait_visible(driver, title_id).text.strip()
    report_status = wait_visible(driver, status_id).text.strip()

    assert report_title, "Selected public report title should not be empty."
    assert report_status, "Selected public report status should not be empty."

    wait_visible(driver, marker_id)
    click_by_id(driver, marker_id, js_event=True)

    popup = wait_visible(driver, popup_id)
    popup_text = popup.text.strip()

    assert report_title in popup_text, (
        f"Map popup should contain selected report title. "
        f"Expected title: {report_title!r}; popup text: {popup_text!r}"
    )
    assert report_status in popup_text, (
        f"Map popup should contain selected report status. "
        f"Expected status: {report_status!r}; popup text: {popup_text!r}"
    )

    click_by_id(driver, open_link_id)


    WebDriverWait(driver, 10).until(
        EC.url_contains(f"/reports/{report_id}")
    )

    wait_visible(driver, "report-detail-page")
    detail_title = wait_visible(driver, "report-detail-title").text.strip()

    assert detail_title == report_title, (
        f"Detail page should show the selected report. "
        f"Expected title: {report_title!r}; detail title: {detail_title!r}"
    )

    wait_visible(driver, "report-detail-map")