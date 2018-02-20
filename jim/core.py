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
