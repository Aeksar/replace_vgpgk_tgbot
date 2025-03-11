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
from filters import GroupFilter
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


@game_rout.message(BotStates.replaces, GroupFilter())
async def give_repl_msg(msg: Message, state: FSMContext):
    group = msg.text.upper()
    data = vgpgk.get_replace(group)
    if data:
        await msg.answer(f'{data[0]}\n{data[1]}')
    else:
        file = FSInputFile(path=vgpgk._docx, filename='norm-zameni.docx')
        await msg.answer_document(document=file, caption='Замен нет, но это не точно')
        
    await state.clear()
    
    
@game_rout.callback_query(F.data == 'new_repl')
@game_rout.message(Command("sub"))
async def start_mailing(msg: Message | CallbackQuery, state: FSMContext):
    if isinstance(msg, CallbackQuery):
        await msg.answer()
        await msg.message.edit_text("Введите название группы")
    elif isinstance(msg, Message):
        await msg.answer("Введите название группы")
    await state.set_state(BotStates.mailing)
    
    
@game_rout.message(BotStates.mailing, GroupFilter())
async def sub_to_mailing(msg: Message, bot: Bot, state: FSMContext):
    await state.clear()
    chat_id = msg.chat.id
    group = msg.text.upper()
    ok = await mongo.add_chat(group, chat_id)
    if ok:
        await msg.answer(f'Вы подписались на рассылку замен для {group}')
        return
    await msg.answer(f'Вы уже подписаны на рассылку замен для {group}')
    
    
@game_rout.message(Command("unsub"))
async def satrt_unsub(msg: Message, state: FSMContext):
    await msg.answer("Введите название группы")
    await state.set_state(BotStates.unsub)
    
    
@game_rout.message(BotStates.unsub, GroupFilter())
async def unsub_to_mailing(msg: Message, state: FSMContext):
    await state.clear()
    chat_id = msg.chat.id
    group = msg.text.upper()
    ok = await mongo.delete_chat(group, chat_id)
    if ok:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Да', callback_data='new_repl'), InlineKeyboardButton(text='Нет', callback_data='unluck')]
        ])
        await msg.answer('Вы отписались от рассылки замен\nХотите добавить другую группу?', reply_markup=kb)
    else:
        await msg.answer('Вы и так не подписаны на рассылку для этой группы')

    
@game_rout.callback_query(F.data == 'unluck')
async def gg(call: CallbackQuery):
    await call.message.edit_text('Пидора ответ')

@game_rout.message(BotStates.unsub)
@game_rout.message(BotStates.replaces)
async def wrong_group(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
    ])
    await msg.answer('Введите корректное название группы:\n XX-000', reply_markup=kb)
    

@game_rout.callback_query(F.data == 'cancel')
async def cancel_hand(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await state.clear()


@game_rout.message(Command('refresh'))
async def new_repl(msg: Message):
    res = await vgpgk.download_replace()
    if res:
        await msg.answer('замены успешно обновлены')
    else:
        await msg.answer('замены не были обновлены')