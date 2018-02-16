import time
from socket import *
from jim.event import send_message, get_message

message = {
    'action': 'presence',
    'time': time.time(),
    'type': 'status',
    'user': {
        'account_name': 'name',
        'status': 'online'
    }
}


def response(msg):
    if 'response' in msg and msg['response'] == 200:
        return 'OK'
    elif 'response' in msg and msg['response'] == 400:
        return msg['error']


if __name__ == '__main__':
    import sys
    sock = socket()
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

    sock.connect((addr, port))
    send_message(sock, message)
    # rmessage = get_message(sock)
    # print(response(rmessage))
    sock.close()
