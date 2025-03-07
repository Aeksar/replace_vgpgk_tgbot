from aiogram.fsm.state import State, StatesGroup

class BotStates(StatesGroup):
    game = State()
    replaces = State()