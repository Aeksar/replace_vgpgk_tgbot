from aiogram.types import CallbackQuery, Message
from aiogram.filters import BaseFilter
from datetime import datetime
import re

# class GroupFilter(BaseFilter):
#     async def  __call__(self, message: Message):
#         valid = r"[А-Яа-я]{2}-2[1-9][1-5]$"
#         ok = re.match(valid, message.text)
#         if ok:
#             return True
#         return False


class GroupFilter(BaseFilter):
    async def __call__(self, message: Message):
        text = message.text.strip()
        if not text[2] == '-' or len(text) != 6:
            return False
        letters, nums = text.split('-')
        n_year, g_num = int('20' + nums[:2]), int(nums[-1])
        year = datetime.now().year
        if year-4 <= n_year <= year and 1 <= g_num <= 5 and \
            re.match(r'^[А-я]{2}$', letters):
            return True
        return False