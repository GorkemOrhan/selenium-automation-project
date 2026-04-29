# Selenium Automation Project

This project is a Python-based Selenium UI test automation skeleton. It works with `pytest`, follows the `Page Object Model (POM)` structure, and provides a ready foundation for running basic web scenarios on Chrome and Firefox.

Currently, the project contains simple smoke, navigation, and search flow tests for the eBay homepage. The goal is to create a simple, readable, and reusable framework that can be expanded through team collaboration.

## Summary

* Uses Python + Selenium WebDriver + pytest
* Supports Chrome and Firefox
* Uses explicit wait approach instead of `sleep`
* Separates page behaviors from tests with POM structure
* Provides a modular folder structure suitable for adding new tests and page objects

## Technologies Used

* Python 3.11+
* Selenium 4
* pytest 8+

## Project Structure

```text
selenium-automation-project/
|-- README.md
|-- requirements.txt
|-- pages/
|   |-- __init__.py
|   |-- base_page.py
|   `-- home_page.py
|-- utils/
|   |-- __init__.py
|   |-- driver_factory.py
|   `-- wait_helpers.py
`-- tests/
    |-- conftest.py
    |-- test_smoke_setup.py
    |-- test_home_navigation.py
    `-- test_search_flow.py
```

## What The Folders Do

### `pages/`

Page-specific behaviors are kept here.

* `base_page.py`: Contains common Selenium helpers
* `home_page.py`: Contains flows such as opening the homepage, waiting for loading, and title validation

### `utils/`

Reusable infrastructure helpers are located here.

* `driver_factory.py`: Creates WebDriver based on browser type
* `wait_helpers.py`: Provides explicit wait functions

### `tests/`

Pytest tests and fixture definitions are located here.

* `conftest.py`: Defines `driver`, `base_url`, and `--browser` parameter
* `test_smoke_setup.py`: Basic smoke test that checks the page title is not empty
* `test_home_navigation.py`: Test that performs homepage navigation and title validation
* `test_search_flow.py`: Test that types a keyword, validates results are returned, selects a product, and verifies product detail information

## Installation

### Windows PowerShell

```powershell
python --version
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Requirements

* Python 3.11 or higher
* Google Chrome and/or Mozilla Firefox
* Internet connection

Note: Since Selenium Manager is used with Selenium 4, in most cases you do not need to manually download driver binary files.

## Running Tests

To run all tests with the default browser selection:

```bash
pytest -v
```

Only for Chrome:

```bash
pytest -v --browser chrome
```

Only for Firefox:

```bash
pytest -v --browser firefox
```

To run the same tests on all supported browsers:

```bash
pytest -v --browser all
```

## Browser Selection Logic

The project uses `pytest` custom argument structure:

* `chrome`: Tests run only on Chrome
* `firefox`: Tests run only on Firefox
* `all`: Every test is parametrized for both Chrome and Firefox

Since the default value is `all`, the `pytest -v` command targets both browsers.

## Current Test Scenarios

### 1. Smoke Setup Test

`tests/test_smoke_setup.py`

This test:

* Opens the browser
* Goes to the eBay homepage
* Validates that the page title is not empty

### 2. Home Navigation Test

`tests/test_home_navigation.py`

This test:

* Opens the homepage
* Waits until `ebay` appears in the title
* Validates that the page loaded as expected

### 3. Search Flow Test

`tests/test_search_flow.py`

This test:

* Opens the homepage
* Validates the title information
* Types a keyword into the search box
* Validates transition to the search results page
* Validates that search results are present
* Selects the first product from results
* Verifies product detail title information is not empty

## Framework Behavior

### Driver management

The `utils/driver_factory.py` file creates the related WebDriver based on the selected browser:

* `webdriver.Chrome()` for `chrome`
* `webdriver.Firefox()` for `firefox`

Additionally:

* Page load timeout is set to `30` seconds
* The window is maximized when possible

### Wait approach

Helpers inside `utils/wait_helpers.py` use explicit wait:

* `wait_for_visibility`
* `wait_for_clickable`
* `wait_for_presence`

The default timeout value is `10` seconds.

### Base Page

`pages/base_page.py` centralizes common Selenium operations:

* `open`
* `find_visible`
* `find_clickable`
* `find_present`
* `click`
* `type_text`
* `get_text`
* `get_title`
* `current_url`

Thanks to this structure, tests remain more readable and locator/interaction logic is collected in the page object layer.

## Adding a New Test or Page Object

A typical flow for expanding the project is as follows:

1. Add a new page object under `pages/`
2. Collect page-specific locators and behaviors in this file
3. Create a new pytest file under `tests/`
4. Write the scenario using the page object in the test
5. Add shared helpers under `utils/` if necessary

Example expansion areas:

* Search box scenarios
* Validation of result lists
* Transition to product detail page
* Add-to-cart flows

## Useful Notes

* Tests run by opening a real browser
* UI tests may require updates when the site design or title behavior changes
* This skeleton can be expanded with advanced reporting, screenshot capturing, logging, or CI integration

## Improvement Ideas

The following improvements can be added in the future:

* Environment-based `base_url` management
* `.env` or config structure
* Screenshot capture on failure
* HTML test report
* CI/CD integration
* More systematic management of locator constants

## License

If license information is not defined for this repo, a `LICENSE` file can be added according to needs.

