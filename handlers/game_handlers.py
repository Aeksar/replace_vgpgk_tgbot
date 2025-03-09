from aiogram import Dispatcher, Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton, 
    InlineKeyboardMarkup,)
from aiogram.fsm.context import FSMContext
import asyncio

from utils.vgpgk import vgpgk, sheduled_replace
from states.game_state import BotStates
from dbs.mongo import mongo, Group

game_rout = Router()

@game_rout.message(Command('start'))
async def start_command(msg: Message):
    
    await msg.answer('Замены: /zam')


@game_rout.message(Command('zam'))
async def run_repl(msg: Message, state: FSMContext):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='ИБ-211', callback_data='ib-211')]
    ])
    await msg.answer('Группа?', reply_markup=kb)
    await state.set_state(BotStates.replaces)


@game_rout.callback_query(F.data == 'ib-211')
async def give_repl(call: CallbackQuery, state: FSMContext):
    data = vgpgk.get_replace('ИБ-211')
    if data:
        await call.message.answer(f'{data[0]}\n{data[1]}')
    else:
        file = FSInputFile(path=vgpgk._docx, filename='norm-zameni.docx')
        await call.message.answer_document(document=file, caption='Замен нет, но это не точно')
    await call.answer()
    await state.clear()


@game_rout.message(BotStates.replaces)
async def give_repl_msg(msg: Message, state: FSMContext):
    group = msg.text.upper()
    data = vgpgk.get_replace(group)
    if data:
        await msg.answer(f'{data[0]}\n{data[1]}')
    else:
        file = FSInputFile(path=vgpgk._docx, filename='norm-zameni.docx')
        await msg.answer_document(document=file, caption='Замен нет, но это не точно')
        
    await state.clear()
    
    
@game_rout.message(Command("letter"))
async def start_letter(msg: Message, state: FSMContext):
    await msg.answer("ВВедите название группы")
    await state.set_state(BotStates.letter)
    
@game_rout.message(BotStates.letter)
async def sub_to_letter(msg: Message, bot: Bot, state: FSMContext):
    await state.clear()
    chat_id = msg.chat.id
    group = msg.text.upper()
    status = await mongo.add_chat(group, chat_id)
    print('-------------------------')
    print(status)
    print('-----------------------------')
    if status:
        asyncio.create_task(sheduled_replace(bot))
        await msg.answer('Группа подписана на рассылку')
        return
    await msg.answer('Не удалось добавить группу в рассылку')
    

@game_rout.message(Command('refresh'))
async def new_repl(msg: Message):
    res = await vgpgk.download_replace()
    if res:
        await msg.answer('замены успешно обновлены')
    else:
        await msg.answer('замены не были обновлены')