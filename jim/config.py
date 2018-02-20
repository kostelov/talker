"""
Константы для JIM протокола
"""
ENCODING = 'utf-8'
# Ключи
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
RESPONSE = 'response'
ERROR = 'error'

# Значения
PRESENCE = 'presence'
PROBE = 'probe'
MSG = 'msg'
QUIT = 'quit'
AUTH = 'auth'
JOIN = 'join'
LEAVE = 'leave'
TO = 'to'
FROM = 'from'
MESSAGE = 'message'

# Коды ответов (будут дополняться)
BASIC_NOTICE = 100
OK = 200
ACCEPTED = 202
WRONG_REQUEST = 400  # неправильный запрос/json объект
SERVER_ERROR = 500
