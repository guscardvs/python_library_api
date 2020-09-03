from schemas import BaseSchema
from schemas.users import UserResponseSchema
from pydantic.fields import Field
from datetime import datetime, date


class BookSchema(BaseSchema):
    ISBN: str = Field(None)
    title: str = Field(...)
    pages: int = Field(None)
    description: str = Field(None)
    sinopsis: str = Field(None)
    author: str = Field(...)
    year: int = Field(..., gt=1000, lt=datetime.now().year)


class BookResponseSchema(BaseSchema):
    id: str


class UserBookSchema(BaseSchema):
    owner: str
    book: str


class UserBookResponseSchema(BaseSchema):
    id: str
    owner: UserResponseSchema
    book: BookResponseSchema


class LoanSchema(BaseSchema):
    user_book: str
    borrower: str
    validity: date


class LoanResponseSchema(BaseSchema):
    id: str
    user_book: UserBookResponseSchema
    borrower: UserResponseSchema
    validity: date
