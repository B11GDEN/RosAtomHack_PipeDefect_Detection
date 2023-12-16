from __future__ import annotations

import cv2
import time

from pathlib import Path
from multiprocessing import Process

from functions import init_connection_consumer, init_connection_producer
from functions import get_images, img_prepare


def sender():
    producer = None
    try:
        producer = init_connection_producer(exchange='server_input')

        img_dir = Path(__file__).absolute().parents[1] / 'imgs'
        size = (960, 600)

        while True:
            img_names = get_images(img_dir=img_dir)
            for img_name in img_names:
                img = cv2.imread(str(img_dir / img_name))
                img = cv2.resize(img, size)
                prep_img = img_prepare(img_orig=img)
                producer.publish(msg=prep_img, routing_key='server_input')

    except KeyboardInterrupt:
        if producer:
            producer.close()


def reader():
    consumer = None
    try:
        connect = False
        while not connect:
            try:
                consumer = init_connection_consumer(queue='client_consumer',
                                                    routing_key='server_output',
                                                    exchange='server_output')
                connect = True
            except AssertionError:
                continue

        while True:
            msg = consumer.read()
            if msg is not None:
                print(msg)
    except KeyboardInterrupt:
        if consumer:
            consumer.close()


def main():
    sender_process = None
    reader_process = None

    try:
        sender_process = Process(target=sender)
        sender_process.start()

        reader_process = Process(target=reader)
        reader_process.start()

        while True:
            time.sleep(0.01)

    except KeyboardInterrupt:
        if sender_process:
            sender_process.terminate()
            sender_process.join()
            sender_process.close()

        if reader_process:
            reader_process.terminate()
            reader_process.join()
            reader_process.close()


if __name__ == '__main__':
    main()
