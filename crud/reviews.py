from operator import and_
from typing import List, Tuple
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, func

import models
from core.database import Session
from models import WordsModel, ReviewStatus, WordReviewModel
from schema.review import ReviewList


def check_review(db: Session, words: List[Tuple[int, str]]):
    filters = [
        and_(WordReviewModel.word_id == wd[0], WordReviewModel.create_date == wd[1])
        for wd in words
    ]
    db_words = db.query(WordReviewModel).filter(or_(*filters)).all()
    words_ret = {wd: None for wd in words}
    for db_wd in db_words:
        words_ret[(db_wd.word_id, db_wd.create_date)] = db_wd
    return words_ret


def check_reivewed_word(db: Session, word: WordsModel) -> bool:
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    now = datetime.now()
    query = db.query(models.WordReviewLogModel).filter(
        models.WordReviewLogModel.word_id == word.id,
        models.WordReviewLogModel.created_at.between(today, now),
    )
    return query.count() > 0


def add_words_review_log(db: Session, word: WordsModel, status: ReviewStatus):
    try:
        db_review_log = models.WordReviewLogModel(
            word_id=word.id, review_status=status.value
        )
        db.add(db_review_log)
        db.commit()
        db.refresh(db_review_log)
        return True, None
    except SQLAlchemyError as sae:
        return False, sae


def review_words(db: Session, q: ReviewList):

    review_days = get_review_days(db)
    skip = max(q.page - 1, 0) * q.page_size
    fields = [
        models.WordsModel.id,
        models.WordsModel.word,
        models.WordsModel.voice,
        models.WordsModel.dict_link,
        models.WordsModel.type_zh,
        models.WordReviewModel.create_date,
    ]

    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    now = datetime.today()
    query = (
        db.query(*fields)
        .join(models.WordReviewModel)
        .filter(
            and_(
                models.WordReviewModel.create_date.in_(review_days),
                models.WordReviewModel.word_id.not_in(
                    db.query(models.WordReviewLogModel.word_id).filter(
                        models.WordReviewLogModel.created_at.between(today, now)
                    )
                ),
            )
        )
        .group_by(models.WordReviewModel.word_id)
        .order_by(func.random())
    )

    return {
        "list": query.slice(skip, skip + q.page_size).all(),
        "total": query.count(),
        "page": q.page,
        "page_size": q.page_size,
        "review_days": review_days,
        "skip": skip,
        "sql": str(query),
    }


def get_review_days(db: Session, end_date: str = "now", diff_delta: int = 10):
    query = (
        db.query(models.WordReviewModel.create_date)
        .group_by(models.WordReviewModel.create_date)
        .order_by(models.WordReviewModel.create_date)
    )

    words_keys = [item.create_date for item in query.all()]

    _start_date = datetime.strptime("2023-03-12", "%Y-%m-%d")
    if end_date == "now":
        _end_date = datetime.now()
    else:
        _end_date = datetime.strptime(end_date, "%Y-%m-%d")
    _rs_delta = (_end_date - _start_date).days - diff_delta

    rv_idxs = [-1, -2] if len(words_keys) > 1 else []
    rv_idxs += [(rs_idx + _rs_delta) % len(words_keys) - 2 for rs_idx in [0, 2, 7]]

    review_keys = list(set([words_keys[_idx] for _idx in rv_idxs]))
    review_keys.sort()

    return review_keys
