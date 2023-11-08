from fastapi import APIRouter, Depends
from core.database import get_db, Session
import models, utils
from crud.depends import get_word_by_id
from crud.reviews import review_words, add_words_review_log, check_reivewed_word
from schema.review import ReviewList
from utils.tools import router_prefix

_router = APIRouter(prefix=router_prefix(__file__), tags=['reviews'])


@_router.get("/", tags=['reviews'])
async def index(
    rvQry: ReviewList = Depends(),
    db: Session = Depends(get_db)
):
    
    wList = review_words(db, rvQry)

    return utils.response.success(wList)


@_router.get("/{word_id}")
async def review_word(
    word_id: int, status: models.ReviewStatus, db: Session = Depends(get_db)
):
    word = get_word_by_id(db, word_id)

    if not check_reivewed_word(db, word):
        result, msg = add_words_review_log(db, word, status)
        if result:
            return utils.response.success()
        else:
            return utils.response.fail(1, str(msg))
    else:
        return utils.response.success("word has been reviewed tody")
