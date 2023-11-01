import abc
import time
from collections.abc import Callable
from dataclasses import dataclass
from pprint import pprint
from typing import ClassVar, Union

from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

EMAIL = 'grayemurze@gmail.com'
PASSWORD = '12345678'


class BaseFeature(abc.ABC):
    name: ClassVar[str]
    driver: WebDriver

    @abc.abstractmethod
    def execute(self) -> Union[dict, list]: ...


@dataclass
class Parser:
    url: ClassVar[str] = 'https://dreamgf.ai/'
    driver: WebDriver
    features: list[BaseFeature]

    def parse(self) -> WebDriver:
        self.driver.get(self.url)

        result = {
            feature.name: feature.execute()
            for feature in self.features
        }

        pprint(result)

        # self.driver.quit()

        time.sleep(1_000_000)

        return self.driver


@dataclass
class AuthFeature(BaseFeature):
    name: ClassVar[str] = 'auth'
    driver: WebDriver

    def execute(self):
        print(1)
        self.wait_clickable(By.CSS_SELECTOR, '.used-item')
        _elem = self.driver.find_element(By.CSS_SELECTOR, '.used-item')
        self.save_click(_elem)

        print(2)
        self.wait_clickable(
            By.XPATH,
            '/html/body/div[1]/div[5]/div/div/div/div[2]/div/div/div[4]/button'
        )
        __elem = self.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div[5]/div/div/div/div[2]/div/div/div[4]/button'
        )
        self.save_click(__elem)

        print(3)
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, '#email')
            )
        )
        input_email = self.driver.find_element(By.CSS_SELECTOR, '#email')
        input_email.send_keys(EMAIL)
        input_email.send_keys(Keys.ENTER)

        print(4)
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, '#password')
            )
        )
        input_email = self.driver.find_element(By.CSS_SELECTOR, '#password')
        input_email.send_keys(PASSWORD)

        print(5)
        self.wait_clickable(
            By.XPATH,
            '/html/body/div[1]/div[5]/div/div/div[2]/div[3]/span/button'
        )
        ___elem = self.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div[5]/div/div/div[2]/div[3]/span/button'
        )
        self.save_click(___elem)

    def wait_clickable(self, by: By, value: str) -> None:
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(
                (by, value),
            )
        )

    @staticmethod
    def save_click(func: WebElement) -> None:
        try:
            func.click()
        except ElementClickInterceptedException as err:
            print(f'auth error {err}')


@dataclass
class FirstFeature(BaseFeature):
    name: ClassVar[str] = 'articles'
    driver: WebDriver

    def execute(self) -> Union[dict, list]:
        self.load_more_articles(self.driver)

        elems = self.driver.find_elements(
            By.XPATH, '//*[@id="gfHome"]/div/div[1]/div/*[@class="gf-box"]'
        )
        articles = [
            {
                'name': elem.find_element(
                    By.CSS_SELECTOR, '.gt-name .d-block'
                ).text,

                'href': elem.find_element(
                    By.CSS_SELECTOR, '.gf-box-link'
                ).get_attribute('href'),

                'image': elem.find_element(
                    By.CSS_SELECTOR, '.gf-box-link img'
                ).get_attribute('src'),
            }
            for elem in elems
        ]
        print(len(articles))
        return articles

    @staticmethod
    def load_more_articles(driver: WebDriver, scrolls: int = 100):
        for _ in range(scrolls):
            height = driver.execute_script(
                'return document.body.scrollHeight',
            )
            time.sleep(.3)
            WebDriverWait(driver, 10).until(
                ec.presence_of_all_elements_located(
                    (By.XPATH,
                     '//*[@id="gfHome"]/div/div[1]/div/*[@class="gf-box"]')
                )
            )
            driver.execute_script(f'window.scrollTo(0, {height - 500})')
