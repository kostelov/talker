from pytest import raises
from .event import dict_to_byte


def test_dict_to_byte():
    with raises(TypeError):
        dict_to_byte('test')
        dict_to_byte(['test'])
        dict_to_byte(123)
        dict_to_byte(('test',))
    assert dict_to_byte({'test': 'test'}) == b'{"test": "test"}'
