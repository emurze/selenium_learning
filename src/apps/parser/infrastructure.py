from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from .domain import BaseDriverFactory


class DockerChromeDriverFactory(BaseDriverFactory):
    @staticmethod
    def get_driver() -> WebDriver:
        options = Options()
        options.add_argument("start-maximized")  # open
        options.add_argument("disable-infobars")  # disabling
        options.add_argument("--disable-extensions")  # disabling
        options.add_argument("--disable-gpu")  # applicable
        options.add_argument("--disable-dev-shm-usage")  # overcome
        options.add_argument("--no-sandbox")
        options.add_argument('--headless')
        _driver = webdriver.Chrome(
            options=options,
        )
        return _driver


class FirefoxDriverFactory(BaseDriverFactory):
    @staticmethod
    def get_driver() -> WebDriver:
        return webdriver.Firefox()
