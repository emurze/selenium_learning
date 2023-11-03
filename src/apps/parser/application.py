from dataclasses import dataclass
from pprint import pprint
from typing import ClassVar

from .domain import BaseFeature
from .infrastructure import WebDriver


@dataclass
class Parser:
    url: ClassVar[str] = 'https://dreamgf.ai/'
    driver: WebDriver
    features: list[BaseFeature]

    def parse(self) -> dict:
        self.driver.get(self.url)

        result = {
            feature.name: feature.execute()
            for feature in self.features
        }
        self.driver.quit()

        return result
