from socket import *
from .jim.event import send_message

message = {
    'user': 'Max',
    'text': 'Hello, Leo'
}

sock = socket()
sock.connect(('localhost', 7777))
send_message(sock, message)
sock.close()
