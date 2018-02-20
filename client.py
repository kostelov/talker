import time
import logging
from socket import socket, AF_INET, SOCK_STREAM
from jim.event import send_message, get_message

import log.client_log_config
from log.loger import Log

logger = logging.getLogger('client')
logg = Log(logger)

message = {
    'action': 'presence',
    'time': time.time(),
    'type': 'status',
    'user': {
        'account_name': 'name',
        'status': 'В сети'
    }
}


# @logg
# def add_to_log(args):
#     return args


@logg
def response(msg):
    if 'response' in msg and msg['response'] == 200:
        return msg['message']
    elif 'response' in msg and msg['response'] == 400:
        return msg['error']


def start(address, port):
    host = (address, port)
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(host)
        while True:
            msg = input('Сообщение: ')
            if msg == 'exit':
                break
            else:
                sock.send(msg.encode('utf-8'))
            # send_message(sock, message)
            # rmessage = get_message(sock)
            # print(response(get_message(sock)))
            # print(rmessage)


if __name__ == '__main__':
    import sys
    try:
        addr = sys.argv[1]
    except IndexError:
        addr = 'localhost'
    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        sys.exit(0)

    start(addr, port)
