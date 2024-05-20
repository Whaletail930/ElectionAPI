import logging
import datetime

logger = logging.getLogger('election_app_logger')

# Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
time = datetime.datetime.now()
time = time.strftime("%Y-%m-%d-%H-%M-%S")
file_handler = logging.FileHandler(f'{time}_election_app.log')

console_handler.setLevel(logging.WARNING)
file_handler.setLevel(logging.DEBUG)

console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
