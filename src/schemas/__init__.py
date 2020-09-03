import re
from pydantic.main import BaseModel, ModelMetaclass, create_model
from pydantic.fields import ModelField, Field


class MetaSchema(ModelMetaclass):

    @property
    def EditSchema(cls):
        edit_fields = {**cls.__fields__}
        for key, value in edit_fields.items():
            if isinstance(value, ModelField):
                edit_fields[key] = (value.type_, Field(None))
        Schema = create_model("EditSchema", **edit_fields)

        class EditSchema(Schema, cls):
            pass
        return EditSchema


def to_camel(string):
    return re.sub(r"_([a-zA-Z])", lambda x: x[1].upper(), string)


class BaseSchema(BaseModel, metaclass=MetaSchema):

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True
