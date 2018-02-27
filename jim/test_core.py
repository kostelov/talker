from .core import *
from .config import *


class TestJim:
    def test_to_dict(self):
        self.test = Jim()
        result = self.test.to_dict()
        assert result[ACTION] is None


class TestJimPresence:
    def setup(self):
        self.test = JimPresence(PRESENCE, 'Test')

    def test_create(self):
        result = self.test.create()
        print(result)
        assert result[ACTION] == PRESENCE
        assert result[USER] == 'Test'


class TestJimResponse:
    def setup(self):
        self.test0 = JimResponse(200)
        self.test1 = JimResponse(500, 'Ошибка сервера')
        self.test2 = JimResponse(400, 'Не верный запрос')

    def test_to_dict(self):
        res0 = self.test0.to_dict()
        res1 = self.test1.to_dict()
        res2 = self.test2.to_dict()
        assert res0[ACTION] == RESPONSE and res0[CODE] == OK
        assert res1[ACTION] == RESPONSE and res1[CODE] == SERVER_ERROR and res1[MESSAGE] == 'Ошибка сервера'
        assert res2[ACTION] == RESPONSE and res2[CODE] == WRONG_REQUEST and res2[MESSAGE] == 'Не верный запрос'
