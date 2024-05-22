import logging
import datetime
import os

from pathlib import Path

logger = logging.getLogger('election_app_logger')

logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
time = datetime.datetime.now()
time = time.strftime("%Y-%m-%d-%H-%M-%S")
DATA = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'DATA'))
file_handler = logging.FileHandler(DATA / Path(f'{time}_election_app.log'))

console_handler.setLevel(logging.WARNING)
file_handler.setLevel(logging.DEBUG)

console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
