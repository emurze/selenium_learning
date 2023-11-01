import unittest

from main import get_parser


class ParserCapacityTest(unittest.TestCase):
    def setUp(self) -> None:
        parser = get_parser()
        self.driver = parser.parse

    def tearDown(self) -> None:
        self.driver.quit()

    def test_parser(self):
        self.assertIn('AI', self.driver.title)
        self.assertIn('GIRLS', self.driver.title)
