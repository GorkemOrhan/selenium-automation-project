import pytest
from urllib.parse import quote
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException
from pages.home_page import HomePage

SEARCH_WRAPPER = 'div[role="search"]'
SEARCH_INPUT = '[data-test-id="search-bar-input"]'


class TestSearchFlow:

    def _search(self, driver, keyword):
        """Click the search wrapper div, then type in the input."""
        for attempt in range(5):
            try:
                # Wrapper div'e tıkla — bu blocker'ı tetikler ve açar
                wrapper = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, SEARCH_WRAPPER))
                )
                ActionChains(driver).move_to_element(wrapper).click().perform()

                # Input'a yaz
                el = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, SEARCH_INPUT))
                )
                el.send_keys(keyword)
                el.send_keys(Keys.ENTER)
                return
            except (StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException):
                continue
        raise RuntimeError("Could not interact with search box after retries")

    def _wait_for_search_url(self, driver, keyword, timeout=20):
        """Wait for URL to contain keyword or its URL-encoded equivalent."""
        encoded = quote(keyword, safe="")
        WebDriverWait(driver, timeout).until(
            lambda d: keyword in d.current_url.lower() or encoded.lower() in d.current_url.lower(),
            message=f"URL did not contain '{keyword}'. Current URL: {driver.current_url}"
        )

    def test_search_box_is_visible_on_homepage(self, driver, base_url):
        """Search bar should be visible on homepage."""
        home = HomePage(driver)
        home.wait_until_loaded()
        assert home.is_loaded()

    def test_search_box_can_search_product(self, driver, base_url):
        """Searching 'laptop' should result in URL containing 'laptop'."""
        self._search(driver, "laptop")
        self._wait_for_search_url(driver, "laptop")
        assert "laptop" in driver.current_url.lower()

    @pytest.mark.parametrize("keyword", ["telefon", "laptop", "kulaklık"])
    def test_search_works_for_multiple_keywords(self, driver, base_url, keyword):
        """Search results URL should contain the searched keyword."""
        self._search(driver, keyword)
        self._wait_for_search_url(driver, keyword)
        encoded = quote(keyword, safe="")
        assert keyword in driver.current_url.lower() or encoded.lower() in driver.current_url.lower()