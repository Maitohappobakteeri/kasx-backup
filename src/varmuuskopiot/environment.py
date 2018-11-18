
import socket
import datetime


class Environment:
    def __init__(self):
        self.hostname = None
        self.date = None

    @staticmethod
    def current_environment():
        env = Environment()
        env.hostname = socket.gethostname()
        env.date = datetime.datetime.today()
        return env
