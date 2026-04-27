from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class HomePage(BasePage):
    # Locators
    SEARCH_INPUT = (By.CSS_SELECTOR, '[data-test-id="search-bar-input"]')
    PAGE_READY_INDICATOR = (By.CSS_SELECTOR, '[data-test-id="search-bar-input"]')

    def open_homepage(self, base_url: str):
        self.open(base_url)

    def wait_until_loaded(self, timeout: int = 15):
        """Sayfanın yüklendiğini arama kutusunun görünür olmasıyla doğrula."""
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.PAGE_READY_INDICATOR),
            message="Ana sayfa yüklenemedi: arama kutusu görünür olmadı."
        )

    def is_loaded(self) -> bool:
        """Sayfa yüklendi mi? Boolean döner, exception fırlatmaz."""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.PAGE_READY_INDICATOR)
            )
            return True
        except Exception:
            return False

    def search_for_product(self, keyword: str):
        """
        Arama kutusuna keyword yazar ve Enter ile aramayı tetikler.
        - Önce kutuyu tıklanabilir hale gelmesi için bekler
        - Var olan içeriği temizler
        - Keyword'ü yazar
        - RETURN ile aramayı başlatır
        """
        search_box = self.find_clickable(*self.SEARCH_INPUT)
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)