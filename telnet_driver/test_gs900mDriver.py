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

    def test_timeout(self):
        driver = Gs900mDriver('10.0.6.7')
        driver.connect()
        driver.login()
        driver.prompt = 'random >'  # 誤ったプロンプトを与えてタイムアウトを誘う
        try:
            response = driver.say('show console')
        except Exception as e:
            print(e.args)
        finally:
            driver.close()
