from email.policy import default
from core.database import DataBaseModel

from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as TypeEnum


class AppDataBaseModel:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)


class Words(DataBaseModel, AppDataBaseModel):
    __tablename__ = "word_list"

    word = Column(String, index=True)
    dict_link = Column(String)
    voice = Column(String)
    type_zh = Column(String)
    
    def __str__(self):
        return f'<Words>({self.word}[{self.id}])'


class ReviewStatus(TypeEnum):
    GET = "forget"
    LOSS = "remember"

    @classmethod
    def get_options(cls) -> list:
        vs = [getattr(cls, m).value for m in cls.__members__]
        return vs

    def __len__(self):
        return len(self.get_options())


class WordReviewModel(DataBaseModel, AppDataBaseModel):
    __tablename__ = "word_review"

    create_date = Column(Date)
    word_id = Column(Integer, ForeignKey("word_list.id"))
    word = relationship("Words")

    show_times = Column(Integer, default=0)
    forget_times = Column(Integer, default=0)
    remember_times = Column(Integer, default=0)

    @property
    def create_date_str(self):
        return self.create_date.strftime("%Y-%m-%d")


class WordReviewLogModel(DataBaseModel, AppDataBaseModel):
    __tablename__ = "word_review_log"

    word_id = Column(Integer, ForeignKey("word_list.id"))
    word = relationship("Words")

    review_status = Column(Enum(*ReviewStatus.get_options()), default="loss")
