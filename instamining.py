import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

browser: WebDriver = webdriver.Chrome()

main_hashtag = "dog"


def login():
    username = ""
    password = ""

    browser.get("https://www.instagram.com/accounts/login")

    time.sleep(5)

    username_input = browser.find_element(By.NAME, "email")
    password_input = browser.find_element(By.NAME, "pass")
    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)


login()
time.sleep(5)

browser.get(f"https://www.instagram.com/explore/tags/{main_hashtag}")

post = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/p/')]"))
)

post.click()

time.sleep(5)

header = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "h1"))
)

hashtags = header.find_elements(By.TAG_NAME, "a")

for hashtag in hashtags:
    link = hashtag.get_attribute("href")
    browser.execute_script(f"window.open('{link}', '_blank');")

for window in browser.window_handles:
    browser.switch_to.window(window)
    hashtag_name = browser.current_url.split("explore/search/keyword/?q=%23")[-1].strip(
        "/"
    )
    print(hashtag_name)
    time.sleep(1)

time.sleep(3)
browser.quit()
