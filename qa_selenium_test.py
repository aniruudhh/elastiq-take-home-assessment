import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.lambdatest.com/selenium-playground/table-sort-search-demo"
HEADER_XPATH = "/html/body/div[1]/div/section[1]/div/div/h1"
EXPECTED_HEADER_TEXT = "Table Sorting And Searching"
SEARCH_TERM = "New York"
TABLE_INFO_ID = "example_info"
TABLE_ROWS_XPATH = "//table[@id='example']/tbody/tr"

@pytest.fixture(scope="session")
def browser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    yield driver  
    input("Press Enter to close the browser...")  
    driver.quit()

@pytest.fixture(scope="function")
def navigate_to_page(browser):
    browser.get(URL)

def test_page_load(browser, navigate_to_page):
    header_text = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, HEADER_XPATH))
    ).text
    assert EXPECTED_HEADER_TEXT in header_text, f"Unexpected page text: {header_text}"
    print(f"Page loaded successfully: {header_text}")

def test_search_functionality(browser, navigate_to_page):
    search_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']"))
    )
    search_box.clear()
    search_box.send_keys(SEARCH_TERM)

    WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element((By.ID, TABLE_INFO_ID), "filtered from 24 total entries")
    )

    rows = browser.find_elements(By.XPATH, TABLE_ROWS_XPATH)
    visible_rows = [row for row in rows if row.is_displayed()]

    assert len(visible_rows) == 5, f"Expected 5 results, but found {len(visible_rows)}."
    print("Search results correctly show 5 entries (filtered from 24 total).")
