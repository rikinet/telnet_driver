# Copyright (c) 2017 Riki Network Systems, Inc.
# All rights reserved.

import sys
from telnetlib import TELNET_PORT
from telnet_driver import TelnetDriver
from logging import getLogger

logger = getLogger(__name__)


class Gs900mDriver(TelnetDriver):
    """Allied Telesis 製スイッチ CentreCOM GS900M のコンソールを操作する"""

    def __init__(self, host, port=TELNET_PORT, user='manager', password='friend', encoding='shift_jis',
                 sys_name=''):
        """初期化する。

        :param host: リモートホスト名またはIPアドレス
        :type host: str
        :param port: TCPポート番号。省略時は 23
        :type port: int
        :param user: ログイン時のユーザ名。省略時は初期値の manager
        :type user: str
        :param password: ログイン時のパスワード。省略時は初期値の friend
        :type password: str
        :param encoding: コンソールで使用する文字コード名。省略時は Shift_JIS
        :type encoding: str
        :param sys_name: コマンドプロンプトに埋め込まれるホスト名。工場出荷時は空欄
        :type sys_name: str
        """
        super().__init__(host)
        self.host = host
        self.port = port
        self.encoding = encoding
        self.user = user
        self.password = password
        self.sys_name = sys_name

    def __repr__(self):
        return 'Gs900mDriver({!r}, port={!r}, user={!r}, password={!r})'.format(self.host, self.port, self.user,
                                                                              self.password)

    @property
    def prompt(self):
        """
        プロンプトはユーザ名とシステム名から生成されるようだ。
        システム名はあとで分かって変更され乳母愛もあるので、動的に生成する。

        :return: プロンプトもじ列
        """
        return self.user.capitalize() + ' ' + self.sys_name + '>'

    def login(self):
        """与えられた認証パラメータでログインする。
        あらかじめ connect() しておくこと。

        :return: ログインが成功したときは True、失敗したときは False を返す。
        :rtype: bool
        :raises ConnectionError: 接続に失敗したとき
        """
        if self.telnet is None:
            raise ConnectionError()
        try:
            user_byte = (self.user + '\r').encode()
            password_byte = (self.password + '\r').encode()
            prompt_byte = self.prompt.encode()
            buf = self.telnet.read_until(b"login: ", timeout=5)
            self.telnet.write(user_byte)
            buf = self.telnet.read_until(b"assword:", timeout=5)
            self.telnet.write(password_byte)
            buf = self.telnet.read_until(prompt_byte, timeout=5)
        except EOFError as e:
            logger.warning('Failed to login.', exc_info=sys.exc_info())
            return False
        else:
            return True
