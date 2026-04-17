import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class Instaminer:
    def __init__(self, initial_hashtag, max_hashtags):
        self.browser: WebDriver = webdriver.Chrome()
        self.initial_hashtag = initial_hashtag
        self.max_hashtags = max_hashtags
        self.counted_hashtags = []
        self.used_hashtags = []

    def login(self):
        username = ""
        password = ""

        self.browser.get("https://www.instagram.com/accounts/login")

        time.sleep(5)

        username_input = self.browser.find_element(By.NAME, "email")
        password_input = self.browser.find_element(By.NAME, "pass")
        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

        time.sleep(5)

    def wait_for(self, locator):
        return WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(locator)
        )

    def save_file(self):
        file = open(f"{self.initial_hashtag}-report.csv", "w")
        writer = csv.writer(file)
        writer.writerow(["Hashtag", "Post Count"])

        for hashtag in self.counted_hashtags:
            writer.writerow(hashtag)

    def start(self):
        self.login()
        self.get_related(
            f"https://www.instagram.com/explore/search/keyword/?q=%23{self.initial_hashtag}"
        )

    def get_related(self, target_url):
        self.browser.get(target_url)
        post = self.wait_for((By.XPATH, "//a[contains(@href, '/p/')]"))
        post.click()

        time.sleep(5)

        header = self.wait_for(((By.TAG_NAME, "h1")))
        hashtags = header.find_elements(By.TAG_NAME, "a")

        for hashtag in hashtags:
            link = hashtag.get_attribute("href")
            hashtag_name = link.rstrip("/").split("/")[-1]
            if hashtag_name in self.used_hashtags:
                continue
            self.browser.execute_script("window.open(arguments[0], '_blank');", link)

        for window in self.browser.window_handles:
            self.browser.switch_to.window(window)
            self.extract_data(self.initial_hashtag)
            time.sleep(1)

        if len(self.used_hashtags) < self.max_hashtags:
            for window in self.browser.window_handles[0:-1]:
                self.browser.switch_to.window(window)
                self.browser.close()
            self.browser.switch_to.window(self.browser.window_handles[0])
            self.get_related(self.browser.current_url)
        else:
            self.browser.quit()
            self.save_file()

    def extract_data(self, target_hashtag):
        hashtag_name = self.browser.current_url.split("explore/search/keyword/?q=%23")[
            -1
        ].strip("/")
        time.sleep(2)
        if "." in hashtag_name:
            hashtag_name = target_hashtag
        post_count = self.wait_for(
            (
                By.CSS_SELECTOR,
                ".html-span.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x1hl2dhg.x16tdsg8.x1vvkbs",
            )
        )
        # 현재는 post_count를 가져올 수 없음
        if hashtag_name and post_count:
            if hashtag_name not in self.used_hashtags:
                self.counted_hashtags.append((hashtag_name, post_count.text))
                self.used_hashtags.append(hashtag_name)


Instaminer("cat", 10).start()
