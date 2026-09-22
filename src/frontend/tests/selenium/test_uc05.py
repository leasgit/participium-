import os
import re

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:5173")


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


def public_report_rows(driver):
    return driver.find_elements(
        By.XPATH,
        "//tr[starts-with(@id, 'public-report-row-')]",
    )


def wait_for_at_least_one_public_report(driver, timeout: int = 10):
    return WebDriverWait(driver, timeout).until(
        lambda d: public_report_rows(d) if len(public_report_rows(d)) > 0 else False
    )


def wait_for_no_public_reports(driver, timeout: int = 10):
    WebDriverWait(driver, timeout).until(
        lambda d: len(public_report_rows(d)) == 0
    )


def extract_report_id_from_row_id(row_id: str) -> str:
    match = re.fullmatch(r"public-report-row-(\d+)", row_id)
    assert match is not None, f"Unexpected public report row id: {row_id}"
    return match.group(1)


def read_public_report_row(driver, row_id: str) -> dict[str, str]:
    return {
        "id": driver.find_element(By.ID, f"{row_id}-id").text.strip(),
        "title": driver.find_element(By.ID, f"{row_id}-title").text.strip(),
        "status": driver.find_element(By.ID, f"{row_id}-status").text.strip(),
        "category": driver.find_element(By.ID, f"{row_id}-category").text.strip(),
    }


def read_all_public_report_rows(driver) -> list[dict[str, str]]:
    rows = public_report_rows(driver)
    result = []

    for row in rows:
        row_id = row.get_attribute("id")
        result.append(read_public_report_row(driver, row_id))

    return result


def select_by_visible_text(driver, select_id: str, visible_text: str):
    select = Select(wait_visible(driver, select_id))
    select.select_by_visible_text(visible_text)


def set_datetime_local(driver, input_id: str, value: str):
    element = wait_visible(driver, input_id)

    driver.execute_script(
        """
        const input = arguments[0];
        const value = arguments[1];
        const setter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype,
            "value"
        ).set;

        setter.call(input, value);
        input.dispatchEvent(new Event("input", { bubbles: true }));
        input.dispatchEvent(new Event("change", { bubbles: true }));
        """,
        element,
        value,
    )


def clear_datetime_local(driver, input_id: str):
    set_datetime_local(driver, input_id, "")


def submit_filters(driver):
    button = wait_clickable(driver, "public-filter-submit")
    click_element(driver, button)


def wait_until_all_rows_match_category(driver, expected_category: str, timeout: int = 10):
    def condition(d):
        rows = read_all_public_report_rows(d)
        return rows if rows and all(row["category"] == expected_category for row in rows) else False

    return WebDriverWait(driver, timeout).until(condition)


def wait_until_all_rows_match_status(driver, expected_status: str, timeout: int = 10):
    def condition(d):
        rows = read_all_public_report_rows(d)
        return rows if rows and all(row["status"] == expected_status for row in rows) else False

    return WebDriverWait(driver, timeout).until(condition)


def test_uc05_search_and_filter_reports(driver):
    """
    UC05 - Search and filter reports.

    Visitor opens the public table view, filters published reports by category,
    status, and time period, changes sorting, and sees an empty result when no
    report matches the selected filters.
    """
    driver.get(FRONTEND_BASE_URL)

    wait_visible(driver, "home-page")
    wait_visible(driver, "public-filter-section")
    wait_visible(driver, "public-filter-form")
    wait_visible(driver, "public-report-table")

    wait_visible(driver, "public-filter-category")
    wait_visible(driver, "public-filter-status")
    wait_visible(driver, "public-filter-date-from")
    wait_visible(driver, "public-filter-date-to")
    wait_visible(driver, "public-filter-sort")
    wait_visible(driver, "public-filter-submit")

    rows = wait_for_at_least_one_public_report(driver)
    first_row = rows[0]
    first_row_id = first_row.get_attribute("id")
    first_report_id = extract_report_id_from_row_id(first_row_id)
    first_report_before = read_public_report_row(driver, first_row_id)

    assert first_report_before["title"], "Seed public report title should not be empty."
    assert first_report_before["status"], "Seed public report status should not be empty."
    assert first_report_before["category"], "Seed public report category should not be empty."

    # Step 1: filter by category.
    select_by_visible_text(
        driver,
        "public-filter-category",
        first_report_before["category"],
    )
    submit_filters(driver)

    category_filtered_rows = wait_until_all_rows_match_category(
        driver,
        first_report_before["category"],
    )

    assert len(category_filtered_rows) > 0, (
        "Category filter should keep at least the selected seed report visible."
    )

    # Step 2: filter by status while category filter is still active.
    select_by_visible_text(
        driver,
        "public-filter-status",
        first_report_before["status"],
    )
    submit_filters(driver)

    status_filtered_rows = wait_until_all_rows_match_status(
        driver,
        first_report_before["status"],
    )

    assert len(status_filtered_rows) > 0, (
        "Status filter should keep at least the selected seed report visible."
    )

    for row in status_filtered_rows:
        assert row["category"] == first_report_before["category"], (
            f"Combined category/status filter returned wrong category. "
            f"Expected {first_report_before['category']!r}, got {row['category']!r}."
        )
        assert row["status"] == first_report_before["status"], (
            f"Combined category/status filter returned wrong status. "
            f"Expected {first_report_before['status']!r}, got {row['status']!r}."
        )

    # Step 3: change sorting control.
    sort_select = Select(wait_visible(driver, "public-filter-sort"))

    sort_select.select_by_value("asc")
    submit_filters(driver)
    assert Select(wait_visible(driver, "public-filter-sort")).first_selected_option.get_attribute("value") == "asc"

    wait_for_at_least_one_public_report(driver)

    sort_select = Select(wait_visible(driver, "public-filter-sort"))
    sort_select.select_by_value("desc")
    submit_filters(driver)
    assert Select(wait_visible(driver, "public-filter-sort")).first_selected_option.get_attribute("value") == "desc"

    wait_for_at_least_one_public_report(driver)

    # Step 4: valid time-period filter with no matching reports.
    set_datetime_local(driver, "public-filter-date-from", "2999-01-01T00:00")
    set_datetime_local(driver, "public-filter-date-to", "2999-12-31T23:59")
    submit_filters(driver)

    wait_for_no_public_reports(driver)

    assert len(public_report_rows(driver)) == 0, (
        "Future date range should produce an empty public report table."
    )

    # Step 5: remove date filters and verify filtering did not mutate report data.
    clear_datetime_local(driver, "public-filter-date-from")
    clear_datetime_local(driver, "public-filter-date-to")
    submit_filters(driver)

    restored_row_id = f"public-report-row-{first_report_id}"
    restored_row = wait_visible(driver, restored_row_id)
    assert restored_row.is_displayed(), "Original public report row should become visible again."

    first_report_after = read_public_report_row(driver, restored_row_id)

    assert first_report_after["title"] == first_report_before["title"], (
        "Filtering must not change the stored report title."
    )
    assert first_report_after["status"] == first_report_before["status"], (
        "Filtering must not change the stored report status."
    )
    assert first_report_after["category"] == first_report_before["category"], (
        "Filtering must not change the stored report category."
    )