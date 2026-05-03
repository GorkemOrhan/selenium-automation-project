from pages.base_page import BasePage


# Verify that the homepage title is not empty after loading.
def test_hepsiburada_homepage_title_is_not_empty(driver, base_url):
    base_page = BasePage(driver)
    base_page.open(base_url)

    assert base_page.get_title().strip() != ""
