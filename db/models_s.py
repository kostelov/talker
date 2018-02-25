from .config_db import *
from sqlalchemy import Column, Integer, ForeignKey, String


class User(Base):
    # Название таблицы
    __tablename__ = 'User'
    # id первичный ключ
    uid = Column(Integer, primary_key=True, autoincrement=True)
    # имя пользователя
    name = Column(String(25), nullable=False, unique=True)
    # информация о пользователе (не обязательно)
    info = Column(String(50), nullable=True)

    def __init__(self, name, info=None):
        self.name = name
        if info:
            self.info = info

    def __repr__(self):
        return "<User('%s')>" % self.name


class Contacts(Base):
    __tablename__ = 'Contacts'
    # id первичный ключ
    cid = Column(Integer, primary_key=True, autoincrement=True)
    # id пользователя
    user_id = Column(Integer, ForeignKey('User.uid'))
    # id контакта
    contact_id = Column(Integer, ForeignKey('User.uid'))

    def __init__(self, user_id, contact_id):
        # .user_id должно совпадать с именем атрибута в таблице user_id
        self.user_id = user_id
        self.contact_id = contact_id
