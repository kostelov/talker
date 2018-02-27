"""
Константы для JIM протокола
"""
ENCODING = 'utf-8'
# Ключи
ACTION = 'action'
TIME = 'time'
USER = 'user'
TO = 'to'
CODE = 'code'
MESSAGE = 'message'

# Значения
PRESENCE = 'presence'
RESPONSE = 'response'
PROBE = 'probe'
AUTH = 'auth'
JOIN = 'join'
LEAVE = 'leave'
MSG = 'msg'
QUIT = 'quit'
ADD_USER = 'add_user'
GET_USER = 'get_user'
ADD_CONTACT = 'add_contact'
GET_CONTACTS = 'get_contacts'
DEL_CONTACT = 'del_contact'
ACCOUNT_NAME = 'account_name'
FROM = 'from'
ERROR = 'error'

# Коды ответов (будут дополняться)
BASIC_NOTICE = 100
OK = 200
ACCEPTED = 202
WRONG_REQUEST = 400  # неправильный запрос/json объект
SERVER_ERROR = 500

# Кортеж из кодов ответа
CODES = (BASIC_NOTICE, OK, ACCEPTED, WRONG_REQUEST, SERVER_ERROR)

# Кортеж из действий
ACTIONS = (PRESENCE, RESPONSE, MSG, ADD_USER, GET_USER, ADD_CONTACT, GET_CONTACTS, DEL_CONTACT)