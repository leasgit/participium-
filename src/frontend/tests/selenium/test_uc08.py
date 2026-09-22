"""UC-08 — Export reports as CSV from the public table view."""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

FRONTEND_BASE_URL = "http://localhost:5173"
DEFAULT_WAIT = 10


def go_to(driver, path):
    driver.get(f"{FRONTEND_BASE_URL}{path}")


def scroll_and_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    element.click()


def open_public_table(driver):
    go_to(driver, "/")
    WebDriverWait(driver, DEFAULT_WAIT).until(
        EC.visibility_of_element_located((By.ID, "public-report-table"))
    )


def set_datetime_local(driver, input_id, value):
    element = WebDriverWait(driver, DEFAULT_WAIT).until(
        EC.visibility_of_element_located((By.ID, input_id))
    )
    driver.execute_script(
        """
        const input = arguments[0];
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(input, arguments[1]);
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        """,
        element, value,
    )


def submit_filters(driver):
    btn = WebDriverWait(driver, DEFAULT_WAIT).until(
        EC.element_to_be_clickable((By.ID, "public-filter-submit"))
    )
    scroll_and_click(driver, btn)


def count_rows(driver):
    return len(driver.find_elements(By.XPATH, "//tr[starts-with(@id,'public-report-row-')]"))


class TestExportCSV:
    """UC-08: Export reports as CSV."""

    def test_export_button_visible(self, driver):
        """CSV export button is visible and enabled on the public table view."""
        open_public_table(driver)
        btn = WebDriverWait(driver, DEFAULT_WAIT).until(
            EC.presence_of_element_located((By.ID, "public-export-link"))
        )
        assert btn.is_displayed(), "CSV export button must be visible on the table view"
        assert btn.is_enabled(), "CSV export button must be enabled when reports are present"

    def test_export_does_not_navigate_away(self, driver):
        """Clicking export stays on the table view."""
        open_public_table(driver)
        url_before = driver.current_url

        btn = WebDriverWait(driver, DEFAULT_WAIT).until(
            EC.element_to_be_clickable((By.ID, "public-export-link"))
        )
        scroll_and_click(driver, btn)

        WebDriverWait(driver, DEFAULT_WAIT).until(lambda d: d.current_url == url_before)
        assert driver.current_url == url_before, "Clicking export must not navigate away from the table view"

    def test_export_after_category_filter(self, driver):
        """Export works after applying a category filter."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        open_public_table(driver)

        first_row = wait.until(
            EC.presence_of_element_located((By.XPATH, "//tr[starts-with(@id,'public-report-row-')]"))
        )
        row_id = first_row.get_attribute("id")
        category = driver.find_element(By.ID, f"{row_id}-category").text.strip()

        Select(wait.until(EC.visibility_of_element_located((By.ID, "public-filter-category")))).select_by_visible_text(category)
        submit_filters(driver)
        wait.until(EC.presence_of_element_located((By.XPATH, "//tr[starts-with(@id,'public-report-row-')]")))

        url_before = driver.current_url
        btn = wait.until(EC.element_to_be_clickable((By.ID, "public-export-link")))
        scroll_and_click(driver, btn)

        WebDriverWait(driver, DEFAULT_WAIT).until(lambda d: d.current_url == url_before)
        assert driver.current_url == url_before, "CSV export after category filter must not navigate away"

    def test_export_after_status_filter(self, driver):
        """Export works after applying a status filter."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        open_public_table(driver)

        first_row = wait.until(
            EC.presence_of_element_located((By.XPATH, "//tr[starts-with(@id,'public-report-row-')]"))
        )
        row_id = first_row.get_attribute("id")
        status = driver.find_element(By.ID, f"{row_id}-status").text.strip()

        Select(wait.until(EC.visibility_of_element_located((By.ID, "public-filter-status")))).select_by_visible_text(status)
        submit_filters(driver)
        wait.until(EC.presence_of_element_located((By.XPATH, "//tr[starts-with(@id,'public-report-row-')]")))

        url_before = driver.current_url
        btn = wait.until(EC.element_to_be_clickable((By.ID, "public-export-link")))
        scroll_and_click(driver, btn)

        WebDriverWait(driver, DEFAULT_WAIT).until(lambda d: d.current_url == url_before)
        assert driver.current_url == url_before, "CSV export after status filter must not navigate away"

    def test_export_empty_result(self, driver):
        """No crash or navigation when exporting an empty result set."""
        open_public_table(driver)

        set_datetime_local(driver, "public-filter-date-from", "2999-01-01T00:00")
        set_datetime_local(driver, "public-filter-date-to", "2999-12-31T23:59")
        submit_filters(driver)

        WebDriverWait(driver, DEFAULT_WAIT).until(lambda d: count_rows(d) == 0)
        assert count_rows(driver) == 0, "Future date range must produce an empty table"

        export_btns = driver.find_elements(By.ID, "public-export-link")
        if export_btns and export_btns[0].is_enabled():
            url_before = driver.current_url
            scroll_and_click(driver, export_btns[0])
            WebDriverWait(driver, DEFAULT_WAIT).until(lambda d: d.current_url == url_before)
            assert driver.current_url == url_before, "Export on empty result must not navigate away"

        body = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert "uncaught" not in body, "Page must not show a JS error after export on empty result"

    def test_anonymous_report_hides_identity(self, driver):
        """Anonymous report rows must not contain an email address (NFR-04)."""
        open_public_table(driver)
        WebDriverWait(driver, DEFAULT_WAIT).until(
            EC.presence_of_element_located((By.XPATH, "//tr[starts-with(@id,'public-report-row-')]"))
        )

        rows = driver.find_elements(By.XPATH, "//tr[starts-with(@id,'public-report-row-')]")
        violations = [
            row.get_attribute("id") for row in rows
            if ("anonymous" in row.text.lower() or "anonimo" in row.text.lower())
            and "@" in row.text
        ]
        assert len(violations) == 0, f"Anonymous rows exposing identity: {violations}"