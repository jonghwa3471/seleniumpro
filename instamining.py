import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

browser: WebDriver = webdriver.Chrome()

main_hashtag = "dog"

browser.get(f"https://www.instagram.com/explore/tags/{main_hashtag}")

header = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "header"))
)

hashtags = header.find_element(By.CLASS_NAME, "AC7dp")
