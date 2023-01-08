from pydantic import BaseModel, Field


class AddPizza(BaseModel):
    id: str = Field(default=None)
    item_id: str = Field(default=None)
    size: str = Field(default=None)