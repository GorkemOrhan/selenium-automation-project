from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage(BasePage):
    SEARCH_INPUT = (By.NAME, "_nkw")

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