from unittest import TestCase
from .gs900m import Gs900mDriver


class TestGs900mDriver(TestCase):
    def test_say(self):
        driver = Gs900mDriver('10.0.6.7')
        driver.connect()
        driver.login()
        response = driver.say('show console')
        self.assertTrue('Console Information' in response)
        driver.close()
