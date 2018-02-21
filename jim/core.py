from .config import *
import time


class Jim:

    # def __init__(self, *args, **dictmsg):
    #     self.dictmsg = dictmsg

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

    def __init__(self, msg_to, login, text):
        self.msg_to = msg_to
        self.login = login
        self.text = text

    def create(self):
        message = {ACTION: MSG, TIME: time.time(), TO: self.msg_to, FROM: self.login, MESSAGE: self.text}
        return message

    def parsed(self):
        pass
