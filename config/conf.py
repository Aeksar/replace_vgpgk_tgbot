from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ConfigDict
import logging
import sys


class Environ(BaseSettings):
    TOKEN: str
    
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

file_h = logging.FileHandler('logs.log', mode='w', encoding='UTF-8')
stdout_h = logging.StreamHandler(sys.stdout)

file_h.setFormatter(formatter)

logger.addHandler(file_h)
logger.addHandler(stdout_h)

logger.debug('logger active фыафврп')