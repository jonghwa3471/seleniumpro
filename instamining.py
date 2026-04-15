import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

initial_hashtag = "dog"
max_hashtags = 20
browser: WebDriver = webdriver.Chrome()
counted_hashtags = []
used_hashtags = []


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


def wait_for(locator):
    return WebDriverWait(browser, 10).until(EC.presence_of_element_located(locator))


def extract_data(target_hashtag):
    hashtag_name = browser.current_url.split("explore/search/keyword/?q=%23")[-1].strip(
        "/"
    )
    time.sleep(2)
    if "." in hashtag_name:
        hashtag_name = target_hashtag
    post_count = wait_for(
        (
            By.CSS_SELECTOR,
            ".html-span.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x1hl2dhg.x16tdsg8.x1vvkbs",
        )
    )
    # 현재는 post_count를 가져올 수 없음
    if hashtag_name and post_count:
        if hashtag_name not in used_hashtags:
            counted_hashtags.append((hashtag_name, post_count.text))
            used_hashtags.append(hashtag_name)


def get_related(target_url):
    browser.get(target_url)
    post = wait_for((By.XPATH, "//a[contains(@href, '/p/')]"))
    post.click()

    time.sleep(5)

    header = wait_for(((By.TAG_NAME, "h1")))
    hashtags = header.find_elements(By.TAG_NAME, "a")

    for hashtag in hashtags:
        link = hashtag.get_attribute("href")
        browser.execute_script(f"window.open('{link}', '_blank');")

    for window in browser.window_handles:
        browser.switch_to.window(window)
        extract_data(initial_hashtag)
        time.sleep(1)

    if len(used_hashtags) < max_hashtags:
        for window in browser.window_handles[0:-1]:
            browser.switch_to.window(window)
            browser.close()
        browser.switch_to.window(browser.window_handles[0])
        get_related(browser.current_url)


login()
time.sleep(5)

get_related(f"https://www.instagram.com/explore/search/keyword/?q=%23{initial_hashtag}")
