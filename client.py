import sys
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

if __name__ == '__main__':
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
    print(get_message(sock))
    sock.close()
