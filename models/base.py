"""
database base model
"""
from datetime import datetime
from typing import List, Iterable
import uuid
import models

TIMESTAMP_FORMAT = "%Y-%m-%d%T%H:%M:%S.%f"

class Base():
    """
    base class
    """
    def __init__(self):
        """
        main initialisation
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        # to check if it is rebuilding
        self.built = False

    @classmethod
    def delete(cls, obj):
        """
        delete document from db
        """
        models.storage.delete(cls, obj)

    def to_dict(self):
        new_dict = {}
        for i, j in self.__dict__.items():
            if i == "created_at":
                new_dict[i] = j.strftime(TIMESTAMP_FORMAT)
                continue
            if i in self.keys:
                new_dict[i] = j
        return new_dict

    @classmethod
    def confirm(cls, id):
        """
        confirm if user exist
        """
        # id is sopose to be a built in func but has been overried
        try:
            result = models.storage.find(cls, {"id": id}, {"id": 1})
        except Exception as e:
            models.handleError(e)
            result = []
        if len(list(result)) == 1:
            return id
        else:
            models.handleError("NotFoundError", f"@{cls.__name__}.confirm: User does not exist")
        return None

    @classmethod
    def find(cls, obj, resultFormat=None):
        result = []
        try:
            result = models.storage.find(cls, obj, resultFormat)
            result =list(result)
            if len(result) > 0:
                return result
        except Exception as e:
            models.handleError(e)
        return result

    def save(self):
        if not self.built:
            try:
                models.storage.new(self.__class__, self.to_dict())
            except Exception as e:
                models.handleError(e)
        else:
            try:
                models.storage.update(self.__class__, {"id": self.id}, self.to_dict())
            except Exception as e:
                models.handleError(e)

    @classmethod
    def update(cls, obj, newobj):
        if not self.built:
            try:
                models.storage.update(cls, obj, newobj)
            except Exception as e:
                models.handleError(e)
