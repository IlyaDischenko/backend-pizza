from pydantic import BaseModel, Field


# from sqlalchemy.dialects.postgresql import json


class Promocode(BaseModel):
    number: str = Field(default=None)
    promocode: str = Field(default=None)

class Insert_promocode(BaseModel):
    promocode: str = Field(default=None)
    count: int = Field(default=None)
    type: int = Field(default=None)
    return_data: object = Field(default=None)
    min_sum: int = Field(default=None)
    need_number: bool = Field()
    number: str = Field(default=None)
    is_view: bool = Field()