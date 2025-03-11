from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
import asyncio

from handlers.game_handlers import game_rout
from dbs.mongo import mongo
from dbs.conf_redis import get_redis_client
from config.conf import environ
from utils.vgpgk import sheduled_replace
redis_client = get_redis_client()
storage = RedisStorage(redis=redis_client)

bot = Bot(token=environ.TOKEN)
dp = Dispatcher(storage=storage)

dp.include_router(game_rout)

async def main():
    
    asyncio.create_task(sheduled_replace(bot))
    await mongo.initilization()
    await dp.start_polling(bot)
    
    
if __name__=="__main__":
    asyncio.run(main())