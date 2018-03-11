import time
import logging
from socket import socket, AF_INET, SOCK_STREAM
from jim.event import send_message, get_message
from jim.core import *
from jim.config import *

import log.client_log_config
from log.loger import Log

from queue import Queue

logger = logging.getLogger('client')
logg = Log(logger)


class User:

    def __init__(self, login, addr=None, port=None):
        self.login = login
        if not addr:
            addr = 'localhost'
        if not port:
            port = 7777
        self.host = (addr, port)
        self.receiver_queue = Queue()
        self.sender_queue = Queue()

    @logg
    def parsing(self, msg):
        result = Jim()
        return result.from_dict(msg)

    @logg
    def presence(self):
        """
        Формируем сообщение приветствие
        :return: сообщение (словарь)
        """
        presence_msg = JimPresence(PRESENCE, self.login, time.time())
        return presence_msg.create()

    def prepare_message(self, action, msg_to=None, text=None):
        """
        Подготовка сообщения для отправки на сервер
        :param action: тип отправляемого сообщения
        :param msg_to: получатель
        :param text: текст сообщения
        :return: словарь
        """
        # data = (msg_to, self.login, text,)
        msg = JimMessage(action, self.login, msg_to, text)
        return msg.create()

    def get_contacts(self):
        msg = JimGetContacts(self.login)
        send_message(self.sock, msg.to_dict())
        response = get_message(self.sock)
        # response = self.receiver_queue.get()
        return response[MESSAGE]

    def add_contact(self, contact_name):
        msg = JimAddContact(self.login, contact_name)
        send_message(self.sock, msg.to_dict())
        # response = get_message(self.sock)
        response = self.receiver_queue.get()
        return response

    def del_contact(self, contact_name):
        msg = JimDelContact(self.login, contact_name)
        send_message(self.sock, msg.to_dict())
        # response = get_message(self.sock)
        response = self.receiver_queue.get()
        return response

    def stop(self):
        self.sock.close()

    def message_send(self, msg_to, text):
        msg = self.prepare_message(MSG, msg_to, text)
        send_message(self.sock, msg)
        return msg

    def start(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(self.host)
        send_message(self.sock, self.presence())
        response_msg = get_message(self.sock)
        result_response = Jim.from_dict(response_msg)
        return result_response


if __name__ == '__main__':
    import sys
    try:
        addr = sys.argv[1]
    except IndexError:
        addr = 'localhost'
    try:
        prt = int(sys.argv[2])
    except IndexError:
        prt = 7777
    except ValueError:
        sys.exit(0)
    try:
        mode = sys.argv[3]
    except IndexError:
        mode = 'r'

    client = User('Nick')
    client.start()
