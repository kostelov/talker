from pytest import raises
from event import dict_to_byte, byte_to_dict


def test_dict_to_byte():
    with raises(TypeError):
        dict_to_byte(['test'])
    assert dict_to_byte({'test': 'test'}) == b'{"test": "test"}'


def test_byte_to_dict():
    assert byte_to_dict(b'{"test": "test"}') == {'test': 'test'}