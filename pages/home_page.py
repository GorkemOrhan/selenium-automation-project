from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage(BasePage):

    def open_homepage(self, url):
        self.open(url)

    def wait_until_loaded(self):
        WebDriverWait(self.driver, self.timeout).until(
            EC.title_contains("Hepsiburada")
        )

    def is_loaded(self):
        return "Hepsiburada" in self.get_title()