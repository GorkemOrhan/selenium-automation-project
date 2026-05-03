from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


class HomePage(BasePage):
    SEARCH_INPUT = (By.NAME, "_nkw")
    SEARCH_BUTTON_LOCATORS = (
        (By.ID, "gh-btn"),
        (By.ID, "gh-search-btn"),
        (By.CSS_SELECTOR, "#gh-f button[type='submit']"),
        (By.CSS_SELECTOR, "#gh-f input[type='submit']"),
        (By.CSS_SELECTOR, "header button[type='submit']"),
        (By.CSS_SELECTOR, "[data-marko*='Search'] button[type='submit']"),
        (
            By.XPATH,
            "//input[@name='_nkw']/ancestor::form//button[@type='submit']",
        ),
        (
            By.XPATH,
            "//input[@name='_nkw']/ancestor::form//input[@type='submit']",
        ),
    )
    RESULT_ITEMS = (
        (By.CSS_SELECTOR, "ul.srp-results li.s-item"),
        (By.CSS_SELECTOR, "li.s-item"),
        (By.CSS_SELECTOR, "[data-view*='mi:1686|iid']"),
    )
    RESULT_ITEM_LINKS = (
        (By.CSS_SELECTOR, "ul.srp-results li.s-item a.s-item__link"),
        (By.CSS_SELECTOR, "a.s-item__link"),
        (By.CSS_SELECTOR, "a[href*='/itm/']"),
    )
    PRODUCT_TITLE = (
        (By.CSS_SELECTOR, "h1.x-item-title__mainTitle span"),
        (By.CSS_SELECTOR, "h1.x-item-title__mainTitle .ux-textspans"),
        (By.CSS_SELECTOR, "h1 span.ux-textspans"),
    )

    # Open the homepage using the provided URL.
    def open_homepage(self, url):
        self.open(url)

    # Wait until the homepage title confirms the page is loaded.
    def wait_until_loaded(self):
        WebDriverWait(self.driver, self.timeout).until(
            EC.title_contains("eBay")
        )

    # Check whether the homepage title indicates a loaded state.
    def is_loaded(self):
        return "eBay" in self.get_title()

    # Enter a product name and submit the homepage search form.
    def search_for_product(self, product_name):
        search_input = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        )
        search_input.clear()
        search_input.send_keys(product_name)
        search_button = WebDriverWait(self.driver, self.timeout).until(
            lambda d: self._resolve_search_submit_after_input(search_input)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", search_button
        )
        try:
            search_button.click()
        except (ElementClickInterceptedException, ElementNotInteractableException):
            self.driver.execute_script("arguments[0].click();", search_button)

    # Wait until the search results URL reflects the searched keyword.
    def wait_for_search_results(self, keyword):
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: keyword.lower() in d.current_url.lower()
            or f"_nkw={keyword.lower()}" in d.current_url.lower()
        )

    # Wait until at least one results container or product link is available.
    def wait_for_results_list(self):
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: len(self._get_product_links()) > 0
            or len(self._find_first_non_empty(self.RESULT_ITEMS)) > 0
        )

    # Return the number of detected product result links.
    def get_results_count(self):
        self.wait_for_results_list()
        return len(self._get_product_links())

    # Check whether the results page contains any visible results.
    def has_results(self):
        return self.get_results_count() > 0 or len(self._find_first_non_empty(self.RESULT_ITEMS)) > 0

    # Open the first available product result.
    def click_first_result(self):
        links = WebDriverWait(self.driver, self.timeout).until(
            lambda d: self._get_product_links()
        )
        first_link = links[0]
        current_window = self.driver.current_window_handle
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_link)
        target_href = first_link.get_attribute("href")

        if target_href:
            self.driver.get(target_href)
        else:
            try:
                first_link.click()
            except (ElementClickInterceptedException, ElementNotInteractableException):
                try:
                    self.driver.execute_script("arguments[0].click();", first_link)
                except Exception:
                    raise

        WebDriverWait(self.driver, self.timeout).until(
            lambda d: len(d.window_handles) > 1 or "/itm/" in d.current_url.lower()
        )

        if len(self.driver.window_handles) > 1:
            for handle in self.driver.window_handles:
                if handle != current_window:
                    self.driver.switch_to.window(handle)
                    break

    # Wait until the product detail page has a valid title and URL.
    def wait_for_product_detail_loaded(self):
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.current_url != "about:blank" and d.title.strip() != ""
        )

    # Return the most reliable product title found on the detail page.
    def get_product_title(self):
        for locator in self.PRODUCT_TITLE:
            elements = self.driver.find_elements(*locator)
            for element in elements:
                text = element.text.strip()
                if text:
                    return text
        page_title = self.driver.title.strip()
        if page_title and "ebay" not in page_title.lower():
            return page_title
        return page_title

    # Resolve the best submit control related to the active search input.
    def _resolve_search_submit_after_input(self, search_input):
        try:
            submit = search_input.find_element(
                By.XPATH,
                "./ancestor::form//*[@type='submit']",
            )
            if submit.is_displayed() and submit.is_enabled():
                return submit
        except (NoSuchElementException, StaleElementReferenceException):
            pass
        return self._find_clickable_search_button()

    # Find the first visible and enabled search button candidate.
    def _find_clickable_search_button(self):
        for locator in self.SEARCH_BUTTON_LOCATORS:
            for element in self.driver.find_elements(*locator):
                try:
                    if element.is_displayed() and element.is_enabled():
                        return element
                except Exception:
                    continue
        return False

    # Return the first locator group that produces elements.
    def _find_first_non_empty(self, locators):
        for locator in locators:
            elements = self.driver.find_elements(*locator)
            if elements:
                return elements
        return []

    # Collect enabled product links that point to item detail pages.
    def _get_product_links(self):
        links = self._find_first_non_empty(self.RESULT_ITEM_LINKS)
        product_links = []
        for link in links:
            href = (link.get_attribute("href") or "").lower()
            if "/itm/" in href and link.is_enabled():
                product_links.append(link)
        return product_links
