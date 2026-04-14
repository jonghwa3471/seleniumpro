from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

KEYWORD = "buy domain"

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
browser: WebDriver = webdriver.Chrome(options=options)

browser.get("https://google.com")

search_bar = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
)
search_bar.send_keys(KEYWORD)
search_bar.send_keys(Keys.ENTER)

search_results = WebDriverWait(browser, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "MjjYud"))
)

for index, search_result in enumerate(search_results):
    if search_result.is_displayed() and search_result.size["height"] > 0:
        search_result.screenshot(f"screenshots/{KEYWORD}x{index}.png")

browser.quit()
