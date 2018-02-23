from db.config_server_db import *
from sqlalchemy import Column, Integer, ForeignKey, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    # Название таблицы
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    info = Column(String, nullable=True)

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


engine = create_engine('sqlite:///{}'.format(DB_PATH), echo=True)
metadata = Base.metadata
metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
