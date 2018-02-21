import os
import logging
import logging.handlers

LOG_FOLDERS_PATH = os.path.dirname(os.path.abspath(__file__))
CLIENT_LOG_FILE_PATH = os.path.join(LOG_FOLDERS_PATH, 'client.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# Логгер с именем client
client_logger = logging.getLogger('client')
# Обработчик будет логгер, который пишет в файл
client_handler = logging.FileHandler(CLIENT_LOG_FILE_PATH, encoding='utf-8')
# Связываем логгер с обработчиком
client_logger.addHandler(client_handler)
# Связываем обработчик с форматером
client_handler.setFormatter(formatter)
client_logger.setLevel(logging.INFO)
