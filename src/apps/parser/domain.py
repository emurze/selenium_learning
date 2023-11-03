import abc
from typing import ClassVar, Union


class BaseFeature(abc.ABC):
    name: ClassVar[str]
    driver: object

    @abc.abstractmethod
    def execute(self) -> Union[dict, list]: ...


class BaseDriverFactory(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_driver(): ...
