from __future__ import annotations

import json
import pika

from base import MineWorker


class RProducer(MineWorker):
    def __init__(self, exchange: str):
        super(RProducer, self).__init__(exchange)

        res = self._connect()
        assert res is None, res

        print(f"{self.__class__.__name__} ready")

    def _connect(self) -> None | str:
        try:
            if not self._conn or self._conn.is_closed:
                self._conn = pika.BlockingConnection(self._params)
                self._channel = self._conn.channel()
                self._channel.exchange_declare(exchange=self._exchange)
        except Exception as e:
            return f'{self.__class__.__name__}: {e.__class__.__name__}: {e}'

    def _publish(self, msg, routing_key: str) -> None:
        self._channel.basic_publish(exchange=self._exchange, routing_key=routing_key, body=json.dumps(msg))

    def publish(self, msg, routing_key: str) -> None:
        try:
            self._publish(msg, routing_key)
        except pika.exceptions.ConnectionClosed:
            self._connect()
            self._publish(msg, routing_key)
