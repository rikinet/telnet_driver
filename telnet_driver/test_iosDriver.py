from unittest import TestCase
from .ios import IosDriver


class TestIosDriver(TestCase):
    def test_version(self):
        driver = IosDriver('10.0.6.9', password='manager', enable_password='friend', prompt_base='cat01')
        driver.connect()
        driver.login_simple()
        driver.enable()
        driver.off_page_mode()
        response = driver.say('show version')
        self.assertTrue('IOS' in response)
        driver.close()
