from aiogram import Bot, Dispatcher
from config.conf import environ
import asyncio

from handlers.game_handlers import game_rout
from utils.vgpgk import vgpgk, sheduled_replace


bot = Bot(token=environ.TOKEN)
dp = Dispatcher()
vgpgk_obj = vgpgk(bot)


dp.include_router(game_rout)


async def main():
    await dp.start_polling(bot)
    
    
if __name__=="__main__":
    asyncio.run(main())