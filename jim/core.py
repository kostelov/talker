from .config import *
import time


class Jim:

    def to_dict(self):
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
        if ACTION in dictmsg and dictmsg[ACTION] == PRESENCE and TIME in dictmsg and isinstance(dictmsg[TIME], float):
            return OK
        elif RESPONSE in dictmsg and isinstance(dictmsg[RESPONSE], int) and TIME in dictmsg \
                and isinstance(dictmsg[TIME], float):
            if dictmsg[RESPONSE] == OK:
                return dictmsg[RESPONSE]
            elif dictmsg[RESPONSE] == WRONG_REQUEST or dictmsg[RESPONSE] == SERVER_ERROR:
                return dictmsg[RESPONSE], dictmsg[ERROR]
        else:
            return WRONG_REQUEST


class JimResponse:

    def __init__(self, response, error=None):
        self.response = response
        self.error = error

    def to_dict(self):
        if self.response == BASIC_NOTICE or self.response == OK:
            return {RESPONSE: self.response, TIME: time.time()}
        elif self.response == WRONG_REQUEST or self.response == SERVER_ERROR:
            return {RESPONSE: self.response, TIME: time.time(), ERROR: self.error}


class JimPresence:

    def __init__(self, login):
        self.login = login

    def create(self):
        message = {ACTION: PRESENCE, TIME: time.time(), USER: {ACCOUNT_NAME: self.login}}
        return message


class JimMessage:

    @staticmethod
    def create(data):
        message = {ACTION: MSG, TIME: time.time(), TO: data[0], FROM: data[1], MESSAGE: data[2]}
        return message

    @staticmethod
    def parsed(dictmsg):
        message = dictmsg[MESSAGE]
        return message


class JimContactList:

    def __init__(self, login):
        self.login = login

    def getcontacts(self):
        message = {ACTION: GET_CONTACTS, TIME: time.time(), USER: {ACCOUNT_NAME: self.login}}
        return message

    def parsed(self, dictmsg):
        pass
