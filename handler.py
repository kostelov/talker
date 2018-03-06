from jim.event import get_message, send_message
from jim.config import *
from jim.core import JimMessage


class Sender:
    """ Класс отправки сообщений """
    def __init__(self, sock, login, sender_queue=None):
        self.sock = sock
        self.sender_queue = sender_queue
        self.is_alive = False
        self.login = login

    def process_message(self, text):
        pass

    def pull(self):
        self.is_alive = True
        while True:
            if not self.is_alive:
                break
            # Получаем запрос/сообщение из очереди
            data = self.sender_queue.get()
            if isinstance(data, dict):
                # Отправляем на сервер
                send_message(self.sock, data)

    def stop(self):
        self.sender_queue.put(None)
        self.sender_queue.join()
        self.is_alive = False


class Receiver:
    """ Класс получения сообщений """
    def __init__(self, sock, receiver_queue=None):
        self.sock = sock
        self.receiver_queue = receiver_queue
        self.is_alive = False

    def process_message(self, message):
        pass

    def pull(self):
        self.is_alive = True
        while True:
            if not self.is_alive:
                break
            # Получаем ответ сервера
            data = get_message(self.sock)
            self.process_message(data)

    def stop(self):
        self.receiver_queue.put(None)
        self.receiver_queue.join()
        self.is_alive = False


class ConsoleReceiver(Receiver):

    def process_message(self, message):
        if message[USER] is not None:
            print('\n>> {}: {}'.format(message[USER], message[MESSAGE]))
        else:
            print('\n>> {}'.format(message[MESSAGE]))
