from fastapi import APIRouter, File, Depends
from core.database import get_db, Session
import re, datetime, utils
from crud.depends import get_word_by_id
from schema.word import WordQuery

from utils.tools import router_prefix

_router = APIRouter(prefix=router_prefix(__file__), tags=['words'])


@_router.get("/")
async def list_words(
    wq: WordQuery = Depends(),
    db: Session = Depends(get_db),
):
    from crud.words import WordQuery, query_words

    wList = query_words(
        db, WordQuery(**wq.dict())
    )
    return wList


@_router.get("/{word_id}")
async def detail(word_id: int, db: Session = Depends(get_db)):
    word = get_word_by_id(db, word_id)
    return utils.success(word)


@_router.post("/add/md_line")
async def add_words_by_md_line(tag: str, md_line: str, db: Session = Depends(get_db)):
    return {"message": parse_md_line(md_line, tag)}


@_router.post("/add/md_file")
async def add_words_by_md_file(md_file: bytes = File(), db: Session = Depends(get_db)):
    try:
        words_list = parse_md_content(bytes.decode(md_file, encoding="utf-8"))
        wd_list = []
        [wd_list.extend(wds) for _, wds in words_list.items()]

        from crud.words import WordAdd, add_words

        was = [WordAdd(**wd) for wd in wd_list]
        ok, msg = add_words(db, was)
        if ok:
            return utils.success(data=msg)
        else:
            return utils.fail(500, msg)
    except BaseException as be:
        return utils.fail(code=1, message=str(be))


def parse_md_content(md_cnt):
    lines = md_cnt.split("\n")
    words_list = {}

    tag = "unknown"
    tag_pattern = r"^#.*@\s*([\d]{4}\-[\d]{2}\-[\d]{2})"

    for _, line in enumerate(lines):
        try:
            m_tag = re.match(tag_pattern, line)
            if m_tag:
                tag = m_tag.group(1)
                continue

            if tag == "unknown":
                print("tag match fail, not next")
                continue
            print(tag)
            word_info = parse_md_line(line, tag)
            if word_info:
                words_list.setdefault(tag, []).append(word_info)
        except BaseException as be:
            raise be

    return words_list


def parse_md_line(md_line: str, tag: str):
    word_info = {}

    word_pattern = r"^[\d]+\.\s+"
    if len(md_line) <= 0 or not re.search(word_pattern, md_line):
        return word_info

    word_info_pattern = r"\[([^\[\]]+)\]\(([^\(\)]+)(,#[^#]+)?\)"
    word_voice_pattern = r"\s*\*\*/(.*)/\*\*"

    word_line = re.sub(word_pattern, "", md_line)

    m_word_info = re.match(word_info_pattern, word_line)
    if m_word_info:
        word_info["word"] = m_word_info.group(1)
        word_info["dict_link"] = m_word_info.group(2)
        word_line = re.sub(word_info_pattern, "", word_line)

    m_word_voice = re.match(word_voice_pattern, word_line)
    if m_word_voice:
        word_info["voice"] = m_word_voice.group(1)
        word_line = re.sub(word_voice_pattern, "", word_line)

    word_info["type_zh"] = word_line.strip()
    word_info["create_date"] = datetime.datetime.strptime(tag, "%Y-%m-%d").date()

    return word_info
