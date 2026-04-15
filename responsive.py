import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

browser: WebDriver = webdriver.Chrome()

browser.get("https://nomadcoders.co")
browser.maximize_window()

sizes = [320, 480, 960, 1366, 1920]

# print(browser.get_window_size())

for size in sizes:
    browser.set_window_size(size, 949)
    time.sleep(5)

input("pause")
