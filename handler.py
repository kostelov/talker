from jim.event import get_message, send_message
from jim.config import *
from jim.core import JimMessage


class Sender:
    """ Класс отправки сообщений """
    def __init__(self, sock, login, response_queue=None):
        self.sock = sock
        self.response_queue = response_queue
        self.is_alive = False
        self.login = login

    def process_message(self, text):
        pass

    def pull(self):
        self.is_alive = True
        while True:
            if not self.is_alive:
                break
            # Получаем запрос/сообщение из очереди
            data = self.response_queue.get()
            self.response_queue.task_done()
            # Отправляем на обработку
            msg = self.process_message(data)
            if isinstance(msg, dict):
                # Отправляем на сервер
                send_message(self.sock, msg)

    def stop(self):
        self.response_queue.put(None)
        self.response_queue.join()
        self.is_alive = False


class Receiver:
    """ Класс получения сообщений """
    def __init__(self, sock, request_queue=None):
        self.sock = sock
        self.request_queue = request_queue
        self.is_alive = False

    def process_message(self, message):
        pass

    def pull(self):
        self.is_alive = True
        while True:
            if not self.is_alive:
                break
            # Получаем ответ сервера
            data = get_message(self.sock)
            # data = self.request_queue.get()
            # if data[ACTION] == QUIT:
            #     self.stop()
            # else:
            # Кладем в очередь
            self.request_queue.put(data)
            # self.process_message(data)
            # else:
            #     self.request_queue.put(data)

    def stop(self):
        self.request_queue.put(None)
        self.request_queue.join()
        self.is_alive = False


class ConsoleReceiver(Receiver):

    def process_message(self, message):
        print('\n>> {}'.format(message[MESSAGE]))


class ConsoleSender(Sender):

    def prepare_message(self, action, login, msg_to=None, text=None):
        """
        Подготовка сообщения для отправки на сервер
        :param action: тип отправляемого сообщения
        :param login: отправитель
        :param msg_to: получатель
        :param text: текст сообщения
        :return: словарь
        """
        # data = (msg_to, self.login, text,)
        msg = JimMessage(action, login, msg_to, text)
        return msg.create()

    def process_message(self, text):
        # text = input('<< ')
        if text.startswith('list'):
            msg = self.prepare_message(GET_CONTACTS, self.login)
        # elif text.startswith('quit'):
        #     msg = self.prepare_message(QUIT, self.login)
        elif text.startswith('add'):
            msg = self.prepare_message(ADD_CONTACT, self.login, text.split()[1], None)
        elif text.startswith('del'):
            msg = self.prepare_message(DEL_CONTACT, self.login, text.split()[1], None)
        else:
            msg = self.prepare_message(MSG, self.login, None, text)
        return msg
