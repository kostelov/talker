import json

ENCODING = 'utf-8'


def dict_to_byte(dict_message):
    if isinstance(dict_message, dict):
        json_message = json.dumps(dict_message)
        message = json_message.encode(ENCODING)
        if isinstance(message, bytes):
            return message
    else:
        raise TypeError


def byte_to_dict(byte_message):
    if isinstance(byte_message, bytes):
        json_message = byte_message.decode(ENCODING)
        message = json.loads(json_message)
        if isinstance(message, dict):
            return message
        else:
            raise TypeError
    else:
        raise TypeError


def get_message(sock):
    message = sock.recv(1024)
    result = byte_to_dict(message)
    return result


def send_message(sock, message):
    byte_message = dict_to_byte(message)
    sock.send(byte_message)
