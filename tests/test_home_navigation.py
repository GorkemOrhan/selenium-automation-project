from pages.home_page import HomePage


# Verify that the homepage opens and reports a valid title.
def test_homepage_navigation_and_title(driver, base_url):
    home = HomePage(driver)

    # 1. Navigation
    home.open_homepage(base_url)

    # 2. Wait until the homepage is fully loaded
    home.wait_until_loaded()

    # 3. Assertion
    assert home.is_loaded()
