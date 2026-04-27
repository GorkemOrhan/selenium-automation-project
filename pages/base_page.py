from utils.wait_helpers import (
    DEFAULT_TIMEOUT,
    wait_for_clickable,
    wait_for_presence,
    wait_for_visibility,
    wait_for_url_to_contain,
)


class BasePage:
    """Common page helpers shared across page objects."""

    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout

    def open(self, url):
        self.driver.get(url)

    def find_visible(self, locator, timeout=None):
        return wait_for_visibility(self.driver, locator, timeout or self.timeout)

    def find_clickable(self, locator, timeout=None):
        return wait_for_clickable(self.driver, locator, timeout or self.timeout)

    def find_present(self, locator, timeout=None):
        return wait_for_presence(self.driver, locator, timeout or self.timeout)

    def click(self, locator, timeout=None):
        element = self.find_clickable(locator, timeout)
        element.click()

    def type_text(self, locator, text, clear_first=True, timeout=None):
        element = self.find_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator, timeout=None):
        element = self.find_visible(locator, timeout)
        return element.text

    def get_title(self):
        return self.driver.title

    def current_url(self):
        return self.driver.current_url

    def wait_for_url_to_contain(self, keyword, timeout=None):
        wait_for_url_to_contain(self.driver, keyword, timeout or self.timeout)