import logging
import logging.handlers
import os

LOG_FOLDERS_PATH = os.path.dirname(os.path.abspath(__file__))
SERVER_LOG_FILE_PATH = os.path.join(LOG_FOLDERS_PATH, 'server.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# Логгер с именем server
server_logger = logging.getLogger('server')
# Создаем обработчик с ротацией файла лога по дням
server_handler = logging.handlers.TimedRotatingFileHandler(SERVER_LOG_FILE_PATH, when='MIDNIGHT')
# Связывваем обработчки с форматером
server_handler.setFormatter(formatter)
# Связываем логгер с обработчиком
server_logger.addHandler(server_handler)
server_logger.setLevel(logging.DEBUG)
