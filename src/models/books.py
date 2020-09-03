from models import BaseDocument
import mongoengine as mongo
from models.users import UserDocument


class BookDocument(BaseDocument):
    ISBN = mongo.StringField()
    title = mongo.StringField()
    pages = mongo.IntField()
    description = mongo.StringField()
    sinopsis = mongo.StringField()
    author = mongo.StringField()
    year = mongo.IntField()


class UserBook(BaseDocument):
    owner = mongo.ReferenceField(UserDocument)
    book = mongo.ReferenceField(BookDocument)


class LoanDocument(BaseDocument):
    user_book = mongo.ReferenceField(UserBook)
    borrower = mongo.ReferenceField(UserDocument)
    validity = mongo.DateField()
