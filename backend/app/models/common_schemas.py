from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page_num: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
