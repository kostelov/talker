from jim.event import get_message, send_message
from jim.config import *
from jim.core import JimMessage


class Sender:
    def __init__(self, sock, login, response_queue=None):
        self.sock = sock
        self.response_queue = response_queue
        self.is_alive = False
        self.login = login

    def process_message(self):
        pass

    def pull(self):
        self.is_alive = True
        while True:
            if not self.is_alive:
                break
            data = self.process_message()
            # data = self.response_queue.get()
            if isinstance(data, dict):
                send_message(self.sock, data)

    def stop(self):
        self.is_alive = False


class Receiver:
    """ Класс получения сообщений"""
    def __init__(self, sock, request_queue=None):
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
            # if data[ACTION] == MSG:
            self.process_message(data)
            # else:
            #     self.request_queue.put(data)

    def stop(self):
        self.is_alive = False


class ConsoleReceiver(Receiver):

    def process_message(self, message):
        print('\n>> {}'.format(message[MESSAGE]))


class ConsoleSender(Sender):

    def prepare_message(self, action, login, msg_to=None, text=None):
        """
        Подготовка сообщения для отправки на сервер
        :param action: тип отправляемого сообщения
        :param msg_to: получатель
        :param text: текст сообщения
        :return: словарь
        """
        # data = (msg_to, self.login, text,)
        msg = JimMessage(action, login, msg_to, text)
        return msg.create()

    def process_message(self):
        text = input('<< ')
        if text.startswith('list'):
            msg = self.prepare_message(GET_CONTACTS, self.login)
        elif text.startswith('quit'):
            msg = self.prepare_message(QUIT, self.login)
            self.stop()
        elif text.startswith('add'):
            msg = self.prepare_message(ADD_CONTACT, None, text.split()[1])
        elif text.startswith('del'):
            msg = self.prepare_message(DEL_CONTACT, None, text.split()[1])
        else:
            msg = self.prepare_message(MSG, self.login, None, text)
        return msg
