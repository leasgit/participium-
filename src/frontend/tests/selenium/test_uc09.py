"""UC-09 — Public statistics: visitors can view reports by category and time trends."""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from ui_helpers import find_by_id_return_num

FRONTEND_BASE_URL = "http://localhost:5173"
DEFAULT_WAIT = 10


def go_to(driver, path):
    driver.get(f"{FRONTEND_BASE_URL}{path}")


def scroll_and_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    element.click()


def open_stats(driver):
    # stats are on the home page, not a separate route
    go_to(driver, "/")
    WebDriverWait(driver, DEFAULT_WAIT).until(
        EC.presence_of_element_located((By.ID, "public-statistics-card"))
    )


def click_aggregation(driver, label):
    """Try to click the day/week/month aggregation control. Returns True if found."""
    # the control is a <select> with id public-stat-granularity
    try:
        sel_el = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "public-stat-granularity"))
        )
        Select(sel_el).select_by_visible_text(label)
        return True
    except Exception:
        pass

    # fallback: individual option elements
    opt_id = f"public-stat-granularity-option-{label.lower()}"
    btns = driver.find_elements(By.ID, opt_id)
    if btns and btns[0].is_enabled():
        scroll_and_click(driver, btns[0])
        return True

    return False


class TestPublicStatistics:
    """UC-09: Public statistics page."""

    def test_page_accessible_without_login(self, driver):
        """Statistics are accessible to unauthenticated visitors on the home page."""
        go_to(driver, "/")
        WebDriverWait(driver, DEFAULT_WAIT).until(
            EC.presence_of_element_located((By.ID, "public-statistics-card"))
        )
        assert "/login" not in driver.current_url, (
            "Public stats must not redirect visitors to /login"
        )

    def test_category_stats_rendered(self, driver):
        """At least one category stat element is displayed."""
        open_stats(driver)
        WebDriverWait(driver, DEFAULT_WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[starts-with(@id,'public-category-stat-')]")
            )
        )
        stats = driver.find_elements(By.XPATH, "//*[starts-with(@id,'public-category-stat-')]")
        assert len(stats) > 0, "At least one public-category-stat element must be rendered"

    def test_category_stats_have_content(self, driver):
        """Each category stat is visible and has text."""
        open_stats(driver)
        WebDriverWait(driver, DEFAULT_WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[starts-with(@id,'public-category-stat-')]")
            )
        )
        for stat in driver.find_elements(By.XPATH, "//*[starts-with(@id,'public-category-stat-')]"):
            assert stat.is_displayed(), f"Category stat '{stat.get_attribute('id')}' must be visible"
            assert stat.text.strip() != "", f"Category stat '{stat.get_attribute('id')}' must have text"

    def test_aggregation_control_present(self, driver):
        """A day/week/month aggregation control is present on the page."""
        open_stats(driver)

        found = (
            find_by_id_return_num(driver, "public-stat-granularity") > 0
            or any(
                find_by_id_return_num(driver, f"public-stat-granularity-option-{l}") > 0
                for l in ("day", "week", "month")
            )
        )
        assert found, "Aggregation control (day/week/month) must be present"

    def test_changing_aggregation_does_not_crash(self, driver):
        """Switching aggregation keeps the page stable with no JS errors."""
        open_stats(driver)

        clicked = any(click_aggregation(driver, l) for l in ("Week", "Month", "Day"))
        if not clicked:
            pytest.skip("Aggregation control not found")

        WebDriverWait(driver, DEFAULT_WAIT).until(
            EC.presence_of_element_located((By.ID, "public-statistics-card"))
        )
        body = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert body.strip() != "", "Page must not be blank after changing aggregation"
        assert "uncaught" not in body, "Page must not show a JS error after changing aggregation"

    def test_trend_stats_or_empty_state(self, driver):
        """Trend stats are shown, or an empty state appears — no errors."""
        open_stats(driver)

        try:
            WebDriverWait(driver, DEFAULT_WAIT).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[starts-with(@id,'public-trend-stat-')]")
                )
            )
            stats = driver.find_elements(By.XPATH, "//*[starts-with(@id,'public-trend-stat-')]")
            assert len(stats) > 0, "public-trend-stat elements found but count is zero"
        except TimeoutException:
            body = driver.find_element(By.TAG_NAME, "body").text.lower()
            assert "uncaught" not in body, "No trend data: must show empty state, not a JS error"
            assert body.strip() != "", "No trend data: page body must not be blank"

    def test_empty_period_no_error(self, driver):
        """Selecting day aggregation on sparse data shows empty state, not an error."""
        open_stats(driver)
        click_aggregation(driver, "Day")

        WebDriverWait(driver, DEFAULT_WAIT).until(
            EC.presence_of_element_located((By.ID, "public-statistics-card"))
        )
        body = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert "uncaught" not in body, "Day aggregation must not produce a JS error"
        assert body.strip() != "", "Page must not be blank after selecting Day aggregation"

    def test_admin_stats_not_visible(self, driver):
        """Admin-only stats are not visible on the public statistics page."""
        go_to(driver, "/")
        WebDriverWait(driver, DEFAULT_WAIT).until(
            EC.presence_of_element_located((By.ID, "public-statistics-card"))
        )
        assert len(driver.find_elements(By.XPATH, "//*[starts-with(@id,'admin-metric-item-')]")) == 0, (
            "admin-metric-item elements must not appear on the public stats page"
        )
        assert len(driver.find_elements(By.XPATH, "//*[starts-with(@id,'admin-user-row-')]")) == 0, (
            "admin-user-row elements must not appear on the public stats page"
        )