from __future__ import annotations

import pika

from pika.connection import ConnectionParameters
from pika.adapters.blocking_connection import BlockingConnection, BlockingChannel


class MineWorker:
    def __init__(self, exchange: str):

        self._params: ConnectionParameters | None = None
        self._conn: BlockingConnection | None = None
        self._channel: BlockingChannel | None = None
        self._exchange = exchange

        res = self._set_params()
        assert res is None, res

    def _set_params(self) -> None | str:
        user = 'guest'
        password = 'guest'
        host = 'localhost'

        try:
            self._params = pika.connection.ConnectionParameters(
                host=host,
                credentials=pika.credentials.PlainCredentials(user, password))
        except Exception as e:
            return f'{self.__class__.__name__}: {e.__class__.__name__}: {e}'

    def close(self) -> None | str:
        try:
            if self._conn and self._conn.is_open:
                self._channel.close()
                self._conn.close()
        except Exception as e:
            return f'{self.__class__.__name__}: {e.__class__.__name__}: {e}'
