"""
Функции сервера:
- принимает сообщение клиента;
- формирует ответ клиенту;
- отправляет ответ клиенту;
- имеет параметры командной строки:
-p <port> - TCP-порт для работы (по умолчанию использует порт 7777)
-a <addr> - IP-адрес для прослушивания (по умолчанию слушает все доступные адреса)
"""
import time
import logging
from select import select
from socket import socket, AF_INET, SOCK_STREAM
from jim.event import get_message, send_message
from jim.core import Jim, JimResponse

import log.server_log_config
from log.loger import Log

logger = logging.getLogger('server')
logg = Log(logger)


class Handler:

    @logg
    def greet(self, presence_msg):
        """
        Выполнить приветствие
        :param presence_msg: запрос (словарь)
        :return: ответ сервера (словарь)
        """
        try:
            Jim.from_dict(presence_msg)
        except Exception as e:
            response = JimResponse(400, error=str(e))
            return response.to_dict()
        else:
            response = JimResponse(200)
            return response.to_dict()

    @logg
    def request(self, r_clients, all_clients):
        """
        Чтение запросов из списка клиентов
        :param r_clients: список клиентов, которые пишут
        :param all_clients: все клиенты
        :return: Словарь ответов сервера вида {сокет: запрос}
        """
        requests = {}
        for sock in r_clients:
            try:
                requests[sock] = get_message(sock)
            except:
                # add_to_log('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                all_clients.remove(sock)
        return requests

    @logg
    def response(self, requests, w_clients, all_clients):
        """
        Эхо-ответ сервера клиентам, от которых были запросы
        :param requests: {сокет: запрос}
        :param w_clients: список клиентов, которые ожидают ответа
        :param all_clientts: список всех клиентов
        :return: None
        """
        for sock in w_clients:
            for msg in requests:
                try:
                    # sock.send(requests[msg].encode('utf-8'))
                    send_message(sock, requests[msg])
                    # send_message(w_sock, {'response': time.asctime()})
                except:
                    # Сокет недоступен, клиент отключился
                    # add_to_log('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
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
                # add_to_log('Получен запрос на соединение от {}'.format(adr))
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
