from beanie import Document, Indexed
from typing import List, Annotated

class Group(Document):
    group_name: Annotated[str, Indexed()]
    chats: List[int]
    
    class Settings:
        name = "chats"
