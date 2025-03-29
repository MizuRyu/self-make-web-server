import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multithreadwebserver import MultiThreadWebServer
from common.server.server import Server
if __name__ == "__main__":
    # MultiThreadWebServer().serve()
    Server().serve()