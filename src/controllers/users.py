from controllers import BaseController, allow_access
from models.users import UserDocument
from schemas.users import UserResponseSchema


class UserController(BaseController):
    model = UserDocument
    schema = UserResponseSchema

    def create(self, schema):
        document = super().create(schema, raw=True)
        document.set_password(schema.get("password"))
        return self.schema.from_orm(document)

    @allow_access
    def fetch(self, filters, raw=False):
        return super().fetch(filters, raw=raw)

    def update(self, id, schema):
        document = super().update(id, schema, raw=True)
        if "password" in schema:
            document.set_password(schema["password"])
        return self.schema.from_orm(document)
