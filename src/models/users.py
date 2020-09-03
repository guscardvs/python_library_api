from models import BaseDocument
import mongoengine as mongo
from passlib.hash import bcrypt


class UserDocument(BaseDocument):
    username = mongo.StringField(unique=True)
    password = mongo.StringField()
    email = mongo.EmailField(unique=True)
    birth_date = mongo.DateField()
    active = mongo.BooleanField()
    document = mongo.StringField(unique=True)

    def set_password(self, password):
        self.password = bcrypt.hash(password)
        self.save()

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)
