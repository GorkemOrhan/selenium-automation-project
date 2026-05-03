import pytest
from pages.home_page import HomePage


@pytest.mark.parametrize("keyword", ["kulaklik", "laptop", "phone"])
# Verify that searching from the homepage leads to a valid product detail page.
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

    # 7. Verify results are visible and not empty
    home.wait_for_results_list()
    assert home.has_results(), "No product results were found on search results page."

    # 8. Click the first returned product
    home.click_first_result()

    # 9. Verify selected product detail information
    assert home.get_product_title() != "", "Product title is empty on detail page."
