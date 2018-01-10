from unittest import TestCase, skip
from .gs900m import Gs900mDriver


class TestGs900mDriver(TestCase):
    HOST_ADDRESS = '10.0.6.7'
    driver = None

    def setUp(self):
        self.driver = Gs900mDriver(TestGs900mDriver.HOST_ADDRESS, sys_name='gs1')

    def test_say(self):
        self.driver.connect()
        self.driver.login()
        response = self.driver.say('show console')
        self.assertTrue('Console Information' in response)
        self.driver.close()

    def test_say_timeout(self):
        """誤ったプロンプトを与えてタイムアウトを誘う"""
        self.driver.connect()
        self.driver.login()
        self.driver.sys_name = 'bad_name'
        try:
            self.driver.say('show console')
        except Exception as e:
            print(e.args)
        else:
            self.fail('time out not occurred.')
        finally:
            self.driver.close()

    def test_say_null_command(self):
        self.driver.connect()
        self.driver.login()
        response = self.driver.say(None)
        self.assertFalse(response)
        self.driver.close()

    @skip("bad IP address")
    def test_connect_timeout(self):
        """存在しないアドレスを指定してタイムアウトを誘う"""
        self.driver = Gs900mDriver('127.0.0.254', sys_name='gs1')
        try:
            self.driver.connect()
        except ConnectionError as e:
            print(e.args)
        else:
            self.fail('Connection not timed out.')
        finally:
            self.driver.close()

    def test_reconnect(self):
        self.driver.connect()
        self.driver.login()
        self.driver.close()
        self.driver.connect()
        self.driver.login()
        response = self.driver.say('show console')
        self.assertTrue('Console Information' in response)
        self.driver.close()

    def test_repr(self):
        r = repr(self.driver)
        self.assertIn(TestGs900mDriver.HOST_ADDRESS, r)
