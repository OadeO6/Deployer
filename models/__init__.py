""""
doc
"""
from os import getenv

storageType = getenv("DB_TYPE", "mongodb")

def handleError(err, message=None):
    """
    handle error by loging it instead of breaking the app
    """
    mode = getenv("ERROR_MODE", "dev")
    from models.error import error
    print(err)
    if isinstance(err, str):
        if err in error:
            error = getattr(__import__("models.error"), err)
            if mode != "production":
                raise error(message=message)
            else:
                print("log error")
        else:
            if mode != "production":
                raise NotImplementedError
            else:
                print("log error")
    else:
        if mode != "production":
            raise err
        else:
            print("log error")

if storageType == "mongodb":
    from models.engine.mongo_storage import MongoStorage
    storage = MongoStorage()
else:
    from models.engine.mongo_storage import MongoStorage
    storage = MongoStorage()
# check for connnection here and retry if neded
