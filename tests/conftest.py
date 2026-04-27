import sys
from pathlib import Path

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.driver_factory import create_driver


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="all",
        choices=["chrome", "firefox", "all"],
        help="Browser selection: chrome, firefox, or all.",
    )


def pytest_generate_tests(metafunc):
    if "browser_name" not in metafunc.fixturenames:
        return

    selected_browser = metafunc.config.getoption("--browser")
    browsers = ["chrome", "firefox"] if selected_browser == "all" else [selected_browser]
    metafunc.parametrize("browser_name", browsers)


@pytest.fixture
def base_url():
    return "https://www.hepsiburada.com/"


@pytest.fixture
def driver(browser_name):
    web_driver = create_driver(browser_name)
    yield web_driver
    web_driver.quit()


@pytest.fixture(autouse=True)
def handle_popup(driver, base_url):
    """Opens homepage, closes cookie banner, waits for search box to be ready."""
    driver.get(base_url)
    try:
        WebDriverWait(driver, 8).until(
            lambda d: d.execute_script("""
                const host = document.querySelector('efilli-layout-dynamic');
                if (!host || !host.shadowRoot) return false;
                return !!host.shadowRoot.querySelector('#hb-accept-all');
            """)
        )
        driver.execute_script("""
            document.querySelector('efilli-layout-dynamic')
                .shadowRoot.querySelector('#hb-accept-all').click();
        """)
        WebDriverWait(driver, 5).until(
            lambda d: not d.execute_script("""
                const host = document.querySelector('efilli-layout-dynamic');
                if (!host || !host.shadowRoot) return false;
                return !!host.shadowRoot.querySelector('#hb-accept-all');
            """)
        )
    except TimeoutException:
        pass

    # Arama wrapper'ının DOM'da hazır olmasını bekle
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="search"]'))
        )
    except TimeoutException:
        pass

    yield