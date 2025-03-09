from beanie import Document
from typing import List

class Group(Document):
    group_name: str
    chats: List[int]
    
    class Settings:
        name = "chats"
