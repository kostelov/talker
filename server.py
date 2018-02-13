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
from jim.event import get_message


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
        conn.close()
