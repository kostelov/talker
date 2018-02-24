from db.config_server_db import *
from sqlalchemy import Column, Integer, ForeignKey, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    # Название таблицы
    __tablename__ = 'users'
    # id первичный ключ
    uid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), nullable=False, unique=True)
    info = Column(String(50), nullable=True)

    def __init__(self, name, info=None):
        self.name = name
        if info:
            self.info = info

    def __repr__(self):
        return "<User('%s')>" % self.name


class Contacts(Base):
    __tablename__ = 'contacts'
    cid = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.uid'))
    contact_id = Column(Integer, ForeignKey('User.uid'))

    def __init__(self, user_id, contact_id):
        self.uid = user_id
        self.cid = contact_id


# Создаем движок
engine = create_engine('sqlite:///{}'.format(DB_PATH), echo=True)
# Создаем структуру БД
metadata = Base.metadata
metadata.create_all(engine)
# Создаем сессию для работы
Session = sessionmaker(bind=engine)
session = Session()
