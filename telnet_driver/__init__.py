# Copyright (c) 2017 Riki Network Systems, Inc.
# All rights reserved.
"""TELNET 接続を介してリモートホストとコマンドラインベースの
対話を行うための基礎ライブラリ"""

from telnetlib import Telnet, TELNET_PORT


class TelnetDriver:
    """TELNET コンソールを操作する。
    このクラスを継承して機種毎の差異を実装すること。"""

    def __init__(self, host, port=TELNET_PORT, encoding='utf-8'):
        """最低限の初期化をする。

        :param host: リモートホスト名またはIPアドレス
        :type host: str
        :param port: TCPポート番号。省略時は 23
        :type port: int
        :param encoding: リモートホストの入出力の文字コード。省略時は utf-8
        :type encoding: str
        """
        self.host = host
        self.port = port
        self.encoding = encoding
        self.prompt = None
        self.telnet = None

    def __repr__(self):
        return 'TelnetDriver({!r}, port={!r})'.format(self.host, self.port)

    def connect(self):
        """リモートホストに TELNET 接続する。
        既に接続済みだった場合はクローズして、再度接続する。

        :raises ConnectionError: TELNET接続に失敗したとき"""
        if self.telnet is None:
            self.telnet = Telnet()
        else:
            self.telnet.close()
        try:
            self.telnet.open(self.host, port=self.port)
        except TimeoutError as e:
            raise ConnectionError from e
        except Exception as e:
            raise ConnectionError from e

    def close(self):
        """TELNET接続を終了する。"""
        self.telnet.close()
        self.telnet = None

    def say(self, command, expect=None, timeout=5):
        """コマンドを送信し、プロンプトを待つ。
        プロンプトまでの応答を文字列として返す。
        プロンプトを設定してないときの動作は保証しない。

        :param command: リモートホストに送信する文字列。改行を含まない
        :type command: str
        :param expect: コマンド実行の終了を判断するプロンプト。与えないときは prompt プロパティが使われる
        :type expect: str
        :param timeout: プロンプトが応答に現れるまで待ち受ける秒数
        :type timeout: int
        :return: 最後のプロンプトを含むリモートホストの出力文字列
        :rtype: str
        :raises EOFError: 読み込めるものがなかったとき
        :raises TimeoutError: timeout の時間経過してもプロンプトまで読めなかったとき
        """
        if self.telnet is None:
            return ''
        cmd_byte = (command + '\r').encode(self.encoding)
        if expect:
            p = expect
        else:
            p = self.prompt
        prompt_byte = p.encode(self.encoding)
        try:
            self.telnet.write(cmd_byte)
            buf = self.telnet.read_until(prompt_byte, timeout)
            if prompt_byte not in buf:
                raise TimeoutError(buf.decode(self.encoding))
        except EOFError as _:
            raise
        else:
            return buf.decode(self.encoding)
