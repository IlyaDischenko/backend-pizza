from pydantic import BaseModel, Field

class Promocode(BaseModel):
    promocode: str = Field(default=None)