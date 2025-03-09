import requests
from docx import Document
from aiogram import Bot
from comtypes.client import CreateObject
from typing import Optional, List
import asyncio
import aiohttp
import hashlib
import os

from config.conf import logger
from dbs.conf_redis import get_redis_client
from dbs.mongo import Group, mongo

class vgpgk:

    _url = "https://vgpgk.ru/raspisanie/vgpgk-zameny-1-korpus.doc?v=2023011141816"
    _doc = os.path.abspath('.\\files\\zameni.doc')
    _docx = os.path.abspath('.\\files\\norm-zameni.docx')
    _hash_file = os.path.abspath('.\\files\\zameni.doc.sha256')

    @classmethod
    def _calculate_sha256(cls, filepath: str) -> str:
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(), b""):
                    sha256_hash.update(chunk)
            logger.debug(f'Хеш посчитан для {filepath}')
            return sha256_hash.hexdigest()
        
        except Exception as e:
            logger.error(f'Траблы с вычислением хеша: {e}')
            
        
    @classmethod
    def _save_hash(cls, hash_val: str) -> None:
        try:
            client = get_redis_client()
            client.set('zam_hash', hash_val)
            logger.debug(f'Хеш сохранен в {hash_val}')
        except Exception as e:
            logger.error(f'Пролемы с сохранением хеша: {e}')
            
    
    @classmethod
    def _load_hash(cls) -> Optional[str]:
        try:
            client = get_redis_client()
            hash_val = client.get('zam_hash')
            logger.debug(f"Хеш прочитан {hash_val}")
            return hash_val
        except Exception as e:
            logger.error(f"Ошибка при сохранении хеша: {e}")
            return None

    @classmethod
    async def download_replace(cls) -> None:
        old_hash = cls._load_hash()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(cls._url) as response:
                    
                    response.raise_for_status()
                    logger.info('Отправлен запрос на получение замен')
                    
                    client = get_redis_client()
                    hash_val = b""
                    async for chunk in response.content.iter_chunked(1024):
                        hash_val += chunk
                    client.set('new_zam_hash', hash_val)
            
            new_hash = cls._calculate_sha256(cls._doc)
            
            if new_hash is None:
                logger.error('Проблемы с рассчетом новго хеша')
                return False
            if new_hash != old_hash:
                cls._save_hash(new_hash)
                cls.convert_doc_to_docx(cls._doc, cls._docx)
                logger.info(f'Замены обновлены\n{new_hash}\n{old_hash}')
                return True
            else:
                logger.info('Замены те же')
                return False
        except Exception as e:
            logger.error(f"Ошибка при скачивании файла: {e}")
            return False

    @staticmethod
    def convert_doc_to_docx(doc_path: str, docx_path: str) -> None:
        try:
            word = CreateObject("Word.Application")
            word.Visible = False
            doc = word.Documents.Open(doc_path)
            doc.SaveAs2(docx_path, FileFormat=12)
            doc.Close()
            word.Quit()

        except Exception as e: 
            logger.error(f"Ошибка при конвертации: {e}")
            raise e


    @classmethod
    def get_replace(cls, group_name: str) -> Optional[List[str]]:
        find = False
        document = Document(cls._docx)

        for table in document.tables:
            for row_i in range(len(table.rows)):
                for col_i in range(len(table.columns)):
                    ans = table.cell(row_i, col_i).text
                    if ans.startswith(group_name):
                        group = table.cell(row_i, col_i).text
                        replace = table.cell(row_i+1, col_i).text
                        find = True
                    if find:
                        return [group, replace]
                    
        return None



async def sheduled_replace(bot: Bot, interval: int = 10):
    while True:
        try:
            await asyncio.sleep(interval)
            if await vgpgk.download_replace():
                groups = await mongo.get_all_groups()
                for group in groups:
                    group_replace = vgpgk.get_replace(group.group_name)
                    for chat in group.chats:
                        await bot.send_message(chat_id=chat, text=f'{group_replace[0]}\n{group_replace[1]}')
            else:
                groups = await mongo.get_all_groups()
                for group in groups:
                    group_replace = vgpgk.get_replace(group.group_name)
                    for chat in group.chats:
                        await bot.send_message(chat_id=chat, text='Файл с заменами не был изменен')
        except Exception as e:
            logger.error(f"Ошибка при автоматическом обновлении замен {e}")
            

            
if __name__=="__main__":
    replace_data = vgpgk.get_replace("ИС-223")
    if replace_data:
        print(replace_data[0])
        print(replace_data[1])
        print(vgpgk._docx)
    else:
        print('pusto')
        