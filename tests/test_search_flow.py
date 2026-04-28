import pytest
from pages.home_page import HomePage


@pytest.mark.parametrize("keyword", ["kulaklik", "laptop", "phone"])
def test_search_flow_from_homepage(driver, base_url, keyword):
    home = HomePage(driver)

    # 1. Navigate to homepage
    home.open_homepage(base_url)

    # 2. Wait until homepage is loaded
    home.wait_until_loaded()

    # 3. Verify homepage title
    assert home.is_loaded()

    # 4. Type keyword into search box and submit search
    home.search_for_product(keyword)

    # 5. Wait for search results page
    home.wait_for_search_results(keyword)

    # 6. Verify results page URL
    assert keyword.lower() in home.current_url().lower() or f"_nkw={keyword.lower()}" in home.current_url().lower()