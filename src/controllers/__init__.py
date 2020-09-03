import json
from models import BaseDocument
from schemas import BaseSchema
from bson.objectid import ObjectId
from bson.errors import BSONError
from fastapi import HTTPException
from typing import Union, Callable
import mongoengine as mongo
from models.users import UserDocument
from functools import wraps


def controller_name(self):
    return self.__class__.__name__.replace("Controller", "")


class BaseController:
    model = BaseDocument
    schema = BaseSchema

    def __init__(self, user: Union[UserDocument, None] = None):
        self.user = user

    def create(self, schema: dict, raw: bool = False):
        try:
            document = self.model.create(schema)
        except mongo.errors.NotUniqueError:
            raise HTTPException(400, detail="%s already exists" %
                                controller_name(self))
        if raw:
            return document
        else:
            return self.schema.from_orm(document)

    def get(self, id: str, raw: True) -> Union[BaseDocument, BaseSchema]:
        try:
            document = self.model.objects.get(pk=ObjectId(id))
            if raw:
                return document
            return self.schema.from_orm(document)
        except BSONError:
            raise HTTPException(400, detail="Invalid id")
        except self.model.DoesNotExist:
            raise HTTPException(404, detail="%s not found" %
                                controller_name(self))

    def fetch(self, filters: dict, raw: bool = False):
        filters.pop("id", None)
        documents = self.model.objects(__raw__=filters)
        if raw:
            return documents
        docs = (self.schema.from_orm(document) for document in documents)
        return docs

    def update(self, id: str, schema: dict, raw: bool = False):
        document = self.get(id, raw=True)
        for key, value in schema.items():
            if key != 'password' and value is not None:
                setattr(document, key, value)
        document.save()
        if raw:
            return document
        return self.schema.from_orm(document)

    def delete(self, id: str):
        document = self.get(id, raw=True)
        document.delete()


def allow_access(func: Callable = None, *, disallow_inactive=True):
    def outer(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            if not disallow_inactive:
                return func(self, *args, **kwargs)

            if not self.user or getattr(self.user, "active", False):
                return func(self, *args, **kwargs)
            else:
                raise HTTPException(403, detail="Access Denied")
        return inner
    return outer if not func else outer(func)
