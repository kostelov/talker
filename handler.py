from jim.event import get_message, send_message
from jim.config import *
from PyQt5.QtCore import QObject, pyqtSignal
from datetime import datetime
from history.history_config import HistoryFrom

history = HistoryFrom()


class Sender:
    """ Класс отправки сообщений """
    def __init__(self, sock, login, sender_queue):
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
    def __init__(self, sock, receiver_queue):
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
            if data[ACTION] == RESPONSE and data[CODE] != GONE:
                self.receiver_queue.put(data)
            else:
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


class GuiReceiver(Receiver, QObject):
    gotData = pyqtSignal(str)
    finished = pyqtSignal(int)

    def __init__(self, sock, receiver_queue):
        # инициализируем как Receiver
        Receiver.__init__(self, sock, receiver_queue)
        # инициализируем как QObject
        QObject.__init__(self)

    def process_message(self, message):
        tm = datetime.fromtimestamp(message[TIME]).strftime('%X')
        if message[USER] is None:
            message[USER] = 'Server'
        text = '{} {}: {}'.format(tm, message[USER], message[MESSAGE])
        self.add_to_history(message)
        self.gotData.emit(text)

    def pull(self):
        super().pull()
        self.finished.emit(0)

    @history
    def add_to_history(self, msg):
        return msg
