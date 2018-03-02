import time
import logging
from socket import socket, AF_INET, SOCK_STREAM
from jim.event import send_message, get_message
from jim.core import *
from jim.config import *

import log.client_log_config
from log.loger import Log

logger = logging.getLogger('client')
logg = Log(logger)


class User:

    def __init__(self, login):
        self.login = login
        self.host = ('localhost', 7777)

    @logg
    def parsing(self, msg):
        result = JimMessage()
        return result.parsed(msg)

    @logg
    def presence(self):
        """
        Формируем сообщение приветствие
        :return: сообщение (словарь)
        """
        presence_msg = JimPresence(PRESENCE, self.login, time.time())
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

    def get_contacts(self):
        msg = JimGetContacts(self.login)
        send_message(self.sock, msg.to_dict())
        response = get_message(self.sock)
        return response[MESSAGE]

    def add_contact(self, contact_name):
        msg = JimAddContact(self.login, contact_name)
        send_message(self.sock, msg.to_dict())
        response = get_message(self.sock)
        return response

    def del_contact(self, contact_name):
        msg = JimDelContact(self.login, contact_name)
        send_message(self.sock, msg.to_dict())
        response = get_message(self.sock)
        return response

    def stop(self):
        self.sock.close()

    def read_message(self):
        print('Режим чтения...')
        while True:
            msg = get_message(self.sock)
            print(self.parsing(msg))

    def write_message(self):
        print('Режим трансляции...')
        while True:
            text = input('>> ')
            if text.startswith('list'):
                print('Список контактов:')
                for items in self.get_contacts():
                    print(items)
            elif text == QUIT:
                break
            elif text.startswith('add'):
                    response = self.add_contact(text.split()[1])
                    if response[CODE] == ACCEPTED:
                        print('Контакт добавлен')
                    else:
                        print(response[MESSAGE])
            elif text.startswith('del'):
                response = self.del_contact(text.split()[1])
                if response[CODE] == ACCEPTED:
                    print('Контакт удален')
                else:
                    print(response[MESSAGE])
            else:
                msg = self.prepare_message('#all', text)
                send_message(self.sock, msg)

    def start(self, rw_mode):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(self.host)
        send_message(self.sock, self.presence())
        response_msg = get_message(self.sock)
        result_response = Jim.from_dict(response_msg)
        return result_response
        # if result_response[CODE] == OK:
        #     if rw_mode == 'r':
        #         self.read_message()
        #     if rw_mode == 'w':
        #         self.write_message()
        #     else:
        #         print(result_response[CODE], result_response[MESSAGE])


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
        mode = 'w'

    client = User('Nick')
    client.start(mode)
    client.write_message()
