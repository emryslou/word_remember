from operator import and_
from typing import List
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, func

import models
from core.app import Session
from models import WordsModel, ReviewStatus, WordReviewModel
from schema import WordAdd, WordQuery
from .reviews import check_review


def add_word(db: Session, word: WordAdd):
    try:
        return add_words(db, [word])
    except SQLAlchemyError as sae:
        return False, str(sae)


def add_words(db: Session, words: List[WordAdd]):
    try:
        with db.begin():
            wordModels = []
            checkWords = check_words(db, [w.word for w in words])
            for w in words:
                if not checkWords[w.word]:
                    new_w = w.dict()
                    del new_w["create_date"]
                    wordModels.append(WordsModel(**new_w))
            db.add_all(wordModels)
            db.begin_nested()
            checkWords = {
                **{key: cw for key, cw in checkWords.items() if cw is not None},
                **{wm.word: wm for wm in wordModels},
            }

            checkReviews = []
            for w in words:
                checkReviews.append((checkWords[w.word].id, w.create_date))

            checkReviews = check_review(db, checkReviews)
            wordReviewModes = []
            for key, val in checkReviews.items():
                if val is None:
                    wordReviewModes.append(
                        WordReviewModel(
                            **{
                                "word_id": key[0],
                                "create_date": key[1],
                            }
                        )
                    )
            if wordReviewModes:
                db.add_all(wordReviewModes)
            db.commit()
        return True, None
    except SQLAlchemyError as sae:
        db.rollback()
        return False, str(sae)
    finally:
        db.close()


def check_words(db: Session, words: List[str]):
    """
    检测单词是否存在，
    """
    db_words = db.query(WordsModel).filter(WordsModel.word.in_(words)).all()

    words_ret = {w: None for w in words}
    for db_word in db_words:
        words_ret[db_word.word] = db_word

    return words_ret


def query_words(db: Session, wd: WordQuery):
    rulers = []

    attrs = ["word", "type_zh"]
    for attr in attrs:
        if getattr(wd, attr):
            rulers.append(
                getattr(models.WordsModel, attr).like("%" + getattr(wd, attr) + "%")
            )

    query = db.query(models.WordsModel)
    if len(rulers):
        query = query.filter(or_(*rulers))

    skip = max(wd.page - 1, 0) * wd.page_size
    query_count = query.count()
    query_sets = query.slice(skip, skip + wd.page_size).all()

    return {
        "list": query_sets,
        "total": query_count,
        "page": wd.page,
        "page_size": wd.page_size,
        "skip": skip,
        "sql": str(query),
    }
