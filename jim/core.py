from .config import *
import time as nix_time


class Jim:

    def to_dict(self):
        """
        Формируем базовый словарь
        :return: возвращаем шаблон для всех типов сообщений
        """
        result = {
            ACTION: None,
            TIME: None,
            USER: None,
            TO: None,
            CODE: None,
            MESSAGE: None
        }
        return result

    @staticmethod
    def from_dict(dictmsg):
        """
        Проверяет входной словарь на корректность
        :param dictmsg: входной словарь
        :return: если все ОК вернет исходный словарь
        """
        # Проверяем есть ли в словаре действие
        if ACTION in dictmsg:
            # Достаем дейтсвие
            action = dictmsg[ACTION]
            user = dictmsg[USER]
            account_name = dictmsg[TO]
            if action in ACTIONS:
                if action == PRESENCE:
                    return dictmsg[USER]
                elif action == RESPONSE and dictmsg[CODE] is not None:
                    return dictmsg
                elif action == ADD_USER or action == GET_USER or action == GET_CONTACTS \
                        and user is not None:
                    return dictmsg
                elif action == ADD_CONTACT or action == DEL_CONTACT and user is not None and account_name is not None:
                    return dictmsg
                elif action == MSG:
                    return dictmsg


class JimResponse(Jim):

    def __init__(self, response, error=None):
        self.response = response
        self.error = error

    def to_dict(self):
        message = super().to_dict()
        if self.response == BASIC_NOTICE or self.response == OK or self.response == ACCEPTED:
            message[ACTION] = RESPONSE
            message[TIME] = nix_time.time()
            message[CODE] = self.response
            message[MESSAGE] = self.error
            return message
        elif self.response == WRONG_REQUEST or self.response == SERVER_ERROR:
            message[ACTION] = RESPONSE
            message[TIME] = nix_time.time()
            message[CODE] = self.response
            message[MESSAGE] = self.error
            return message


class JimPresence(Jim):

    def __init__(self, action, login, time=None):
        self.action = action
        self.user = login
        if time:
            self.time = time
        else:
            self.time = nix_time.time()

    def create(self):
        message = super().to_dict()
        message[ACTION] = self.action
        message[TIME] = self.time
        message[USER] = self.user
        return message


class JimMessage(Jim):
    def __init__(self, action, login, msg_to, text, time=None):
        self.action = action
        self.login = login
        self.to = msg_to
        self.text = text
        if time:
            self.time = time
        else:
            self.time = nix_time.time()

    def create(self):
        message = super().to_dict()
        message[ACTION] = self.action
        message[TIME] = nix_time.time()
        message[USER] = self.login
        message[TO] = self.to
        message[MESSAGE] = self.text
        return message


class JimGetContacts(Jim):

    def __init__(self, login):
        self.login = login

    def to_dict(self):
        message = super().to_dict()
        message[ACTION] = GET_CONTACTS
        message[TIME] = nix_time.time()
        message[USER] = self.login
        return message


class JimAddContact(Jim):
    def __init__(self, login, contact_name):
        self.login = login
        self.contact = contact_name

    def to_dict(self):
        message = super().to_dict()
        message[ACTION] = ADD_CONTACT
        message[TIME] = nix_time.time()
        message[USER] = self.login
        message[TO] = self.contact
        return message


class JimDelContact(Jim):
    def __init__(self, login, contact_name):
        self.login = login
        self.contact = contact_name

    def to_dict(self):
        message = super().to_dict()
        message[ACTION] = DEL_CONTACT
        message[TIME] = nix_time.time()
        message[USER] = self.login
        message[TO] = self.contact
        return message
