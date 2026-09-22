import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    """ Global fixture to initialize and quit the WebDriver for each test. """
    options = Options()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "autofill.profile_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    
    d = webdriver.Chrome(options=options)
    yield d
    d.quit()