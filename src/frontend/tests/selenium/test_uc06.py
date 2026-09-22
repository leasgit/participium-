import os
import re

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:5173")
INVALID_REPORT_ID = os.getenv("INVALID_REPORT_ID", "999999")


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--window-size=1440,1000")
    # 本地调试保留可视浏览器；CI 中可打开 headless。
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


def first_public_report_row(driver, timeout: int = 10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, "//tr[starts-with(@id, 'public-report-row-')]")
        )
    )


def extract_report_id_from_row_id(row_id: str) -> str:
    match = re.fullmatch(r"public-report-row-(\d+)", row_id)
    assert match is not None, f"Unexpected public report row id: {row_id}"
    return match.group(1)


def read_public_report_summary(driver, row_id: str) -> dict[str, str]:
    return {
        "id_text": driver.find_element(By.ID, f"{row_id}-id").text.strip(),
        "title": driver.find_element(By.ID, f"{row_id}-title").text.strip(),
        "status": driver.find_element(By.ID, f"{row_id}-status").text.strip(),
        "category": driver.find_element(By.ID, f"{row_id}-category").text.strip(),
    }


def wait_visible_photos(driver, timeout: int = 10):
    def condition(d):
        photo_images = d.find_elements(By.XPATH, "//*[starts-with(@id, 'photo-item-')]")
        visible_photo = [img for img in photo_images if img.is_displayed()]

        if visible_photo: 
            return visible_photo
        return False

    return WebDriverWait(driver, timeout).until(condition)


def test_uc06_view_selected_report_detail(driver):
    """
    UC06 - View report details.

    Visitor selects a published report from the public table view and sees the
    complete public detail page: title, description, category, map location,
    photos section, current status, and available status updates.
    """
    driver.get(FRONTEND_BASE_URL)

    wait_visible(driver, "home-page")
    wait_visible(driver, "public-report-table")

    row = first_public_report_row(driver)
    row_id = row.get_attribute("id")
    report_id = extract_report_id_from_row_id(row_id)
    summary = read_public_report_summary(driver, row_id)

    assert summary["title"], "Selected report title should not be empty."
    assert summary["status"], "Selected report status should not be empty."
    assert summary["category"], "Selected report category should not be empty."

    open_link = wait_clickable(driver, f"{row_id}-open-link")
    click_element(driver, open_link)

    WebDriverWait(driver, 10).until(
        EC.url_contains(f"/reports/{report_id}")
    )

    wait_visible(driver, "report-detail-page")

    detail_title = wait_visible(driver, "report-detail-title").text.strip()
    detail_status = wait_visible(driver, "report-detail-status").text.strip()
    detail_description = wait_visible(driver, "report-detail-description").text.strip()
    detail_category = wait_visible(driver, "report-detail-category-value").text.strip()
    detail_reporter = wait_visible(driver, "report-detail-reporter-value").text.strip()
    detail_created = wait_visible(driver, "report-detail-created-value").text.strip()
    detail_updated = wait_visible(driver, "report-detail-updated-value").text.strip()

    assert detail_title == summary["title"], (
        f"Detail title should match selected report. "
        f"Expected {summary['title']!r}, got {detail_title!r}."
    )

    assert summary["status"] in detail_status, (
        f"Detail status should contain selected report status. "
        f"Expected {summary['status']!r}, got {detail_status!r}."
    )

    assert detail_description, "Report detail description should be visible and non-empty."

    assert detail_category == summary["category"], (
        f"Detail category should match selected report category. "
        f"Expected {summary['category']!r}, got {detail_category!r}."
    )

    assert detail_reporter, "Report detail reporter display name should be visible."
    assert detail_created, "Report detail created date should be visible."
    assert detail_updated, "Report detail updated date should be visible."

    wait_visible(driver, "report-detail-map-card")
    wait_visible(driver, "report-detail-map")

    marker_id = f"public-report-row-{report_id}-map-marker"
    wait_visible(driver, marker_id)

    wait_visible(driver, "report-detail-photos-card")
    wait_visible(driver, "report-detail-photo-grid")
    
    visible_photos = wait_visible_photos(driver)

    assert len(visible_photos)>=1, (
        "Report detail should display at least one attached photo."   
    )

    assert len(visible_photos <=3),(
        f"Report detail should display at most 3 attached photos, "
        f"but displayed {len(visible_photos)}."
    )

    wait_visible(driver, "status-history-card")
    wait_visible(driver, "status-history-list")

    wait_visible(driver, "messages-card")
    wait_visible(driver, "messages-title")

    unavailable_messages = driver.find_elements(By.ID, "messages-unavailable")
    message_lists = driver.find_elements(By.ID, "messages-list")

    assert unavailable_messages or message_lists, (
        "Report detail should expose either an unavailable conversation message "
        "or a message list, depending on visitor permissions."
    )


def test_uc06_unavailable_report_detail(driver):
    """
    UC06 extension 2a - Report no longer available.

    Visitor opens a non-existing report detail route and sees a controlled
    unavailable/error state, not a partial report detail page.
    """
    driver.get(f"{FRONTEND_BASE_URL}/reports/{INVALID_REPORT_ID}")

    wait_visible(driver, "report-detail-page")
    error_message = wait_visible(driver, "report-detail-error").text.strip()

    assert error_message, "Unavailable report page should show a clear error message."

    assert len(driver.find_elements(By.ID, "report-detail-title")) == 0, (
        "Unavailable report page must not show a normal report title."
    )

    assert len(driver.find_elements(By.ID, "report-detail-description")) == 0, (
        "Unavailable report page must not show partial report description."
    )

    assert len(driver.find_elements(By.ID, "report-detail-category-value")) == 0, (
        "Unavailable report page must not show partial report category."
    )

    assert len(driver.find_elements(By.ID, "report-detail-map")) == 0, (
        "Unavailable report page must not show a report map."
    )

    assert len(driver.find_elements(By.ID, "report-detail-photo-grid")) == 0, (
        "Unavailable report page must not show report photos."
    )