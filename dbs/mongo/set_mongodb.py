from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, List

from config.conf import environ, logger
from dbs.mongo.models import Group


class Mongo:
    
    _solo = None
    
    def __new__(cls):
        if cls._solo is None:
            cls._solo = super(Mongo, cls).__new__(cls)
        return cls._solo
    
    def __init__(self):
        self.client = None
        self.init = None
    
    async def initilization(self):
        if self.init:
            return
        try:
            self.client = AsyncIOMotorClient(environ.MONGO_URL)
            self.db = self.client['users-db']
            await init_beanie(database=self.db, document_models=[Group])
            logger.debug("Установлено подключение к MongoDB")
            self.init = True
        except Exception as e:
            logger.error(f"Ошибка подключения к MongoDB: {e}")
            raise
    
    @staticmethod
    async def get_group(group_name: str) -> Optional[Group]:
        doc = await Group.find_one(Group.group_name == group_name)
        return doc
    
    @staticmethod
    async def create_group(group_name: str, chat_id: int) -> Group:
        doc = Group(group_name=group_name, chats=[chat_id])
        await doc.insert()
        return doc
    
    async def add_chat(self, group_name: str, chat_id: int) -> bool:
        try:
            doc = await Mongo.get_group(group_name)
            if doc:
                if chat_id in doc.chats:
                    logger.info(f"Попытка добавления существующего чата {chat_id}")
                    return True
                doc.chats.append(chat_id)
                await doc.save()
                logger.debug(f"Группа {group_name} найдена, чат {chat_id} добавлен")
                return True
            else:
                doc = await Mongo.create_group(group_name, chat_id)
                doc.chats.append(chat_id)
                await doc.save()
                logger.debug(f"Группа {group_name} была создана, и добавлен чат {chat_id}")
                return True
        except Exception as e:
            logger.error(f"Ошибка при добавлении группы: {e}")
            return False
            
    async def delete_chat(self, group_name: str, chat_id: int) -> bool:
        doc = await Mongo.get_group(group_name)
        if doc:
            if chat_id in doc.chats:
                doc.chats.remove(chat_id)
                logger.debug(f"Группа {group_name} найдена, чат {chat_id} удален")
                
            if not doc.chats:
                await doc.delete()
            else:
                doc.save()
                logger.debug(f"Группа {group_name} без чатов удалена")
            return True
        else:
            logger.info("Попытка удаления чата из несуществующего документа")
            return False
        
    @staticmethod
    async def get_all_groups() -> List[Group]:   
        try:
            groups = await Group.find_all().to_list()
            return groups
        except Exception as e:
            logger.error(f"Ошибка при получении всех групп: {e}")
            return []
   
mongo = Mongo()