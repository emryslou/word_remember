from pydantic import BaseModel


class Query(BaseModel):
    page: int = 1
    page_size: int = 10
