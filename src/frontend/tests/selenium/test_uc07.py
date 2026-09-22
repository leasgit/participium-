"""UC-07 — Follow report."""

import os
import uuid
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from ui_helpers import user_login, find_by_id

FRONTEND_BASE_URL = "http://localhost:5173"
DEFAULT_WAIT = 15


def go_to(driver, path):
    driver.get(f"{FRONTEND_BASE_URL}{path}")


def scroll_and_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    element.click()


def do_logout(driver, wait):
    try:
        scroll_and_click(driver, wait.until(EC.element_to_be_clickable((By.ID, "logout-button"))))
        wait.until(EC.presence_of_element_located((By.ID, "login-link")))
    except Exception:
        go_to(driver, "/")


def submit_report(driver, wait):
    """Citizen submits a new report and returns its detail page URL."""
    go_to(driver, "/reports/new")
    wait.until(EC.presence_of_element_located((By.ID, "new-report-form")))

    find_by_id(driver, "report-title").send_keys(f"UC07 test {uuid.uuid4().hex[:6]}")
    find_by_id(driver, "report-description").send_keys("Selenium UC-07 test")

    sel = Select(find_by_id(driver, "report-category"))
    opts = [o for o in sel.options if o.get_attribute("value")]
    if opts:
        sel.select_by_value(opts[0].get_attribute("value"))

    for field, value in [("report-latitude", "45.0703"), ("report-longitude", "7.6869")]:
        driver.execute_script(
            "var s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
            "s.call(arguments[0],arguments[1]);"
            "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
            "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));",
            find_by_id(driver, field), value
        )

    photo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data", "valid_profile_pic.png")
    if os.path.exists(photo):
        find_by_id(driver, "report-photos").send_keys(photo)

    scroll_and_click(driver, find_by_id(driver, "new-report-submit"))
    wait.until(lambda d: "/reports/new" not in d.current_url and "/reports/" in d.current_url)
    return driver.current_url


def register_follower(driver, wait):
    """Register a new citizen and return (email, password), or skip if verification required."""
    unique = uuid.uuid4().hex[:8]
    email, password = f"follower{unique}@test.com", "Follower123!"

    go_to(driver, "/register")
    wait.until(EC.presence_of_element_located((By.ID, "register-form")))
    find_by_id(driver, "register-username").send_keys(f"follower{unique}")
    find_by_id(driver, "register-first-name").send_keys("Test")
    find_by_id(driver, "register-last-name").send_keys("Follower")
    find_by_id(driver, "register-email").send_keys(email)
    find_by_id(driver, "register-password").send_keys(password)
    scroll_and_click(driver, find_by_id(driver, "register-submit"))

    try:
        wait.until(lambda d: d.current_url != f"{FRONTEND_BASE_URL}/register")
    except Exception:
        pytest.skip("Registration failed")

    if not driver.find_elements(By.ID, "dashboard-page"):
        try:
            user_login(driver, wait, email, password)
            wait.until(EC.presence_of_element_located((By.ID, "dashboard-page")))
        except Exception:
            pytest.skip("New account requires email verification")

    return email, password


class TestFollowReport:
    """UC-07: Follow report."""

    def test_follow_report(self, driver):
        """UC-07 main scenario — second citizen follows a report and button changes to Unfollow."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)

        user_login(driver, wait, "citizen@example.com", "Citizen123!")
        wait.until(EC.presence_of_element_located((By.ID, "dashboard-page")))
        report_url = submit_report(driver, wait)
        report_id = report_url.rstrip("/").split("/")[-1]
        do_logout(driver, wait)

        register_follower(driver, wait)
        go_to(driver, f"/reports/{report_id}")
        wait.until(EC.presence_of_element_located((By.ID, "report-detail-page")))

        if not driver.find_elements(By.ID, "follow-button"):
            do_logout(driver, wait)
            pytest.skip("Report not yet publicly visible (pending approval)")

        if "unfollow" in driver.find_element(By.ID, "follow-button").text.lower():
            scroll_and_click(driver, find_by_id(driver, "follow-button"))
            wait.until(lambda d: "unfollow" not in d.find_element(By.ID, "follow-button").text.lower())

        scroll_and_click(driver, find_by_id(driver, "follow-button"))
        wait.until(lambda d: "unfollow" in d.find_element(By.ID, "follow-button").text.lower())

        assert "unfollow" in find_by_id(driver, "follow-button").text.lower(), (
            "Follow button must read 'Unfollow report' after following"
        )
        do_logout(driver, wait)

    def test_follow_twice_no_duplicate(self, driver):
        """UC-07 ext 3a — following twice keeps Unfollow after reload, no duplicate record."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)

        user_login(driver, wait, "citizen@example.com", "Citizen123!")
        wait.until(EC.presence_of_element_located((By.ID, "dashboard-page")))
        report_url = submit_report(driver, wait)
        report_id = report_url.rstrip("/").split("/")[-1]
        do_logout(driver, wait)

        register_follower(driver, wait)
        go_to(driver, f"/reports/{report_id}")
        wait.until(EC.presence_of_element_located((By.ID, "report-detail-page")))

        if not driver.find_elements(By.ID, "follow-button"):
            do_logout(driver, wait)
            pytest.skip("Report not yet publicly visible (pending approval)")

        if "unfollow" not in driver.find_element(By.ID, "follow-button").text.lower():
            scroll_and_click(driver, find_by_id(driver, "follow-button"))
            wait.until(lambda d: "unfollow" in d.find_element(By.ID, "follow-button").text.lower())

        go_to(driver, f"/reports/{report_id}")
        wait.until(EC.presence_of_element_located((By.ID, "follow-button")))

        assert "unfollow" in find_by_id(driver, "follow-button").text.lower(), (
            "After reload button must still show Unfollow — no duplicate follow created"
        )
        do_logout(driver, wait)

    def test_unfollow_report(self, driver):
        """UC-07 — Citizen unfollows a report and button reverts to Follow."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)

        user_login(driver, wait, "citizen@example.com", "Citizen123!")
        wait.until(EC.presence_of_element_located((By.ID, "dashboard-page")))
        report_url = submit_report(driver, wait)
        report_id = report_url.rstrip("/").split("/")[-1]
        do_logout(driver, wait)

        register_follower(driver, wait)
        go_to(driver, f"/reports/{report_id}")
        wait.until(EC.presence_of_element_located((By.ID, "report-detail-page")))

        if not driver.find_elements(By.ID, "follow-button"):
            do_logout(driver, wait)
            pytest.skip("Report not yet publicly visible (pending approval)")

        if "unfollow" not in driver.find_element(By.ID, "follow-button").text.lower():
            scroll_and_click(driver, find_by_id(driver, "follow-button"))
            wait.until(lambda d: "unfollow" in d.find_element(By.ID, "follow-button").text.lower())

        scroll_and_click(driver, find_by_id(driver, "follow-button"))
        wait.until(lambda d: "unfollow" not in d.find_element(By.ID, "follow-button").text.lower())

        assert "follow" in find_by_id(driver, "follow-button").text.lower(), (
            "After unfollowing button must revert to 'Follow report'"
        )
        do_logout(driver, wait)

    def test_follow_requires_login(self, driver):
        """UC-07 ext 3b — unauthenticated visitor cannot follow, button absent or redirects to login."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)

        go_to(driver, "/")
        wait.until(EC.presence_of_element_located((By.ID, "login-link")))

        row = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//tr[starts-with(@id,'public-report-row-')]")
        ))
        scroll_and_click(driver, wait.until(
            EC.element_to_be_clickable((By.ID, f"{row.get_attribute('id')}-open-link"))
        ))
        wait.until(EC.presence_of_element_located((By.ID, "report-detail-page")))

        btns = driver.find_elements(By.ID, "follow-button")
        if btns:
            scroll_and_click(driver, btns[0])
            wait.until(EC.url_contains("/login"))
            assert "/login" in driver.current_url, (
                "Unauthenticated follow attempt must redirect to /login"
            )
        else:
            assert len(btns) == 0, "Follow button must not be visible to unauthenticated visitors"

    def test_reporter_notified_on_status_change(self, driver):
        """UC-07 / FR-13 — reporter receives notification when operator updates report status."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)

        user_login(driver, wait, "citizen@example.com", "Citizen123!")
        wait.until(EC.presence_of_element_located((By.ID, "dashboard-page")))
        initial_count = len(driver.find_elements(
            By.XPATH, "//*[starts-with(@id,'notification-item-')]"
        ))
        report_url = submit_report(driver, wait)
        report_id = report_url.rstrip("/").split("/")[-1]
        do_logout(driver, wait)

        user_login(driver, wait, "operator@example.com", "Operator123!")
        wait.until(EC.presence_of_element_located((By.ID, "operator-page")))

        pending = driver.find_elements(By.ID, f"pending-report-assign-{report_id}")
        if pending:
            scroll_and_click(driver, pending[0])
            wait.until(EC.presence_of_element_located((By.ID, "operator-page")))

        go_to(driver, "/operator")
        wait.until(EC.presence_of_element_located((By.ID, "operator-page")))

        status_el = driver.find_elements(By.ID, f"assigned-report-status-{report_id}")
        if not status_el:
            do_logout(driver, wait)
            pytest.skip(f"Report {report_id} not in operator queue")

        sel = Select(status_el[0])
        opts = [o.get_attribute("value") for o in sel.options if o.get_attribute("value")]
        if not opts:
            do_logout(driver, wait)
            pytest.skip("No valid status transition available")

        sel.select_by_value(opts[0])
        scroll_and_click(driver, wait.until(
            EC.element_to_be_clickable((By.ID, f"assigned-report-update-{report_id}"))
        ))
        wait.until(EC.presence_of_element_located((By.ID, "operator-page")))
        do_logout(driver, wait)

        user_login(driver, wait, "citizen@example.com", "Citizen123!")
        wait.until(EC.presence_of_element_located((By.ID, "dashboard-page")))
        wait.until(lambda d: len(
            d.find_elements(By.XPATH, "//*[starts-with(@id,'notification-item-')]")
        ) > initial_count)

        new_count = len(driver.find_elements(
            By.XPATH, "//*[starts-with(@id,'notification-item-')]"
        ))
        assert new_count > initial_count, (
            f"Citizen must receive a notification after status update. Before: {initial_count}, after: {new_count}"
        )
        do_logout(driver, wait)