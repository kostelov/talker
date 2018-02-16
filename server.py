"""
Функции сервера:
- принимает сообщение клиента;
- формирует ответ клиенту;
- отправляет ответ клиенту;
- имеет параметры командной строки:
-p <port> - TCP-порт для работы (по умолчанию использует порт 7777)
-a <addr> - IP-адрес для прослушивания (по умолчанию слушает все доступные адреса)
"""
from select import select
from socket import socket, AF_INET, SOCK_STREAM
from jim.event import get_message, send_message


def presence_response(msg):
    if 'action' in msg and msg['action'] == 'presence' and 'time' in msg and isinstance(msg['time'], float):
        return {'response': 200}
    else:
        return {'response': 400, 'error': 'не верный запрос'}

def request(r_clients, all_clients):
    '''
    Чтение запросов из списка клиентов
    :param r_clients:
    :param all_clients:
    :return:
    '''
    # Словарь ответов сервера вида {сокет: запрос}
    response = {}
    for sock in r_clients:
        try:
            response[sock] = get_message(sock)
        except:
            print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
            all_clients.remove(sock)
    return response


def mainloop(address, port):
    '''
    Данные хоста:
    :param address: адрес, на который отправляют запрос клиенты (localhost))
    :param port: порт, на которым сервер принимает запросы (7777)
    :return:
    '''
    host = (address, port)
    # Список клментов
    clients = []
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(host)
    sock.listen(5)
    # Таймаут для операций с сокетом
    sock.settimeout(0.2)
    print('Эхо-сервер запущен!')
    while True:
        try:
            conn, adr = sock.accept()
        except OSError as e:
            # Время ожидания вышло
            pass
        else:
            print("Получен запрос на соединение от {}".format(adr))
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
            print(requests)
            # response(requests, w, clients)
            # message = get_message(conn)
            # print(message)
            # response = presence_response(message)
            # send_message(conn, response)
            # conn.close()

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

    mainloop(addr, port)
