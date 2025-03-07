from aiogram import Dispatcher, Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext 
import asyncio
import os 

from utils.vgpgk import vgpgk, sheduled_replace
from states.game_state import BotStates

game_rout = Router()

@game_rout.message(Command('start'))
async def start_command(msg: Message, bot: Bot):
    vgpgk_obj = vgpgk(bot)
    asyncio.create_task(sheduled_replace(vgpgk_obj))
    await msg.answer('Замены: /zam')


@game_rout.message(Command('zam'))
async def run_repl(msg: Message, state: FSMContext):
    await state.set_state(BotStates.replaces)
    await msg.answer('Группа?')


@game_rout.message(BotStates.replaces)
async def give_repl(msg: Message, state: FSMContext):
    group = msg.text.upper()
    data = vgpgk.get_replace(group)
    if data:
        await msg.answer(f'    {data[0]}\n{data[1]}')
    else:
        file = FSInputFile(path=vgpgk._docx, filename='norm-zameni.docx')
        await msg.answer_document(document=file, caption='Замен нет, но это не точно')
        
    await state.set_state()
    
    
@game_rout.message(Command('refresh'))
async def new_repl(msg: Message):
    res = vgpgk.download_replace()
    if res:
        msg.answer('замены успешно обновлены')
    else:
        msg.answer('замены не были обновлены')