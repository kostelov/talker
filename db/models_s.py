from .config_db import *
from sqlalchemy import Column, Integer, ForeignKey, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Base = declarative_base()


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
        self.uid = user_id
        self.cid = contact_id


# # Создаем движок
# engine = create_engine('sqlite:///{}'.format(DB_SEVER_PATH), echo=True)
# # Создаем структуру БД
# metadata = Base.metadata
# metadata.create_all(engine)
# # Создаем сессию для работы
# Session = sessionmaker(bind=engine)
# session = Session()
