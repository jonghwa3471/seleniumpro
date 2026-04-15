import time
from math import ceil
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class ResponsiveTester:
    def __init__(self, urls):
        self.browser: WebDriver = webdriver.Chrome()
        self.browser.maximize_window()
        self.urls = urls
        self.sizes = [480, 960, 1366, 1920]
        self.BROWSER_HEIGHT = 949

    def screenshot(self, url):
        self.browser.get(url)

        time.sleep(6)
        ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()

        # print(browser.get_window_size())

        for size in self.sizes:
            self.browser.set_window_size(size, self.BROWSER_HEIGHT)
            self.browser.execute_script("window.scrollTo(0, 0)")
            time.sleep(3)
            scroll_size = self.browser.execute_script(
                "return document.body.scrollHeight"
            )
            total_sections = ceil(scroll_size / self.BROWSER_HEIGHT)

            for section in range(total_sections):
                self.browser.execute_script(
                    f"window.scrollTo(0, {(section + 1) * self.BROWSER_HEIGHT})"
                )
                self.browser.save_screenshot(f"screenshots/{size}x{section + 1}.png")
                time.sleep(2)

    def start(self):
        for url in self.urls:
            self.screenshot(url)


tester = ResponsiveTester(["https://nomadcoders.co"])
tester.start()
