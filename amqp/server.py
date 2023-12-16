from __future__ import annotations

import cv2

import numpy as np

from functions import init_connection_producer, init_connection_consumer
from functions import img_restore


def main():
    consumer = None
    producer = None
    try:
        connect = False
        while not connect:
            try:
                consumer = init_connection_consumer(queue='server_consumer',
                                                    routing_key='server_input',
                                                    exchange='server_input')
                connect = True
            except AssertionError:
                continue

        producer = init_connection_producer(exchange='server_output')

        shape = (600, 960, 3)

        while True:
            msg = consumer.read()
            if msg is not None:
                img = img_restore(msg, shape)

                cv2.imshow('server', img)
                cv2.waitKey(1)

                # TODO: we need the model
                res = np.zeros((5, 3), dtype='uint8').tolist()

                producer.publish(msg=res, routing_key='server_output')
    except KeyboardInterrupt:
        if consumer:
            consumer.close()
        if producer:
            producer.close()


if __name__ == '__main__':
    main()
