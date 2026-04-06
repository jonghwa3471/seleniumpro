from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser: WebDriver = webdriver.Chrome()

browser.get("https://google.com")

search_bar = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
)
search_bar.send_keys("hello!")
search_bar.send_keys(Keys.ENTER)

search_results = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "MjjYud"))
)

print(search_results)

input("pause")
