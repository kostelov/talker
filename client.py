import time
import logging
from socket import socket, AF_INET, SOCK_STREAM
from jim.event import send_message, get_message
from jim.core import *
from jim.config import *

import log.client_log_config
from log.loger import Log

from threading import Thread

logger = logging.getLogger('client')
logg = Log(logger)


class User:

    def __init__(self, login):
        self.login = login
        self.host = ('localhost', 7777)
        self.is_alive = False

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

    def prepare_message(self, msg_to, text):
        """
        Подготовка сообщения для отправки на сервер
        :param msg_to: получатель
        :param text: текст сообщения
        :return: словарь
        """
        # data = (msg_to, self.login, text,)
        msg = JimMessage(MSG, self.login, msg_to, text)
        return msg.create()

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

    def listener(self):
        self.is_alive = True
        print('Режим чтения...')
        while True:
            if not self.is_alive:
                break
            msg = get_message(self.sock)
            res = self.parsing(msg)
            print('>> ', res[MESSAGE])

    def speaker(self):
        """
         Принимает сообщение пользователя
         формирует корректное сообщение (доделать, убрать вызов get_, add_, del_contact)
         отправляет
        :return:
        """
        self.is_alive = True
        print('Режим трансляции...')
        while True:
            if not self.is_alive:
                break
            text = input('\n<< ')
            if text.startswith('list'):
                print('Список контактов:')
                self.get_contacts()
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

    def start(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(self.host)
        send_message(self.sock, self.presence())
        response_msg = get_message(self.sock)
        result_response = Jim.from_dict(response_msg)
        # return result_response
        if result_response[CODE] == OK:
            thread_listen = Thread(target=self.listener)
            thread_listen.daemon = True

            thread_speak = Thread(target=self.speaker)
            thread_speak.daemon = True

            thread_listen.start()
            thread_speak.start()

            while True:
                if not thread_listen.is_alive:
                    break
                if not thread_speak.is_alive:
                    break

            self.stop()
        #     if rw_mode == 'r':
        #         self.listener()
        #     if rw_mode == 'w':
        #         self.speaker()
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
        mode = 'r'

    client = User('Nick')
    client.start()
    # client.speaker()
