from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


# Create a WebDriver instance for the requested browser name.
def create_driver(browser_name: str):
    """Create and return a Selenium WebDriver for the requested browser."""
    normalized_browser = browser_name.strip().lower()

    if normalized_browser == "chrome":
        options = ChromeOptions()
        driver = webdriver.Chrome(options=options)
    elif normalized_browser == "firefox":
        options = FirefoxOptions()
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(
            f"Unsupported browser: '{browser_name}'. Supported browsers are: chrome, firefox."
        )

    driver.set_page_load_timeout(30)

    try:
        driver.maximize_window()
    except Exception:
        pass

    return driver
