import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

PROMISED_DOWN = 200
PROMISED_UP = 80
CHROME_DRIVER_PATH = "/Users/hatimalattas/Development/chromedriver"
TWITTER_USERNAME = os.environ.get("USERNAME")
TWITTER_PASSWORD = os.environ.get("PASSWORD")


class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        self.down = PROMISED_DOWN
        self.up = PROMISED_UP

    def get_internet_speed(self):
        self.driver.get("https://www.speedcheck.org/")
        start_btn = self.driver.find_element_by_xpath('//*[@id="app-container"]/angular-main/main/div/div/div/div/div'
                                                      '/div/start-button/div/a')
        start_btn.click()

        time.sleep(60)
        try:
            down = self.driver.find_element_by_xpath('//*[@id="app-container"]/angular-main/main/div/div/result/div'
                                                     '/div[ '
                                                     '1]/div[1]/div[2]/div/div/div[1]/div/div[3]').text.split(" ")[0]
            up = self.driver.find_element_by_xpath('//*[@id="app-container"]/angular-main/main/div/div/result/div/div['
                                                   '1]/div[1]/div[3]/div/div/div[1]/div/div[3]').text.split(" ")[0]
        except NoSuchElementException as e:
            down = self.driver.find_element_by_xpath('//*[@id="app-container"]/angular-main/main/div/div/test/div'
                                                     '/div[1]/div/div/div/div[2]/div/div/span[1]').text
            up = self.driver.find_element_by_xpath('//*[@id="app-container"]/angular-main/main/div/div/test/div/div['
                                                   '1]/div/div/div/div[3]/div/div/span[1]').text

        result = {
            "down": float(down),
            "up": float(up)
        }

        return result

    def tweet_at_provider(self, result):
        self.driver.get("https://twitter.com/")
        time.sleep(5)
        login_btn = self.driver.find_element_by_xpath(
            '/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[3]/a[2]')
        login_btn.click()

        time.sleep(5)
        username_field = self.driver.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')
        username_field.send_keys(TWITTER_USERNAME)
        password_field = self.driver.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')
        password_field.send_keys(TWITTER_PASSWORD)
        login_btn = self.driver.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div')
        login_btn.click()

        time.sleep(5)
        tweet_field = self.driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div['
                                                        '1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div['
                                                        '1]/div/div/div/div/div/div/div/div/label/div['
                                                        '1]/div/div/div/div/div[2]/div/div/div/div/span')
        tweet_field.send_keys(
            f"Hey Internet Provider, why is my internet speed {result['down']}down/{result['up']}up when I pay for "
            f"{PROMISED_DOWN}down/{PROMISED_UP}up?")

        tweet_btn = self.driver.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div['
            '2]/div[3]/div/div/div[2]/div[3]')
        tweet_btn.click()


twitter_bot = InternetSpeedTwitterBot()
result = twitter_bot.get_internet_speed()
twitter_bot.tweet_at_provider(result)
