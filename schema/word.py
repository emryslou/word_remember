import datetime
from pydantic import BaseModel
from typing import Optional

from .base import Query


class WordBase(BaseModel):
    word: str
    dict_link: str
    voice: Optional[str] = ""
    type_zh: str
    create_date: datetime.date

    class Config:
        orm_mode = True


class WordAdd(WordBase):
    created_at: int = datetime.datetime.now()
    updated_at: int = datetime.datetime.now()


class WordQuery(Query):
    word: str = None
    type_zh: str = None
