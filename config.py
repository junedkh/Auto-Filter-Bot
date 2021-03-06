
import os
import logging
from logging.handlers import RotatingFileHandler
from pyrogram import Client
from dotenv import load_dotenv


load_dotenv('config.env')

LOGGER = logging.getLogger(__name__)

def getConfig(name: str):
    return os.environ[name]

try:
    TG_BOT_TOKEN = getConfig('TG_BOT_TOKEN')
    APP_ID = int(getConfig('APP_ID'))
    API_HASH = getConfig('API_HASH')
    MAINCHANNEL_ID = getConfig('MAINCHANNEL_ID')
except KeyError as e:
    LOGGER.error("One or more env variables missing! Exiting now")
    exit(1)

LOGGER.info("Generating USER_SESSION_STRING")
with Client(':memory:', api_id=int(APP_ID), api_hash=API_HASH, bot_token=TG_BOT_TOKEN) as app:
    TG_USER_SESSION = app.export_session_string()

TG_BOT_SESSION = getConfig('TG_BOT_SESSION')
TG_BOT_WORKERS = int(getConfig('TG_BOT_WORKERS'))
LOG_FILE_NAME = getConfig('LOG_FILE_NAME')

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
