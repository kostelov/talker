import sys
from jim.config import *
from client import User
from handler import ConsoleReceiver, ConsoleSender
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
    name = 'Nick'

client = User(name)
client.start()

listener = ConsoleReceiver(client.sock, client.request_queue)
thread_listener = Thread(target=listener.pull)
thread_listener.daemon = False
thread_listener.start()

speaker = ConsoleSender(client.sock, client.login, client.response_queue)
thread_speaker = Thread(target=speaker.pull)
thread_speaker.daemon = False
thread_speaker.start()

while True:
    # # Получаем запрос/текст от пользователя
    # text = input('<< ')
    # if text.startswith('quit'):
    #     thread_listener.is_alive = False
    #     thread_speaker.is_alive = False
    # # Кладем в очередь для отправки на сервер
    # client.response_queue.put(text)
    # # Забираем ответ из очереди
    # response = client.request_queue.get()
    # # client.request_queue.task_done()
    # # Выводим сообщение
    # # message = client.parsing(response)
    # print('>> ', response[MESSAGE])
    if not thread_listener.is_alive:
        break
    if not thread_speaker.is_alive:
        break


client.stop()
