# Copyright (c) 2017 Riki Network Systems, Inc.
# All rights reserved.

from telnetlib import TELNET_PORT
from telnet_driver import TelnetDriver


class IosDriver(TelnetDriver):
    """Cisco 製ネットワーク機器、特に IOS 搭載機のコンソールを操作する"""

    def __init__(self, host, port=TELNET_PORT, password='cisco', enable_password='cisco', encoding='utf-8', prompt_base='router'):
        """初期化する。

        :param host: リモートホスト名またはIPアドレス
        :type host: str
        :param port: TCPポート番号。省略時は 23
        :type port: int
        :param password: ログイン時のパスワード
        :type password: str
        :param enable_password: 特権モードへ移行するためのパスワード
        :type enable_password: str
        :param encoding: コンソールで使用する文字コード名
        :type encoding: str
        :param prompt_base: プロンプト文字列でモードを表す '>' や '#' を除いた部分
        :type prompt_base: str"""
        super().__init__(host)
        self.host = host
        self.port = port
        self.encoding = encoding
        self.password = password
        self.enable_password = enable_password
        self.prompt_base = prompt_base
        self.prompt = self.prompt_base + '>'
        self.enabled = False
        self.page_mode = False

    def connect(self):
        super().connect()
        self.enabled = False
        self.page_mode = True

    def login_simple(self):
        """ユーザ名なし、パスワードのみでログインする。
        あらかじめ connect() しておくこと。

        :return: ログインが成功したときは True、失敗したときは False を返す
        :rtype: bool"""
        if self.telnet == None:
            raise ConnectionError()
        try:
            password_byte = (self.password + '\r').encode(self.encoding)
            prompt_byte = self.prompt.encode()
            buf = self.telnet.read_until(b"assword:", timeout=5)
            self.telnet.write(password_byte)
            buf = self.telnet.read_until(prompt_byte, timeout=5)
        except EOFError as e:
            print(e)
            return False
        else:
            return True

    def enable(self):
        """特権モードへ移行する。ログインが済んでいること。"""
        self.prompt = 'Password:'
        self.say('enable')
        self.prompt = self.prompt_base + '#'
        self.say(self.enable_password)
        self.enabled = True

    def off_page_mode(self):
        """コンソール出力のページ分割を抑制する。"""
        self.say('terminal length 0')
        self.page_mode = False
