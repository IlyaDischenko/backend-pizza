from pydantic import BaseModel, Field, EmailStr


class Number(BaseModel):
    number: str = Field(default=None)


class Code(BaseModel):
    number: str = Field(default=None)
    code: str = Field(default=None)


class Token(BaseModel):
    token: bytes = Field(default=None)


class Email(BaseModel):
    token: bytes = Field(default=None)
    email: EmailStr = Field(default=None)


class Name(BaseModel):
    token: bytes = Field(default=None)
    name: str = Field(default=None)


class Address(BaseModel):
    token: bytes = Field(default=None)
    street: str = Field(default=None)
    house: str = Field(default=None)
    entrance: str = Field(default=None)
    floor: str = Field(default=None)
    apartment: str = Field(default=None)
