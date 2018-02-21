import time
import logging
from socket import socket, AF_INET, SOCK_STREAM
from jim.event import send_message, get_message
from jim.core import Jim, JimResponse, JimPresence, JimMessage
from jim.config import *

import log.client_log_config
from log.loger import Log

logger = logging.getLogger('client')
logg = Log(logger)

# @logg
# def add_to_log(args):
#     return args


class Client:

    def __init__(self, address, port, login='Guest'):
        self.login = login
        self.host = (address, port)
        self.sock = socket(AF_INET, SOCK_STREAM)

    @logg
    def parsing(self, msg):
        if 'response' in msg and msg['response'] == 200:
            return msg['message']
        elif 'response' in msg and msg['response'] == 400:
            return msg['error']

    @logg
    def presence(self):
        presence_msg = JimPresence(self.login)
        return presence_msg.create()

    def prepare_message(self, msg_to, text):
        """
        Подготовка сообщения для отправки на сервер
        :param msg_to: получатель
        :param text: тест сообщения
        :return: словарь
        """
        msg = JimMessage(msg_to, self.login, text)
        return msg.create()

    def read_message(self):
        print('Режим чтения...')
        while True:
            msg = get_message(self.sock)
            print(msg['message'])

    def write_message(self):
        print('Режим трансляции...')
        while True:
            text = input('>> ')
            if text == 'quit':
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
        # while True:
            # msg = input('Сообщение: ')
            # if msg == 'exit':
            #     break
            # else:
            #     sock.send(msg.encode('utf-8'))
            # send_message(self.sock, message)
            # rmessage = get_message(self.sock)
            # print(response(get_message(sock)))
            # print(rmessage)


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
