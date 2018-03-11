"""
Пришлось написать два класса чтобы история писалась в один файл,
т.к. при отправки наш контакт в поле TO, а при получении сообщения -
в поле USER
"""
import os
from jim.config import *
from datetime import datetime

# Получаем директорию, в которой будет лежать файл истории
HISTORY_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))


class History:
    def __init__(self):
        # Получаем директорию, в которой будет лежать файл истории
        self.history_folder_path = HISTORY_FOLDER_PATH


class HistoryTo(History):
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # В сообщении лежит время в UNIX формате, достаем его и преобразуем к норм виду
            tm = datetime.fromtimestamp(result[TIME]).strftime('%X')
            # Формируем имя для файла истории по имени контакта
            history_file_name = 'inf_{}.his'.format(result[TO])
            # Формируем полное имя файла истории
            full_name_history_file = os.path.join(self.history_folder_path, history_file_name)
            with open(full_name_history_file, 'a', encoding='utf-8') as hfile:
                hfile.write('{} {}: {}\n'.format(tm, result[USER], result[MESSAGE]))
            return result
        return wrapper


class HistoryFrom(History):
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # В сообщении лежит время в UNIX формате, достаем его и преобразуем к норм виду
            tm = datetime.fromtimestamp(result[TIME]).strftime('%X')
            # Формируем имя для файла истории по имени контакта
            history_file_name = 'inf_{}.his'.format(result[USER])
            # Формируем полное имя файла истории
            full_name_history_file = os.path.join(self.history_folder_path, history_file_name)
            with open(full_name_history_file, 'a', encoding='utf-8') as hfile:
                hfile.write('{} {}: {}\n'.format(tm, result[USER], result[MESSAGE]))
            return result
        return wrapper
