from pydantic.fields import Field
from pydantic import EmailStr
from schemas import BaseSchema
from datetime import date


class UserSchema(BaseSchema):
    username: str
    email: EmailStr
    birth_date: date
    active: bool = True


class RegisterSchema(UserSchema):
    password: str = Field(..., min_length=8)


class UserResponseSchema(UserSchema):
    id: str
