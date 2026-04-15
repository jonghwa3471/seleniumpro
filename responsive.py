import time
from math import ceil
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

BROWSER_HEIGHT = 949

browser: WebDriver = webdriver.Chrome()

browser.get("https://nomadcoders.co")

browser.maximize_window()

time.sleep(6)
ActionChains(browser).send_keys(Keys.ESCAPE).perform()


sizes = [480, 960, 1366, 1920]

# print(browser.get_window_size())

for size in sizes:
    browser.set_window_size(size, BROWSER_HEIGHT)
    browser.execute_script("window.scrollTo(0, 0)")
    time.sleep(3)
    scroll_size = browser.execute_script("return document.body.scrollHeight")
    total_sections = ceil(scroll_size / BROWSER_HEIGHT)

    for section in range(total_sections):
        browser.execute_script(f"window.scrollTo(0, {(section + 1) * BROWSER_HEIGHT})")
        browser.save_screenshot(f"screenshots/{size}x{section + 1}.png")
        time.sleep(2)
input("pause")
