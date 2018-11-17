
import socket


class Environment:
    def __init__(self):
        self.hostname = None

    @staticmethod
    def current_environment():
        env = Environment()
        env.hostname = socket.gethostname()
        return env
