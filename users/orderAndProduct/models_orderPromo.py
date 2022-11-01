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

class Order(BaseModel):
    token: bytes = Field(default=None)
    number: str = Field(default=None)
    pizzas: object = Field(default=None)
    drinks: object = Field(default=None)
    promocode: str = Field(default=None)

    street: str = Field(default=None)
    house: str = Field(default=None)
    entrance: str = Field(default=None)
    floor: str = Field(default=None)
    apartment: str = Field(default=None)

    device: str = Field(default=None)
    paytype: str = Field(default=None)
    comment: str = Field(default=None)
    status: str = Field(default=None)