from __future__ import annotations

import time

from multiprocessing import Process

from client import main as client_main
from server import main as server_main


def main():
    client_process = None
    server_process = None
    
    try:
        client_process = Process(target=client_main)
        client_process.start()
    
        server_process = Process(target=server_main)
        server_process.start()
    
        while True:
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        if client_process:
            client_process.terminate()
            client_process.join()
            client_process.close()
        
        if server_process:
            server_process.terminate()
            server_process.join()
            server_process.close()


if __name__ == '__main__':
    main()
