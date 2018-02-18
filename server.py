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
from select import select
from socket import socket, AF_INET, SOCK_STREAM
from jim.event import get_message, send_message
import logging
import server_log_config
import os

logger = logging.getLogger('server')


def log(func):
    def wrap(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.info('функция: {}|модуль: {}|инфо: {}'.format(func.__name__, os.path.basename(__file__), result))
        return result
    return wrap


@log
def add_to_log(args):
    return args


@log
def make_response(msg):
    """
    Обработка полученного запроса клиента и формирование ответа
    :param msg: запрос (словарь)
    :return: ответ сервера (словарь)
    """
    if 'action' in msg and msg['action'] == 'presence' and 'time' in msg and isinstance(msg['time'], float) \
            and 'user' in msg:
        return {'response': 200, 'message': msg['user']['status']}
    else:
        return {'response': 400, 'error': 'не верный запрос'}


@log
def request(r_clients, all_clients):
    """
    Чтение запросов из списка клиентов
    :param r_clients:
    :param all_clients:
    :return: Словарь ответов сервера вида {сокет: запрос}
    """
    requests = {}
    for sock in r_clients:
        try:
            requests[sock] = get_message(sock)
        except:
            add_to_log('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
            print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
            all_clients.remove(sock)
    return requests


@log
def response(requests, w_clients, all_clients):
    """
    Эхо-ответ сервера клиентам, от которых были запросы
    :param requests: {сокет: запрос}
    :param w_clients: список клиентов, которые ожидают ответа
    :param all_clientts: список всех клиентов
    :return:
    """
    for sock in all_clients:
        for w_sock in w_clients:
            if sock in requests:
                try:
                    send_message(w_sock, make_response(requests[sock]))
                    # send_message(w_sock, {'response': time.asctime()})
                except:
                    # Сокет недоступен, клиент отключился
                    add_to_log('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                    print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                    sock.close()
                    all_clients.remove(sock)


def start(address, port):
    """
    Данные хоста:
    :param address: адрес, на который отправляют запрос клиенты (localhost))
    :param port: порт, на которым сервер принимает запросы (7777)
    :return:
    """
    host = (address, port)
    # Список клментов
    clients = []
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind(host)
        sock.listen(5)
        # Таймаут для операций с сокетом
        sock.settimeout(0.2)
        add_to_log('Эхо-сервер запущен...')
        print('Эхо-сервер запущен...')
        while True:
            try:
                conn, adr = sock.accept()
            except OSError as e:
                # Время ожидания вышло
                pass
            else:
                add_to_log('Получен запрос на соединение от {}'.format(adr))
                print('Получен запрос на соединение от {}'.format(adr))
                # Клиент подключился - добавляем его в список
                clients.append(conn)
            finally:
                timeout = 0
                r = []
                w = []
                try:
                    # Опрос сокетов, которые подключились
                    # r - сокеты, которые отправляеют сообщения
                    # w - сокеты, которые ожидают ответ
                    # e -  сокеты с ошибкой
                    r, w, e = select(clients, clients, [], timeout)
                except:
                    # Клиент отключился - ничего не делать
                    pass

                requests = request(r, clients)
                response(requests, w, clients)


if __name__ == '__main__':
    import sys
    try:
        addr = sys.argv[1]
    except IndexError:
        addr = ''
    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        print('Не верный параметр')
        sys.exit(0)

    start(addr, port)
