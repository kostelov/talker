import time
from socket import socket, AF_INET, SOCK_STREAM
from jim.event import send_message, get_message
import logging
import client_log_config
import os

logger = logging.getLogger('client')

message = {
    'action': 'presence',
    'time': time.time(),
    'type': 'status',
    'user': {
        'account_name': 'name',
        'status': 'online'
    }
}


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
def response(msg):
    if 'response' in msg and msg['response'] == 200:
        return 'OK'
    elif 'response' in msg and msg['response'] == 400:
        return msg['error']


def start(address, port):
    host = (address, port)
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(host)
        while True:
            send_message(sock, message)
            rmessage = get_message(sock)
            print(response(rmessage))


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
