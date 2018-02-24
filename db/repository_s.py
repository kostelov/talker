from .models_s import User, Contacts
# from .config_db import session
from .errors import *


class Repository:
    """ Серверное хранилище """
    def __init__(self, session):
        self.session = session

    def add_user(self, username, info=None):
        """ Добавление нового пользователя """
        new_user = User(username, info)
        if self.user_exist(new_user):
            raise UserAlreadyExists(username)
        else:
            self.session.add(new_user)
            self.session.commit()

    def user_exist(self, username):
        """ Проверяем существует ли пользователь """
        result = self.session.query(User).filter(User.name == username).count() > 0
        return result
