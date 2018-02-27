from .core import Jim
from .config import *


class TestJim:
    def test_to_dict(self):
        self.test = Jim()
        result = self.test.to_dict()
        print(result)
        assert result[ACTION] is None