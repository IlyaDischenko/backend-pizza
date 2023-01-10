from pydantic import BaseModel, Field


class AddPizza(BaseModel):
    id: str = Field(default=None)
    item_id: str = Field(default=None)

class AddPromocode(BaseModel):
    id: str = Field(default=None)
    promocode: str = Field(default=None)