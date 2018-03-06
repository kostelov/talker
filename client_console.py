from jim.config import *
from client import User
from handler import ConsoleReceiver, ConsoleSender
from threading import Thread

client = User('Nick')
client.start()

listener = ConsoleReceiver(client.sock, client.request_queue)
thread_listener = Thread(target=listener.pull)
thread_listener.daemon = True
thread_listener.start()

speaker = ConsoleSender(client.sock, client.login, client.response_queue)
thread_speaker = Thread(target=speaker.pull)
thread_speaker.daemon = True
thread_speaker.start()

while True:
    # Получаем запрос/текст от пользователя
    text = input('<< ')
    if text.startswith('quit'):
        thread_listener.is_alive = False
        thread_speaker.is_alive = False
    # Кладем в очередь для отправки на сервер
    client.response_queue.put(text)
    # Забираем ответ из очереди
    response = client.request_queue.get()
    client.request_queue.task_done()
    # Разбираем и выводим
    message = client.parsing(response)
    print('>> {}: {}'.format(message[USER], message[MESSAGE]))
    if not thread_listener.is_alive:
        break
    if not thread_speaker.is_alive:
        break


client.stop()
