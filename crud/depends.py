from fastapi import HTTPException
from sqlalchemy.orm import Session
import models


def get_word_by_id(db: Session, word_id: int):
    word = db.query(models.WordsModel)\
        .filter(models.WordsModel.id == word_id).first()

    if not word:
        raise HTTPException(status_code=404, detail='word not found')
    
    return word
