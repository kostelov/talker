import sys
from jim.config import *
from client import User
from handler import ConsoleReceiver, Sender
from threading import Thread

try:
    addr = sys.argv[1]
except IndexError:
    addr = 'localhost'
try:
    prt = int(sys.argv[2])
except IndexError:
    prt = 7777
except ValueError:
    sys.exit(0)
try:
    name = sys.argv[3]
except IndexError:
    name = 'Leo'

client = User(name)
client.start()

listener = ConsoleReceiver(client.sock, client.receiver_queue)
thread_listener = Thread(target=listener.pull)
thread_listener.daemon = True
thread_listener.start()

speaker = Sender(client.sock, client.login, client.sender_queue)
thread_speaker = Thread(target=speaker.pull)
thread_speaker.daemon = True
thread_speaker.start()

while True:
    # Получаем запрос/текст от пользователя
    text = input('<< ')
    # Корректное завершение потоков при выходе
    if text.startswith('quit'):
        thread_listener.is_alive = False
        thread_speaker.is_alive = False
        break
    else:
        # Готовим сообщение для отправки
        if text.startswith('list'):
            msg = client.prepare_message(GET_CONTACTS)
        elif text.startswith('add'):
            msg = client.prepare_message(ADD_CONTACT, text.split()[1], None)
        elif text.startswith('del'):
            msg = client.prepare_message(DEL_CONTACT, text.split()[1], None)
        elif text.startswith('msg'):
            # Делим сообщение на команду, имя и содержимое
            contact_name = text.split()[1]
            num = len(text.split()[0] + text.split()[1]) + 2
            msg = client.prepare_message(MSG, contact_name, text[num:])
        else:
            msg = client.prepare_message(MSG, None, 'Не верный формат сообщения')
        # Кладем в очередь для отправки на сервер
        client.sender_queue.put(msg)

client.stop()
