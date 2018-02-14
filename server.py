"""
Функции сервера:
- принимает сообщение клиента;
- формирует ответ клиенту;
- отправляет ответ клиенту;
- имеет параметры командной строки:
-p <port> - TCP-порт для работы (по умолчанию использует порт 7777)
-a <addr> - IP-адрес для прослушивания (по умолчанию слушает все доступные адреса)
"""

import sys
from socket import *
from jim.event import get_message, send_message


def presence_response(msg):
    if 'action' in msg and msg['action'] == 'presence' and 'time' in msg and isinstance(msg['time'], float):
        return {'response': 200}
    else:
        return {'response': 400, 'error': 'неверный формат запроса'}


if __name__ == '__main__':
    sock = socket()
    try:
        addr = sys.argv[1]
    except IndexError:
        addr = ''
    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        sys.exit(0)

    sock.bind((addr, port))
    sock.listen(5)
    print('server started')

    while True:
        conn, adr = sock.accept()
        print("Получен запрос на соединение от {}".format(adr))
        message = get_message(conn)
        print(message)
        response = presence_response(message)
        send_message(conn, response)
        conn.close()
