from utils.wait_helpers import (
    DEFAULT_TIMEOUT,
    wait_for_clickable,
    wait_for_presence,
    wait_for_visibility,
)


class BasePage:
    """Common page helpers shared across page objects."""

    # Initialize the page with a shared driver and timeout value.
    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout

    # Open the given page URL in the current browser session.
    def open(self, url):
        self.driver.get(url)

    # Return a visible element for the provided locator.
    def find_visible(self, locator, timeout=None):
        return wait_for_visibility(self.driver, locator, timeout or self.timeout)

    # Return a clickable element for the provided locator.
    def find_clickable(self, locator, timeout=None):
        return wait_for_clickable(self.driver, locator, timeout or self.timeout)

    # Return a present element for the provided locator.
    def find_present(self, locator, timeout=None):
        return wait_for_presence(self.driver, locator, timeout or self.timeout)

    # Click the element found by the provided locator.
    def click(self, locator, timeout=None):
        element = self.find_clickable(locator, timeout)
        element.click()

    # Type text into the located element and clear it first if needed.
    def type_text(self, locator, text, clear_first=True, timeout=None):
        element = self.find_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)

    # Read and return the text of the located element.
    def get_text(self, locator, timeout=None):
        element = self.find_visible(locator, timeout)
        return element.text

    # Return the current browser page title.
    def get_title(self):
        return self.driver.title

    # Return the current browser URL.
    def current_url(self):
        return self.driver.current_url
