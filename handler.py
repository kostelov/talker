from jim.event import get_message, send_message
from jim.config import *


class Sender:
    def __init__(self, sock, response_queue):
        self.sock = sock
        self.response_queue = response_queue
        self.is_alive = False

    def pull(self):
        self.is_alive = True
        while True:
            if not self.is_alive:
                break
            data = self.response_queue.get()
            if isinstance(data, dict):
                send_message(self.sock, data)

    def stop(self):
        self.is_alive = False


class Receiver:
    """ Класс получения сообщений"""
    def __init__(self, sock, request_queue):
        self.sock = sock
        self.request_queue = request_queue
        self.is_alive = False

    def process_message(self, message):
        pass

    def pull(self):
        self.is_alive = True
        while True:
            if not self.is_alive:
                break
            data = get_message(self.sock)
            if data[ACTION] == MSG:
                self.process_message(data)
            else:
                self.request_queue.put(data)

    def stop(self):
        self.is_alive = False


class ConsoleReceiver(Receiver):

    def process_message(self, message):
        print('\n>> {}: {}'.format(message[USER], message[MESSAGE]))
