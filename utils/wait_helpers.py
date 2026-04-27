from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 10


def wait_for_visibility(driver, locator, timeout=DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def wait_for_clickable(driver, locator, timeout=DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )


def wait_for_presence(driver, locator, timeout=DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )


def wait_for_url_to_contain(driver, keyword, timeout=DEFAULT_TIMEOUT):
    try:
        WebDriverWait(driver, timeout).until(
            EC.url_contains(keyword)
        )
    except TimeoutException:
        raise TimeoutException(
            f"URL did not contain '{keyword}'. Current URL: {driver.current_url}"
        )