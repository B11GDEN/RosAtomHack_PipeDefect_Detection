import base64

import numpy as np

from pathlib import Path
from os import listdir
from os.path import isfile, join

from producer import RProducer
from consumer import RConsumer


def init_connection_consumer(queue: str,
                             routing_key: str,
                             exchange: str):
    consumer = RConsumer(queue=queue,
                         routing_key=routing_key,
                         exchange=exchange)
    consumer.start()
    return consumer


def init_connection_producer(exchange: str):
    producer = RProducer(exchange=exchange)
    return producer


def get_images(img_dir: Path | str):
    return [f for f in listdir(img_dir) if isfile(join(img_dir, f))]


def img_prepare(img_orig: np.ndarray) -> str:
    img = img_orig.tobytes()
    encoded = base64.b64encode(img).decode('ascii')
    return encoded


def img_restore(msg, shape: tuple) -> np.ndarray:
    decoded = base64.b64decode(msg)
    return np.frombuffer(decoded, dtype=np.uint8).reshape(shape)
