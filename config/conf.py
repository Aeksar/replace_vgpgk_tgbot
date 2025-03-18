from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ConfigDict
import pymongo 
import logging
import sys

import pymongo.logger


class Environ(BaseSettings):
    TOKEN: str
    
    R_PORT: int
    R_HOST: str
    R_DB: int
    
    Y_TOKEN: str
    Y_ID: str
    Y_SECRET: str
    
    MONGO_URL: str
    
    
    model_config = SettingsConfigDict(
        env_file = ".env"
    )
    
environ = Environ()



logging.basicConfig(
    level=logging.DEBUG,
    format="[{asctime}] #{levelname} {filename} ({lineno}): {message}",
    style='{',
    encoding='UTF-8'
)

formatter = logging.Formatter("[{asctime}] #{levelname} {filename} ({lineno}): {message}", style='{',)

logger = logging.getLogger(__name__)
mongo_log = logging.getLogger("pymongo")
mongo_log.setLevel(logging.ERROR)

file_h = logging.FileHandler('logs.log', mode='w', encoding='UTF-8')
stdout_h = logging.StreamHandler(sys.stdout)

file_h.setFormatter(formatter)

logger.addHandler(file_h)
logger.addHandler(stdout_h)

logger.debug('logger active')