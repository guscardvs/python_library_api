from mongoengine import Document


class BaseDocument(Document):

    meta = {
        "abstract": True,
        "allow_inheritance": True
    }

    def __redo(self):
        if self.pk:
            self.id = str(self.pk)

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.__redo()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.__redo()
        return self

    @classmethod
    def create(cls, fields: dict):
        return cls(**fields).save()
