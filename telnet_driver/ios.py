# Copyright (c) 2017 Riki Network Systems, Inc.
# All rights reserved.

import sys
from telnetlib import TELNET_PORT
from telnet_driver import TelnetDriver
from logging import getLogger

logger = getLogger(__name__)


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

    def __repr__(self):
        return 'IosDriver({!r}, port={}, password={!r}, enable_password={!r})'.format(self.host, self.port,
                                                                                      self.password,
                                                                                      self.enable_password)

    def connect(self):
        super().connect()
        self.enabled = False
        self.page_mode = True

    def login(self):
        """当面はユーザ名のないログインのみサポートする。
        ユーザ名のあるログインをサポートする必要があるなら修整が必要。"""
        return self.login_simple()

    def login_simple(self):
        """ユーザ名なし、パスワードのみでログインする。
        あらかじめ connect() しておくこと。

        :return: ログインが成功したときは True、失敗したときは False を返す
        :rtype: bool
        :raises ConnectionError: 接続に失敗したとき
        """
        if self.telnet is None:
            raise ConnectionError()
        try:
            password_byte = (self.password + '\r').encode(self.encoding)
            prompt_byte = self.prompt.encode()
            buf = self.telnet.read_until(b"assword:", timeout=5)
            self.telnet.write(password_byte)
            buf = self.telnet.read_until(prompt_byte, timeout=5)
        except EOFError as e:
            logger.warning('Failed to login.', exc_info=sys.exc_info())
            return False
        else:
            return True

    def enable(self):
        """特権モードへ移行する。ログインが済んでいること。

        :return: 成功したとき True、それ以外は False
        :rtype: bool
        """
        try:
            self.say('enable', expect='Password:')
            self.say(self.enable_password, expect=self.prompt_base + '#')
            self.prompt = self.prompt_base + '#'
            self.enabled = True
        except TimeoutError as _:
            logger.warning('Failed to ', exc_info=sys.exc_info())
            return False
        else:
            return True

    def off_page_mode(self):
        """コンソール出力のページ分割を抑制する。"""
        self.say('terminal length 0')
        self.page_mode = False
