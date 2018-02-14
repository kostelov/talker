import json

ENCODING = 'utf-8'


def dict_to_byte(dict_message):
    '''
    :param dict_message: на вход подается словарь
    :return: кодированное сообщение
>>> dict_to_byte({'test': 'test'})
b'{"test": "test"}'

    '''
    if isinstance(dict_message, dict):
        json_message = json.dumps(dict_message)
        message = json_message.encode(ENCODING)
        if isinstance(message, bytes):
            return message
    else:
        raise TypeError


def byte_to_dict(byte_message):
    '''
    :param byte_message: кодированное сообщение
    :return: словарь
>>> byte_to_dict(b'{"test": "test"}')
{'test': 'test'}

    '''
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

if __name__ == '__main__':
    import doctest
    doctest.testmod()