import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DB_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
DB_SEVER_PATH = os.path.join(DB_FOLDER_PATH, 'server.db')
# Создаем движок
engine = create_engine('sqlite:///{}'.format(DB_SEVER_PATH), echo=False)
# Создаем структуру БД
metadata = Base.metadata
metadata.create_all(engine)
# Создаем сессию для работы
Session = sessionmaker(bind=engine)
session = Session()
# session = session