from pydantic import BaseModel, Field

class Promocode(BaseModel):
    number: str = Field(default=None)
    promocode: str = Field(default=None)