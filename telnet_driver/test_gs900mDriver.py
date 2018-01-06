from unittest import TestCase
from .gs900m import Gs900mDriver


class TestGs900mDriver(TestCase):
    HOST_ADDRESS = '10.0.6.7'

    def test_say(self):
        driver = Gs900mDriver(TestGs900mDriver.HOST_ADDRESS)
        driver.connect()
        driver.login()
        response = driver.say('show console')
        self.assertTrue('Console Information' in response)
        driver.close()

    def test_say_timeout(self):
        driver = Gs900mDriver(TestGs900mDriver.HOST_ADDRESS)
        driver.connect()
        driver.login()
        driver.prompt = 'random >'  # 誤ったプロンプトを与えてタイムアウトを誘う
        try:
            driver.say('show console')
        except Exception as e:
            print(e.args)
        else:
            self.fail('time out not occurred.')
        finally:
            driver.close()

    def test_say_null_command(self):
        driver = Gs900mDriver(TestGs900mDriver.HOST_ADDRESS)
        driver.connect()
        driver.login()
        response = driver.say(None)
        self.assertFalse(response)
        driver.close()

    def test_connect_timeout(self):
        """存在しないアドレスを指定してタイムアウトを誘う"""
        driver = Gs900mDriver('127.0.0.254')
        try:
            driver.connect()
        except ConnectionError as e:
            print(e.args)
        else:
            self.fail('Connection not timed out.')
        finally:
            driver.close()

    def test_reconnect(self):
        driver = Gs900mDriver(TestGs900mDriver.HOST_ADDRESS)
        driver.connect()
        driver.login()
        driver.close()
        driver.connect()
        driver.login()
        response = driver.say('show console')
        self.assertTrue('Console Information' in response)
        driver.close()

    def test_repr(self):
        driver = Gs900mDriver(TestGs900mDriver.HOST_ADDRESS)
        r = repr(driver)
        self.assertIn(TestGs900mDriver.HOST_ADDRESS, r)
        print(r)
