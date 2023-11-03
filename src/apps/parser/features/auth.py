from dataclasses import dataclass
from typing import ClassVar

from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from ..domain import BaseFeature

EMAIL = 'grayemurze@gmail.com'
PASSWORD = '12345678'


@dataclass
class AuthFeature(BaseFeature):
    name: ClassVar[str] = 'auth'
    driver: WebDriver

    def execute(self):

        self.wait_clickable(By.CSS_SELECTOR, '.used-item')
        _elem = self.driver.find_element(By.CSS_SELECTOR, '.used-item')
        self.save_click(_elem)

        self.wait_clickable(
            By.XPATH,
            '/html/body/div[1]/div[5]/div/div/div/div[2]/div/div/div[4]/button'
        )
        __elem = self.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div[5]/div/div/div/div[2]/div/div/div[4]/button'
        )
        self.save_click(__elem)

        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, '#email')
            )
        )
        input_email = self.driver.find_element(By.CSS_SELECTOR, '#email')
        input_email.send_keys(EMAIL)
        input_email.send_keys(Keys.ENTER)

        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, '#password')
            )
        )
        input_email = self.driver.find_element(By.CSS_SELECTOR, '#password')
        input_email.send_keys(PASSWORD)

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
        WebDriverWait(self.driver, 20).until(
            ec.element_to_be_clickable(
                (by, value),
            )
        )

    def save_click(self, elem: WebElement) -> None:
        try:
            elem.click()
        except ElementClickInterceptedException:
            self.driver.execute_script('arguments[0].click();', elem)
