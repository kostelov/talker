import os
import logging
import logging.handlers

LOG_FOLDERS_PATH = os.path.dirname(os.path.abspath(__file__))
SERVER_LOG_FILE_PATH = os.path.join(LOG_FOLDERS_PATH, 'server.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# Логгер с именем server
server_logger = logging.getLogger('server')
# Создаем обработчик с ротацией файла лога по дням
server_handler = logging.handlers.TimedRotatingFileHandler(SERVER_LOG_FILE_PATH, when='D')
# Связываем логгер с обработчиком
server_logger.addHandler(server_handler)
# Связывваем обработчки с форматером
server_handler.setFormatter(formatter)
server_logger.setLevel(logging.INFO)
