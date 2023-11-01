from collections.abc import Callable
from typing import cast

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from parser.application import Parser, FirstFeature, AuthFeature


def get_parser() -> Parser:
    # _driver = webdriver.Firefox()

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--start-maximized')

    _driver = webdriver.Chrome(options=options)

    features = [
        AuthFeature,
        FirstFeature
    ]
    features = cast(list[Callable], features)

    _parser = Parser(
        _driver,
        features=[
            feature(_driver)
            for feature in features
        ]
    )
    return _parser


if __name__ == '__main__':
    print('RUN APP')
    parser = get_parser()
    parser.parse()
