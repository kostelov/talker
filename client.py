import time
import logging
from socket import socket, AF_INET, SOCK_STREAM
from jim.event import send_message, get_message
from jim.core import Jim, JimPresence, JimMessage
from jim.config import *

import log.client_log_config
from log.loger import Log

logger = logging.getLogger('client')
logg = Log(logger)


class Client:

    def __init__(self, address, port, login='Guest'):
        self.login = login
        self.host = (address, port)
        self.sock = socket(AF_INET, SOCK_STREAM)

    @logg
    def parsing(self, msg):
        result = JimMessage()
        return result.parsed(msg)

    @logg
    def presence(self):
        presence_msg = JimPresence(PRESENCE, self.login)
        return presence_msg.create()

    def prepare_message(self, msg_to, text):
        """
        Подготовка сообщения для отправки на сервер
        :param msg_to: получатель
        :param text: текст сообщения
        :return: словарь
        """
        data = (msg_to, self.login, text,)
        msg = JimMessage()
        return msg.create(data)

    def read_message(self):
        print('Режим чтения...')
        while True:
            msg = get_message(self.sock)
            print(msg)
            print(self.parsing(msg))

    def write_message(self):
        print('Режим трансляции...')
        while True:
            text = input('>> ')
            if text == QUIT:
                break
            else:
                msg = self.prepare_message('#all', text)
                send_message(self.sock, msg)

    def start(self, rw_mode):
        self.sock.connect(self.host)
        send_message(self.sock, self.presence())
        response_msg = get_message(self.sock)
        result_response = Jim.from_dict(response_msg)
        if result_response == OK:
            if rw_mode == 'r':
                self.read_message()
            if rw_mode == 'w':
                self.write_message()
            else:
                raise Exception('Не верный режим работы клиента')


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

    user = 'Nick'
    client = Client(addr, prt, user)
    client.start(mode)
