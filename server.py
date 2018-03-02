"""
Функции сервера:
- принимает сообщение клиента;
- формирует ответ клиенту;
- отправляет ответ клиенту;
- имеет параметры командной строки:
-p <port> - TCP-порт для работы (по умолчанию использует порт 7777)
-a <addr> - IP-адрес для прослушивания (по умолчанию слушает все доступные адреса)
"""
import logging
from select import select
from socket import socket, AF_INET, SOCK_STREAM
from jim.event import get_message, send_message
from jim.core import *
from jim.config import *
from db.repository_s import Repository
from db.config_db import session
from db.errors import *


import log.server_log_config
from log.loger import Log

logger = logging.getLogger('server')
logg = Log(logger)


class Handler:
    def __init__(self):
        self.repo = Repository(session)

    @logg
    def greet(self, presence_msg):
        """
        Выполнить приветствие, регистрацию пользователя если его еще нет
        :param presence_msg: запрос (словарь)
        :return: ответ сервера (словарь)
        """
        try:
            user = Jim.from_dict(presence_msg)
            if not self.repo.user_exist(user):
                self.repo.add_user(user)
        except Exception as e:
            response = JimResponse(WRONG_REQUEST, error=str(e))
            return response.to_dict()
        else:
            response = JimResponse(OK)
            return response.to_dict()

    @logg
    def request(self, r_clients, all_clients):
        """
        Чтение запросов из списка клиентов
        :param r_clients: список клиентов, которые пишут
        :param all_clients: все клиенты
        :return: Словарь ответов сервера вида {сокет: запрос}
        """
        # requests = {}
        messages = []
        for sock in r_clients:
            try:
                msg = get_message(sock)
                messages.append(msg)
                # requests[sock] = msg
            except:
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                all_clients.remove(sock)
        return messages # requests

    @logg
    def response(self, messages, w_clients, all_clients):
        """
        Эхо-ответ сервера клиентам, от которых были запросы
        :param requests: {сокет: запрос}
        :param w_clients: список клиентов, которые ожидают ответа
        :param all_clientts: список всех клиентов
        :return: None
        """
        for sock in w_clients:
            for msg in messages:
                try:
                    # Получаем словарь
                    jmsg = Jim.from_dict(msg)
                    if jmsg[ACTION] == MSG:
                        send_message(sock, msg)
                    elif jmsg[ACTION] == GET_CONTACTS:
                        # Извлекаем имя пользователя и передаем в запрос
                        contacts = self.repo.get_contacts(jmsg[USER])
                        # Получаем контакты и заносим в список
                        contact_names = [contact.name for contact in contacts]
                        # Все ОК, формируем ответ (список контактов помещаем в поле для сообщений) и отправляем
                        resp = JimResponse(OK, contact_names)
                        send_message(sock, resp.to_dict())
                    elif jmsg[ACTION] == ADD_CONTACT:
                        # Извлекам пользователя и контакт
                        user_name = jmsg[USER]
                        contact_name = jmsg[TO]
                        try:
                            if not self.repo.contact_exist(user_name, contact_name):
                                # Добавляем в друзья пользователю контакт
                                self.repo.add_contact(user_name, contact_name)
                                # Все ОК, формируем ответ и отправляем
                                resp = JimResponse(ACCEPTED, 'Контакт добавлен')
                                send_message(sock, resp.to_dict())
                            else:
                                resp = JimResponse(WRONG_REQUEST, error='Контакт уже добавлен')
                                send_message(sock, resp.to_dict())
                        except UserDoesNotExist as e:
                            resp = JimResponse(WRONG_REQUEST, error='Контакт отсутствует')
                            send_message(sock, resp.to_dict())
                    elif jmsg[ACTION] == DEL_CONTACT:
                        # Извлекам пользователя и контакт
                        user_name = jmsg[USER]
                        contact_name = jmsg[TO]
                        try:
                            # Удаляем контакт из друзей пользователя
                            self.repo.del_contact(user_name, contact_name)
                            # Все ОК, формируем ответ и отправляем
                            resp = JimResponse(ACCEPTED, 'Контакт удален')
                            send_message(sock, resp.to_dict())
                        except UserDoesNotExist as e:
                            # Контакта нет, вызываем исключение
                            resp = JimResponse(WRONG_REQUEST, error='Контакт отсутствует')
                            send_message(sock, resp.to_dict())
                except:
                    # Сокет недоступен, клиент отключился
                    print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                    sock.close()
                    all_clients.remove(sock)


class Server:

    def __init__(self, handler, address, port):
        """
        Данные хоста:
        :param address: адрес, на который отправляют запрос клиенты (localhost))
        :param port: порт, на которым сервер принимает запросы (7777)
        :return:
        """
        self.handler = handler
        self.host = (address, port)
        # Список клиентов
        self.clients = []
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((address, port))
        self.sock.listen(5)
        # Таймаут для операций с сокетом
        self.sock.settimeout(0.2)

    def start(self):
        print('Эхо-сервер запущен...')
        while True:
            try:
                conn, adr = self.sock.accept()
                presence = get_message(conn)
                response = self.handler.greet(presence)
                send_message(conn, response)
            except OSError:
                # Время ожидания вышло
                pass
            else:
                print('Получен запрос на соединение от {}'.format(adr))
                # Клиент подключился - добавляем его в список
                self.clients.append(conn)
            finally:
                timeout = 0
                r = []
                w = []
                try:
                    # Опрос сокетов, которые подключились
                    # r - сокеты, которые отправляеют сообщения
                    # w - сокеты, которые ожидают ответ
                    # e -  сокеты с ошибкой
                    r, w, e = select(self.clients, self.clients, [], timeout)
                except:
                    # Клиент отключился - ничего не делать
                    pass

                requests = self.handler.request(r, self.clients)
                self.handler.response(requests, w, self.clients)


if __name__ == '__main__':
    import sys
    try:
        addr = sys.argv[1]
    except IndexError:
        addr = ''
    try:
        prt = int(sys.argv[2])
    except IndexError:
        prt = 7777
    except ValueError:
        print('Не верный параметр')
        sys.exit(0)

    handler = Handler()
    server = Server(handler, addr, prt)
    server.start()
