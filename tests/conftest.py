import sys
from pathlib import Path

import pytest

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
    return "https://www.ebay.com/"


@pytest.fixture
def driver(browser_name):
    web_driver = create_driver(browser_name)
    yield web_driver
    web_driver.quit()
