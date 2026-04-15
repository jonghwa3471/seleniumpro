from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class GoogleKeywordScreenshooter:
    def __init__(self, keyword, screenshots_dir):
        self.options = Options()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.browser: WebDriver = webdriver.Chrome(options=self.options)
        self.keyword = keyword
        self.screenshots_dir = screenshots_dir

    def start(self):
        self.browser.get("https://google.com")
        search_bar = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
        )
        search_bar.send_keys(self.keyword)

        search_bar.send_keys(Keys.ENTER)

        search_results = WebDriverWait(self.browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "MjjYud"))
        )

        # self.browser.execute_script(
        #     """
        #     const shitty = arguments[0];
        #     shitty.parentElement.removeChild(shitty)
        #     """,
        #     shitty_element,
        # )

        for index, search_result in enumerate(search_results):
            if search_result.is_displayed() and search_result.size["height"] > 0:
                search_result.screenshot(
                    f"{self.screenshots_dir}/{self.keyword}x{index}.png"
                )

    def finish(self):
        self.browser.quit()


domain_competitors = GoogleKeywordScreenshooter("buy domain", "screenshots")
domain_competitors.start()
domain_competitors.finish()

python_competitors = GoogleKeywordScreenshooter("python book", "screenshots")
python_competitors.start()
python_competitors.finish()
