from .application import Parser
from .features.list import features
from .infrastructure import DockerChromeDriverFactory


class ParserApp:
    def __new__(cls) -> Parser:
        driver = DockerChromeDriverFactory.get_driver()
        _parser = Parser(
            driver,
            features=[
                feature(driver)
                for feature in features
            ]
        )
        return _parser
