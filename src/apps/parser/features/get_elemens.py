import time
from dataclasses import dataclass
from typing import ClassVar, Union

import redis
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from config.settings.redis import REDIS_FEATURE_DB, REDIS_FEATURE_PORT, \
    REDIS_FEATURE_HOST
from ..domain import BaseFeature


class StateStorageRepository:
    def __init__(self) -> None:
        self.conn = redis.Redis(
            db=REDIS_FEATURE_DB,
            port=REDIS_FEATURE_PORT,
            host=REDIS_FEATURE_HOST,
        )

    def get_state(self) -> str:
        state: bytes | None = self.conn.get('PARSE_STATE')
        if state is None:
            return 'pending'
        else:
            return state.decode('utf-8')

    def save_state(self, state: str) -> None:
        print(state)
        self.conn.set('PARSE_STATE', state)

    def clear_state(self) -> None:
        self.conn.delete('PARSE_STATE')


@dataclass
class ElementsGetter(BaseFeature):
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
        return articles

    @staticmethod
    def load_more_articles(driver: WebDriver, scrolls: int = 50) -> None:
        storage = StateStorageRepository()

        for index in range(1, scrolls+1):
            storage.save_state(f'{(index / scrolls * 100):.0f}%')

            height = driver.execute_script(
                'return document.body.scrollHeight',
            )
            time.sleep(.5)
            WebDriverWait(driver, 10).until(
                ec.presence_of_all_elements_located(
                    (By.XPATH,
                     '//*[@id="gfHome"]/div/div[1]/div/*[@class="gf-box"]')
                )
            )
            driver.execute_script(f'window.scrollTo(0, {height - 500})')

        storage.clear_state()
