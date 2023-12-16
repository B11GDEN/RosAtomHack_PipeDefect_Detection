from __future__ import annotations

import json
import pika

from collections import deque
from threading import Thread

from base import MineWorker


class RConsumer(MineWorker, Thread):
    def __init__(self,
                 queue: str,
                 routing_key: str,
                 exchange: str):
        MineWorker.__init__(self, exchange)
        Thread.__init__(self)

        self._queue = queue
        self._routing_key = routing_key

        self.received = deque()

        res = self._connect()
        assert res is None, res

        print(f"{self.__class__.__name__} ready")

    def _connect(self) -> None | str:
        try:
            if not self._conn or self._conn.is_closed:
                self._conn = pika.BlockingConnection(self._params)
                self._channel = self._conn.channel()

                self._channel.queue_declare(queue=self._queue, auto_delete=True, arguments={'x-message-ttl': 30000})
                self._channel.queue_bind(exchange=self._exchange,
                                         queue=self._queue,
                                         routing_key=self._routing_key)
        except Exception as e:
            return f'{self.__class__.__name__}: {e.__class__.__name__}: {e}'

    def _receive(self) -> None:
        def callback(ch, method, properties, body):
            self.received.append(json.loads(body))

        self._channel.basic_consume(queue=self._queue, on_message_callback=callback, auto_ack=True)

    def run(self) -> None:
        self._receive()
        self._channel.start_consuming()

    def read(self) -> dict | None:
        try:
            return self.received.pop()
        except IndexError:
            return None

    def close(self) -> None | str:
        try:
            if self._conn and self._conn.is_open:
                self._channel.stop_consuming()
                self._channel.close()
                self._conn.close()
        except Exception as e:
            return f'{self.__class__.__name__}: {e.__class__.__name__}: {e}'
