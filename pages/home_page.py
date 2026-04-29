from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException


class HomePage(BasePage):
    SEARCH_INPUT = (By.NAME, "_nkw")
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

    def open_homepage(self, url):
        self.open(url)

    def wait_until_loaded(self):
        WebDriverWait(self.driver, self.timeout).until(
            EC.title_contains("eBay")
        )

    def is_loaded(self):
        return "eBay" in self.get_title()

    def search_for_product(self, product_name):
        search_input = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        )
        search_input.clear()
        search_input.send_keys(product_name)
        search_input.send_keys(Keys.ENTER)

    def wait_for_search_results(self, keyword):
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: keyword.lower() in d.current_url.lower()
            or f"_nkw={keyword.lower()}" in d.current_url.lower()
        )

    def wait_for_results_list(self):
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: len(self._get_product_links()) > 0
            or len(self._find_first_non_empty(self.RESULT_ITEMS)) > 0
        )

    def get_results_count(self):
        self.wait_for_results_list()
        return len(self._get_product_links())

    def has_results(self):
        return self.get_results_count() > 0 or len(self._find_first_non_empty(self.RESULT_ITEMS)) > 0

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

    def wait_for_product_detail_loaded(self):
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.current_url != "about:blank" and d.title.strip() != ""
        )

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

    def _find_first_non_empty(self, locators):
        for locator in locators:
            elements = self.driver.find_elements(*locator)
            if elements:
                return elements
        return []

    def _get_product_links(self):
        links = self._find_first_non_empty(self.RESULT_ITEM_LINKS)
        product_links = []
        for link in links:
            href = (link.get_attribute("href") or "").lower()
            if "/itm/" in href and link.is_enabled():
                product_links.append(link)
        return product_links